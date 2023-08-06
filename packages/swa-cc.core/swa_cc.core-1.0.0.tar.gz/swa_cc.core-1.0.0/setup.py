from setuptools import setup, find_packages


with open("README.md") as fp:
    long_description = fp.read()


setup(
    name="swa_cc.core",
    version="1.0.0",

    description="A set of core objects utilized by the rest of the SWA Cloud Catalog",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Seth Dobson",
    author_email="sd0408@gmail.com",

    package_dir={"": "src"},
    packages=["swa_cc.core"],

    # install_requires=[
    # ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
