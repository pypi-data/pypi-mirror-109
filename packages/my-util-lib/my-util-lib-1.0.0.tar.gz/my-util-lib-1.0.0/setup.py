from setuptools import find_packages, setup

"""
reference:
https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f
"""
setup(
    name='my-util-lib',
    packages=find_packages(where='.', include=['src'], exclude=['tests']),
    version='1.0.0',
    description='My util library in Python',
    author='Me',
    author_email="me@test.com",
    url="http://localhost",
    license='MIT',
    install_requires=['numpy==1.20.3'],  # any dependencies that this library needs go here
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest==6.2.4'],
    # test_suite='tests',
)
