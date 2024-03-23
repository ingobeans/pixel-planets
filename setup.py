from setuptools import setup, find_packages

setup(
    name='pixelplanets',
    version='0.1.1',
    install_requires=[
        "pillow>=10.2.0"
    ],
    packages=find_packages(),
    exclude_package_data={'': ['example.py']},
)
