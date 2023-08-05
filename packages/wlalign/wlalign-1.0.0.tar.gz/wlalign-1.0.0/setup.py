from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

# Read the version from the main package.
with open('wlalign/__init__.py') as f:
    for line in f:
        if '__version__' in line:
            _, version, _ = line.split("'")
            break

setup(
    author='Matteo Frigo, Emilio Cruciani, David Coudert, Rachid Deriche, '
           'Emanuele Natale, Samuel Deslauriers-Gauthier',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
    description='A Python package that implements the WL-align algorithm that '
                'solves the graph alignment problem',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['numpy', 'scipy'],
    name='wlalign',
    packages=['wlalign'],
    python_requires='>=3',
    scripts=['script/wlalign'],
    url='https://gitlab.inria.fr/brain-graph/wl-align',
    version=version,
    project_urls={
        'Source': 'https://gitlab.inria.fr/brain-graph/wl-align',
        'Bug Reports': 'https://gitlab.inria.fr/brain-graph/wl-align/issues',
        'Documentation': 'https://gitlab.inria.fr/brain-graph/wl-align',
    },
)
