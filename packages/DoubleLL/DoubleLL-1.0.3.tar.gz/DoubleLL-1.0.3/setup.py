  
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DoubleLL", 
    version="1.0.3",
    author="Маскаленко Максим",
    author_email="Maxs.ru2002@gmail.com",
    description="Двусвязный список в Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lev1asan",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "Code"},
    packages=setuptools.find_packages(where="Code"),
    python_requires=">=3.0",
)