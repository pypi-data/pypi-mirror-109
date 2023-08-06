import setuptools

import codecs
with codecs.open('README.md', 'r', 'utf-8') as f:
    long_description = f.read()

version = None
with open('src/tidal_stability/__version__.py', 'r') as f:
    exec(f.read())

setuptools.setup(
    name="tidal-stability",
    version=version,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        "arrow>=0.17.0",
        "attrs>=20.3.0",
        "h5py>=2.10.0",
        "matplotlib>=3.3.2",
        "mpmath>=1.1.0",
        "numpy>=1.19.2",
        "scipy>=1.5.2",
        # todo: sundials -> allows scikits.
    ],
    # python_requires='==3.8',
    author="Blake Staples",
    author_email="yourlocalblake@gmail.com",
    description="Solver for gas clouds around Black Holes",
    #long_description=long_description,
    license="GPLv3",
    url="https://github.com/YourLocalBlake/TidalStability",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Astronomy',
    ],
    include_package_data=True,
)