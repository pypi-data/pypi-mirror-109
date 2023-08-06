import setuptools
import os

with open(os.path.join(os.getcwd(), "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="docsdk",
    version="2.0.2",
    author="ChenMing",
    author_email="chenming@9yuntu.com",
    description="Python REST API wrapper for docsdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/docsdk/docsdk-python",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "urllib3"
    ],
    tests_require=["requests-mock"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)