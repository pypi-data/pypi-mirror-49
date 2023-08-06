try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="regsnp",
    version="0.2.5.2",
    packages=["regsnp_intron", "regsnp_intron.utils"],
    scripts=["regsnp_intron.py"],
    install_requires=["pandas==0.17.1", "pysam==0.15.2", "pymongo"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    url="https://github.com/mmammel12/regSNP",
    license="MIT",
    author="linhai, mamammel",
    author_email="linhai@iupui.edu, mamammel@iu.edu",
    description="Predict disease-causing probability of human intronic SNVs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
