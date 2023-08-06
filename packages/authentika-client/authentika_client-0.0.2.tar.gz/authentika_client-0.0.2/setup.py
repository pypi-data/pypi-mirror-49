
import io

from setuptools import find_packages, setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

from authentika_client import __version__

setup(
  name='authentika_client',
  version=__version__,
  url='',
  license='',
  maintainer='PUC-Rio',
  maintainer_email='thompsonp17@hotmail.com',
  description="Flask-client for Authentika Server.",
  long_description=readme,
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  install_requires=[
    'flask',
    'requests',
    'tldextract'
  ],
  extras_require={
    'test':[
      'pytest',
      'pytest-ordering',
      'docker',
      'coverage',
      'requests',
    ],
    'documentation': [
      'Sphinx',
      'recommonmark',
      'apispec'
    ]
  }
)

