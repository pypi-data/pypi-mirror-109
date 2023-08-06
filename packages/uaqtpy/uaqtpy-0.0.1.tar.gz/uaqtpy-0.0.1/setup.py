from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='uaqtpy',
  version='0.0.1',
  description='a test',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Boe Reh',
  author_email='justboereh@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='cutiepy, cute, cutie, cutiepie', 
  packages=find_packages(),
  install_requires=[''] 
)