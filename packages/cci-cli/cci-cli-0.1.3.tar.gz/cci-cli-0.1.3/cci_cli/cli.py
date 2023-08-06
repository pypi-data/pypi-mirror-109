import typer

from cci_cli.commands.artifacts import artifacts_app
from cci_cli.commands.config import config_app
from cci_cli.commands.pipelines import pipelines_app
from cci_cli.commands.workflows import workflows_app
from cci_cli.commands.jobs import jobs_app

from cci_cli import __version__

app = typer.Typer()
app.add_typer(artifacts_app, name="artifacts", help="Manage pipeline artifacts")
app.add_typer(pipelines_app, name="pipelines", help="Manage pipelines")
app.add_typer(config_app, name="config", help="Configure the CCI CLI")
app.add_typer(workflows_app, name="workflows", help="Manage workflows")
app.add_typer(jobs_app, name="jobs", help="Manage jobs")


@app.command(help="Display current CLI version")
def version():
    typer.echo(f"CLI Version: {__version__}")
    raise typer.Exit()
