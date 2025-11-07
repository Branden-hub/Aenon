"""
Secondary Brain - Middle layer of processing (36 sections total)
18 sections per hemisphere - handles integration and reasoning
"""
from typing import Dict, Any, List
from .brain_section import BrainSection, IntegrationSection, ReasoningSection


class SecondaryBrain:
    """
    Secondary Brain: Integration and reasoning layer
    Left Hemisphere: 18 sections (logical reasoning, analysis)
    Right Hemisphere: 18 sections (creative synthesis, pattern recognition)
    """
    
    def __init__(self):
        self.left_hemisphere = self._create_left_hemisphere()
        self.right_hemisphere = self._create_right_hemisphere()
        self.all_sections = {**self.left_hemisphere, **self.right_hemisphere}
        
        # Connect hemispheres
        self._create_inter_hemispheric_connections()
    
    def _create_left_hemisphere(self) -> Dict[str, BrainSection]:
        """
        Left hemisphere - Logical reasoning and analytical integration
        """
        sections = {}
        
        # Integration sections (SL1-SL6)
        for i in range(1, 7):
            sections[f'SL{i}'] = IntegrationSection(
                f'SL{i}', 'left', 'secondary', 
                f'Logical Integration {i}'
            )
        
        # Reasoning sections (SL7-SL12)
        for i in range(7, 13):
            sections[f'SL{i}'] = ReasoningSection(
                f'SL{i}', 'left', 'secondary',
                f'Analytical Reasoning {i-6}'
            )
        
        # Advanced processing (SL13-SL18)
        specializations = [
            'Causal Analysis',
            'Deductive Logic',
            'Mathematical Reasoning',
            'Systematic Planning',
            'Rule-Based Processing',
            'Formal Verification'
        ]
        for i, spec in enumerate(specializations, 13):
            sections[f'SL{i}'] = ReasoningSection(
                f'SL{i}', 'left', 'secondary', spec
            )
        
        return sections
    
    def _create_right_hemisphere(self) -> Dict[str, BrainSection]:
        """
        Right hemisphere - Creative synthesis and pattern integration
        """
        sections = {}
        
        # Integration sections (SR1-SR6)
        for i in range(1, 7):
            sections[f'SR{i}'] = IntegrationSection(
                f'SR{i}', 'right', 'secondary',
                f'Holistic Integration {i}'
            )
        
        # Creative reasoning (SR7-SR12)
        for i in range(7, 13):
            sections[f'SR{i}'] = ReasoningSection(
                f'SR{i}', 'right', 'secondary',
                f'Creative Synthesis {i-6}'
            )
        
        # Advanced processing (SR13-SR18)
        specializations = [
            'Pattern Synthesis',
            'Analogical Reasoning',
            'Intuitive Leaps',
            'Contextual Understanding',
            'Metaphorical Thinking',
            'Emergent Pattern Detection'
        ]
        for i, spec in enumerate(specializations, 13):
            sections[f'SR{i}'] = ReasoningSection(
                f'SR{i}', 'right', 'secondary', spec
            )
        
        return sections
    
    def _create_inter_hemispheric_connections(self):
        """
        Create rich connections between hemispheres
        """
        # Connect corresponding sections
        for i in range(1, 19):
            left_id = f'SL{i}'
            right_id = f'SR{i}'
            weight = 0.7 + (i / 100)  # Slightly varying weights
            
            self.left_hemisphere[left_id].connect_to(
                self.right_hemisphere[right_id], weight
            )
            self.right_hemisphere[right_id].connect_to(
                self.left_hemisphere[left_id], weight
            )
        
        # Create cross-connections for integration
        for i in range(1, 10):
            left_id = f'SL{i}'
            right_id = f'SR{i+9}'
            self.left_hemisphere[left_id].connect_to(
                self.right_hemisphere[right_id], 0.5
            )
    
    def process(self, input_data: Any, outer_brain_output: Dict = None) -> Dict[str, Any]:
        """
        Process input through secondary brain
        Integrates output from outer brain
        """
        # Use outer brain output if available
        processing_input = outer_brain_output if outer_brain_output else input_data
        
        results = {
            'layer': 'secondary',
            'left_results': [],
            'right_results': [],
            'integrated': None
        }
        
        # Process through left hemisphere
        for section in self.left_hemisphere.values():
            result = section.activate(processing_input)
            results['left_results'].append(result)
        
        # Process through right hemisphere
        for section in self.right_hemisphere.values():
            result = section.activate(processing_input)
            results['right_results'].append(result)
        
        # Integration
        results['integrated'] = {
            'left_activations': len(results['left_results']),
            'right_activations': len(results['right_results']),
            'total_sections': len(self.all_sections),
            'reasoning_depth': 'intermediate',
            'processing_complete': True
        }
        
        return results
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current state of secondary brain
        """
        return {
            'layer': 'secondary',
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
        Reset all sections in secondary brain
        """
        for section in self.all_sections.values():
            section.reset()
