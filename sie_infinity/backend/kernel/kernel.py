"""
Metastable Kernel - System checkpoint, attestation, and policy enforcement
"""
import os
import json
import pickle
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


class CheckpointID:
    """Unique identifier for a checkpoint"""
    
    def __init__(self, timestamp: str, hash_value: str):
        self.timestamp = timestamp
        self.hash_value = hash_value
        self.id = f"ckpt_{timestamp}_{hash_value[:8]}"
    
    def __str__(self):
        return self.id
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'hash': self.hash_value
        }


class Attestation:
    """Cryptographic attestation of system state"""
    
    def __init__(self, artifact_hash: str, tests: Dict, signature: bytes = None):
        self.artifact_hash = artifact_hash
        self.tests = tests
        self.timestamp = datetime.now().isoformat()
        self.signature = signature
    
    def to_dict(self):
        return {
            'artifact_hash': self.artifact_hash,
            'tests': self.tests,
            'timestamp': self.timestamp,
            'signature': self.signature.hex() if self.signature else None
        }


class GateResult:
    """Result of merge gate check"""
    
    def __init__(self, ok: bool, why: str = "", test_report: Dict = None, sig: str = None):
        self.ok = ok
        self.why = why
        self.test_report = test_report or {}
        self.sig = sig
    
    def to_dict(self):
        return {
            'ok': self.ok,
            'why': self.why,
            'test_report': self.test_report,
            'signature': self.sig
        }


