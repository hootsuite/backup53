import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='backup53',
      version='1.0',
      author='Steven Richards',
      author_email='steven.richards@hootsuite.com',
      description='Tool for backing up and restoring Route53 Zones/Records',
      packages=['backup53'],
      scripts=['bin/backup53'],
      install_requires=open('requirements.txt').readlines(),
      classifiers=[
          'Development Status :: 1 - Stable',
          'Environment :: Console',
          'License :: Apache Software License',
          'Topic :: Utilities'
      ]
)