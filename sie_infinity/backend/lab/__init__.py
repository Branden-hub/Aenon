"""
Self-Modification Lab - AST-level code evolution
"""

from .diff_ast import ASTDiffEngine
from .verify import Verifier
from .merge import Merger
from .lab import SelfModificationLab

__all__ = ['ASTDiffEngine', 'Verifier', 'Merger', 'SelfModificationLab']