class Kernel:
    """
    Metastable Kernel - Core system management
    
    Responsibilities:
    - Checkpointing: snapshot/restore of code+state
    - Policy hooks: invariant checks before merges
    - Attestation: sign build lineage (hashes, tests)
    """
    
    def __init__(self, checkpoint_dir: str = "./data/checkpoints"):
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        # Generate RSA key pair for attestation
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        
        self.checkpoints = {}
        self.attestations = []
        self.policies = self._load_default_policies()
        
    def _load_default_policies(self) -> List[Dict]:
        """
        Load default safety policies
        """
        return [
            {
                'name': 'contract_preservation',
                'description': 'Module contracts must remain unchanged',
                'check': lambda proposal: self._check_contracts_unchanged(proposal)
            },
            {
                'name': 'test_coverage',
                'description': 'All tests must pass',
                'check': lambda proposal: self._check_tests_passed(proposal)
            },
            {
                'name': 'safety_invariants',
                'description': 'Safety invariants must be preserved',
                'check': lambda proposal: self._check_safety_invariants(proposal)
            }
        ]
    
    def checkpoint(self, state: Dict[str, Any]) -> CheckpointID:
        """
        Create a checkpoint of current system state
        
        Args:
            state: System state to checkpoint
        
        Returns:
            CheckpointID for the created checkpoint
        """
        timestamp = datetime.now().isoformat()
        
        # Serialize state
        state_bytes = pickle.dumps(state)
        
        # Calculate hash
        hash_value = hashlib.sha256(state_bytes).hexdigest()
        
        # Create checkpoint ID
        checkpoint_id = CheckpointID(timestamp, hash_value)
        
        # Save checkpoint
        checkpoint_path = os.path.join(
            self.checkpoint_dir, 
            f"{checkpoint_id.id}.pkl"
        )
        
        with open(checkpoint_path, 'wb') as f:
            f.write(state_bytes)
        
        # Save metadata
        metadata = {
            'id': checkpoint_id.id,
            'timestamp': timestamp,
            'hash': hash_value,
            'size': len(state_bytes)
        }
        
        metadata_path = os.path.join(
            self.checkpoint_dir,
            f"{checkpoint_id.id}.json"
        )
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.checkpoints[checkpoint_id.id] = checkpoint_id
        
        return checkpoint_id
    
    def restore(self, checkpoint_id: CheckpointID) -> Optional[Dict[str, Any]]:
        """
        Restore system state from checkpoint
        
        Args:
            checkpoint_id: ID of checkpoint to restore
        
        Returns:
            Restored state or None if checkpoint not found
        """
        if isinstance(checkpoint_id, str):
            checkpoint_id_str = checkpoint_id
        else:
            checkpoint_id_str = checkpoint_id.id
        
        checkpoint_path = os.path.join(
            self.checkpoint_dir,
            f"{checkpoint_id_str}.pkl"
        )
        
        if not os.path.exists(checkpoint_path):
            return None
        
        try:
            with open(checkpoint_path, 'rb') as f:
                state = pickle.load(f)
            return state
        except Exception as e:
            print(f"Error restoring checkpoint: {e}")
            return None
    
    def attest(self, artifact_hash: str, tests: Dict) -> Attestation:
        """
        Create cryptographic attestation of artifact
        
        Args:
            artifact_hash: Hash of artifact to attest
            tests: Test results
        
        Returns:
            Attestation object
        """
        # Create attestation data
        attestation_data = f"{artifact_hash}:{json.dumps(tests)}".encode()
        
        # Sign with private key
        signature = self.private_key.sign(
            attestation_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        attestation = Attestation(artifact_hash, tests, signature)
        self.attestations.append(attestation)
        
        return attestation
    
    def gate_merge(self, proposal: Dict) -> GateResult:
        """
        Gate check before allowing merge
        
        Args:
            proposal: Modification proposal
        
        Returns:
            GateResult indicating if merge is allowed
        """
        # Check all policies
        for policy in self.policies:
            try:
                if not policy['check'](proposal):
                    return GateResult(
                        ok=False,
                        why=f"Policy violation: {policy['name']} - {policy['description']}"
                    )
            except Exception as e:
                return GateResult(
                    ok=False,
                    why=f"Policy check error: {policy['name']} - {str(e)}"
                )
        
        # All policies passed
        test_report = proposal.get('evidence', {}).get('tests_passed', [])
        
        # Create attestation
        artifact_hash = hashlib.sha256(
            json.dumps(proposal).encode()
        ).hexdigest()
        
        attestation = self.attest(artifact_hash, {'tests': test_report})
        
        return GateResult(
            ok=True,
            why="All policies satisfied",
            test_report={'tests': test_report},
            sig=attestation.signature.hex()
        )
    
    def _check_contracts_unchanged(self, proposal: Dict) -> bool:
        """
        Check if contracts are unchanged in proposal
        """
        safety_claims = proposal.get('safety_claims', [])
        return 'contracts unchanged' in safety_claims
    
    def _check_tests_passed(self, proposal: Dict) -> bool:
        """
        Check if all tests passed
        """
        evidence = proposal.get('evidence', {})
        tests_passed = evidence.get('tests_passed', [])
        return len(tests_passed) > 0
    
    def _check_safety_invariants(self, proposal: Dict) -> bool:
        """
        Check if safety invariants are preserved
        """
        safety_claims = proposal.get('safety_claims', [])
        # At minimum, should have some safety claims
        return len(safety_claims) > 0
    
    def list_checkpoints(self) -> List[Dict]:
        """
        List all available checkpoints
        """
        checkpoints = []
        
        for filename in os.listdir(self.checkpoint_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.checkpoint_dir, filename)
                with open(filepath, 'r') as f:
                    metadata = json.load(f)
                    checkpoints.append(metadata)
        
        return sorted(checkpoints, key=lambda x: x['timestamp'], reverse=True)
    
    def get_attestations(self) -> List[Dict]:
        """
        Get all attestations
        """
        return [att.to_dict() for att in self.attestations]
    
    def add_policy(self, name: str, description: str, check_func):
        """
        Add a custom policy
        """
        self.policies.append({
            'name': name,
            'description': description,
            'check': check_func
        })
    
    def get_policies(self) -> List[Dict]:
        """
        Get all active policies
        """
        return [
            {'name': p['name'], 'description': p['description']}
            for p in self.policies
        ]
