from setuptools import setup, find_packages




def readme():
    with open('README.md', encoding='utf-8') as f:
        README = f.read()
    return README


VERSION = '0.0.2'
DESCRIPTION = 'Python tools to control android'
LONG_DESCRIPTION = readme() #'Python tools to control android by python'

# Setting up
setup(
    name="pykivdroid",
    version=VERSION,
    author="SK SAHIL",
    #author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['kivy','pyjnius','android'],
    keywords=['python', 'kivy', 'android', 'pyjnius'],
    url='https://github.com/Sahil-pixel/Pykivdroid',
    license="MIT",
    classifiers=[]
) 
