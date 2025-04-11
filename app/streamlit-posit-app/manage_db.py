import os
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command
from streamlit_posit_app.database.model import Base
from sqlalchemy import create_engine
import click


def get_alembic_config():
    return Config("alembic.ini")


@click.group()
def cli():
    """Database management commands for the Streamlit Posit App."""
    pass


@cli.command()
def init():
    """Initialize the database and Alembic."""
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    # Create database engine and tables
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)

    # Initialize Alembic
    alembic_cfg = get_alembic_config()
    command.stamp(alembic_cfg, "head")
    click.echo("Database initialized successfully!")


@cli.command()
@click.argument("message", required=True)
def migrate(message):
    """Create a new migration with a message."""
    alembic_cfg = get_alembic_config()
    command.revision(alembic_cfg, autogenerate=True, message=message)
    click.echo(f"Created new migration with message: {message}")


@cli.command()
def upgrade():
    """Upgrade the database to the latest version."""
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, "head")
    click.echo("Database upgraded successfully!")


if __name__ == "__main__":
    cli()
