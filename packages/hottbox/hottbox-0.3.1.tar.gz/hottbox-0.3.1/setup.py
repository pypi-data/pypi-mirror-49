import os
import re
from setuptools import setup, find_packages


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')


def get_version():
    init = open(os.path.join(ROOT, 'hottbox', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


def readme():
    with open('README.rst') as f:
        return f.read()


def install_requires():
    with open('requirements.txt') as f:
        return list(f.read().strip().split('\n'))


def extras_require():
    extra_requirements = {
        'tests': [
            'pytest',
            'pytest-cov'
        ],
        'docs': [
            'sphinx',
            'guzzle_sphinx_theme',
            'numpydoc',
            'm2r'
        ]
    }
    all_requires = [item for sublist in extra_requirements.values() for item in sublist]
    extra_requirements['all'] = all_requires
    return extra_requirements


config = dict(
    name='hottbox',
    version=get_version(),
    packages=find_packages(exclude=['docs']),
    url='https://github.com/hottbox/hottbox',
    license='Apache License 2.0',
    author='Ilya Kisil',
    author_email='ilyakisil@gmail.com',
    description='Higher Order Tensors ToolBOX',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ],
    keywords=['tensor decompositions', 'machine learning'],
    install_requires=install_requires(),
    extras_require=extras_require(),
    include_package_data=True,
    zip_safe=False
)

setup(**config)

print("\nWelcome to HOTTBOX!")
print("If any questions please visit documentation page https://hottbox.github.io")
