from setuptools import setup, find_packages

setup(
    name="cappa",
    version="0.14.1",
    description="Package installer for Captricity. Supports apt-get, pip, bower, and npm.",
    author="Yoriyasu Yano",
    author_email="yorinasub17@gmail.com",

    packages=find_packages(),
    scripts=["scripts/cappa"],
    install_requires=open("requirements.txt").read().split(),
    tests_requires=open("test_requirements.txt").read().split(),
    test_suite='tests'
)
