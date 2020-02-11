from setuptools import setup

PACKAGE_NAME = 'reddit-aloite_bot'

PACKAGE_REQUIREMENTS = [
    'praw',
]

setup(
    name=PACKAGE_NAME,
    version='0.0.1',
    description='Reddit bot - See homepage for more information',
    url='https://github.com/raspi/reddit-aloite_bot',
    author='raspi',
    author_email='',
    license='Apache 2.0',
    packages=[PACKAGE_NAME],
    install_requires=PACKAGE_REQUIREMENTS,
    zip_safe=False
)