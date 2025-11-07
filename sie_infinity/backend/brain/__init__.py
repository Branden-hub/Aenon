"""
SIE-∞ Three-Brain Architecture
Outer Brain (12 sections) → Secondary Brain (36 sections) → Primary Brain (60 sections)
Each brain has left and right hemispheres with specialized sections
"""

from .outer_brain import OuterBrain
from .secondary_brain import SecondaryBrain
from .primary_brain import PrimaryBrain
from .brain_system import BrainSystem

__all__ = ['OuterBrain', 'SecondaryBrain', 'PrimaryBrain', 'BrainSystem']
