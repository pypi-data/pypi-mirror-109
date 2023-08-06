from setuptools import setup

name = "types-PyYAML"
description = "Typing stubs for PyYAML"
long_description = '''
## Typing stubs for PyYAML

This is an auto-generated PEP 561 type stub package for `PyYAML` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `PyYAML`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/PyYAML. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `64f463172b27d7321461890dd3edf416a103ace7`.
'''.lstrip()

setup(name=name,
      version="5.4.3",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['yaml-stubs'],
      package_data={'yaml-stubs': ['error.pyi', 'scanner.pyi', 'serializer.pyi', 'nodes.pyi', 'tokens.pyi', 'emitter.pyi', 'resolver.pyi', 'dumper.pyi', 'constructor.pyi', 'loader.pyi', 'representer.pyi', 'events.pyi', 'parser.pyi', 'composer.pyi', '__init__.pyi', 'cyaml.pyi', 'reader.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
