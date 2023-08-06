from setuptools import setup, find_packages

VERSION = '0.0.11' 
DESCRIPTION = 'ML as a service toolkit'
LONG_DESCRIPTION = 'ML as a service toolkit'

install_requires = [
    'requests',
]
# Setting up
setup(
        name="mlaas", 
        version=VERSION,
        author="dvirginz@gmail.com",
        author_email="<dvirginz@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        keywords=['python', 'ML'],
        install_requires=install_requires,
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
        ]
)