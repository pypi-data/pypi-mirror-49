from setuptools import find_packages, setup

description = 'Pandas Table Tooltip is a Python librarythat only adds '\
              'tooltips to Pandas tables on Jupyter.'

long_description = \
    'Pandas Table Tooltip is a Python librarythat only adds tooltips '\
    'to Pandas tables on Jupyter. For more information, please see '\
    'github README: https://github.com/simon-ritchie/pandas-table-tooltip'

setup(
    name='pandastabletooltip',
    version='0.0.1',
    url='https://github.com/simon-ritchie/pandas-table-tooltip',
    author='simon-ritchie',
    author_email='',
    maintainer='simon-ritchie',
    maintainer_email='',
    description=description,
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
