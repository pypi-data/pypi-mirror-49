import os
import setuptools

_README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

_REQUIREMENTS = [
    line.strip() for line in open(os.path.join(os.path.dirname(__file__),'requirements.upvest.txt')).readlines()
]

_CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.7',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

_KEYWORDS = [
    'api', 
    'upvest', 
    'bitcoin', 
    'ethereum', 
    'oauth2', 
    'client',
]

_PACKAGES = setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

setuptools.setup(
    name="upvest",
    version="0.0.5",
    author="Upvest GmbH",
    author_email="tech@upvest.co",
    maintainer="Alexander Reichhardt",
    maintainer_email="alexander@upvest.co",
    description="Upvest API client library",
    keywords=_KEYWORDS,
    license='MIT',
    long_description=_README,
    long_description_content_type="text/markdown",
    url="https://github.com/toknapp/python-sdk-upvest/",
    packages=_PACKAGES,
    include_package_data=True,
    classifiers=_CLASSIFIERS,
    install_requires=_REQUIREMENTS,
)
