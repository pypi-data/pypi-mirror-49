import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = 'toh5py',
    version = '0.0.1',
    author = 'bouseng',
    author_email = 'c@bouseng.com',
    description = 'Saving and loading a large number of images (data) into a single HDF5 file',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/rokuki',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]

)
