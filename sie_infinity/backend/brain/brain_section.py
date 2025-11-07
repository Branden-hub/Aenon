"""
Base Brain Section - fundamental processing unit
"""
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class BrainSection:
    """
    Individual brain section with specialized processing capabilities
    """
    
    def __init__(self, section_id: str, hemisphere: str, layer: str, 
                 specialization: str, processing_capacity: float = 1.0):
        self.section_id = section_id
        self.hemisphere = hemisphere  # 'left' or 'right'
        self.layer = layer  # 'outer', 'secondary', 'primary'
        self.specialization = specialization
        self.processing_capacity = processing_capacity
        
        # State
        self.activation_level = 0.0
        self.memory_buffer = []
        self.connections = {}  # Connected sections
        self.processing_history = []
        
        # Metrics
        self.total_processed = 0
        self.last_activation = None
        
    def activate(self, input_data: Any, intensity: float = 1.0) -> Dict[str, Any]:
        """
        Activate this brain section with input data
        """
        self.activation_level = min(1.0, intensity * self.processing_capacity)
        self.last_activation = datetime.now()
        
        # Process based on specialization
        result = self._process(input_data)
        
        # Store in memory buffer
        self.memory_buffer.append({
            'timestamp': self.last_activation.isoformat(),
            'input': str(input_data)[:100],  # Truncate for storage
            'output': str(result)[:100],
            'activation': self.activation_level
        })
        
        # Keep buffer size manageable
        if len(self.memory_buffer) > 100:
            self.memory_buffer = self.memory_buffer[-100:]
        
        self.total_processed += 1
        
        return {
            'section_id': self.section_id,
            'result': result,
            'activation': self.activation_level,
            'timestamp': self.last_activation.isoformat()
        }
    
    def _process(self, input_data: Any) -> Any:
        """
        Specialized processing based on section type
        Override in specialized sections
        """
        return input_data
    
    def connect_to(self, other_section: 'BrainSection', weight: float = 1.0):
        """
        Create connection to another brain section
        """
        self.connections[other_section.section_id] = {
            'section': other_section,
            'weight': weight
        }
    
    def propagate(self, data: Any) -> List[Dict[str, Any]]:
        """
        Propagate activation to connected sections
        """
        results = []
        for conn_id, conn_info in self.connections.items():
            section = conn_info['section']
            weight = conn_info['weight']
            intensity = self.activation_level * weight
            
            result = section.activate(data, intensity)
            results.append(result)
        
        return results
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current state of this section
        """
        return {
            'section_id': self.section_id,
            'hemisphere': self.hemisphere,
            'layer': self.layer,
            'specialization': self.specialization,
            'activation_level': self.activation_level,
            'total_processed': self.total_processed,
            'last_activation': self.last_activation.isoformat() if self.last_activation else None,
            'connections': list(self.connections.keys()),
            'memory_buffer_size': len(self.memory_buffer)
        }
    
    def reset(self):
        """
        Reset section state
        """
        self.activation_level = 0.0
        self.memory_buffer = []
        self.processing_history = []


class SensorySection(BrainSection):
    """Specialized for sensory input processing"""
    
    def _process(self, input_data: Any) -> Any:
        # Sensory preprocessing
        if isinstance(input_data, str):
            return {
                'type': 'text',
                'length': len(input_data),
                'tokens': input_data.split()[:10],
                'processed': True
            }
        return {'raw': input_data, 'processed': True}


class IntegrationSection(BrainSection):
    """Specialized for integrating multiple inputs"""
    
    def _process(self, input_data: Any) -> Any:
        # Integration logic
        if isinstance(input_data, (list, tuple)):
            return {
                'integrated': True,
                'count': len(input_data),
                'summary': 'Integrated multiple inputs'
            }
        return {'integrated': input_data}


class ReasoningSection(BrainSection):
    """Specialized for logical reasoning"""
    
    def _process(self, input_data: Any) -> Any:
        # Reasoning logic
        return {
            'reasoning_applied': True,
            'input_analyzed': True,
            'logical_structure': 'analyzed',
            'data': input_data
        }


class MetaCognitiveSection(BrainSection):
    """Specialized for self-reflection and meta-cognition"""
    
    def _process(self, input_data: Any) -> Any:
        # Meta-cognitive processing
        return {
            'self_reflection': True,
            'awareness_level': self.activation_level,
            'meta_analysis': 'Processing own processing',
            'data': input_data
        }
