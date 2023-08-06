# coding:utf-8

from setuptools import setup
# or
# from distutils.core import setup  
foruser = '''# Author:KuoYuan Li </br> pyCamRecord.record(maxDuration=0.1)'''
setup(
        name='pyCamRecord',   
        version='1.0.1',   
        description='Record by Webcam and save automatically while there is different in screen',
        long_description=foruser,
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://pypi.org/project/pyCamRecord',      
        packages=['pyCamRecord'],   
        include_package_data=True,
        keywords = ['record webcam', 'record webcam by difference','cam recording'],   # Keywords that define your package best
        install_requires=['opencv-contrib-python'],
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
      ],
)
