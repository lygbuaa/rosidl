from setuptools import setup
import re

def get_version(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/_version.py').read())
    return result.group(1)

setup(
   name='wolfes_cg',
   version=get_version("__version__", "wolfes_cg"),
   description='wolfes code generator',
   author='Elon Musk',
   author_email='ElonMusk@mars.com',
   packages=['wolfes_cg'],  #same as name
   install_requires=['empy>=3.0'], #external packages as dependencies
)