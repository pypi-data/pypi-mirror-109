import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplepythonwer",
    version="1.0.3",
    author="Rob Smith",
    author_email="robmsmt@gmail.com",
    description="A small basic python implementation of WER (word error rate) and levenshtein",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robmsmt/SimplePythonWER",
    packages=setuptools.find_packages(exclude="test",),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

#python3 -m pip install --upgrade setuptools wheel
#python3 setup.py sdist bdist_wheel
#sudo apt install twine -y
#twine upload dist/*
