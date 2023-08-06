from setuptools import setup, find_packages

setup(
  name='dfir-unfurl',
  packages=find_packages(),
  include_package_data=True,
  scripts=['unfurl_app.py', 'unfurl_cli.py'],
  version='20210615',
  description='Unfurl takes a URL and expands ("unfurls") it into a directed graph',
  url='https://github.com/obsidianforensics/unfurl',
  author='Ryan Benson',
  author_email='ryan@dfir.blog',
  license='Apache',
  keywords=['unfurl', 'forensics', 'dfir', 'reverse-engineering', 'security'],
  classifiers=[],
  install_requires=[
    'blackboxprotobuf==1.0.1',
    'flask',
    'flask_cors',
    'maclookup',
    'networkx',
    'protobuf==3.10.0',
    'publicsuffix2',
    'pycountry',
    'Requests',
    'torf',
    'ulid-py'
  ]
)

