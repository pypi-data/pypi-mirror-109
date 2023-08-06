from setuptools import setup, find_packages

VERSION = '0.1.6'
DESCRIPTION = 'Almost all Searching and Sorting Algorithms for Python 3.x'

file = open("readme.md", encoding='utf-8')
LONG_DESCRIPTION = file.read()

# Setting up
setup(
    name="searchsort",
    version=VERSION,
    author="Programmin-in-Python (MK)",
    author_email="<kalanithi6014@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    python_requires=">=3",
    project_urls={"GitHub":"https://github.com/Programmin-in-Python/searchsort"},
    keywords=['python3', 'sort', 'search', 'sorting', 'searching', 'sorting-algorithms',
                'searching-algorithms', 'search-sort', 'searchsort'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
