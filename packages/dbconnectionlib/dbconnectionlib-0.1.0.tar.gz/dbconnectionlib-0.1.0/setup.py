from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    description = fh.read()
setup(
    name="dbconnectionlib",
    packages=find_packages(),
    install_requires=["sqlalchemy"],
    python_requires=">=3.5",
    url="https://github.com/Divya-Ravindran/dbconnectionlib",
    download_url="https://github.com/Divya-Ravindran/dbconnectionlib/archive/refs/tags/0.1.0.tar.gz",
    version="0.1.0",
    description="DB Connection Python library",
    author="Divya Ravindran",
    author_email="divya.ravindran@gfk.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)