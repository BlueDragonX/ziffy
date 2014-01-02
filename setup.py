from setuptools import setup, find_packages

version = (0, 1, 0)
requires = ['exifread']

setup(
    name='ziffy',
    version='.'.join(str(n) for n in version),
    description='Image organization tools.',
    long_description='Image organization tools for the command line.',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
    keywords='',
    author='Ryan Bourgeois',
    author_email='bluedragonx@gmail.com',
    url='https://github.com/BlueDragonX/ziffy',
    license='GPLv2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="",
    entry_points={
        'console_scripts': [
            'ziffy-sort=ziffy.sort:main',
        ],
    }
)
