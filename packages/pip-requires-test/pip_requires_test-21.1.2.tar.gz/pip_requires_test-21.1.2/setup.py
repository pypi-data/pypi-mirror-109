import pkg_resources
from setuptools import setup


version = "21.1.2"

pkg_resources.require([f"pip >= {version}"])

setup(
    name="pip_requires_test",
    version=f"{version}",
    # install_requires=f"pip>={version}",
)
