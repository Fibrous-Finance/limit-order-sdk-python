from setuptools import setup, find_packages

setup(
    name='fibrous-limit-order-python-sdk',
    version='1.0.0',  
    author='zeroonesymphony', 
    author_email='kermo@fibrous.finance',
    description='A Python SDK for Fibrous Finance Limit Order',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/Fibrous-Finance/limit-order-python-sdk', 
    packages=find_packages(),  
    install_requires=[
        # 'aiohttp>= 3.9.3',
        # 'starknet_py>=0.21.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
)