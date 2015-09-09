from setuptools import setup

with open('requirements.txt') as f:
    requires = f.read().strip().splitlines()

setup(
    name='KibotoBotSDK',
    version='0.01',
    packages=[
        'KibotoBotSDK',
    ],
    install_requires=requires
)
