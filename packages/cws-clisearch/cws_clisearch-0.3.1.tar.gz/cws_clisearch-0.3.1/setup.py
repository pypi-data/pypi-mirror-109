"""Info for setup tools."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cws_clisearch",
    version="0.3.1",
    author="j wizzle",
    author_email="info@hossel.net",
    description="A CLI web search tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jwizzle/cws",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'cws=cws:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
