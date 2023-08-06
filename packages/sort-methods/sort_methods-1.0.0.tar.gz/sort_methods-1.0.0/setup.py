import setuptools
import sort_methods

with open('Readme.md') as fr:
    long_description = fr.read()

setuptools.setup(
    name='sort_methods',
    version=sort_methods.__version__,
    author='Borenkov Roman',
    author_email='',
    description='5 methods of sort in python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rborkv/sort_methods/',
    packages=setuptools.find_packages(),
    install_requires=[],
    test_suite='tests',
    python_requires='>=3.7',
    platforms=["any"]
)