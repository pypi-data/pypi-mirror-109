import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oursms_py",
    version="0.9",
    author="alimiracle",
    author_email="alimiracle@riseup.net",
    description="a oursms Library in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://notabug.org/alimiracle/oursms_py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
   'opencv-python',
   'pyobjc-core;platform_system=="Darwin"', 
   'pyobjc;platform_system=="Darwin"',
   'python3-Xlib;platform_system=="Linux" and python_version>="3.0"',
   'Xlib;platform_system=="Linux" and python_version<"3.0"',
  "requests",
],
)
