# ai_cdss_cli/cli.py
import os
import logging
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv
import typer
from ai_cdss import DataLoader, DataProcessor
from ai_cdss.interface import CDSSInterface

logger = logging.getLogger(__name__)

cli = typer.Typer(help="CLI for the AI-CDSS Client.")

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # RGS_MODE: str = "app"
    WEIGHTS: List[int] = [1, 1, 1]
    ALPHA: float = 0.5
    N: int = 12
    DAYS: int = 7
    PROTOCOLS_PER_DAY: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # or "allow" if you prefer
    )

def get_settings(env_file: Optional[Path] = None) -> Settings:
    """
    Build Settings once, optionally pointing at a custom .env file.
    If env_file is None, falls back to the default '.env'.
    """
    load_dotenv(dotenv_path=env_file)  # Load environment variables from the specified .env file
    if env_file:
        return Settings(_env_file=str(env_file))
    return Settings()

def build_cdss(settings: Settings) -> CDSSInterface:
    # Centralized construction for loader/processor/env-bound stuff
    loader = DataLoader(rgs_mode="plus")
    processor = DataProcessor(weights=settings.WEIGHTS, alpha=settings.ALPHA)
    return CDSSInterface(loader=loader, processor=processor)

@cli.command()
def recommend(
    study_id: List[int] = typer.Option(
        ..., "--study-id", "-s",
        help="Repeat this option to provide multiple integers."
    ),
    n: int = typer.Option(
        None, "--n", "-n", help="Number of recommendations per patient."
    ),
    days: int = typer.Option(
        None, "--days", "-d", help="Number of days to cover in the recommendation"
    ),    
    protocols_per_day: int = typer.Option(
        None, "--protocols-per-day", "-p", help="Number of protocols per day."
    ),
    env_file: Path = typer.Option(
        None, "--env-file", "-e", help="Path to a .env file with environment variables."
    ),
):
    """
    Generate treatment recommendations for a given patient.
    """
    
    try:
        settings = get_settings(env_file)
        cdss = build_cdss(settings)
        return cdss.recommend_for_study(
            study_id=study_id,
            n=n or settings.N,
            days=days or settings.DAYS,
            protocols_per_day=protocols_per_day or settings.PROTOCOLS_PER_DAY,
        )
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        typer.echo(f"Error generating recommendations: {e}")    


@cli.command("compute-metrics")
def compute_metrics(
    patient_id: int = typer.Option(
        ..., "--patient-id", "-p", help="Patient ID to compute metrics for."
    ),
    env_file: Path = typer.Option(
        None, "--env-file", "-e", help="Path to a .env file with environment variables."
    ),
):
    """
    Computes Patient-Protocol Fit (PPF) based on loaded data.
    Returns the computed PPF with contributions.
    """
    try:
        settings = get_settings(env_file)
        cdss = build_cdss(settings)
        result = cdss.compute_patient_fit([patient_id])
        typer.echo(result)
    except Exception as e:
        logger.error(f"Error computing metrics: {e}")
        typer.echo(f"Error computing metrics: {e}")


@cli.command("compute-protocol-metrics")
def compute_protocol_metrics(
    env_file: Path = typer.Option(
        None, "--env-file", "-e", help="Path to a .env file with environment variables."
    ),
):
    """
    Computes Protocol Similarity Metrics based on loaded data.
    Returns the computed metrics.
    """
    try:
        settings = get_settings(env_file)
        cdss = build_cdss(settings)
        result = cdss.compute_protocol_metrics()
        typer.echo(result)
    except Exception as e:
        logger.error(f"Error computing protocol metrics: {e}")
        typer.echo(f"Error computing protocol metrics: {e}")


