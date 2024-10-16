from setuptools import setup
import re, sys

def get_version(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/_version.py').read())
    return result.group(1)

minimum_version = (3, 6)
if sys.version_info < minimum_version:
    sys.exit('This package requires at least Python %d.%d' % minimum_version)

setup(
   name='wolfes_cg',
   version=get_version("__version__", "wolfes_cg"),
   description='wolfes code generator',
   author='Elon Musk',
   author_email='ElonMusk@mars.com',
   packages=['wolfes_cg', 'wolfes_cg.be', 'wolfes_cg.fe', 'wolfes_cg.bin', 'wolfes_cg.ir', 'wolfes_cg.utils'],  #same as name
   package_data={
       "wolfes_cg": ['bin/run_wolfes_cg.sh', 'bin/run_wolfes_cg.bat']
   },
   install_requires=['empy>=3.0'], #external packages as dependencies
)