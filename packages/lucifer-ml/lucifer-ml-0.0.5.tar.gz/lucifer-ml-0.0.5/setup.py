from setuptools import setup, find_packages
from codecs import open
from os import path
setup(
    name='lucifer-ml',         
    packages=['luciferml', 'luciferml.supervised'],
    version='0.0.5',      
    license='MIT',
    description="Automated ML by d4rk-lucif3r",
    author='Arsh Anwar',                   
    author_email="lucifer78908@gmail.com",    
    url="https://github.com/d4rk-lucif3r/LuciferML",
    keywords=['luciferML', 'AutoML', 'Python'],
    install_requires=[
        "numpy",
        "pandas",
        "scipy",
        "seaborn",
        "matplotlib",
        "scikit-learn",
        "imblearn",
        "xgboost",
        "tensorflow",
    ],
    classifiers=[ 
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
