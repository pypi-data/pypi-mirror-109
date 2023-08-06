import os
import io
import re
from setuptools import setup, find_packages

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
    io.open('ad_logger/__version__.py'
            '', encoding='utf_8_sig').read()
).group(1)
path = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    with open(os.path.join(path, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name="ad_logger",
    version=__version__,
    keywords=["logging", "wrap"],
    # project_urls={
    #     "Documentation": "/",
    #     "Code": "/",
    #     "Issue tracker": "/",
    # },
    description="Python Logging library wrapper",
    long_description=read_file("README.md"),
    long_description_content_type='text/markdown',
    python_requires=">=3.6.0",
    license="Group 42 Licence",
    author="Daqian",
    url="http://power_dev.adalytyx.ai/",
    author_email="daqian.zhang@g42.ai",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=read_requirements('requirements.txt'),
    platforms="any",
    scripts=[],
    zip_safe=False
)
