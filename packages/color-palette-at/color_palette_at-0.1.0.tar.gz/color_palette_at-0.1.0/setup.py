from setuptools import find_packages, setup

setup(
    name = 'color_palette_at',
    version = '0.1.0',
    author = 'Adam Tabaczyński',
    author_email = 'adam.tabaczynski96@gmail.com',
    description = 'Library that allows to get a color palette from an image.',
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
        "Programming Language :: Python :: 3.7",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
