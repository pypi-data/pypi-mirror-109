from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='M-Funcs',
  version='0.0.1',
  description='Library of basic functions.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Muhammad Muzammil Alam',
  author_email='muzammil.alam231@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='BaFunc', 
  packages=find_packages(),
  install_requires=[''] 
)