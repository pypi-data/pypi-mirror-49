import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythondcs",
    version="0.1.1",
    author="Mark Jarvis",
    description="Python Module for interfacing with the Coherent Research DCS v3+ remote metering server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jarvisms/pythondcs",
    packages=setuptools.find_packages(),
    py_modules=["pythondcs", "pythondcspro"],
    python_requires='>=3.6',
    install_requires=['requests'],
    license="GPLv3",
    zip_safe=True,
    keywords = ['energy', 'metering', 'coherent', 'DCS'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
)