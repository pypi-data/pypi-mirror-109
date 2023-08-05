import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="croppy", # Replace with your own username
    version="0.1.0.1.8",
    author="Surasak Choedpasuporn",
    author_email="surasak.cho@gmail.com",
    description="A crop insurance specific package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/surasakcho/croppy",
    packages=setuptools.find_packages(),    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
