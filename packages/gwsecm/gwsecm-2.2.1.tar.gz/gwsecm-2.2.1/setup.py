import json
import os
import re

import setuptools

# from setuptools import setup, find_packages

f = open(
    "./package.json",
)


def get_version():
    data = json.load(f)
    return data["version"]


setuptools.setup(
    name="gwsecm",
    version=get_version(),
    description=f"GWSE Change Management API code",
    url="https://bitbucket.es.ad.adp.com/projects/GWSE/repos/co-automation-api/browse",
    author="Yash Panchal",
    author_email="yash.panchal@adp.com",
    license="(c) ADP, LLC",
    package_dir={"": "app"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    # packages=[
    #     "appdirs",
    #     "astroid",
    #     "attrs",
    #     "bson",
    #     "cached-property",
    #     "certifi",
    #     "chardet",
    #     "click",
    #     "defusedxml",
    #     "distlib",
    #     "filelock",
    #     "flask",
    #     "flask-cors",
    #     "flatten-json",
    #     "gevent",
    #     "greenlet",
    #     "gunicorn",
    #     "idna",
    #     "importlib-metadata",
    #     "isodate",
    #     "isort",
    #     "itsdangerous",
    #     "jinja2",
    #     "lazy-object-proxy",
    #     "lxml",
    #     "markupsafe",
    #     "mccabe",
    #     "more-itertools",
    #     "numpy",
    #     "pip-chill",
    #     "pipenv",
    #     "pluggy",
    #     "py",
    #     "pylint",
    #     "pymongo",
    #     "pyparsing",
    #     "pytest",
    #     "python-dateutil",
    #     "pytz",
    #     "requests",
    #     "requests-toolbelt",
    #     "six",
    #     "toml",
    #     "typed-ast",
    #     "urllib3",
    #     "utils",
    #     "virtualenv",
    #     "virtualenv-clone",
    #     "wcwidth",
    #     "werkzeug",
    #     "wrapt",
    #     "zeep",
    #     "zipp",
    #     "zope-event",
    #     "zope-interface",
    #     "xmltodict",
    #     "iteration-utilities",
    #     "psutil",
    #     "json2html",
    #     "pandas",
    #     "apscheduler",
    #     "fastapi",
    #     "uvicorn",
    #     "backoff",
    #     "pydantic",
    #     "fastapi-utils",
    #     "uvloop",
    #     "httptools",
    #     "pyjwt",
    # ],
)
# import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

# setuptools.setup(
#     name="example-pkg-YOUR-USERNAME-HERE",
#     version="0.0.1",
#     author="Example Author",
#     author_email="author@example.com",
#     description="A small example package",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/pypa/sampleproject",
#     project_urls={
#         "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
#     },
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     package_dir={"": "src"},
#     packages=setuptools.find_packages(where="src"),
#     python_requires=">=3.6",
# )
