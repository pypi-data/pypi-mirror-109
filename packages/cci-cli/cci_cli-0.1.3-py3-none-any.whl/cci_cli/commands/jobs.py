from requests.exceptions import HTTPError
import typer

from cci_cli.circle.api import CircleCI
from cci_cli.common import utils

jobs_app = typer.Typer()


@jobs_app.command()
def cancel(project_name: str, job_number: int):
    cci = CircleCI()
    try:
        cci.cancel_job(project_name, job_number)
    except HTTPError as e:
        utils.exit_cli(
            message=e,
            status_code=1,
        )
