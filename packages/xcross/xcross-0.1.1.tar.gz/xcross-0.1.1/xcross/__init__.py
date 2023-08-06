'''
    xcross
    ======

    A utility for 1-line builds from the parent host.
'''

import argparse
import collections
import os
import pathlib
import re
import subprocess
import sys

version_info = collections.namedtuple('version_info', 'major minor patch build')

__version_major__ = '0'
__version_minor__ = '1'
__version_patch__ = '1'
__version_build__ = ''
__version_info__ = version_info(major='0', minor='1', patch='1', build='')
__version__ = '0.1.1'

# Create our arguments.
parser = argparse.ArgumentParser(description='Cross-compile C/C++ with a single command.')
parser.add_argument(
    '--target',
    help='''The target triple for the cross-compiled architecture.
This may also be supplied via the environment variable `CROSS_TARGET`.
Ex: `--target=alpha-unknown-linux-gnu`.''',
)
parser.add_argument(
    '--dir',
    help='''The directory to share to the docker image.
This may also be supplied via the environment variable `CROSS_DIR`.
This directory may be an absolute path or relative to
the current working directory. Both the input and output arguments
must be relative to this. Defaults to `/`.
Ex: `--dir=..`''',
)
parser.add_argument(
    '-E',
    '--env',
    action='append',
    help='''Pass through an environment variable to the image.
May be provided multiple times, or as a comma-separated list of values.
If an argument is provided without a value, it's passed through using
the value in the current shell.
Ex: `-E=CXX=/usr/bin/c++,CC=/usr/bin/cc,AR`''',
)
parser.add_argument(
    '--cpu',
    help='''Set the CPU model for the compiler/Qemu emulator.
This may also be supplied via the environment variable `CROSS_CPU`.
A single CPU type may be provided. To enumerate valid CPU types
for the cross compiler, you may run `cc -mcpu=x`, where `x` is an
invalid CPU type. To enumerate valid CPU types for the Qemu emulator,
you may run `run -cpu help`.
Ex: `--cpu=e500mc`''',
)
parser.add_argument(
    '--username',
    help='''The username for the Docker Hub image.
This may also be supplied via the environment variable `CROSS_USERNAME`.
Ex: `--username=ahuszagh`''',
)
parser.add_argument(
    '--repository',
    help='''The repository for the Docker Hub image.
This may also be supplied via the environment variable `CROSS_REPOSITORY`.
Ex: `--repository=cross`''',
)
parser.add_argument(
    '--docker',
    help='''The path or name of the Docker binary.
This may also be supplied via the environment variable `CROSS_DOCKER`.
Ex: `--docker=docker`''',
)
parser.add_argument(
    '-V', '--version',
    action='version',
    version=f'%(prog)s {__version__}'
)
args, unknown = parser.parse_known_args()

def error(message, code=126):
    '''Print message, help, and exit on error.'''

    sys.stderr.write(f'error: {message}.\n')
    parser.print_help()
    sys.exit(code)

def validate_username(username):
    return re.match('^[A-Za-z0-9_-]*$', username)

def validate_repository(repository):
    return re.match('^[A-Za-z0-9_-]+$', repository)

def validate_target(target):
    return re.match('^[A-Za-z0-9_-]+$', target)

def quote(string):
    # We first need to properly escape all backslashes, so each
    # is transformed into 2 backslashes `\\` when passed into
    # the shell. 8 backslashes is turned into 2 for `bash -c`,
    # which is then read as 1. Likewise, 4 quotes for
    # `"` is then read as 1 in `bash -c`, which provides a
    # literal escape. The rest can be provided as a literal escape.
    esc1 = re.sub(r"\\", r"\\\\\\\\", string)
    esc2 = re.sub(r"\"", r"\\\\\"", esc1)
    return re.sub(r"([^\\\"A-Za-z0-9%+.|/:=@_-])", r"\\\1", esc2)

def quote_path(path):
    # We want to quote here, since we don't want **any** globs,
    # or special characters, since this is the most important part.
    # This should **always** be valid.
    if "'" in path:
        error('Invalid quote in path `{path}`, path is not valid')
    return f"'{path}'"

