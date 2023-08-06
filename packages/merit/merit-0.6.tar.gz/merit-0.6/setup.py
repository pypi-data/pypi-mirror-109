from os import path
from distutils.core import setup


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
  name = 'merit',
  packages = ['merit'],
  version = '0.6',
  license='MIT',
  description = 'A Python SDK for the Merit API.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Taylor Robinson',
  author_email = 'taylor.howard.robinson@gmail.com',
  url = 'https://github.com/tayrobin/merit',
  download_url = 'https://github.com/tayrobin/merit/archive/refs/tags/0.6.tar.gz',
  keywords = ['Merit', 'API', 'SDK', 'Digital Credentials'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
