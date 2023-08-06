from setuptools import find_packages, setup

setup(
    name='stock_prophet',
    packages=find_packages(),
    version='0.1.0',
    install_requires=['flask==2.0.1', 'prophet==1.0.1','yfinance==0.1.59']
)