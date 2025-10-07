#!/usr/bin/env python3
"""
Raspberry Pi Camera Interface Module with CycloneDDS Integration

This module interfaces with the Raspberry Pi camera and publishes image streams
via CycloneDDS middleware. It supports camera calibration, various image formats,
and real-time configuration changes.
"""

import sys
import os
import time
import threading
import json
import logging
from dataclasses import dataclass, asdict
from typing import Optional, Tuple, Dict, Any
import signal

import numpy as np
import cv2

# DDS imports (with fallback for development)
try:
    import cyclonedx
    from cyclonedx.domain import DomainParticipant
    from cyclonedx.topic import Topic
    from cyclonedx.pub import DataWriter
    from cyclonedx.sub import DataReader
    HAS_DDS = True
except ImportError:
    print("Warning: CycloneDDS not available, running in stub mode")
    HAS_DDS = False

# Camera imports (with fallback for development)
try:
    from picamera2 import Picamera2
    HAS_CAMERA = True
except ImportError:
    print("Warning: Picamera2 not available, using mock camera")
    HAS_CAMERA = False


@dataclass
class CameraSettings:
    """Camera configuration settings"""
    resolution: Tuple[int, int] = (1920, 1080)
    framerate: int = 30
    exposure_mode: str = "auto"
    white_balance: str = "auto"
    iso: int = 0
    brightness: int = 50
    contrast: int = 0
    saturation: int = 0
    sharpness: int = 0
    digital_gain: float = 1.0
    rotation: int = 0
    hflip: bool = False
    vflip: bool = False


@dataclass
class CameraCalibration:
    """Camera calibration parameters"""
    camera_matrix: Optional[np.ndarray] = None
    distortion_coeffs: Optional[np.ndarray] = None
    optimal_camera_matrix: Optional[np.ndarray] = None
    roi: Optional[Tuple[int, int, int, int]] = None
    calibrated: bool = False


