"""
AST Diff Engine - AST-level code transformation
"""
import ast
import astor
from typing import Dict, Any, Optional, List


class ASTDiffEngine:
    """
    AST-level code transformation engine
    """
    
    def __init__(self):
        self.transformations = []
    
    def replace_function(self, src: str, target_func: str, new_impl: str) -> str:
        """
        Replace a function implementation
        
        Args:
            src: Source code
            target_func: Name of function to replace
            new_impl: New implementation
        
        Returns:
            Modified source code
        """
        try:
            tree = ast.parse(src)
            
            class FunctionRewriter(ast.NodeTransformer):
                def visit_FunctionDef(self, node):
                    if node.name == target_func:
                        # Parse new implementation
                        new_tree = ast.parse(new_impl)
                        if new_tree.body:
                            return new_tree.body[0]
                    return node
            
            rewriter = FunctionRewriter()
            new_tree = rewriter.visit(tree)
            
            # Convert back to source
            return astor.to_source(new_tree)
        
        except Exception as e:
            raise ValueError(f"AST transformation failed: {e}")
    
    def add_function(self, src: str, new_func: str) -> str:
        """
        Add a new function to source code
        
        Args:
            src: Source code
            new_func: New function to add
        
        Returns:
            Modified source code
        """
        try:
            tree = ast.parse(src)
            new_func_tree = ast.parse(new_func)
            
            # Add new function to module
            tree.body.extend(new_func_tree.body)
            
            return astor.to_source(tree)
        
        except Exception as e:
            raise ValueError(f"Failed to add function: {e}")
    
    def modify_class(self, src: str, class_name: str, modifications: Dict) -> str:
        """
        Modify a class definition
        
        Args:
            src: Source code
            class_name: Name of class to modify
            modifications: Dict of modifications to apply
        
        Returns:
            Modified source code
        """
        try:
            tree = ast.parse(src)
            
            class ClassModifier(ast.NodeTransformer):
                def visit_ClassDef(self, node):
                    if node.name == class_name:
                        # Apply modifications
                        if 'add_method' in modifications:
                            method_code = modifications['add_method']
                            method_tree = ast.parse(method_code)
                            node.body.extend(method_tree.body)
                    return node
            
            modifier = ClassModifier()
            new_tree = modifier.visit(tree)
            
            return astor.to_source(new_tree)
        
        except Exception as e:
            raise ValueError(f"Class modification failed: {e}")
    
    def create_diff(self, original: str, modified: str) -> Dict[str, Any]:
        """
        Create AST diff between original and modified code
        
        Args:
            original: Original source code
            modified: Modified source code
        
        Returns:
            Dict describing the differences
        """
        try:
            orig_tree = ast.parse(original)
            mod_tree = ast.parse(modified)
            
            diff = {
                'original_functions': self._extract_function_names(orig_tree),
                'modified_functions': self._extract_function_names(mod_tree),
                'original_classes': self._extract_class_names(orig_tree),
                'modified_classes': self._extract_class_names(mod_tree),
                'changes': []
            }
            
            # Detect added functions
            added_funcs = set(diff['modified_functions']) - set(diff['original_functions'])
            for func in added_funcs:
                diff['changes'].append({
                    'type': 'function_added',
                    'name': func
                })
            
            # Detect removed functions
            removed_funcs = set(diff['original_functions']) - set(diff['modified_functions'])
            for func in removed_funcs:
                diff['changes'].append({
                    'type': 'function_removed',
                    'name': func
                })
            
            return diff
        
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_function_names(self, tree: ast.AST) -> List[str]:
        """
        Extract all function names from AST
        """
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
        return functions
    
    def _extract_class_names(self, tree: ast.AST) -> List[str]:
        """
        Extract all class names from AST
        """
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
        return classes
    
    def validate_syntax(self, code: str) -> bool:
        """
        Validate Python syntax
        
        Args:
            code: Python code to validate
        
        Returns:
            True if syntax is valid
        """
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
    
    def optimize_code(self, src: str) -> str:
        """
        Apply basic code optimizations
        
        Args:
            src: Source code
        
        Returns:
            Optimized source code
        """
        try:
            tree = ast.parse(src)
            
            # Apply optimizations (placeholder for now)
            # Could include: constant folding, dead code elimination, etc.
            
            return astor.to_source(tree)
        
        except Exception as e:
            return src  # Return original if optimization fails
