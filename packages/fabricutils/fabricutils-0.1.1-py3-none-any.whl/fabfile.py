"""
This filie contains package development automation commands.

Typical workflow is:

    - `fab init`
    - edit code of the package
    - `fab build`, verify results
    - `fab bump {major|minor|patch}`
    - `fab build upload` to upload to PyPi
"""

from fabric import task
import sys

from fabricutils import is_windows

PTY = not is_windows()


@task
def init(c):
    """Initialize development environment."""
    c.run(f'{sys.executable} -m pip install -r requirements.txt')


@task
def build(c):
    """Build next version."""
    c.run(f'{sys.executable} setup.py sdist bdist_wheel')
    c.run(f'{sys.executable} -m twine check dist/*')


@task
def bump(c, part):
    """Bump package version."""
    c.run(f'bumpversion {part}', replace_env=False)


@task
def upload(c):
    """Upload package to PyPi."""
    c.run(f'{sys.executable} -m twine upload dist/* --verbose', pty=PTY)
