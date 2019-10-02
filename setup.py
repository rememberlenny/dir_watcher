import setuptools

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

pipfile = Project(chdir=False).parsed_pipfile

packages = pipfile["packages"].copy()
requirements = convert_deps_to_pip(packages, r=False)

def readme():
    with open("README.md") as f:
        return f.read()

setuptools.setup(
    name="publicart_watcher",
    version="0.0.4",  # PEP-440
    description="Library to help index street art",
    long_description=readme(),
    url="https://publicart.io",
    author="Public Art LLC",
    author_email="lenny@publicart.io",
    license="Apache 2",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    # Requirements
    install_requires=requirements,
    python_requires='>=3.5',
    zip_safe=False,  # install source files not egg
    include_package_data=True,  # copy html and friends
    entry_points={
        'console_scripts': ['publicart-watcher=publicart_watcher.command_line:main'],
    },
)
