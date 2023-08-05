import pkg_resources
from setuptools import setup


version = "0"

pkg_resources.require([f"pip >= {version}"])

setup(
    name="pip_requires_test",
    version=f"{version}",
    # install_requires=f"pip>={version}",
)
