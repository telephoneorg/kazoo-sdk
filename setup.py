import re
from setuptools import setup, find_packages


with open('kazoo/__init__.py', 'rt') as fd:
    version = re.search(r'^VERSION\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open('README.rst') as fd:
    long_description = fd.read()

setup(
    name="kazoo-sdk",
    version=version,
    description="Wrapper for the Kazoo API",
    long_description=long_description,
    author="Alex Good, Updated by Brock Haywood, Refreshed by Joe Black",
    author_email='me@joeblack.nyc',
    url='https://github.com/telephoneorg/kazoo-sdk',
    download_url=(
        'https://github.com/telephoneorg/kazoo-sdk/tarball/v%s' % version),
    packages=find_packages(),
    install_requires=["requests>=2.2.1", "six"],
    test_requires=["mock", "tox"],
    license="MIT License",
    readme='README.rst',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Telephony',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ]
)
