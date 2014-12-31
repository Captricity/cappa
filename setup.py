from setuptools import setup
setup(
    name = "cappa",
    version = "0.4",
    description = "Package installer for Captricity. Supports apt-get, pip, bower, and npm.",
    author = "Yoriyasu Yano",
    author_email = "yorinasub17@gmail.com",

    py_modules = ['cappa'], 
    scripts = ['scripts/cappa'],
    install_requires = open('requirements.txt').read().split()
)
