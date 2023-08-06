from setuptools import setup, find_packages

setup(
    name='oapi',

    version="0.0.47",

    description=(
        'An SDK for parsing OpenAPI (Swagger) 2.0 - 3.0 specifications'
    ),

    # The project's main homepage.,
    url='https://bitbucket.com/davebelais/oapi.git',

    # Author details,
    author='David Belais',
    author_email='david@belais.me',

    # Choose your license,
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers,
    classifiers=[
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='openapi swagger json rest',

    packages=find_packages(),
    # packages=[], # explicitly set packages
    # py_modules=[], # Single-file module names

    # dependencies
    # See https://packaging.python.org/en/latest/requirements.html,
    install_requires=[
        "future>=0.17.1",
        "pyyaml>=5.1.1",
        "iso8601>=0.1.12",
        "sob>=0.1.24",
        "jsonpointer>=2.0"
    ],
    extras_require={
        "dev": [
            "pytest>=5.0.1"
        ],
        "test": [
            "pytest>=5.0.1"
        ]
    },

    data_files=[],

    entry_points={
        'console_scripts': [],
    }
)