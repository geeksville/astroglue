import logging
import typer
from typing_extensions import Annotated

import starbash.url as url
import starbash

from .app import Starbash, get_user_config_path, setup_logging
from .commands import info, process, repo, select, user
from . import console

app = typer.Typer(
    rich_markup_mode="rich",
    help=f"Starbash - Astrophotography workflows simplified.\n\nFor full instructions and support [link={url.project}]click here[/link].",
)
app.add_typer(user.app, name="user", help="Manage user settings.")
app.add_typer(repo.app, name="repo", help="Manage Starbash repositories.")
app.add_typer(select.app, name="select", help="Manage session and target selection.")
app.add_typer(info.app, name="info", help="Display system and data information.")
app.add_typer(
    process.app, name="process", help="Process images using automated workflows."
)


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            help="Enable debug logging output.",
        ),
    ] = False,
):
    """Main callback for the Starbash application."""
    # Set the log level based on --debug flag
    if debug:
        starbash.log_filter_level = logging.DEBUG

    if ctx.invoked_subcommand is None:
        if not get_user_config_path().exists():
            with Starbash("app.first") as sb:
                user.do_reinit(sb)
        else:
            # No command provided, show help
            console.print(ctx.get_help())
        raise typer.Exit()


if __name__ == "__main__":
    app()