def main():
    '''Entry point'''

    current_dir = pathlib.PurePath(os.getcwd())
    root = current_dir.root

    # Normalize our arguments.
    args.target = args.target or os.environ.get('CROSS_TARGET')
    args.dir = args.dir or root
    args.cpu = args.cpu or os.environ.get('CROSS_DIR')
    args.cpu = args.cpu or os.environ.get('CROSS_CPU')
    if args.username is None:
        args.username = os.environ.get('CROSS_USERNAME')
    if args.username is None:
        args.username = 'ahuszagh'
    args.repository = args.repository or os.environ.get('CROSS_REPOSITORY')
    args.repository = args.repository or 'cross'
    args.docker = args.docker or os.environ.get('CROSS_DOCKER')
    args.docker = args.docker or 'docker'

    # Validate our arguments.
    if not unknown:
        error('Must provide at least an argument for the command')
    if args.target is None or not validate_target(args.target):
        error('Must provide a valid target')
    if args.username is None or not validate_username(args.username):
        error('Must provide a valid Docker Hub username')
    if args.repository is None or not validate_repository(args.repository):
        error('Must provide a valid Docker Hub repository')

    # Need to add a toolchain if we don't have one with CMake.
    if any(i == 'cmake' for i in unknown):
        if not any(i.startswith('-DCMAKE_TOOLCHAIN_FILE') for i in unknown):
            unknown.append('-DCMAKE_TOOLCHAIN_FILE=/toolchains/toolchain.cmake')

    # Normalize our paths here.
    parent_dir = pathlib.PurePath(os.path.realpath(args.dir))
    if not os.path.isdir(parent_dir):
        error('`dir` is not a directory')
    if not current_dir.is_relative_to(parent_dir):
        error('`dir` must be a parent of the current working directory')
    relpath = current_dir.relative_to(parent_dir).as_posix()

    # Normalize our arguments for paths on Windows.
    # We want to be very... lenient here.
    # Backslash characters are **generally** not valid
    # in most cases, except for paths on Windows.
    #
    # Only change the value if:
    #   1. The path exists
    #   2. The path contains backslashes (IE, isn't a simple command).
    #   3. The path is relative to the parent dir shared to Docker.
    if os.name == 'nt':
        for index in range(len(unknown)):
            value = unknown[index]
            if '\\' in value and os.path.exists(value):
                path = pathlib.PurePath(os.path.realpath(value))
                if path.is_relative_to(parent_dir):
                    relative = os.path.relpath(path, start=current_dir)
                    unknown[index] = pathlib.PurePath(relative).as_posix()

    # Process our environment variables.
    # We don't need to escape these, since we aren't
    # using a shell. For example, `VAR1="Some Thing"`
    # and `VAR1=Some Thing` will both be passed correctly.
    args.env = args.env or []
    env = [item for e in args.env for item in e.split(',')]

    # Process our subprocess call.
    # We need to escape every custom argument, so we
    # can ensure the args are properly passed if they
    # have spaces. We use single-quotes for the path,
    # and escape any characters and use double-quotes
    # for the command, to ensure we avoid any malicious
    # escapes. This allows us to have internal `'` characters
    # in our commands, without actually providing a dangerous escape.
    image = f'{args.repository}:{args.target}'
    if args.username:
        image = f'{args.username}/{image}'
    command = ['docker', 'run', '-t']
    for var in env:
        command += ['--env', var]
    command += ['--volume', f'{parent_dir}:/src']
    command.append(image)
    chdir = f'cd /src/{quote_path(relpath)}'
    escaped = f'{" ".join(map(quote, unknown))}'
    if args.cpu:
        escaped = f'export CPU={args.cpu}; {escaped}'
    nonroot = f'su crosstoolng -c "{escaped}"'
    cmd = f'{chdir} && {nonroot}'
    command += ['/bin/bash', '-c', cmd]
    code = subprocess.call(
        command,
        shell=False,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    sys.exit(code)
