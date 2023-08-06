import setuptools

setuptools.setup(
    name="py-classification-cache",
    version="0.0.1",
    author="Philip Huang",
    author_email="p208p2002@gmail.com",
    description="Python classification cache",
    long_description="[https://github.com/p208p2002/py-classification-cache](https://github.com/p208p2002/py-classification-cache \"https://github.com/p208p2002/py-classification-cache\")",
    long_description_content_type="text/markdown",
    url="https://github.com/p208p2002/py-classification-cache",
    packages=setuptools.find_packages(),
    install_requires=['pypinyin==0.35.4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)