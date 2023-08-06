import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="advantech-daq-python",                     # This is the name of the package
    version="0.0.5",                        # The initial release version
    author="tanvubc",                     # Full name of the author
    description="Simple DI DO function to interface with USB-5830",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    include_package_data=True,
    license='mit',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["NavigatorPython"],             # Name of the python package
    package_dir={'':'src'},     # Directory of the source code of the package
    package_data={'':['*.pyd']},
    install_requires=[]                     # Install other dependencies if any
)