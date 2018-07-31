from setuptools import setup

setup(
    name='docker-cli',
    packages=['docker_cli'],
    version='0.0.1',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'docker-cli = docker_cli:main',
        ]
    }
)
