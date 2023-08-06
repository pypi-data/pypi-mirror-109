
from setuptools import setup, find_packages
 
classifiers = []

setup(
  name='miraculous',
  version='1.8.8',
  description='A discord.py bot ready to use!',
  long_description=open('README.md').read() + "",
  long_description_content_type='text/markdown',
  url='https://github.com/I-make-python-module-and-bots-stuff/D.py-M',  
  author='Rukchad Wongprayoon',
  author_email='mooping3roblox@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Tools', 
  packages=find_packages(),
  install_requires=["discord","discord-ext-alternatives","async-timeout","youtube_dl","flask","pynacl"]
)
