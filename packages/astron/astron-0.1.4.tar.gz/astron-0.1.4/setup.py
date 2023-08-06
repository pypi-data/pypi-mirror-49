import os,sys
from setuptools import setup

# For regular package imports, not 'import .packagename'
# modpath = os.path.abspath(os.path.split(sys.argv[0])[0]) + '/astron'
# sys.path.append(modpath)
# import astron

setup(name='astron',
      version='0.1.4',
      description='...',
      url='https://www.python.org/sigs/distutils-sig/',
      author='Addy Bhatia',
      author_email='jude.addy999@gmail.com',
      license='MIT',
      install_requires=['autopep8', 'pygame', 'numpy'],
      packages=['astron'], 
      include_package_data=True,
      zip_safe=True)
