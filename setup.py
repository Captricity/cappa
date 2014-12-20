from setuptools import setup
setup(
    name = "cappa",
    version = "0.1",
    description = "Package installer for Captricity. Supports pip, bower, and npm.",
    author = "Yoriyasu Yano",
    author_email = "yorinasub17@gmail.com",

    py_modules = ['cappa'], 
    scripts = ['scripts/cappa'],
    install_requires = open('requirements.txt').read().split()
)
