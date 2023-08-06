import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Docco-CLI",
    version="0.0.1",
    author="Docco-Labs",
    author_email="",
    description="Work in progress - Docco",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/docco/docco-package",
    project_urls={
        "Bug Tracker": "https://github.com/docco/docco-package/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
