from setuptools import find_packages, setup

"""
reference:
https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f
"""
setup(
    name='my-util-lib',
    packages=find_packages(where='src', include=['my-util-lib'], exclude=[]),
    package_dir={
        '': 'src',
    },
    version='1.0.3',
    description='My util library in Python',
    long_description='My util library in Python (long description)',
    author='Me',
    author_email="me@test.com",
    url="http://localhost",
    license='MIT',
    install_requires=[
        'numpy>=1.19'
    ],  # any dependencies that this library needs go here
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest==6.2.4'],
    # test_suite='tests',
)
