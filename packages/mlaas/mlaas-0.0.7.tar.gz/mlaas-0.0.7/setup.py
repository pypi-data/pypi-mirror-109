from setuptools import setup, find_packages

VERSION = '0.0.7' 
DESCRIPTION = 'ML as a service toolkit'
LONG_DESCRIPTION = 'ML as a service toolkit'

# Setting up
setup(
        name="mlaas", 
        version=VERSION,
        author="dvirginz@gmail.com",
        author_email="<dvirginz@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'ML'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
        ]
)