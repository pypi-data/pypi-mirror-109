from setuptools import setup

name = "types-bleach"
description = "Typing stubs for bleach"
long_description = '''
## Typing stubs for bleach

This is an auto-generated PEP 561 type stub package for `bleach` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `bleach`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/bleach. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `64f463172b27d7321461890dd3edf416a103ace7`.
'''.lstrip()

setup(name=name,
      version="3.3.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['bleach-stubs'],
      package_data={'bleach-stubs': ['sanitizer.pyi', 'html5lib_shim.pyi', 'utils.pyi', 'linkifier.pyi', 'callbacks.pyi', '__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
