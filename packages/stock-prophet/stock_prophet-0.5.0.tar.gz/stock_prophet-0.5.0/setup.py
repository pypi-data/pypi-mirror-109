from setuptools import find_packages, setup

setup(
    name='stock_prophet',
    packages=find_packages(),
    version='0.5.0',
    install_requires=['prophet==1.0.1','yfinance']
)