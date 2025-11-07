"""
Outer Brain - First layer of processing (12 sections total)
6 sections per hemisphere - handles sensory input and basic processing
"""
from typing import Dict, Any, List
from .brain_section import BrainSection, SensorySection


class OuterBrain:
    """
    Outer Brain: Sensory processing and initial filtering
    Left Hemisphere: 6 sections (logical, linguistic, analytical)
    Right Hemisphere: 6 sections (spatial, creative, holistic)
    """
    
    def __init__(self):
        self.left_hemisphere = self._create_left_hemisphere()
        self.right_hemisphere = self._create_right_hemisphere()
        self.all_sections = {**self.left_hemisphere, **self.right_hemisphere}
        
        # Connect hemispheres
        self._create_inter_hemispheric_connections()
    
    def _create_left_hemisphere(self) -> Dict[str, BrainSection]:
        """
        Left hemisphere - Logical, linguistic, analytical processing
        """
        return {
            'OL1': SensorySection('OL1', 'left', 'outer', 'Linguistic Input Processing'),
            'OL2': SensorySection('OL2', 'left', 'outer', 'Logical Pattern Recognition'),
            'OL3': SensorySection('OL3', 'left', 'outer', 'Sequential Analysis'),
            'OL4': SensorySection('OL4', 'left', 'outer', 'Symbolic Interpretation'),
            'OL5': SensorySection('OL5', 'left', 'outer', 'Analytical Filtering'),
            'OL6': SensorySection('OL6', 'left', 'outer', 'Temporal Sequencing')
        }
    
    def _create_right_hemisphere(self) -> Dict[str, BrainSection]:
        """
        Right hemisphere - Spatial, creative, holistic processing
        """
        return {
            'OR1': SensorySection('OR1', 'right', 'outer', 'Spatial Pattern Recognition'),
            'OR2': SensorySection('OR2', 'right', 'outer', 'Holistic Integration'),
            'OR3': SensorySection('OR3', 'right', 'outer', 'Creative Pattern Synthesis'),
            'OR4': SensorySection('OR4', 'right', 'outer', 'Emotional Tone Detection'),
            'OR5': SensorySection('OR5', 'right', 'outer', 'Contextual Awareness'),
            'OR6': SensorySection('OR6', 'right', 'outer', 'Intuitive Processing')
        }
    
    def _create_inter_hemispheric_connections(self):
        """
        Create connections between left and right hemispheres
        """
        # Connect corresponding sections across hemispheres
        connections = [
            ('OL1', 'OR1', 0.8),  # Linguistic <-> Spatial
            ('OL2', 'OR2', 0.7),  # Logical <-> Holistic
            ('OL3', 'OR3', 0.6),  # Sequential <-> Creative
            ('OL4', 'OR4', 0.5),  # Symbolic <-> Emotional
            ('OL5', 'OR5', 0.7),  # Analytical <-> Contextual
            ('OL6', 'OR6', 0.6),  # Temporal <-> Intuitive
        ]
        
        for left_id, right_id, weight in connections:
            self.left_hemisphere[left_id].connect_to(
                self.right_hemisphere[right_id], weight
            )
            self.right_hemisphere[right_id].connect_to(
                self.left_hemisphere[left_id], weight
            )
    
    def process(self, input_data: Any, hemisphere: str = 'both') -> Dict[str, Any]:
        """
        Process input through outer brain
        """
        results = {
            'layer': 'outer',
            'left_results': [],
            'right_results': [],
            'integrated': None
        }
        
        if hemisphere in ['left', 'both']:
            for section in self.left_hemisphere.values():
                result = section.activate(input_data)
                results['left_results'].append(result)
        
        if hemisphere in ['right', 'both']:
            for section in self.right_hemisphere.values():
                result = section.activate(input_data)
                results['right_results'].append(result)
        
        # Simple integration
        results['integrated'] = {
            'left_activations': len(results['left_results']),
            'right_activations': len(results['right_results']),
            'total_sections': len(self.all_sections),
            'processing_complete': True
        }
        
        return results
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current state of outer brain
        """
        return {
            'layer': 'outer',
            'total_sections': len(self.all_sections),
            'left_hemisphere': {
                sid: section.get_state() 
                for sid, section in self.left_hemisphere.items()
            },
            'right_hemisphere': {
                sid: section.get_state() 
                for sid, section in self.right_hemisphere.items()
            }
        }
    
    def reset(self):
        """
        Reset all sections in outer brain
        """
        for section in self.all_sections.values():
            section.reset()
