#!/usr/bin/env python3
# DDS imports (with fallback for development)

from abc import ABC #? maybe

try:
    import cyclonedx
    from cyclonedx.domain import DomainParticipant, QosProfile
    from cyclonedx.topic import Topic
    from cyclonedx.pub import DataWriter
    from cyclonedx.sub import DataReader
    HAS_DDS = True
except ImportError:
    print("Warning: CycloneDDS not available, running in stub mode")
    HAS_DDS = False

debug_levels = {
    0: "NONE",
    1: "ERROR",
    2: "WARNING",
    3: "INFO",
    4: "DEBUG"
}


class BaseDDSModule:
    def __init__ (self, module_id:str, debug_level:int=0,domain_id:int=0,qos_profile:QosProfile=None):
        if not HAS_DDS:
            raise RuntimeError("CycloneDDS is not available")
        # Initialize DDS participant, topics, publishers, subscribers here
        self.participant = DomainParticipant(domain_id=domain_id, qos_profile=qos_profile)
        
        # dynamic configure topic and subscriber based on module_id
        self.configure_topic:Topic = Topic(self.participant, f"/{module_id}/config", str)
        self.subscriber:DataReader = DataReader(self.participant, self.configure_topic, self.configure_callback)
        self.logging_topic:Topic = Topic(self.participant, f"/logging", str) 
        self.logger:DataWriter = DataWriter(self.participant, self.logging_topic)
        self.topic:Topic = Topic(self.participant, "ExampleTopic", str)
        self.publisher:DataWriter = DataWriter(self.participant, self.topic)
        self.subscriber:DataReader = DataReader(self.participant, self.topic, self.on_data_received)
    
    
    def configure_callback(self, data:dict) -> None:
        print(f"Received configuration data: {data}")
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.logger.write(f"Warning: Unknown configuration key {key}")
        # Handle configuration update here

    def start(self) -> None:
        print("Starting DDS module")
        # Start any necessary threads or processes here
        
    def stop(self) -> None:
        print("Stopping DDS module")
        # Stop any running threads or processes here
        
    def _init_module(self):
        raise NotImplementedError("Subclasses should implement this method")
    def _shutdown_module(self):
        raise NotImplementedError("Subclasses should implement this method")
    def _get_status(self) -> dict:
        raise NotImplementedError("Subclasses should implement this method")
    def _get_metrics(self) -> dict:
        raise NotImplementedError("Subclasses should implement this method")
    