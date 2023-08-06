from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name="startpage-ggg",
    version='1.0.0',
    license="GPL-3.0 License",
    description='parsing search results from startpage search engine (based on google.com results)',
    py_modules=["startpageggg"],
    long_description=readme,
    package_dir={'':'src'},
    url='https://github.com/mhmh55516/ggg',
    python_requires='>=3.6',
    install_requires=['bs4','requests','termcolor','argparse']
)
