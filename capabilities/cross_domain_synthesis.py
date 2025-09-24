"""Cross domain synthesis capability for Aenon."""

from __future__ import annotations

from typing import Callable, Dict, List

from core.aenon import CapabilityBase, CapabilityResponse, GoalDescriptor


class CrossDomainSynthesis(CapabilityBase):
    """Combine insights from multiple domains."""

    def __init__(self, config: Dict | None):
        super().__init__(config)

    def applies(self, goal: GoalDescriptor) -> bool:
        related = goal.metadata.get("related_domains", []) if goal.metadata else []
        return bool(related) or "/" in goal.domain

    def execute(self, goal: GoalDescriptor) -> CapabilityResponse:
        synthesis = self._construct_synthesis(goal)
        insights = [item["insight"] for item in synthesis if item.get("insight")]
        summary = "Mapped transferable tactics across the requested domains."
        return CapabilityResponse(
            capability="cross_domain_synthesis",
            summary=summary,
            insights=insights,
            data={"synthesis": synthesis},
        )

    def fuse_capabilities(self, capability_names: List[str]) -> Callable[[GoalDescriptor], List[CapabilityResponse]]:
        """Utility helper to sequentially execute capabilities."""

        def runner(goal: GoalDescriptor) -> List[CapabilityResponse]:
            results: List[CapabilityResponse] = []
            if not self.aenon:
                return results
            for name in capability_names:
                capability = self.aenon.get_capability(name)
                if not capability or not capability.applies(goal):
                    continue
                response = capability.execute(goal)
                if response:
                    results.append(response)
            return results

        return runner

    # ------------------------------------------------------------------
    def _construct_synthesis(self, goal: GoalDescriptor) -> List[Dict[str, str]]:
        related = goal.metadata.get("related_domains", []) if goal.metadata else []
        domains = [goal.domain] + list(related)
        entries: List[Dict[str, str]] = []
        for domain in domains:
            insight = self._retrieve_insight(domain)
            entries.append({
                "domain": domain,
                "insight": insight,
            })
        return entries

    def _retrieve_insight(self, domain: str) -> str:
        if not self.aenon or not self.aenon.memory:
            return f"Document baseline strategies for {domain}."
        memories = self.aenon.memory.retrieve(domain, n_results=1)
        if not memories:
            return f"Document baseline strategies for {domain}."
        memory = memories[0]
        description = memory.get("content", {}).get("description") or memory.get("context", domain)
        return f"Reuse workflow captured in '{description}'."
