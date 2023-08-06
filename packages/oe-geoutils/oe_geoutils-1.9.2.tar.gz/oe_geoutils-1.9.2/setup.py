# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages
from codecs import open

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()

requires = [
    'geoalchemy2 >= 0.6.3',
    # see https://github.com/OnroerendErfgoed/oe_geoutils/issues/93
    'geojson >= 2.5.0',
    'Shapely >= 1.6.4.post2',
    'colander >= 1.7.0',
    'pyramid >= 1.10.4',
    'requests >= 2.22.0',
    'crabpy >= 0.12.0',
    'crabpy_pyramid >= 0.8.1',
    'pyproj >= 2.2.2',
    'oe_utils >= 1.15.0',
    'iso8601 >= 0.1.12',
    'pycountry == 18.12.8; python_version < "3.0.0"',
    'pycountry >= 18.12.8; python_version > "3.0.0"',
]
extras_require = {
    'dev': [
        'pyramid-debugtoolbar>=4.5.1',
        'zope.sqlalchemy>=1.2',
        'transaction>=3.0.0',
        'pytest>=4.6.7,<5.0.0',
        'py>=1.8.0',
        'pytest-cov>=2.8.1',
        'webtest>=2.0.33',
        'mock>=3.0.5',
        'responses>=0.10.8',
        'Sphinx>=1.8.5',
        'sphinxcontrib-httpdomain>=1.7.0',
        'sphinxcontrib-plantuml>=0.17.1',
        'flake8>=3.7.9',
        'waitress>=1.3.1',
        'psycopg2>=2.8.4',
    ],
}

setup(
    name='oe_geoutils',
    version='1.9.2',
    description='Utility Library',
    long_description=README + '\n\n' + CHANGES,
    url='https://github.com/OnroerendErfgoed/oe_geoutils',
    author='Flanders Heritage Agency',
    author_email='ict@onroerenderfgoed.be',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        "Framework :: Pyramid",
    ],
    keywords='geoloc',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    extras_require=extras_require,
    install_requires=requires,
    entry_points="""\
      [paste.app_factory]
      main = oe_geoutils:main
      """,
)
