from setuptools import find_packages, setup

setup(
    name='stock_prophet',
    packages=find_packages(),
    version='0.1.1',
    install_requires=['flask', 'prophet==1.0.1','yfinance']
)