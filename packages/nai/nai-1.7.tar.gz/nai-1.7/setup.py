from distutils.core import setup
setup(
name='nai',
version='1.7',
author='Nasir Ali',
author_email='nasiralis1731@gmail.com',
author_url='https://facebook.com/nasir.xo',
packages=['nai'],
scripts=['bin/phone'],
install_requires=['bs4','requests', ],
)
