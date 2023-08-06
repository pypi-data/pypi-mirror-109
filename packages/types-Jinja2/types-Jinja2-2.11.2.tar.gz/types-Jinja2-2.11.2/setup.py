from setuptools import setup

name = "types-Jinja2"
description = "Typing stubs for Jinja2"
long_description = '''
## Typing stubs for Jinja2

This is an auto-generated PEP 561 type stub package for `Jinja2` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Jinja2`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Jinja2. All fixes for
types and metadata should be contributed there.

*Note:* The `Jinja2` package includes type annotations or type stubs
since version 3.0. Please uninstall the `types-Jinja2`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `64f463172b27d7321461890dd3edf416a103ace7`.
'''.lstrip()

setup(name=name,
      version="2.11.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-MarkupSafe'],
      packages=['jinja2-stubs'],
      package_data={'jinja2-stubs': ['debug.pyi', 'nodes.pyi', 'utils.pyi', 'exceptions.pyi', 'filters.pyi', 'tests.pyi', 'loaders.pyi', 'visitor.pyi', 'ext.pyi', 'compiler.pyi', '_compat.pyi', 'meta.pyi', 'parser.pyi', 'runtime.pyi', 'environment.pyi', 'sandbox.pyi', 'optimizer.pyi', 'defaults.pyi', 'bccache.pyi', 'constants.pyi', 'lexer.pyi', '__init__.pyi', '_stringdefs.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
