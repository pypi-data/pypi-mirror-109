from pathlib import Path
import shutil
import re
import click
import difflib

#
# Create and manage simple backups, where files are numbered.
# Much like https://en.wikipedia.org/wiki/Versioning_file_system#Files-11_(RSX-11_and_OpenVMS)
#

_archive_dir: Path = None


def createBackupFolderName(path: Path):
    # for old,new in [(r'\\','_')]
    path = path.as_posix()
    path = path.replace("/", "_")
    path = path.replace(":", "_")
    return path


def backup(source_path: Path):
    _archive_dir.mkdir(parents=True, exist_ok=True)

    # Backups are numbered, e.g. foo.bar becomes foo.1.bar, subsequent backup creates foo.2.bar, etc
    # For each file to be archived, look for all the backups
    # Get the latest one if it exists, and check if it has changed before creating a new version.
    for source_file in source_path.iterdir():
        backups = sorted(_archive_dir.glob(f"{source_file.stem}*{source_file.suffix}"))
        if len(backups) == 0:
            version = 1
        else:
            latest_backup = backups[-1]
            with open(source_file) as current, open(latest_backup) as latest:
                if current.readlines() == latest.readlines():
                    click.echo(f"{source_file.name}: no change")
                    continue

                # Latest version differs, so get the number
                regex = rf"{source_file.stem}.(\d+){source_file.suffix}"
                version = int(re.match(regex, latest_backup.name).group(1)) + 1

        suffix = f".{version}{source_file.suffix}"
        backup_name = source_file.with_suffix(suffix).name
        backupFile = _archive_dir / backup_name
        shutil.copyfile(source_file, backupFile)
        click.echo(f"{source_file.name}: saved")


def list(source_path: Path):
    for source_file in source_path.iterdir():
        click.echo(f"{source_file.name}:")

        backups = sorted(_archive_dir.glob(f"{source_file.stem}*{source_file.suffix}"))
        if len(backups) == 0:
            click.echo("    No backups")
        else:
            for backup_file in backups:
                click.echo(f"    {backup_file.name}")


# TODO?
def restore():
    pass


# TODO?
def compare():
    pass
