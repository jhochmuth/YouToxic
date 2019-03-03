from distutils.core import setup
from setuptools import find_packages


setup(
    name='toxicity-analysis',
    version='0.1',
    author='Julius Hochmuth',
    description='Analysis for toxicity in text',
    url='https://github.com/jhochmuth/toxicity-analysis',
    packages=find_packages(),
    license='Apache 2.0',
    long_description=open('README.md').read(),
    entry_points="""
        [console_scripts]
        toxicity_analysis=toxicity_analysis.app.__main__:main
    """,
    install_requires=[
        "Flask"
    ]
)
