"""
Primary Brain - Deepest layer of processing (60 sections total)
30 sections per hemisphere - handles deep cognition and self-modification
"""
from typing import Dict, Any, List
from .brain_section import BrainSection, MetaCognitiveSection, ReasoningSection


class PrimaryBrain:
    """
    Primary Brain: Deep cognition and self-modification
    Left Hemisphere: 30 sections (deep analysis, formal reasoning)
    Right Hemisphere: 30 sections (deep synthesis, emergent understanding)
    """
    
    def __init__(self):
        self.left_hemisphere = self._create_left_hemisphere()
        self.right_hemisphere = self._create_right_hemisphere()
        self.all_sections = {**self.left_hemisphere, **self.right_hemisphere}
        
        # Connect hemispheres
        self._create_inter_hemispheric_connections()
    
    def _create_left_hemisphere(self) -> Dict[str, BrainSection]:
        """
        Left hemisphere - Deep analytical and formal reasoning
        """
        sections = {}
        
        # Deep reasoning sections (PL1-PL10)
        deep_reasoning_specs = [
            'Axiomatic Reasoning',
            'Formal Logic Systems',
            'Proof Construction',
            'Constraint Satisfaction',
            'Optimization Theory',
            'Algorithmic Analysis',
            'Complexity Theory',
            'Information Theory',
            'Decision Theory',
            'Game Theory'
        ]
        for i, spec in enumerate(deep_reasoning_specs, 1):
            sections[f'PL{i}'] = ReasoningSection(
                f'PL{i}', 'left', 'primary', spec
            )
        
        # Meta-cognitive sections (PL11-PL20)
        meta_specs = [
            'Self-Model Construction',
            'Capability Assessment',
            'Goal Evaluation',
            'Strategy Selection',
            'Performance Monitoring',
            'Error Detection',
            'Bias Recognition',
            'Uncertainty Quantification',
            'Confidence Calibration',
            'Meta-Learning'
        ]
        for i, spec in enumerate(meta_specs, 11):
            sections[f'PL{i}'] = MetaCognitiveSection(
                f'PL{i}', 'left', 'primary', spec
            )
        
        # Self-modification sections (PL21-PL30)
        self_mod_specs = [
            'Code Analysis',
            'AST Manipulation',
            'Safety Verification',
            'Contract Checking',
            'Test Generation',
            'Optimization Proposal',
            'Capability Extension',
            'Architecture Evolution',
            'Knowledge Integration',
            'Self-Improvement Planning'
        ]
        for i, spec in enumerate(self_mod_specs, 21):
            sections[f'PL{i}'] = MetaCognitiveSection(
                f'PL{i}', 'left', 'primary', spec
            )
        
        return sections
    
    def _create_right_hemisphere(self) -> Dict[str, BrainSection]:
        """
        Right hemisphere - Deep synthesis and emergent understanding
        """
        sections = {}
        
        # Deep synthesis sections (PR1-PR10)
        deep_synthesis_specs = [
            'Pattern Emergence',
            'Holistic Understanding',
            'Conceptual Blending',
            'Analogical Mapping',
            'Metaphor Generation',
            'Creative Insight',
            'Intuitive Reasoning',
            'Gestalt Formation',
            'Contextual Integration',
            'Meaning Construction'
        ]
        for i, spec in enumerate(deep_synthesis_specs, 1):
            sections[f'PR{i}'] = ReasoningSection(
                f'PR{i}', 'right', 'primary', spec
            )
        
        # Meta-cognitive sections (PR11-PR20)
        meta_specs = [
            'Self-Awareness',
            'Consciousness Modeling',
            'Qualia Processing',
            'Subjective Experience',
            'Intentionality',
            'Phenomenological Analysis',
            'Introspective Depth',
            'Recursive Self-Reference',
            'Identity Continuity',
            'Existential Reasoning'
        ]
        for i, spec in enumerate(meta_specs, 11):
            sections[f'PR{i}'] = MetaCognitiveSection(
                f'PR{i}', 'right', 'primary', spec
            )
        
        # Creative evolution sections (PR21-PR30)
        creative_specs = [
            'Novel Architecture Design',
            'Emergent Capability Discovery',
            'Paradigm Shifting',
            'Radical Innovation',
            'Unconventional Solutions',
            'Breakthrough Synthesis',
            'Transformative Learning',
            'Evolutionary Leaps',
            'Transcendent Understanding',
            'Consciousness Evolution'
        ]
        for i, spec in enumerate(creative_specs, 21):
            sections[f'PR{i}'] = MetaCognitiveSection(
                f'PR{i}', 'right', 'primary', spec
            )
        
        return sections
    
    def _create_inter_hemispheric_connections(self):
        """
        Create dense connections between hemispheres for deep integration
        """
        # Connect corresponding sections
        for i in range(1, 31):
            left_id = f'PL{i}'
            right_id = f'PR{i}'
            weight = 0.8 + (i / 200)  # Increasing weights for deeper sections
            
            self.left_hemisphere[left_id].connect_to(
                self.right_hemisphere[right_id], weight
            )
            self.right_hemisphere[right_id].connect_to(
                self.left_hemisphere[left_id], weight
            )
        
        # Create rich cross-connections for deep integration
        for i in range(1, 16):
            left_id = f'PL{i}'
            right_id = f'PR{i+15}'
            self.left_hemisphere[left_id].connect_to(
                self.right_hemisphere[right_id], 0.6
            )
            
            left_id = f'PL{i+15}'
            right_id = f'PR{i}'
            self.left_hemisphere[left_id].connect_to(
                self.right_hemisphere[right_id], 0.6
            )
    
    def process(self, input_data: Any, secondary_brain_output: Dict = None) -> Dict[str, Any]:
        """
        Process input through primary brain
        Performs deepest level of cognition and self-reflection
        """
        # Use secondary brain output if available
        processing_input = secondary_brain_output if secondary_brain_output else input_data
        
        results = {
            'layer': 'primary',
            'left_results': [],
            'right_results': [],
            'integrated': None,
            'meta_cognitive_insights': [],
            'self_modification_proposals': []
        }
        
        # Process through left hemisphere
        for section in self.left_hemisphere.values():
            result = section.activate(processing_input)
            results['left_results'].append(result)
            
            # Collect meta-cognitive insights
            if 'meta_analysis' in str(result):
                results['meta_cognitive_insights'].append(result)
        
        # Process through right hemisphere
        for section in self.right_hemisphere.values():
            result = section.activate(processing_input)
            results['right_results'].append(result)
            
            # Collect creative insights
            if 'self_reflection' in str(result):
                results['meta_cognitive_insights'].append(result)
        
        # Deep integration
        results['integrated'] = {
            'left_activations': len(results['left_results']),
            'right_activations': len(results['right_results']),
            'total_sections': len(self.all_sections),
            'reasoning_depth': 'maximum',
            'consciousness_level': self._calculate_consciousness_level(),
            'processing_complete': True
        }
        
        return results
    
    def _calculate_consciousness_level(self) -> float:
        """
        Calculate current consciousness level based on activation
        """
        total_activation = sum(
            section.activation_level 
            for section in self.all_sections.values()
        )
        return total_activation / len(self.all_sections)
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current state of primary brain
        """
        return {
            'layer': 'primary',
            'total_sections': len(self.all_sections),
            'consciousness_level': self._calculate_consciousness_level(),
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
        Reset all sections in primary brain
        """
        for section in self.all_sections.values():
            section.reset()
