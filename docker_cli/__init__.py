#!/usr/bin/env python3
import argparse
import os.path
import tempfile
import subprocess
from pathlib import Path


def get_parser() -> argparse.ArgumentParser:
    """
    Returns the argument parser for the CLI tool
    """
    parser = argparse.ArgumentParser(description='Runs a Docker image, automatically converting filepaths to a bind'
                                                 'mount inside the container')
    parser.add_argument('-n', '--no-rm', help="Don't delete the container after it runs (the default)", action='store_true')
    parser.add_argument('-p', '--mount-parent', help="Mount the containing folder for each file, rather than mounting "
                                                      "each file individually. This can be helpful when using index "
                                                      "files etc.", action='store_true')
    parser.add_argument('-e', '--echo-command', help="Print the generated docker command instead of running",
                        action='store_true')
    parser.add_argument('arguments', help="Arguments to pass to the docker container", nargs=argparse.REMAINDER)
    return parser


def formulate_command(arguments, no_rm=False, random_tempdir=True, mount_parent=False, cwd=os.getcwd()):
    """
    Generates a docker command, with automatic bind mounting
    """
    # Build the docker command up as two lists
    docker_command = ['docker', 'run']
    container_command = []

    if not no_rm:
        docker_command += ['--rm']

    # We will use this for generating mount locations
    name_gen = tempfile._RandomNameSequence()

    # Convert paths into bind mounts
    for arg in arguments:

        # If it's a file or directory, we need to mount it
        if os.path.isdir(arg) or os.path.isfile(arg):

            arg_path = Path(arg)

            # Make all relative paths absolute
            if not arg_path.is_absolute():
                arg_path = Path(cwd) / arg_path

            # Generate a random temporary directory by default
            if random_tempdir:
                temp_dir = Path(tempfile.gettempdir()) / next(name_gen)
            else:
                temp_dir = Path(tempfile.gettempdir())

            if mount_parent:
                mount_dest = temp_dir / arg_path.parent.name
                docker_command += ['-v', f'{arg_path.parent}:{mount_dest}']
                container_command.append(mount_dest / arg_path.name)
            else:
                mount_dest = temp_dir / arg_path.name
                docker_command += ['-v', f'{arg_path}:{mount_dest}']
                container_command.append(mount_dest)
        else:
            container_command.append(arg)

    # Convert everything back to strings
    return [str(arg) for arg in [*docker_command, *container_command]]


def main():
    """
    Runs the command-line interface
    """
    args = get_parser().parse_args()

    command = formulate_command(
        arguments=args.arguments,
        no_rm=args.no_rm,
        mount_parent=args.mount_parent
    )

    if args.echo_command:
        print(subprocess.list2cmdline(command))
    else:
        subprocess.run(command)


if __name__ == '__main__':
    main()
