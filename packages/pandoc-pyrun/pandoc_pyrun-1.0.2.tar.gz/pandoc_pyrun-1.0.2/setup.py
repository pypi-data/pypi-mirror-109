from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pandoc_pyrun",

    version="1.0.2",
    description="Pandoc filter to run python code blocks",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://gitlab-fil.univ-lille.fr/phm/pandoc-pyrun",
    download_url="https://gitlab-fil.univ-lille.fr/phm/pandoc-pyrun/-/archive/master/pandoc-pyrun-master.tar.gz",
    
    author="D'hulst Thomas, Tayebi Ajwad",
    author_email="thomas.dhulst@hotmail.fr, ajwad.tayebi@gmail.com",

    license="BDS2",

    packages=find_packages(),

    python_requires='>=3.6,<4',

    install_requires=["pandocfilters", "matplotlib"],

    keywords="pandoc filters markdown python notes pandocfilters pdf latex",
    
    zip_safe=False,

    py_modules=["pandoc_pyrun.pandoc_pyrun"],

    entry_points={
        "console_scripts": [
            "pandoc_pyrun = pandoc_pyrun.pandoc_pyrun:main",
        ],
    },
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "coverage"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",  # to be reviewed
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Filters",
    ]
)