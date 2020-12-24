import setuptools

with open('README', 'r') as rm:
    long_description = rm.read()

setuptools.setup(
    name='nc-tei-utils',
    version='0.0.1',
    author='Nicholas P. S. Cole',
    author_email='nicholas.cole@history.ox.ac.uk',
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    scripts=['bin/tei_current_assignments.py']
)
