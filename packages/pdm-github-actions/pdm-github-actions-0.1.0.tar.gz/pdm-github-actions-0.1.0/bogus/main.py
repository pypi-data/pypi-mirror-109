"""a demo CLI application

"""

import typer

cli = typer.Typer()


@cli.callback()
def bogus_callback(ctx: typer.Context) -> None:
    """bogus: a demo python application

    The goal is to have a python command-line interface that
    can be built, tested and deployed automatically by GitHub
    Actions.
    """


@cli.command(name="fetch")
def fetch_subcommand(url: str, path: Path, ) -> None:
    """fetch data from a URL save it to a path.
    
    """

@cli.command(name="mangle")
def mangle_subcommand(path: Path) -> None:
    """Mangle data found in `path`. 

    """
