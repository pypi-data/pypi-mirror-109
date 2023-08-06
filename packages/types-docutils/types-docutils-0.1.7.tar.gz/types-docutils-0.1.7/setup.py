from setuptools import setup

name = "types-docutils"
description = "Typing stubs for docutils"
long_description = '''
## Typing stubs for docutils

This is an auto-generated PEP 561 type stub package for `docutils` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `docutils`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/docutils. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `64f463172b27d7321461890dd3edf416a103ace7`.
'''.lstrip()

setup(name=name,
      version="0.1.7",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['docutils-stubs'],
      package_data={'docutils-stubs': ['nodes.pyi', 'statemachine.pyi', 'frontend.pyi', 'core.pyi', 'io.pyi', 'examples.pyi', '__init__.pyi', 'parsers/null.pyi', 'parsers/recommonmark_wrapper.pyi', 'parsers/__init__.pyi', 'parsers/rst/states.pyi', 'parsers/rst/nodes.pyi', 'parsers/rst/roles.pyi', 'parsers/rst/__init__.pyi', 'writers/__init__.pyi', 'transforms/__init__.pyi', 'languages/__init__.pyi', 'utils/__init__.pyi', 'readers/standalone.pyi', 'readers/doctree.pyi', 'readers/__init__.pyi', 'readers/pep.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
