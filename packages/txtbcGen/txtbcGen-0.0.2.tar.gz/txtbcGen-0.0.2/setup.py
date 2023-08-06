from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'The first upload of the txtbcGen package'
LONG_DESCRIPTION = 'The first upload of the txtbcGen package which generates .txtbc files to feed into MATLAB IQM ODE modelling'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="txtbcGen", 
        version=VERSION,
        author="Yunduo Lan",
        author_email="l810577993@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'txtbc'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)