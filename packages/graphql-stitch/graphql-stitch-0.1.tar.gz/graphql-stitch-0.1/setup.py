from distutils.core import setup

setup(
  name = 'graphql-stitch',         
  packages = ['graphql-stitch'],   
  version = '0.1',      
  license='MIT',        
  description = 'Edits a GraphQL schema to resolve false errors when passed into a schema linter.',   
  author = 'silidos',                   
  author_email = 'psnsilidos@gmail.com',      
  url = 'https://github.com/Silidos/stitch',   
  download_url = 'https://github.com/Silidos/stitch/archive/refs/tags/v_01.tar.gz',
  keywords = ['GraphQL'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
  ],
)