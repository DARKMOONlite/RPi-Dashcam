# Module Framework Template for Raspberry Pi Dashcam

This directory contains templates and guidelines for creating modules in different programming languages that integrate with the CycloneDDS-based dashcam system.

## Overview

All modules in the dashcam system follow a common pattern:
1. **Initialize** - Set up DDS connections and configuration
2. **Subscribe** - Listen to input topics for data/configuration settings
3. **Process** - Perform the module's core functionality
4. **Publish** - Send results to output topics
5. **Monitor** - Provide status and performance metrics

## Module Types

### Camera Interface
- **Purpose**: Interface with camera hardware
- **Input**: Control commands
- **Output**: Raw image streams, status information
- **Example**: `modules/camera_interface/`

### Filter
- **Purpose**: Apply image processing filters
- **Input**: Image streams
- **Output**: Filtered image streams
- **Examples**: Blur, sharpen, color correction, noise reduction

### Neural Network / AI
- **Purpose**: Run ML/AI inference on image streams
- **Input**: Image streams
- **Output**: Detection results, annotated images
- **Examples**: Object detection, license plate recognition, lane detection

### Stream Encoder
- **Purpose**: Encode image streams to video files
- **Input**: Image streams
- **Output**: Video files, encoding status
- **Examples**: H.264, H.265, AV1 encoding

### Web Interface
- **Purpose**: Provide web-based control and monitoring
- **Input**: System status, image streams
- **Output**: HTTP responses, control commands


## Common Interface

All modules must implement:

1. **Configuration Loading**: JSON-based configuration
2. **DDS Communication**: Standardized topic names and data types
3. **dynamic reconfiguration**: change internal configuration based on msgs sent over specialised config topic
3. **Health Monitoring**: Heartbeat and status reporting: performance etc.
4. **Graceful Shutdown**: Signal handling and cleanup
5. **Logging**: Structured logging with configurable levels

## Topic Naming Convention

- **Image Stream**:`{module_type}/{module_id}/output`
- **Control**: `{module_type}/{module_id}/config`
- **Status**: `{module_type}/{module_id}/status`
- **Metrics**: `{module_type}/{module_id}/metrics`

## Getting Started


1. implement module with base class `base_module.py/.go/.rs/.cpp`
2. ensure all required functions are declared and defined.
5. Register node with the orchestrator
