from distutils.core import setup
from setuptools import find_packages


setup(
    name='YouToxic',
    version='0.1',
    author='Julius Hochmuth',
    description='A Python Flask Web Server that predicts the toxicity of text using Deep Learning.',
    url='https://github.com/jhochmuth/YouToxic',
    packages=find_packages(),
    license='Apache 2.0',
    long_description=open('README.md').read(),
    entry_points="""
        [console_scripts]
        youtoxic=youtoxic.app.__main__:main
    """,
    install_requires=[
        "Flask"
    ]
)
