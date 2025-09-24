"""Command line entry point for the Aenon agent."""

from __future__ import annotations

import json

from core.aenon import GoalDescriptor
from core.bootstrap import bootstrap_aenon


def main() -> None:
    aenon = bootstrap_aenon()

    goal = GoalDescriptor(
        domain="smart_home",
        description="Connect the thermostat to weather services and adjust based on forecast.",
        constraints=["use_free_apis"],
        success_metrics={"energy_savings": 0.1},
    )

    report = aenon.execute_goal(goal)
    print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
