## X3D Python Package x3d

Loren Peitso, John Carlson, Masaki Aono, Don Brutzman

This placeholder project is in anticipation of broadly deploying the development version of the Python language x3d package via PyPI.

Autogenerating x3d package from X3DUOM via stylesheet, in x3d stylesheets subdirectory 'python' at same level as subdirectory 'java' for X3DJSAIL.

http://www.web3d.org/x3d/stylesheets/build.xml
Ant build targets
* BuildX3dPythonPackageFromX3duom.saxon
* test.X3dToPython.xslt.one

using stylesheet
http://www.web3d.org/x3d/stylesheets/X3duomToX3dPythonPackage.xslt

producing
http://www.web3d.org/x3d/stylesheets/python/x3d.py

version control:

https://sourceforge.net/p/x3d/code/HEAD/tree/www.web3d.org/x3d/stylesheets/
https://sourceforge.net/p/x3d/code/HEAD/tree/www.web3d.org/x3d/stylesheets/build.xml
https://sourceforge.net/p/x3d/code/HEAD/tree/www.web3d.org/x3d/stylesheets/X3duomToX3dPythonPackage.xslt

https://sourceforge.net/p/x3d/code/HEAD/tree/www.web3d.org/x3d/stylesheets/python/x3d.py

----

These XSLT Stylesheets convert XML-based .x3d scenes into python source,
and a decorated X3D XML Schema into X3D Unified Object Model (X3DUOM).
They are maintained under an open-source license and online at
   http://www.web3d.org/x3d/stylesheets/python

with version control maintained at
   http://svn.code.sf.net/p/x3d/code/www.web3d.org/x3d/stylesheets/python

X3D stylesheet descriptions are included in the X3D Resources, online at
   http://www.web3d.org/x3d/content/examples/X3dResources.html#Stylesheets

Point of contact:   Don Brutzman  brutzman@nps.edu
