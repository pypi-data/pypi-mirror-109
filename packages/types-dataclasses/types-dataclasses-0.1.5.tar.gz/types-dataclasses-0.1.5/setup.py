from setuptools import setup

name = "types-dataclasses"
description = "Typing stubs for dataclasses"
long_description = '''
## Typing stubs for dataclasses

This is an auto-generated PEP 561 type stub package for `dataclasses` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `dataclasses`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/dataclasses. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `64f463172b27d7321461890dd3edf416a103ace7`.
'''.lstrip()

setup(name=name,
      version="0.1.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['dataclasses-stubs'],
      package_data={'dataclasses-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
