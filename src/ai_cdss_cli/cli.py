# ai_cdss_cli/cli.py
import os
import logging
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv
import typer
import json
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
    study_id: Optional[List[int]] = typer.Option(
        None, "--study-id", "-s",
        help="Study cohort ID(s). Repeat to provide multiple integers."
    ),
    patient_id: Optional[List[int]] = typer.Option(
        None, "--patient-id", "-p",
        help="Explicit patient ID(s). Repeat to provide multiple integers."
    ),
    n: Optional[int] = typer.Option(
        None, "--n", "-n", help="Number of recommendations per patient."
    ),
    days: Optional[int] = typer.Option(
        None, "--days", "-d", help="Number of days to cover in the recommendation."
    ),
    protocols_per_day: Optional[int] = typer.Option(
        None, "--protocols-per-day", "-P",
        help="Number of protocols per day."
    ),
    env_file: Optional[Path] = typer.Option(
        None, "--env-file", "-e", help="Path to a .env file with environment variables."
    ),
):
    """
    Generate treatment recommendations for a study OR explicit patient list.
    Use --study-id for a cohort run, or --patient-id for targeted patients.
    """
    try:
        settings = get_settings(env_file)
        cdss = build_cdss(settings)

        # Validate exclusivity
        has_study = bool(study_id)
        has_patients = bool(patient_id)
        if has_study and has_patients:
            raise typer.BadParameter("Use either --study-id or --patient-id, not both.")
        if not has_study and not has_patients:
            raise typer.BadParameter("You must provide either --study-id or --patient-id.")

        # Resolve defaults from settings
        n_val = n or settings.N
        days_val = days or settings.DAYS
        ppd_val = protocols_per_day or settings.PROTOCOLS_PER_DAY

        if has_study:
            result = cdss.recommend_for_study(
                study_id=study_id,
                n=n_val,
                days=days_val,
                protocols_per_day=ppd_val,
            )
        else:
            # Supports one or many patients (e.g., [123] or [123, 456])
            result = cdss.recommend_for_patients(
                patient_ids=patient_id,
                n=n_val,
                days=days_val,
                protocols_per_day=ppd_val,
            )
        
        logger.info("Recommendation result: %s",
                    json.dumps(result, indent=2, default=str))
        typer.echo(json.dumps(result, indent=2, default=str))

    except typer.BadParameter as e:
        # Input/usage error -> friendly message
        logger.error(f"Argument error: {e}")
        typer.echo(f"Argument error: {e}")
        raise typer.Exit(code=2)

    except Exception as e:
        logger.exception("Error generating recommendations")
        typer.echo(f"Error generating recommendations: {e}")
        raise typer.Exit(code=1)

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
        result = cdss.compute_protocol_similarity()
        typer.echo(result)
    except Exception as e:
        logger.error(f"Error computing protocol metrics: {e}")
        typer.echo(f"Error computing protocol metrics: {e}")


