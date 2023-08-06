from setuptools import find_packages, setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = 'color_palette_at',
    version = '0.1.6',
    author = 'Adam Tabaczyński',
    author_email = 'adam.tabaczynski96@gmail.com',
    description = 'Library that allows to get a color palette from an image.',
    long_description = readme(),
    long_description_content_type = "text/markdown",
    licence = 'MIT',
    keywords = 'color color_palette colors',
    url = '',
    packages = find_packages(include=['color_palette']),
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
