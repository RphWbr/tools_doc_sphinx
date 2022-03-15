from setuptools import setup
from tools_doc_sphinx import __version__ as version


description = "Tools for automatic generation of files used in Sphinx documentation"

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='tools_doc_sphinx',
    version=version,    
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RphWbr/tools_doc_sphinx',
    author='Raphael Weber',
    author_email='raphael.weber@univ-rennes1.fr',
    license='CeCILL',
    packages=[
        'tools_doc_sphinx',
    ],
    include_package_data=True,
    install_requires=[],
    python_requires='>=3.6, <4',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developpers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)'
    ],
)
