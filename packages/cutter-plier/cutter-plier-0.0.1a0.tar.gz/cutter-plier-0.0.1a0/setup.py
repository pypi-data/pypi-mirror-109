import io
import re

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("src/cutter_plier/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="cutter-plier",
    version=version,
    description="Bournix team utils for django",
    long_description=readme,
    author="Mahdi Zarrintareh",
    author_email="mza2rintareh@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[],
    extras_require={},
    entry_points={},
)