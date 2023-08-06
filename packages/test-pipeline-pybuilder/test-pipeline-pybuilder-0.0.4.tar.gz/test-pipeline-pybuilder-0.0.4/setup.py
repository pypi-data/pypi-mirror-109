# coding: utf-8
from distutils.core import setup

setup(name='test-pipeline-pybuilder',
      version='0.0.4',
      packages=['pipeline'],
      # py_modules='main',
      author='Shaoyu Yang',
      author_email='s.yang@pipelinesecurity.net',
      url='https://github.com/pipelinelabo/pybuilder-investigation',
      description='This is just a test for uploading',
      entry_points={
              'console_scripts': [
                  'yang=pipeline:yang',
                  'pipeline=pipeline:pipeline'
              ]
          }
      )