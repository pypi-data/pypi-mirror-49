from setuptools import setup, find_packages

setup(
    name='code-stats',
    version='0.1.1',
    description='''A command line tool to generate code statistics for a given directory.
    These statistics include
    1. Total Lines of Code.
    2. Percentage wise break up of different languages used.''',
    author='Abhinav Shaw',
    author_email='abhinav.shaw1993@gmail.com',
    packages=find_packages(),
    install_requires=[
        'click',
        'pathlib',
    ],
    keywords = ['Code statistics', 'lines of code', 'loc'],
    setup_requires=[
        "pytest-runner",
    ],
    test_requires=[
        'pytest',
    ],
    entry_points={
        'console_scripts' : ['codestats=code_stats.cli:generate_code_statistics']
    },
    url="https://github.com/abhinavshaw1993/code-stats",
    classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux"
                    ],
    package_data={'code_stats': ['data/*', 'tests/testing_data/*']},
    include_package_data=True,
    zip_safe=False,
    setup_cfg=True
)
