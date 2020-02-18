from setuptools import setup

packages = ["flashgeotext"]

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="flashgeotext",
    version="0.1.0",
    description="find city names or country names in text using aho-corasick",
    url="http://github.com/iwpnd/flashgeotext",
    author="Benjamin Ramser",
    author_email="ahoi@iwpnd.pw",
    license="MIT",
    include_package_data=True,
    install_requires=required,
    packages=packages,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Natural Language :: aho-corasick",
        "Intended Audience :: Developers :: Journalists :: Analysts",
    ],
)
