
from setuptools import setup, find_packages

setup(
    name="ocspy",
    version="0.4.7",
    keywords=("pip", "optical communication",
              "coherent optical", "ocspy", "ocspy"),
    description="simulate optical communication",
    long_description="simulate optical communication",
    license="MIT Licence",
    packages=find_packages(),

    url="",
    author="nigulasikaochuan",
    author_email="nigulasikaochuan@sjtu.edu.cn",


    include_package_data=True,
    platforms="any",
    install_requires=['plotly','pyqt5','pyqtgraph','numpy','scipy','matplotlib','h5py']
)
