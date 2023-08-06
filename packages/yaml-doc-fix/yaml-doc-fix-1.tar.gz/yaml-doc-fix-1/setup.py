from setuptools import setup, find_packages

NAME = "yaml-doc-fix"
REPO = "ansible-yamldocfix"

VERSION = "1"
ARCHIVE = f"v_{'_'.join(VERSION.split('.'))}.tar.gz"

setup(
    name=NAME,
    packages=find_packages(),
    version=VERSION,
    license="MIT",
    description="Auto fixer for yamllint 'document-start' warning",
    author="Dani Hodovic / Renny Montero",
    author_email="rennym19@gmail.com",
    url=f"https://github.com/rennym19/{REPO}",
    download_url=f"https://github.com/rennym19/{REPO}/archive/{ARCHIVE}",
    keywords=["ANSIBLE", "FIX", "YAML", "LINT", "DOCUMENT", "START", "WARNING"],
    include_package_data=True,
    entry_points={
        "console_scripts": [f"{NAME} = yaml_doc_fix.script:run"]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
