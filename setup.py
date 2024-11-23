from setuptools import setup, find_packages

setup(
    name="censore",
    # noqa
    version="0.2.1",
    description="A package for censoring profanity in text",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Okinea Dev",
    url="https://github.com/censor-text/censore",
    packages=find_packages(),
    package_data={"": ["data/**/*.txt"]},
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
