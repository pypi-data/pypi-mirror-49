import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mkalias-foss',
    author='Adam Bennett',
    author_email="iamcb@teck90.ca",
    url='https://github.com/iamcb/mkalias',
    use_scm_version={
        'write_to': 'mkalias_foss/version.py',
    },
    license='LICENSE.txt',
    description='CLI app to create Finder aliases in OS X',
    long_description=long_description,
    long_description_content_type="text/markdown",
    # packages=setuptools.find_packages(),
    packages=['mkalias_foss'],
    setup_requires=['setuptools_scm', ],
    install_requires=['osascript', 'click', ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
    ],
    entry_points={
        'console_scripts':
            ['mkalias = mkalias_foss.mkalias:main', ],
    }
)
