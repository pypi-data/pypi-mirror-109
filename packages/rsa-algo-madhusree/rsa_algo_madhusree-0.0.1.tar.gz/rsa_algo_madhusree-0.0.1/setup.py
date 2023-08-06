from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
name="rsa_algo_madhusree",
version="0.0.1",
description="Encryption and Decryption of plain text using RSA Algorithm",
long_description=open('readme.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
url='',
author="Madhusree Rana",
author_email='madhusree.rana2017@gmail.com',
license='MIT',
classifiers=classifiers,
keywords='RSA',
packages=find_packages(),
install_requires=['']
)