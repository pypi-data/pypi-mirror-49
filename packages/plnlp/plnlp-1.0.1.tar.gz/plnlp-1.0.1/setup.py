import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="plnlp",
    version="1.0.1",
    description="Keyword Recognition and Pre-processing",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pengluyaoyao/lpnlp",
    author=["Luyao Peng, Rui Yang"],
    author_email="luyaopeng.cn@gmail.com, rkzyang@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["logging", "csv"],
    entry_points={
        "console_scripts": [
            "plnlp=plnlp.__main__:main",
        ]
    },
)
