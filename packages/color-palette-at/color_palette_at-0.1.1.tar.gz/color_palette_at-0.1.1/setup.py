from setuptools import find_packages, setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name = 'color_palette_at',
    version = '0.1.1',
    author = 'Adam Tabaczyński',
    author_email = 'adam.tabaczynski96@gmail.com',
    description = 'Library that allows to get a color palette from an image.',
    long_description = 'README',
    long_description_content_type = "text/markdown",
    licence = 'MIT',
    keywords = 'color color_palette colors',
    url = '',
    packages = find_packages(include = ['color_palette_at, tests']),
    install_requires = [
        'pytest',
        'Pillow',
    ],
    python_requires = '>=3.6',   
    classifiers = [
        "Programming Language :: Python :: 3.6",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
