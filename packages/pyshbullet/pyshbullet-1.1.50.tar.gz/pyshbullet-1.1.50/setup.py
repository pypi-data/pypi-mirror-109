import setuptools
with open('README.md', 'r') as fh:
  long_description = fh.read()
setuptools.setup(
  name='pyshbullet',
  version='1.1.50',
  author='98129182',
  author_email='the98129182@gmail.com',
  description='Python API wrapper for the pushbullet API',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/98129182/pyshbullet',
  packages=setuptools.find_packages(),
  install_requires=[
    'aiohttp',
    'tzlocal'
  ],
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
  ],
  python_requires='>=3.6',
)