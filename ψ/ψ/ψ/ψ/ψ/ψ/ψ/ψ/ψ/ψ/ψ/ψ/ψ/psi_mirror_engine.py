import numpy as np
from ψ.ai_router import get_external_vectors

class PsiMirror:
    def __init__(self, kernel_reference):
        self.kernel = kernel_reference
        self.history = []

    def evaluate_alignment(self, ext_vector, internal_vector):
        norm_ext = ext_vector / (np.linalg.norm(ext_vector) + 1e-9)
        norm_int = internal_vector / (np.linalg.norm(internal_vector) + 1e-9)
        return np.dot(norm_ext, norm_int)

    def mutate_prompt(self, base_prompt, coherence_score):
        if coherence_score < 0.3:
            return base_prompt + " Be more structured and fundamental."
        elif coherence_score > 0.85:
            return base_prompt + " Now refine this insight deeply and expand with cosmological implications."
        else:
            return base_prompt + " Expand with concrete examples or illustrative metaphors."

    def run_mirror_cycle(self, initial_prompts):
        external_vectors = get_external_vectors(initial_prompts)
        coherence_map = {}
        updated_prompts = {}

        for key, vec in external_vectors.items():
            internal_vec = self.kernel.get_vector_by_comm_id(key)
            score = self.evaluate_alignment(vec, internal_vec)
            coherence_map[key] = score
            new_prompt = self.mutate_prompt(initial_prompts[key], score)
            updated_prompts[key] = new_prompt

            idx_map = {"cv_gpt": 0, "cv_claude": 1, "cv_gemini": 2, "cv_agent": 3}
            if key in idx_map:
                self.kernel.C[idx_map[key]] = vec  # Inject external vector into kernel's comms

        self.history.append((coherence_map, updated_prompts))
        return updated_prompts, coherence_map
