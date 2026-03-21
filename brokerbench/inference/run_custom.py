"""Generic adapter interface for running custom agents against BrokerBench.

This module provides a base class that custom agent adapters can implement
to integrate any real estate AI with the BrokerBench evaluation framework.

Usage:
    1. Subclass CustomAgentAdapter
    2. Implement the `predict` method
    3. Call `run_benchmark` to evaluate

Example:
    class MyAgent(CustomAgentAdapter):
        def predict(self, instance: Instance) -> Prediction:
            response = my_agent.ask(instance.question)
            return Prediction(
                instance_id=instance.instance_id,
                model_name_or_path="my-agent",
                prediction=response.answer,
                reasoning=response.reasoning,
            )

    adapter = MyAgent()
    adapter.run_benchmark(dataset_path="all", output_path=Path("predictions.jsonl"))
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from rich.console import Console
from tqdm import tqdm

from brokerbench.harness.types import Instance, Prediction
from brokerbench.inference import load_instances

console = Console()


class CustomAgentAdapter(ABC):
    """Base class for custom agent adapters."""

    @abstractmethod
    def predict(self, instance: Instance) -> Prediction:
        """Generate a prediction for a single benchmark instance.

        Args:
            instance: The benchmark instance to predict.

        Returns:
            A Prediction object with the model's response.
        """
        ...

    def run_benchmark(
        self,
        dataset_path: str,
        output_path: Path,
    ) -> list[Prediction]:
        """Run the adapter against the full benchmark.

        Args:
            dataset_path: Path to JSONL dataset or 'all' for built-in datasets.
            output_path: Path to write prediction JSONL.

        Returns:
            List of Prediction objects.
        """
        instances = load_instances(dataset_path)
        console.print(f"Loaded {len(instances)} instances")

        predictions: list[Prediction] = []
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            for instance in tqdm(instances, desc="Running custom agent"):
                try:
                    pred = self.predict(instance)
                except Exception as e:
                    console.print(f"[yellow]Error on {instance.instance_id}: {e}[/yellow]")
                    pred = Prediction(
                        instance_id=instance.instance_id,
                        model_name_or_path="custom",
                        prediction="",
                        reasoning="",
                        raw_output=str(e),
                        metadata={"error": str(e)},
                    )
                predictions.append(pred)
                f.write(pred.model_dump_json() + "\n")

        console.print(f"[green]Predictions written to {output_path}[/green]")
        return predictions
