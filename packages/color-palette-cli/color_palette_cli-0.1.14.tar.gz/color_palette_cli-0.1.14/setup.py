from setuptools import find_packages, setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = 'color_palette_cli',
    version = '0.1.14',
    author = 'Adam T',
    author_email = 'adam.tabaczynski@bitcomp.fi',
    description = 'Command Line Interface allowing interaction with color_palette_at library.',
    long_description = readme(),
    long_description_content_type = "text/markdown",
    licence = 'MIT',
    keywords = 'color color_palette colors cli',
    url = '',
    entry_points = {
        'console_scripts': [
            'cli_color = color_palette_cli.color_palette_cli:ColorCLI.get_color_palette',
            ],
        },
    packages = find_packages(include=['color_palette_cli']),
    install_requires = [
        'color_palette_at',
    ],
    python_requires = '>=3.7',   
    classifiers = [
        "Programming Language :: Python :: 3.7",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