class MockCamera:
    """Mock camera for development without hardware"""
    def __init__(self):
        self.resolution = (640, 480)
        self.framerate = 30
        self.running = False
    
    def configure(self, config):
        pass
    
    def start(self):
        self.running = True
    
    def stop(self):
        self.running = False
    
    def capture_array(self):
        # Generate a test pattern
        height, width = self.resolution[1], self.resolution[0]
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add some pattern
        cv2.rectangle(image, (50, 50), (width-50, height-50), (0, 255, 0), 2)
        cv2.putText(image, f"Mock Camera {time.time():.1f}", 
                   (60, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        return image


class CameraInterface:
    """Main camera interface class with DDS integration"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.logger = self._setup_logging()
        self.running = False
        self.camera = None
        self.capture_thread = None
        
        # Load configuration
        self.config = self._load_config(config_file)
        self.camera_settings = CameraSettings(**self.config.get("camera", {}))
        self.calibration = CameraCalibration()
        
        # DDS setup
        self.dds_participant = None
        self.image_writer = None
        self.status_writer = None
        self.control_reader = None
        
        # State
        self.frame_count = 0
        self.last_fps_time = time.time()
        self.current_fps = 0.0
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('/var/log/dashcam/camera_interface.log')
            ]
        )
        return logging.getLogger('camera_interface')
    
    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "module_id": "camera_interface",
            "camera": {
                "resolution": [1920, 1080],
                "framerate": 30,
                "exposure_mode": "auto",
                "white_balance": "auto"
            },
            "dds": {
                "domain_id": 0,
                "image_topic": "camera/raw_images",
                "control_topic": "camera/control",
                "status_topic": "camera/status"
            },
            "calibration": {
                "auto_load": True,
                "file": "/etc/dashcam/camera_calibration.json"
            }
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                self.logger.warning(f"Failed to load config file {config_file}: {e}")
        
        return default_config
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
    
    def initialize(self) -> bool:
        """Initialize the camera interface"""
        try:
            self.logger.info("Initializing camera interface...")
            
            # Initialize camera
            if not self._init_camera():
                return False
            
            # Initialize DDS
            if not self._init_dds():
                return False
            
            # Load calibration if available
            self._load_calibration()
            
            self.logger.info("Camera interface initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize camera interface: {e}")
            return False
    
    def _init_camera(self) -> bool:
        """Initialize the camera hardware"""
        try:
            if HAS_CAMERA:
                self.camera = Picamera2()
                config = self.camera.create_preview_configuration(
                    main={"size": tuple(self.camera_settings.resolution)}
                )
                self.camera.configure(config)
                self.logger.info("Picamera2 initialized")
            else:
                self.camera = MockCamera()
                self.camera.resolution = tuple(self.camera_settings.resolution)
                self.logger.info("Mock camera initialized")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize camera: {e}")
            return False
    
    def _init_dds(self) -> bool:
        """Initialize DDS communication"""
        if not HAS_DDS:
            self.logger.warning("DDS not available, running in stub mode")
            return True
        
        try:
            # Create domain participant
            domain_id = self.config["dds"]["domain_id"]
            self.dds_participant = DomainParticipant(domain_id)
            
            # Create topics and writers/readers
            image_topic_name = self.config["dds"]["image_topic"]
            status_topic_name = self.config["dds"]["status_topic"]
            control_topic_name = self.config["dds"]["control_topic"]
            
            # For now, we'll use simplified DDS integration
            # In a full implementation, this would use the generated IDL types
            
            self.logger.info("DDS initialized (stub implementation)")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize DDS: {e}")
            return False
    
    def _load_calibration(self):
        """Load camera calibration parameters"""
        if not self.config["calibration"]["auto_load"]:
            return
        
        calib_file = self.config["calibration"]["file"]
        if os.path.exists(calib_file):
            try:
                with open(calib_file, 'r') as f:
                    calib_data = json.load(f)
                
                self.calibration.camera_matrix = np.array(calib_data["camera_matrix"])
                self.calibration.distortion_coeffs = np.array(calib_data["distortion_coeffs"])
                self.calibration.optimal_camera_matrix = np.array(calib_data["optimal_camera_matrix"])
                self.calibration.roi = tuple(calib_data["roi"])
                self.calibration.calibrated = True
                
                self.logger.info("Camera calibration loaded successfully")
                
            except Exception as e:
                self.logger.warning(f"Failed to load calibration: {e}")
    
    def start(self) -> bool:
        """Start the camera interface"""
        if self.running:
            self.logger.warning("Camera interface already running")
            return True
        
        try:
            self.logger.info("Starting camera interface...")
            
            # Start camera
            if hasattr(self.camera, 'start'):
                self.camera.start()
            
            # Start capture thread
            self.running = True
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            
            self.logger.info("Camera interface started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start camera interface: {e}")
            return False
    
    def stop(self):
        """Stop the camera interface"""
        if not self.running:
            return
        
        self.logger.info("Stopping camera interface...")
        self.running = False
        
        # Wait for capture thread to finish
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=5.0)
        
        # Stop camera
        if self.camera and hasattr(self.camera, 'stop'):
            try:
                self.camera.stop()
            except:
                pass
        
        # Cleanup DDS
        if self.dds_participant:
            # In full implementation, cleanup DDS resources
            pass
        
        self.logger.info("Camera interface stopped")
    
    def _capture_loop(self):
        """Main capture loop running in separate thread"""
        self.logger.info("Starting capture loop")
        
        frame_interval = 1.0 / self.camera_settings.framerate
        last_capture_time = 0
        
        while self.running:
            try:
                current_time = time.time()
                
                # Maintain framerate
                time_since_last = current_time - last_capture_time
                if time_since_last < frame_interval:
                    time.sleep(frame_interval - time_since_last)
                    continue
                
                # Capture frame
                frame = self._capture_frame()
                if frame is not None:
                    self._process_and_publish_frame(frame, current_time)
                    last_capture_time = time.time()
                    
                    # Update FPS calculation
                    self._update_fps()
                
            except Exception as e:
                self.logger.error(f"Error in capture loop: {e}")
                time.sleep(0.1)  # Brief pause before retrying
        
        self.logger.info("Capture loop finished")
    
    def _capture_frame(self) -> Optional[np.ndarray]:
        """Capture a single frame from the camera"""
        try:
            if hasattr(self.camera, 'capture_array'):
                return self.camera.capture_array()
            else:
                # Mock implementation
                return self.camera.capture_array()
        except Exception as e:
            self.logger.error(f"Failed to capture frame: {e}")
            return None
    
    def _process_and_publish_frame(self, frame: np.ndarray, timestamp: float):
        """Process and publish a captured frame"""
        try:
            # Apply calibration if available
            if self.calibration.calibrated:
                frame = self._undistort_frame(frame)
            
            # Create image metadata
            metadata = {
                "timestamp": int(timestamp * 1_000_000),  # microseconds
                "sequence_id": self.frame_count,
                "width": frame.shape[1],
                "height": frame.shape[0],
                "channels": frame.shape[2] if len(frame.shape) > 2 else 1,
                "format": "BGR",
                "encoding": "uint8",
                "source_module": self.config["module_id"]
            }
            
            # Publish via DDS (stub implementation)
            self._publish_image(frame, metadata)
            
            self.frame_count += 1
            
        except Exception as e:
            self.logger.error(f"Failed to process frame: {e}")
    
    def _undistort_frame(self, frame: np.ndarray) -> np.ndarray:
        """Apply camera calibration to undistort the frame"""
        try:
            return cv2.undistort(
                frame,
                self.calibration.camera_matrix,
                self.calibration.distortion_coeffs,
                None,
                self.calibration.optimal_camera_matrix
            )
        except Exception as e:
            self.logger.warning(f"Failed to undistort frame: {e}")
            return frame
    
    def _publish_image(self, frame: np.ndarray, metadata: Dict[str, Any]):
        """Publish image frame via DDS"""
        if HAS_DDS and self.image_writer:
            # In full implementation, create ImageData structure and publish
            pass
        else:
            # Stub implementation - just log
            if self.frame_count % 30 == 0:  # Log every 30 frames
                self.logger.debug(f"Publishing frame {self.frame_count}: "
                                f"{metadata['width']}x{metadata['height']}")
    
    def _update_fps(self):
        """Update FPS calculation"""
        current_time = time.time()
        if current_time - self.last_fps_time >= 1.0:
            self.current_fps = self.frame_count / (current_time - self.last_fps_time)
            self.last_fps_time = current_time
            self.frame_count = 0
            
            if self.frame_count == 0:  # Only log once per second
                self.logger.info(f"Current FPS: {self.current_fps:.1f}")
    
    def update_settings(self, new_settings: Dict[str, Any]):
        """Update camera settings dynamically"""
        try:
            for key, value in new_settings.items():
                if hasattr(self.camera_settings, key):
                    setattr(self.camera_settings, key, value)
                    self.logger.info(f"Updated setting {key} = {value}")
            
            # Apply settings to camera
            self._apply_camera_settings()
            
        except Exception as e:
            self.logger.error(f"Failed to update settings: {e}")
    
    def _apply_camera_settings(self):
        """Apply current settings to the camera hardware"""
        # This would be implemented based on the specific camera API
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current camera status"""
        return {
            "module_id": self.config["module_id"],
            "running": self.running,
            "fps": self.current_fps,
            "frame_count": self.frame_count,
            "resolution": list(self.camera_settings.resolution),
            "calibrated": self.calibration.calibrated,
            "settings": asdict(self.camera_settings)
        }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Raspberry Pi Camera Interface Module")
    parser.add_argument("--config", "-c", help="Configuration file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create and run camera interface
    camera_interface = CameraInterface(args.config)
    
    try:
        if not camera_interface.initialize():
            print("Failed to initialize camera interface")
            sys.exit(1)
        
        if not camera_interface.start():
            print("Failed to start camera interface")
            sys.exit(1)
        
        print("Camera interface running. Press Ctrl+C to stop.")
        
        # Main loop
        while camera_interface.running:
            time.sleep(1)
            status = camera_interface.get_status()
            if status["running"]:
                print(f"FPS: {status['fps']:.1f}, Frames: {status['frame_count']}")
    
    except KeyboardInterrupt:
        print("\nShutdown requested...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        camera_interface.stop()
    
    print("Camera interface shutdown complete")


if __name__ == "__main__":
    main()