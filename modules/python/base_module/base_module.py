#!/usr/bin/env python3
# DDS imports (with fallback for development)

from abc import ABC #? maybe
from dataclasses import dataclass
from enum import Enum
import time
try:
    import cyclonedds
    from cyclonedds.domain import DomainParticipant, Qos
    from cyclonedds.topic import Topic
    from cyclonedds.pub import DataWriter
    from cyclonedds.sub import DataReader
    from cyclonedds.core import WaitSet
    from cyclonedds.idl import IdlStruct
    HAS_DDS = True
except ImportError:
    print("Warning: CycloneDDS not available, running in stub mode")
    HAS_DDS = False


class LogLevels(Enum):
    Debug=0,
    Info=1,
    Warn=2,
    Error=3,
    Critical=4,
    

class ModuleState(Enum):
    Unknown=0,
    Starting=1,
    Running=2,
    Stopping=3,
    Stopped=4,
    Error=5

@dataclass
class heartbeat(IdlStruct,typename="heartbeat.Msg"):
    timestamp: int
    status: int
@dataclass
class logmsg(IdlStruct,typename="log.Msg"):
    timestamp:int
    module_id:str
    log_level:int
    msg:str

class BaseDDSModule:
    def __init__ (self, module_id:str, debug_level:int=0,domain_id:int=0,qos:Qos=None):
        if not HAS_DDS:
            raise RuntimeError("CycloneDDS is not available")
        # Initialize DDS participant, topics, publishers, subscribers here
        self.debug_level = debug_level
        self.module_id = module_id
        self.qos = qos
        
        
        self.participant = DomainParticipant(domain_id=domain_id, qos_profile=self.qos)
        # dynamic configure topic and subscriber based on module_id
        self.configure_topic:Topic = Topic(self.participant, f"/{module_id}/config", str)
        self.subscriber:DataReader = DataReader(self.participant, self.configure_topic, self.configure_callback)
        
        self.logging_topic:Topic = Topic(self.participant, f"/logging", logmsg) 
        self.logger:DataWriter = DataWriter(self.participant, self.logging_topic)
        
        self.heartbeat_topic:Topic = Topic(self.participant, f"/heartbeat", heartbeat) 
        self.heartbeater:DataWriter = DataWriter(self.participant, self.heartbeat_topic)
        
        self.topic:Topic = Topic(self.participant, "ExampleTopic", str)
        self.publisher:DataWriter = DataWriter(self.participant, self.topic)
        self.subscriber:DataReader = DataReader(self.participant, self.topic, self.on_data_received)
        
        self.waitset = WaitSet(self.participant)
        
        self.status = ModuleState('Starting')
        
    
    
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
    
    def run(self)->None:
        self.waitset.wait(1)
        
    def publish_heartbeat(self):
        msg = heartbeat(timestamp=self.get_time(),status=self.status)
        self.heartbeater.write(msg)
    def _publish_log(self,msg:str, log_level:int):
        msg = logmsg(timestamp=self.get_time(),module_id=self.module_id,log_level=log_level,msg=msg)
        self.logger.write(msg)
        
    def debug(self, msg:str):
        self._publish_log(msg=msg,log_level=LogLevels.Debug)
    def info(self,msg:str):
        self._publish_log(msg=msg,log_level=LogLevels.Info)
    def warn(self,msg:str):
        self._publish_log(msg=msg,log_level=LogLevels.Warn)
    def error(self,msg:str):
        self._publish_log(msg=msg,log_level=LogLevels.Error)
    def critical(self,msg:str):
        self._publish_log(msg=msg,log_level=LogLevels.Critical)
        
    def get_time(self) -> int:
        return int(time.time()*1000)
        
        
    
    def _init_module(self):
        raise NotImplementedError("Subclasses should implement this method")
    def _shutdown_module(self):
        raise NotImplementedError("Subclasses should implement this method")
    def _get_status(self) -> dict:
        raise NotImplementedError("Subclasses should implement this method")
    def _get_metrics(self) -> dict:
        raise NotImplementedError("Subclasses should implement this method")
    
    
        
    