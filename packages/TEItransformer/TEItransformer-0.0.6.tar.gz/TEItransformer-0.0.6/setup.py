from setuptools import setup, find_packages

VERSION = '0.0.6' 
DESCRIPTION = 'TEI XML transformer to HTML, DOCX, JSON. Detailed documentation can be found on the project page on Github: https://github.com/Stoneberry/TEITransformer.'
LONG_DESCRIPTION = 'TEI XML transformer to HTML, DOCX, JSON. The main goal of this package is to develop an algorithm of conversion TEI XML into Edition Formats (HTML, DOCX, JSON). The algorithm consists of two main parts: an algorithm for converting TEI XML to a format (TEITransformer); a front and back application architecture for creating a digital publication and integrating it into an application or website (https://github.com/Stoneberry/tei_platform.git). The client interface is implemented by the TEITransformer class. The user interacts with the algorithm only using this module. When initializing the object, the user must specify the scenario according to which the transformation will take place. The algorithm for enabling visualization uses a set of XSLT stylesheets. XSLT stands for the Extensible Stylesheet Language for Transformations. The main idea is to describe the template of the output document and fill it with the extracted information from XML. The extracting process is conducted by writing rules that specify which element should be converted and under what condition. Detailed documentation can be found on the project page on Github: https://github.com/Stoneberry/TEITransformer.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="TEItransformer", 
        version=VERSION,
        author="Anastasiya Kostyanitsyna, Boris Orekhov",
        author_email="",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
         'beautifulsoup4==4.9.3', 
		 'certifi==2020.12.5', 
		 'chardet==4.0.0', 
		 'cssutils==2.3.0', 
		 'idna==2.10', 
		 'importlib-metadata==4.0.1', 
		 'lxml==4.6.3', 
		 'mypy-extensions==0.4.3', 
		 'python-docx==0.8.11', 
		 'PyYAML==5.4.1', 
		 'qwikidata==0.4.0', 
		 'requests==2.25.1', 
		 'soupsieve==2.2.1', 
		 'typing-extensions==3.10.0.0', 
		 'urllib3==1.26.4', 
		 'zipp==3.4.1'
        ], 
        
        include_package_data=True,
        
        keywords=['python', 'TEI', 'XML'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)