from setuptools import setup

name = "types-boto"
description = "Typing stubs for boto"
long_description = '''
## Typing stubs for boto

This is an auto-generated PEP 561 type stub package for `boto` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `boto`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/boto. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `64f463172b27d7321461890dd3edf416a103ace7`.
'''.lstrip()

setup(name=name,
      version="0.1.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-six'],
      packages=['boto-stubs'],
      package_data={'boto-stubs': ['regioninfo.pyi', 'utils.pyi', 'compat.pyi', 'connection.pyi', 'auth.pyi', 'exception.pyi', 'auth_handler.pyi', 'plugin.pyi', '__init__.pyi', 'ec2/__init__.pyi', 'kms/exceptions.pyi', 'kms/layer1.pyi', 'kms/__init__.pyi', 'elb/__init__.pyi', 's3/deletemarker.pyi', 's3/bucketlistresultset.pyi', 's3/lifecycle.pyi', 's3/key.pyi', 's3/bucket.pyi', 's3/website.pyi', 's3/connection.pyi', 's3/user.pyi', 's3/cors.pyi', 's3/prefix.pyi', 's3/multidelete.pyi', 's3/tagging.pyi', 's3/acl.pyi', 's3/keyfile.pyi', 's3/multipart.pyi', 's3/bucketlogging.pyi', 's3/__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
