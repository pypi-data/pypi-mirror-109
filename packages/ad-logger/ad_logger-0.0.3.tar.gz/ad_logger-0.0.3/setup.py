import os
# python setup.py check
# python setup.py sdist
# twine upload dist/ad_logger-*.tar.gz
from setuptools import setup, find_packages

path = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    with open(os.path.join(path, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


setup(
    name="ad_logger",
    version="0.0.3",
    keywords=["logging", "wrap"],
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
    install_requires=[
        "loguru >= 0.5",
        "kafka-python >= 2.0"
    ],
    platforms="any",
    scripts=[],
    zip_safe=False
)
