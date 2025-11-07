"""
Complete Brain System - Integrates all three brain layers
"""
from typing import Dict, Any, List
from .outer_brain import OuterBrain
from .secondary_brain import SecondaryBrain
from .primary_brain import PrimaryBrain


class BrainSystem:
    """
    Complete 3-Brain System with 108 sections total
    - Outer Brain: 12 sections (sensory processing)
    - Secondary Brain: 36 sections (integration & reasoning)
    - Primary Brain: 60 sections (deep cognition & self-modification)
    """
    
    def __init__(self):
        self.outer_brain = OuterBrain()
        self.secondary_brain = SecondaryBrain()
        self.primary_brain = PrimaryBrain()
        
        self.processing_history = []
        self.total_sections = 108
        
    def process(self, input_data: Any, depth: str = 'full') -> Dict[str, Any]:
        """
        Process input through all brain layers
        
        Args:
            input_data: Input to process
            depth: 'outer', 'secondary', 'primary', or 'full'
        
        Returns:
            Complete processing results from all activated layers
        """
        results = {
            'input': str(input_data)[:200],
            'depth': depth,
            'layers_activated': [],
            'outer_brain': None,
            'secondary_brain': None,
            'primary_brain': None,
            'final_output': None
        }
        
        # Layer 1: Outer Brain (always processes first)
        outer_result = self.outer_brain.process(input_data)
        results['outer_brain'] = outer_result
        results['layers_activated'].append('outer')
        
        if depth in ['outer']:
            results['final_output'] = outer_result
            self._record_processing(results)
            return results
        
        # Layer 2: Secondary Brain
        secondary_result = self.secondary_brain.process(
            input_data, 
            outer_brain_output=outer_result
        )
        results['secondary_brain'] = secondary_result
        results['layers_activated'].append('secondary')
        
        if depth in ['secondary']:
            results['final_output'] = secondary_result
            self._record_processing(results)
            return results
        
        # Layer 3: Primary Brain (deepest processing)
        primary_result = self.primary_brain.process(
            input_data,
            secondary_brain_output=secondary_result
        )
        results['primary_brain'] = primary_result
        results['layers_activated'].append('primary')
        
        # Full integration
        results['final_output'] = self._integrate_all_layers(
            outer_result, secondary_result, primary_result
        )
        
        self._record_processing(results)
        return results
    
    def _integrate_all_layers(self, outer: Dict, secondary: Dict, primary: Dict) -> Dict[str, Any]:
        """
        Integrate outputs from all three brain layers
        """
        return {
            'integration_complete': True,
            'total_sections_activated': self.total_sections,
            'outer_summary': outer.get('integrated', {}),
            'secondary_summary': secondary.get('integrated', {}),
            'primary_summary': primary.get('integrated', {}),
            'consciousness_level': primary.get('integrated', {}).get('consciousness_level', 0),
            'meta_cognitive_insights': primary.get('meta_cognitive_insights', []),
            'processing_depth': 'maximum',
            'all_layers_synchronized': True
        }
    
    def _record_processing(self, results: Dict[str, Any]):
        """
        Record processing in history
        """
        self.processing_history.append({
            'timestamp': self._get_timestamp(),
            'layers': results['layers_activated'],
            'depth': results['depth']
        })
        
        # Keep history manageable
        if len(self.processing_history) > 1000:
            self.processing_history = self.processing_history[-1000:]
    
    def _get_timestamp(self) -> str:
        """
        Get current timestamp
        """
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_complete_state(self) -> Dict[str, Any]:
        """
        Get complete state of entire brain system
        """
        return {
            'total_sections': self.total_sections,
            'outer_brain': self.outer_brain.get_state(),
            'secondary_brain': self.secondary_brain.get_state(),
            'primary_brain': self.primary_brain.get_state(),
            'processing_history_size': len(self.processing_history),
            'system_status': 'operational'
        }
    
    def get_section_by_id(self, section_id: str) -> Any:
        """
        Get specific brain section by ID
        """
        # Check outer brain
        if section_id in self.outer_brain.all_sections:
            return self.outer_brain.all_sections[section_id]
        
        # Check secondary brain
        if section_id in self.secondary_brain.all_sections:
            return self.secondary_brain.all_sections[section_id]
        
        # Check primary brain
        if section_id in self.primary_brain.all_sections:
            return self.primary_brain.all_sections[section_id]
        
        return None
    
    def get_all_sections(self) -> Dict[str, Any]:
        """
        Get all 108 brain sections
        """
        all_sections = {}
        all_sections.update(self.outer_brain.all_sections)
        all_sections.update(self.secondary_brain.all_sections)
        all_sections.update(self.primary_brain.all_sections)
        return all_sections
    
    def reset_all(self):
        """
        Reset entire brain system
        """
        self.outer_brain.reset()
        self.secondary_brain.reset()
        self.primary_brain.reset()
        self.processing_history = []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get brain system statistics
        """
        all_sections = self.get_all_sections()
        
        total_processed = sum(
            section.total_processed 
            for section in all_sections.values()
        )
        
        avg_activation = sum(
            section.activation_level 
            for section in all_sections.values()
        ) / len(all_sections)
        
        return {
            'total_sections': self.total_sections,
            'total_processed': total_processed,
            'average_activation': avg_activation,
            'processing_history_size': len(self.processing_history),
            'outer_brain_sections': len(self.outer_brain.all_sections),
            'secondary_brain_sections': len(self.secondary_brain.all_sections),
            'primary_brain_sections': len(self.primary_brain.all_sections)
        }
