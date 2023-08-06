"""A setuptools based setup module."""

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
        name='pltRDF',
        version='0.0.3',
        description='A sample Python project',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/sumitavakundu007/pltRDF',
        author='Sumitava Kundu',
        author_email='kundusumitava@gmail.com',
        classifiers=[
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            ],
        keywords='sample, setuptools, development', 
        packages=['pltRDF'],
        python_requires='>=3.6',
        install_requires=['gsd', 'freud-analysis', 'scikit-build', 'matplotlib'],
        
        entry_points={
                'console_scripts': [
                'pltRDF=pltRDF.plot_rdf:rdf',
            ],
        },
        
        project_urls={  # Optional
            'Bug Reports': 'https://github.com/sumitavakundu007/pltRDF/issues',
            'Say Thanks!': 'http://saythanks.io/to/example',
            'Source': 'https://github.com/sumitavakundu007/pltRDF/',
            },
        )
