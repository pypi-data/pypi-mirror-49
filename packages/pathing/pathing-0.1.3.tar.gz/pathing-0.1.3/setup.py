import setuptools

with open('README.md') as file:

    readme = file.read()

name = 'pathing'

version = '0.1.3'

author = 'Exahilosys'

url = f'https://github.com/{author}/{name}'

setuptools.setup(
    name = name,
    version = version,
    author = author,
    url = url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    description = 'Mapping keys path to value derivation.',
    long_description = readme,
    long_description_content_type = 'text/markdown',
    include_package_data = True,
    py_modules = [
        name
    ],
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
