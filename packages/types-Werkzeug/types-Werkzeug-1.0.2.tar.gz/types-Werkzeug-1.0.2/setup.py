from setuptools import setup

name = "types-Werkzeug"
description = "Typing stubs for Werkzeug"
long_description = '''
## Typing stubs for Werkzeug

This is an auto-generated PEP 561 type stub package for `Werkzeug` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Werkzeug`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Werkzeug. All fixes for
types and metadata should be contributed there.

*Note:* The `Werkzeug` package includes type annotations or type stubs
since version 2.0. Please uninstall the `types-Werkzeug`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `64f463172b27d7321461890dd3edf416a103ace7`.
'''.lstrip()

setup(name=name,
      version="1.0.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['werkzeug-stubs'],
      package_data={'werkzeug-stubs': ['wsgi.pyi', 'formparser.pyi', 'utils.pyi', 'http.pyi', 'exceptions.pyi', 'filesystem.pyi', 'useragents.pyi', 'serving.pyi', 'datastructures.pyi', 'local.pyi', '_internal.pyi', '_reloader.pyi', 'posixemulation.pyi', '_compat.pyi', 'urls.pyi', 'routing.pyi', 'script.pyi', 'testapp.pyi', 'wrappers.pyi', 'security.pyi', '__init__.pyi', 'test.pyi', 'debug/repr.pyi', 'debug/console.pyi', 'debug/__init__.pyi', 'debug/tbtools.pyi', 'middleware/dispatcher.pyi', 'middleware/lint.pyi', 'middleware/shared_data.pyi', 'middleware/__init__.pyi', 'middleware/http_proxy.pyi', 'middleware/profiler.pyi', 'middleware/proxy_fix.pyi', 'contrib/testtools.pyi', 'contrib/securecookie.pyi', 'contrib/limiter.pyi', 'contrib/sessions.pyi', 'contrib/iterio.pyi', 'contrib/cache.pyi', 'contrib/fixers.pyi', 'contrib/atom.pyi', 'contrib/lint.pyi', 'contrib/wrappers.pyi', 'contrib/jsrouting.pyi', 'contrib/__init__.pyi', 'contrib/profiler.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
