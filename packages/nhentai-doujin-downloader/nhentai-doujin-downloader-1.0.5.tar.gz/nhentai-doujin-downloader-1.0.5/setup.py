from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='nhentai-doujin-downloader',
  version='1.0.5',
  description='A program that downloads Doujins from nHentai as JPEG files',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Kazuto Kirito Kirigaya',
  author_email='kirito_kazuto_kirigaya@protonmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='downloader', 
  packages=find_packages(),
  install_requires=['requests'] 
)