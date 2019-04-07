from distutils.core import setup
from setuptools import find_packages


setup(
    name='youtoxic',
    version='0.1',
    author='Julius Hochmuth',
    description='A Python Dash Server that predicts the toxicity of text using Deep Learning.',
    url='https://github.com/jhochmuth/YouToxic',
    package_data={
        'youtoxic': 'youtoxic/app/models/*',
        'youtoxic': 'youtoxic/app/utils/*.pickle',
        'youtoxic': 'youtoxic/app/assets/*',
        'youtoxic': 'youtoxic/app/templates/*'
    },
    include_package_data=True,
    data_files=[('youtoxic/app/templates', ['index.html']),
                ('youtoxic/app/assets', ['image.png', 'image-2.png', 'stylesheet.css'])],
    packages=find_packages(exclude=["tests"]),
    license='Apache 2.0',
    long_description=open('README.md').read(),
    entry_points="""
        [console_scripts]
        youtoxic=youtoxic.app.__main__:main
    """,
    install_requires=[
        "Dash"
    ]
)
