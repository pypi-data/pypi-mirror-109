from setuptools import setup, find_packages

setup(
    name='dslogger',
    version='0.0.1',
    author='ice_coder',
    author_email='1943158197@qq.com',
    description='用于记录日志信息',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['logger']
)