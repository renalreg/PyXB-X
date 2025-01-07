#!/usr/bin/env python

from __future__ import print_function
import sys

# The current version of the release.
# Note: This is NOT the version number PyXB uses internally to
# test compatibility.  The version number used by PyXB is
# set in pyxb/__init__.py:__version__
# Given that PyXB is no longer being maintained, PyXB-X is
# really a project to keep backwards compatibility with the
# last release of PyXB (1.2.6), so the PyXB version will remain
# the same. The release number will remain based on 1.2.6,
# but the rightmost number will be incremented with each patch.
version = "1.2.6.3"

# Require Python 2.6 or higher or Python 3.5 or higher
if (sys.version_info[:2] < (2, 6)) or (
    (sys.version_info[0] == 3) and sys.version_info[:2] < (3, 5)
):
    raise ValueError(
        """PyXB-X requires:
  Python2 version 2.6 or later; or
  Python3 version 3.5 or later
(You have %s.)"""
        % (sys.version,)
    )

import os
import re
from setuptools import setup
import sys
import pyxb.utils.utility

packages = [
    "pyxb",
    "pyxb.namespace",
    "pyxb.binding",
    "pyxb.utils",
    "pyxb.xmlschema",
    "pyxb.bundles",
]
package_data = {}

init_re = re.compile(r"^__init__\.py$")
wxs_re = re.compile(r"^.*\.wxs$")

setup_path = os.path.dirname(__file__)
bundle_base = os.path.join(setup_path, "pyxb", "bundles")
possible_bundles = []
try:
    possible_bundles.extend(os.listdir(bundle_base))
except OSError as e:
    print("Directory %s bundle search failed: %s" % (bundle_base, e))
for possible_bundle in possible_bundles:
    bundle_root = os.path.join(bundle_base, possible_bundle)
    if not os.path.isdir(bundle_root):
        continue
    b_packages = []
    b_data = {}
    for fp in pyxb.utils.utility.GetMatchingFiles("%s//" % (bundle_root,), init_re):
        bundle_path = os.path.dirname(os.path.normpath(fp))
        try:
            package_relpath = os.path.relpath(bundle_path, setup_path)
        except AttributeError as e:
            package_relpath = bundle_path
            if setup_path and "." != setup_path:
                prefix_path = setup_path + os.path.sep
                if not package_relpath.startswith(prefix_path):
                    print(
                        "Unable to determine relative path from %s to %s installation"
                        % (setup_path, bundle_path)
                    )
                    sys.exit(1)
                package_relpath = package_relpath[len(prefix_path) :]
        package = package_relpath.replace(os.path.sep, ".")
        b_packages.append(package)
        wxs_files = [
            os.path.basename(_f)
            for _f in pyxb.utils.utility.GetMatchingFiles(bundle_path, wxs_re)
        ]
        if wxs_files:
            b_data[package] = wxs_files
    if 0 < len(b_data):
        print("Found bundle in %s" % (bundle_root,))
        packages.extend(b_packages)
        package_data.update(b_data)

setup(
    name="PyXB-X",
    description='PyXB-X ("pixbix") is a pure Python package that generates Python source code for classes that correspond to data structures defined by XMLSchema.',
    author="Peter A. Bigot",
    author_email="pabigot@users.sourceforge.net",
    url="http://pyxb.sourceforge.net",
    # Also change in README.TXT, pyxb/__init__.py, and doc/conf.py
    version=version,
    license="Apache License 2.0",
    long_description="""PyXB is a pure `Python <http://www.python.org>`_ package that generates
Python code for classes that correspond to data structures defined by
`XMLSchema <http://www.w3.org/XML/Schema>`_.  In concept it is similar to
`JAXB <http://en.wikipedia.org/wiki/JAXB>`_ for Java and `CodeSynthesis XSD
<http://www.codesynthesis.com/products/xsd/>`_ for C++.

The major goals of PyXB are:

* Provide a generated Python interface that is "Pythonic", meaning similar
  to one that would have been hand-written:

  + Attributes and elements are Python properties, with name conflicts
    resolved in favor of elements
  + Elements with maxOccurs larger than 1 are stored as Python lists
  + Bindings for type extensions inherit from the binding for the base type
  + Enumeration constraints are exposed as class (constant) variables

* Support bi-directional conversion (document to Python and back)

* Allow easy customization of the generated bindings to provide
  functionality along with content

* Support all XMLSchema features that are in common use, including:

  + complex content models (nested all/choice/sequence)
  + cross-namespace dependencies
  + include and import directives
  + constraints on simple types
""",
    provides=["PyXB"],
    packages=packages,
    package_data=package_data,
    # I normally keep these in $purelib, but distutils won't tell me where that is.
    # We don't need them in the installation anyway.
    # data_files= [ ('pyxb/standard/schemas', glob.glob(os.path.join(*'pyxb/standard/schemas/*.xsd'.split('/'))) ) ],
    scripts=["scripts/pyxbgen", "scripts/pyxbwsdl", "scripts/pyxbdump"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Text Processing :: Markup :: XML",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
