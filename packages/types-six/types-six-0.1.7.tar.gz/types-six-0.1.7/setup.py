from setuptools import setup

name = "types-six"
description = "Typing stubs for six"
long_description = '''
## Typing stubs for six

This is an auto-generated PEP 561 type stub package for `six` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `six`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/six. All fixes for
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
      packages=['six-stubs', 'six-python2-stubs'],
      package_data={'six-stubs': ['__init__.pyi', 'moves/queue.pyi', 'moves/cPickle.pyi', 'moves/socketserver.pyi', 'moves/html_entities.pyi', 'moves/builtins.pyi', 'moves/http_cookiejar.pyi', 'moves/SimpleHTTPServer.pyi', 'moves/html_parser.pyi', 'moves/tkinter.pyi', 'moves/http_cookies.pyi', 'moves/urllib_response.pyi', 'moves/urllib_parse.pyi', 'moves/email_mime_multipart.pyi', 'moves/reprlib.pyi', 'moves/tkinter_commondialog.pyi', 'moves/tkinter_dialog.pyi', 'moves/email_mime_nonmultipart.pyi', 'moves/urllib_error.pyi', 'moves/collections_abc.pyi', 'moves/tkinter_constants.pyi', 'moves/http_client.pyi', 'moves/BaseHTTPServer.pyi', 'moves/tkinter_ttk.pyi', 'moves/tkinter_tkfiledialog.pyi', 'moves/urllib_request.pyi', 'moves/_dummy_thread.pyi', 'moves/urllib_robotparser.pyi', 'moves/__init__.pyi', 'moves/_thread.pyi', 'moves/configparser.pyi', 'moves/email_mime_base.pyi', 'moves/tkinter_filedialog.pyi', 'moves/CGIHTTPServer.pyi', 'moves/email_mime_text.pyi', 'moves/urllib/error.pyi', 'moves/urllib/parse.pyi', 'moves/urllib/request.pyi', 'moves/urllib/response.pyi', 'moves/urllib/robotparser.pyi', 'moves/urllib/__init__.pyi', 'METADATA.toml'], 'six-python2-stubs': ['__init__.pyi', 'moves/queue.pyi', 'moves/cPickle.pyi', 'moves/socketserver.pyi', 'moves/html_entities.pyi', 'moves/http_cookiejar.pyi', 'moves/SimpleHTTPServer.pyi', 'moves/html_parser.pyi', 'moves/xmlrpc_client.pyi', 'moves/http_cookies.pyi', 'moves/urllib_response.pyi', 'moves/urllib_parse.pyi', 'moves/email_mime_multipart.pyi', 'moves/reprlib.pyi', 'moves/email_mime_nonmultipart.pyi', 'moves/urllib_error.pyi', 'moves/collections_abc.pyi', 'moves/http_client.pyi', 'moves/BaseHTTPServer.pyi', 'moves/urllib_request.pyi', 'moves/_dummy_thread.pyi', 'moves/urllib_robotparser.pyi', 'moves/__init__.pyi', 'moves/_thread.pyi', 'moves/configparser.pyi', 'moves/email_mime_base.pyi', 'moves/CGIHTTPServer.pyi', 'moves/email_mime_text.pyi', 'moves/urllib/error.pyi', 'moves/urllib/parse.pyi', 'moves/urllib/request.pyi', 'moves/urllib/response.pyi', 'moves/urllib/robotparser.pyi', 'moves/urllib/__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
