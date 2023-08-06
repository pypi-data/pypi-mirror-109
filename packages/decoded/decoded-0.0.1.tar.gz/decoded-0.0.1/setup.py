import setuptools

name = "decoded"
version = "0.0.1"
author = "Zalia Labs"
email = "josh@zaliaflow.io"

description = "A library for rapidly building explanations of Machine-Learning models."
description_type = "text/markdown"

url = "https://github.com/ZaliaFlow/decode-py"
project_urls = { "Bug Tracker": "https://github.com/ZaliaFlow/decode-py/issues" }

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Operating System :: OS Independent",
    "Development Status :: 2 - Pre-Alpha"
]

package_dir = { "" : "src" }
packages = setuptools.find_packages(where = "src") # type: ignore partially unknown

python_requires = ">=3.6"

setuptools.setup( # type: ignore partially unknown
    name = name,
    version = version,
    author = author,
    author_email = email,
    description = description,
    long_description = description,
    long_description_content_type = description_type,
    url = url,
    project_urls = project_urls,
    classifiers = classifiers,
    package_dir = package_dir,
    packages = packages, # type: ignore partially unknown
    python_requires = python_requires,
)
