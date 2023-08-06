import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    setuptools.setup(
        name="PyChart-busnellistefano",
        version="1.0.3",
        author="Busnelli Stefano Antonio",
        author_email="busnelli.stefano@gmail.com",
        description="A simple chart class",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://bitbucket.org/StefanoBusnelli/pychart",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 2.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
   )
