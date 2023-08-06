# {# pkglts, pysetup.kwds
# format setup arguments
from setuptools import setup, find_packages

short_descr = "Extract graph from image"
readme = open('README.rst').read()
history = open('HISTORY.rst').read()

# find packages
pkgs = find_packages('src')



setup_kwds = dict(
    name='graphextract',
    version="1.0.0",
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="revesansparole",
    author_email="revesansparole@gmail.com",
    url='https://github.com/revesansparole/graphextract',
    license='cecill-c',
    zip_safe=False,

    packages=pkgs,
    
    package_dir={'': 'src'},
    setup_requires=[
        "pytest-runner",
        ],
    install_requires=[
        "reportlab",
        "svglib>=1.1, <1.2",
        ],
    tests_require=[
        "pytest",
        "pytest-mock",
        ],
    entry_points={},
    keywords='',
    )
# #}
# change setup_kwds below before the next pkglts tag

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
