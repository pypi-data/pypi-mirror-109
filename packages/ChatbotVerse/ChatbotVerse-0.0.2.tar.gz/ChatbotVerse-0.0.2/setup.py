from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A very simple package for creating amazing neural-network-based chatbots without any hassle.'
LONG_DESCRIPTION = 'Create amazing chat bots with just an intents.json file. Check out Github for examples -- Github: https://github.com/FORTFANOP/ChatbotVerse'

setup(name='ChatbotVerse',
      version='0.0.2',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author='FORTFANOP (Joel John Mathew)',
      author_email='<thetechnologicalelectronicguy@gmail.com>',
      packages=find_packages(),
      install_requires=['numpy', 'nltk', 'tensorflow'],
      keywords=['python', 'neural networks', 'machine learning', 'chatbots', 'chat', 'artificial intelligence',
                'virtual assistant', 'ChatbotVerse'],
      classifiers=[
          "Development Status :: 1 - Planning",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 3",
          "Operating System :: Unix",
          "Operating System :: Microsoft :: Windows",
      ]
      )
