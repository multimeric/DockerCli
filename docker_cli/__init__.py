#!/usr/bin/env python3
import argparse
import os.path
import tempfile
import subprocess
from pathlib import Path


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Runs a Docker image, automatically converting filepaths to a bind'
                                                 'mount inside the container')
    parser.add_argument('-n', '--no-rm', help="Don't delete the container after it runs (the default)")
    parser.add_argument('-e', '--echo-command', help="Print the generated docker command instead of running",
                        action='store_true')
    # parser.add_argument('image', help="Docker image to run")
    parser.add_argument('arguments', help="Arguments to pass to the docker container", nargs=argparse.REMAINDER)
    return parser


def main():
    args = get_parser().parse_args()

    # Build the docker command up as two lists
    docker_command = ['docker', 'run']
    container_command = []

    if not args.no_rm:
        docker_command += ['--rm']

    # We will use this for generating mount locations
    name_gen = tempfile._RandomNameSequence()

    # Convert paths into bind mounts
    for arg in args.arguments:

        # If it's a file or directory, we need to mount it
        if os.path.isdir(arg) or os.path.isfile(arg):
            arg_path = Path(arg)
            temp_dir = Path(tempfile.gettempdir()) / next(name_gen)
            mount_dest = temp_dir / arg_path.name
            docker_command += ['-v', f'{arg_path}:{mount_dest}']
            container_command.append(mount_dest)
        else:
            container_command.append(arg)

    full_command = [str(arg) for arg in [*docker_command, *container_command]]

    if args.echo_command:
        print(subprocess.list2cmdline(full_command))
    else:
        subprocess.run(full_command)


if __name__ == '__main__':
    main()
