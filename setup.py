from setuptools import setup, Extension

module = Extension("absinf", sources=["absinf.c"])

setup(
    name="absinf",
    version="1.0",
    description="AbsInf object that is always greater than any number",
    ext_modules=[module],
)
