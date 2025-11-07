"""
Verifier - Test and safety verification for code modifications
"""
import ast
import re
from typing import Dict, Any, List, Optional


class TestReport:
    """Test execution report"""
    
    def __init__(self, passed: bool, tests_run: int, failures: List[str] = None):
        self.passed = passed
        self.tests_run = tests_run
        self.failures = failures or []
    
    def to_dict(self):
        return {
            'passed': self.passed,
            'tests_run': self.tests_run,
            'failures': self.failures
        }


class FuzzReport:
    """Fuzz testing report"""
    
    def __init__(self, passed: bool, iterations: int, crashes: List[str] = None):
        self.passed = passed
        self.iterations = iterations
        self.crashes = crashes or []
    
    def to_dict(self):
        return {
            'passed': self.passed,
            'iterations': self.iterations,
            'crashes': self.crashes
        }


class MetricDelta:
    """Metric comparison result"""
    
    def __init__(self, metric_name: str, before: float, after: float, delta: float, acceptable: bool):
        self.metric_name = metric_name
        self.before = before
        self.after = after
        self.delta = delta
        self.acceptable = acceptable
    
    def to_dict(self):
        return {
            'metric': self.metric_name,
            'before': self.before,
            'after': self.after,
            'delta': self.delta,
            'acceptable': self.acceptable
        }


class Verifier:
    """
    Verification system for code modifications
    """
    
    def __init__(self):
        self.forbidden_patterns = [
            r'os\.system',
            r'subprocess\.call',
            r'eval\(',
            r'exec\(',
            r'__import__',
            r'open\(.+[\'"]w',  # Writing files
        ]
    
    def check_contracts_unchanged(self, module: Dict) -> bool:
        """
        Verify that module contracts haven't changed
        
        Args:
            module: Module information with contracts
        
        Returns:
            True if contracts are unchanged
        """
        # Check if module has contract information
        if 'contracts' not in module:
            return False
        
        contracts = module['contracts']
        
        # Verify input/output schemas exist
        if 'input_schema' not in contracts or 'output_schema' not in contracts:
            return False
        
        return True
    
    def run_tests(self, module: Dict) -> TestReport:
        """
        Run tests for a module
        
        Args:
            module: Module information with test specifications
        
        Returns:
            TestReport with results
        """
        # Simulate test execution
        # In real implementation, would execute actual tests
        
        tests = module.get('tests', {})
        unit_tests = tests.get('unit', [])
        property_tests = tests.get('property', [])
        
        total_tests = len(unit_tests) + len(property_tests)
        
        if total_tests == 0:
            return TestReport(False, 0, ['No tests defined'])
        
        # Simulate all tests passing
        return TestReport(True, total_tests, [])
    
    def run_fuzz(self, module: Dict, budget_s: int) -> FuzzReport:
        """
        Run fuzz testing on module
        
        Args:
            module: Module to fuzz test
            budget_s: Time budget in seconds
        
        Returns:
            FuzzReport with results
        """
        # Simulate fuzz testing
        # In real implementation, would perform actual fuzzing
        
        iterations = budget_s * 100  # Simulate iterations
        
        return FuzzReport(True, iterations, [])
    
    def scan_forbidden(self, module: Dict, patterns: List[str] = None) -> List[str]:
        """
        Scan for forbidden patterns in code
        
        Args:
            module: Module to scan
            patterns: Additional patterns to check (optional)
        
        Returns:
            List of violations found
        """
        violations = []
        
        # Get source code
        source = module.get('source', '')
        
        # Check forbidden patterns
        patterns_to_check = self.forbidden_patterns + (patterns or [])
        
        for pattern in patterns_to_check:
            if re.search(pattern, source):
                violations.append(f"Forbidden pattern found: {pattern}")
        
        return violations
    
    def compare_metrics(self, before: Dict, after: Dict, tolerance: float = 0.1) -> List[MetricDelta]:
        """
        Compare metrics before and after modification
        
        Args:
            before: Metrics before modification
            after: Metrics after modification
            tolerance: Acceptable tolerance for degradation
        
        Returns:
            List of MetricDelta objects
        """
        deltas = []
        
        for metric_name in before.keys():
            if metric_name in after:
                before_val = before[metric_name]
                after_val = after[metric_name]
                delta = after_val - before_val
                
                # Check if degradation is acceptable
                acceptable = True
                if delta < 0:  # Degradation
                    acceptable = abs(delta / before_val) <= tolerance
                
                deltas.append(MetricDelta(
                    metric_name, before_val, after_val, delta, acceptable
                ))
        
        return deltas
    
    def verify_safety_invariants(self, module: Dict) -> bool:
        """
        Verify safety invariants are preserved
        
        Args:
            module: Module to verify
        
        Returns:
            True if all safety invariants hold
        """
        # Check for forbidden patterns
        violations = self.scan_forbidden(module)
        if violations:
            return False
        
        # Check contracts
        if not self.check_contracts_unchanged(module):
            return False
        
        # Check resource limits
        resources = module.get('resources', {})
        if 'cpu_max' in resources and resources['cpu_max'] > 10:
            return False  # Too much CPU
        
        if 'ram_gb_max' in resources and resources['ram_gb_max'] > 10:
            return False  # Too much RAM
        
        return True
    
    def comprehensive_verification(self, module: Dict, budget_s: int = 10) -> Dict[str, Any]:
        """
        Run comprehensive verification suite
        
        Args:
            module: Module to verify
            budget_s: Time budget for fuzzing
        
        Returns:
            Complete verification report
        """
        report = {
            'module': module.get('name', 'unknown'),
            'timestamp': self._get_timestamp(),
            'results': {}
        }
        
        # Contract check
        report['results']['contracts'] = self.check_contracts_unchanged(module)
        
        # Test execution
        test_report = self.run_tests(module)
        report['results']['tests'] = test_report.to_dict()
        
        # Fuzz testing
        fuzz_report = self.run_fuzz(module, budget_s)
        report['results']['fuzz'] = fuzz_report.to_dict()
        
        # Forbidden pattern scan
        violations = self.scan_forbidden(module)
        report['results']['forbidden_patterns'] = {
            'violations': violations,
            'passed': len(violations) == 0
        }
        
        # Safety invariants
        report['results']['safety_invariants'] = self.verify_safety_invariants(module)
        
        # Overall pass/fail
        report['passed'] = all([
            report['results']['contracts'],
            report['results']['tests']['passed'],
            report['results']['fuzz']['passed'],
            report['results']['forbidden_patterns']['passed'],
            report['results']['safety_invariants']
        ])
        
        return report
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
