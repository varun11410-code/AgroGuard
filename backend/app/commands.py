"""
AgroGuard Backend - Custom CLI Commands

Defines custom Flask CLI commands registered on the application instance.
Provides the database seeding command as a wrapper.
"""

from __future__ import annotations

import click
from flask import Flask


def register_commands(app: Flask) -> None:
    """
    Registers custom Flask CLI commands on the application.

    Args:
        app: The Flask application instance.
    """

    @app.cli.command("seed-crops")
    @click.option(
        "--verbose",
        is_flag=True,
        default=True,
        help="Log skipped entries that are already up-to-date. Defaults to True.",
    )
    def seed_crops(verbose: bool) -> None:
        """
        Idempotently seeds supported crops (Tomato and Potato) into the database.
        
        This is a wrapper around the scripts/seed.py logic.
        """
        env = app.config.get("ENV", "development")
        click.echo(f"[{env.upper()}] Seeding supported crops via Flask CLI command...")

        # Import seeding logic dynamically inside function context to prevent circular/early imports
        from scripts.seed import run_seed
        run_seed(verbose=verbose)
