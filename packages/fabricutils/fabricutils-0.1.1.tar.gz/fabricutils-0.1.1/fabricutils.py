__all__ = [
    'conda_python_executable',
    'docker_mount_path_resolver',
    'docker_mount_path_desktop',
    'docker_mount_path_toolbox',
    'python_executable',
    'is_docker_toolbox',
    'is_windows',
    ]

import fabric
import io
import json
import os
import pathlib
import typing


def conda_python_executable(conn: fabric.Connection, conda_env_name: str) -> pathlib.Path:
    """Get path to python executable for specific anaconda environment."""
    stream = io.StringIO()
    conn.run('conda info --envs --json', replace_env=False, out_stream=stream)
    info = json.loads(stream.getvalue())
    envdir = next(iter(p for p in (pathlib.Path(s) for s in info['envs']) if p.name == conda_env_name))
    return python_executable(envdir)


def docker_mount_path_resolver(conn: fabric.Connection) -> typing.Callable[[pathlib.Path], str]:
    """Get docker mount path resolver function, one of `docker_mount_path_desktop` or `docker_mount_path_toolbox`."""
    return docker_mount_path_toolbox if is_docker_toolbox(conn) else docker_mount_path_desktop


def docker_mount_path_desktop(path: pathlib.Path) -> str:
    """Get the bind mount path for Docker Desktop."""
    return str(path.resolve())


def docker_mount_path_toolbox(path: pathlib.Path) -> str:
    """Get the bind mount path for Docker Toolbox."""
    p = path.resolve()
    mountpath = f'/{p.drive.lower().replace(":", "")}/{pathlib.Path(*p.parts[1:]).as_posix()}'
    if not mountpath.startswith('/c/Users/'):
        raise ValueError('Only files under C:/Users/ can be shared automatically with Docker Toolbox.')
    return mountpath


def python_executable(venvdir: pathlib.Path) -> typing.Optional[pathlib.Path]:
    """Get python executable path by venv directory path."""
    python = (venvdir / 'python.exe') if is_windows() else (venvdir / 'bin' / 'python')
    return python if python.exists() else None


def is_docker_toolbox(conn: fabric.Connection) -> bool:
    """Check if docker uses docker toolbox."""
    stream = io.StringIO()
    conn.run('docker system info', replace_env=False, out_stream=stream)
    info = stream.getvalue()
    return info.find('Operating System: Boot2Docker') >= 0


def is_windows() -> bool:
    """Check if local OS is Windows."""
    return os.name == 'nt'
