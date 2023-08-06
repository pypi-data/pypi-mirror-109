from setuptools import setup



setup(
   name='pandas_spectroscopy',
   version='0.0.1',
   description='Spectroscopy tools for pandas',
   author='Georg Ramer',
   author_email='georg.ramer@tuwien.ac.at',
   packages=['pandas_spectroscopy'],  #same as name
   install_requires=['pandas', 'numpy'], #external packages as dependencies
   long_description="",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics'
      ],
    keywords="spectroscopy pandas hyperspectral",
    python_requires='>=3.7',
    extras_require={'test': ['pytest', 'pytest-xdist', 'tox']},
)
