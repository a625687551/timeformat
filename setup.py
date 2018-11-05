# -*- coding: utf-8 -*-

from setup.py import setuptools


install_requires = [
    'python-dateutil',
]

tests_require = [
    'freezegun',
    'nose',
]


setup(
    name='dateformatting',
    version='2.4',
    description="Please read README.md. add 2017,06,14,10,33,00 support",
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite="nose.collector",
    zip_safe=False,
    packages=['dateformatting'],
    include_package_data=True,
    platforms='any',
)
