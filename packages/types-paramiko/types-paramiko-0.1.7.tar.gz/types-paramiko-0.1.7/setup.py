from setuptools import setup

name = "types-paramiko"
description = "Typing stubs for paramiko"
long_description = '''
## Typing stubs for paramiko

This is an auto-generated PEP 561 type stub package for `paramiko` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `paramiko`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/paramiko. All fixes for
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
      install_requires=['types-cryptography'],
      packages=['paramiko-stubs'],
      package_data={'paramiko-stubs': ['sftp_file.pyi', 'proxy.pyi', 'client.pyi', 'win_pageant.pyi', 'file.pyi', 'kex_group14.pyi', 'kex_ecdh_nist.pyi', 'buffered_pipe.pyi', 'py3compat.pyi', 'ber.pyi', 'sftp.pyi', 'kex_gex.pyi', 'channel.pyi', 'sftp_handle.pyi', 'dsskey.pyi', '_version.pyi', 'sftp_attr.pyi', 'ed25519key.pyi', 'agent.pyi', 'util.pyi', 'transport.pyi', 'kex_curve25519.pyi', 'compress.pyi', 'auth_handler.pyi', 'sftp_server.pyi', 'primes.pyi', 'ssh_exception.pyi', 'sftp_client.pyi', 'common.pyi', 'rsakey.pyi', 'ecdsakey.pyi', 'sftp_si.pyi', 'ssh_gss.pyi', '__init__.pyi', 'message.pyi', 'kex_group16.pyi', 'hostkeys.pyi', 'server.pyi', 'pipe.pyi', 'kex_gss.pyi', 'packet.pyi', 'kex_group1.pyi', '_winapi.pyi', 'pkey.pyi', 'config.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
