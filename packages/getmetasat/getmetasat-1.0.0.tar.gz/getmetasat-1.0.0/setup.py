import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='getmetasat',
    version='1.0.0',
    author='electroefos.mx',
    author_email='ed@electroefos.mx',
    description='Python WSDL SAT - [METADATA]',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://electroefos.mx',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    install_requires = [
        'lxml>=4.2.5',
        'requests>=2.21.0',
        'pycryptodome>=3.7.2',
        'pyOpenSSL>=18.0.0'
    ]
)
