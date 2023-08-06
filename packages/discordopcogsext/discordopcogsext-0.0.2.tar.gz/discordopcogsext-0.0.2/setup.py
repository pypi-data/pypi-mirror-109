from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='discordopcogsext',
  version='0.0.2',
  description='A discord.py bot helper',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='palmtrww',
  author_email='palmbestna@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='discord.py', 
  packages=find_packages(),
  install_requires=['discord'] 
)