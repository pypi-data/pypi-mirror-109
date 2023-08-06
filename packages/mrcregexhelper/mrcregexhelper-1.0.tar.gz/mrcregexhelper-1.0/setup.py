from setuptools import setup

setup(name='mrcregexhelper',
      version='1.0',
      description='Regex utility',
      long_description='Regex utility for OCR based extraction',
      url='',
      author='Mr. Cooper',
      author_email='varshitha.dasari@mrcooper.com',
      license='MIT',
      packages=['mrcregexhelper'],
      install_requires=[
          'pandas','requests','numpy','python-Levenshtein','fuzzywuzzy'
      ],
      zip_safe=False)