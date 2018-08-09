from distutils.core import setup
from Cython.Build import cythonize

setup(
  name='MHPR_Induction_Challenge',
  ext_modules = cythonize( "sim_backend_cython.pyx", 
                           build_dir="build")
)
