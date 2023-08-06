from pathlib import Path
import click
from . import archive


@click.group()
# @click.option('--debug/--no-debug', default=False)
@click.option(
    "--archive",
    "-a",
    "directory",
    envvar="SNIT_DIR",
    metavar="PATH",
    required=True,
    help="Specify the directory for the archive.  Can be set with the SNIT_DIR environment variable.",
)
def cli(directory):
    """A utility to backup IDE/editor settings.


    Currently only supports VSCode.
    """
    snit_dir = Path(directory)
    if snit_dir.exists():
        click.echo(f"SNIT directory is set to {directory}")
    else:
        click.echo(f"SNIT directory {directory} not found", err=True)
        raise click.Abort()

    archive._archive_dir = (
        snit_dir / archive.createBackupFolderName(Path.cwd()) / Path("vscode")
    )


@cli.command(help="Backup editor settings.")  # @cli, not @click!
def backup():
    click.echo("backup")
    archive.backup(Path.cwd() / Path(".vscode"))


@cli.command(help="List any found backups.")  # @cli, not @click!
def list():
    click.echo("list")
    archive.list(Path.cwd() / Path(".vscode"))
