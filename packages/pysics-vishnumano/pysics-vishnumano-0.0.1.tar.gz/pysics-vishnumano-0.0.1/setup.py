from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='pysics-vishnumano',
  version='0.0.1',
  description='An introductory physics library that can execute basic calculations.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Vishnu Mano',
  author_email='vishnu.mano@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='physics', 
  packages=find_packages(),
  install_requires=[''] 
)