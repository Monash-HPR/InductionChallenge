__author__ = 'Hamish Self'

from distutils.core import setup
from Cython.Build import cythonize

setup(
  name='1DoF_Simulation',
  ext_modules = cythonize( "backend/*.pyx",
                           build_dir="build",
                           nthreads=4,
                           compiler_directives={'boundscheck': False,
                                                'cdivision': True,
                                                'profile': True,   # Set to true when profiling for better info.
                                                'infer_types': True})
)
