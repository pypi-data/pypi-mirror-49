"""
This filie contains package development automation commands.

Typical workflow is:

    - `fab init`
    - edit code of the package
    - `fab build`, verify results
    - `fab bump {major|minor|patch}`
    - `fab upload`, go to [TestPyPi](https://test.pypi.org/), check
    - `fab upload pypi` to upload to PyPi
"""

from fabric import task
import sys


@task
def init(c):
    """Initialize development environment."""
    c.run(f'{sys.executable} -m pip install -r requirements.txt')


@task
def build(c):
    """Build next version."""
    c.run(f'{sys.executable} setup.py sdist bdist_wheel')
    c.run(f'twine check dist/*', replace_env=False)


@task
def bump(c, part):
    """Bump package version."""
    c.run(f'bumpversion {part}')


@task
def upload(c, stage='testpypi'):
    """Upload package to (Test)PyPi."""
    if stage == 'testpypi':
        c.run('twine upload --repository-url https://test.pypi.org/legacy/ dist/*')
    elif stage == 'pypi':
        c.run('twine upload dist/*')
    else:
        raise ValueError(f'Unsopported stage: {stage}')
