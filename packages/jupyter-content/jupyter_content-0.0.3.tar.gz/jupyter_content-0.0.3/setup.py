"""Setup Module for Jupyter Content.
"""
import setuptools

VERSION = '0.0.3'

setuptools.setup(
    name = 'jupyter_content',
    version = VERSION,
    description = 'Jupyter Content',
#    long_description = open('README.md').read(),
    packages = setuptools.find_packages(),
    package_data = {
        'jupyter_content': [
            '*',
        ],
    },
    install_requires = [
        'google-cloud-storage',
        'hybridcontents',
        'jupyter_server',
        'nbformat',
        'notebook',
        'tornado',
        'traitlets',
    ],
    extras_require = {
        'test': [
            'pytest',
            'pytest-cov',
            'pylint',
            'unittest'
        ]
    },
)
