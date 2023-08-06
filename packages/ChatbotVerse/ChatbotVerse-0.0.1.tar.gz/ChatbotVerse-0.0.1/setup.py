from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A very simple package for creating amazing neural-network-based chatbots without any hassle.'

# Setting up
setup(
    name="ChatbotVerse",
    version=VERSION,
    author="FORTFANOP (Joel John Mathew)",
    author_email="<thetechnologicalelectronicguy@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'nltk', 'tensorflow'],
    keywords=['python', 'neural networks', 'machine learning', 'chatbots', 'chat', 'artificial intelligence', 'virtual assistant'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)