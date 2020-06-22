from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules = cythonize("test_cython3.pyx")
)