from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'AutoReg',         
  packages = ['AutoReg'],  
  version = '1.1',      
  license='MIT',        
  description = 'A lightweight library to get regex of a string.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'SusmitPanda',                   
  author_email = 'susmit.vssut@gmail.com',     
  url = 'https://github.com/SusmitPanda/AutoReg',   
  keywords = ['regex', 'python regex','autoregex','regex create','string matching'],   
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],)