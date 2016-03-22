# -*- coding: utf-8 -*-
"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

import os
from distutils.sysconfig import get_python_inc
#from distutils import setup, find_packages, Extension
from setuptools import setup, Extension
import platform
import sys
import imp

def system(cmd):
	print("Executing: ", cmd)
	ret = os.system(cmd)
	if ret != 0:
		print("error, return code is", ret)
		sys.exit(ret)

path_version_file = "python/vaex/version.py"
if not os.path.exists(path_version_file):
	system("version=`git describe --tags --long`; python/vaex/setversion.py ${version}")

version = imp.load_source('version', path_version_file)
#system("version=`git describe --tags --long`; python/vaex/vaex/setversion.py ${version}")


has_py2app = False
#import vaex
try:
	import py2app.build_app
	has_py2app = True
except:
	pass

if has_py2app:
	import py2app.recipes
	class astropy(object):
		def check(self, cmd, graph):
			return dict(packages=["astropy"])
	py2app.recipes.astropy = astropy()

#full_name = vaex.__full_name__
cmdclass = {}

if has_py2app and sys.argv[1] == "py2app":
	import vaex.ui
	class my_py2app(py2app.build_app.py2app):
		"""hooks in post script to add in missing libraries and zip the content"""
		def run(self):
			py2app.build_app.py2app.run(self)
			#libQtWebKit.4.dylib
			#libQtNetwork.4.dylib
			if 0:
				libs = [line.strip() for line in """
				libLLVM-3.3.dylib
				libQtGui.4.dylib
				libQtCore.4.dylib
				libQtOpenGL.4.dylib
				libcrypto.1.0.0.dylib
				libssl.1.0.0.dylib
				libpng15.15.dylib
				libfreetype.6.dylib
				libjpeg.8.dylib
				libhdf5_hl.9.dylib
				libhdf5.9.dylib
				""".strip().splitlines()]

				libpath = "/Users/maartenbreddels/anaconda/lib"
				targetdir = 'dist/vaex.app/Contents/Resources/lib/'
				for filename in libs:
					path = os.path.join(libpath, filename)
					cmd = "cp %s %s" % (path, targetdir)
					print(cmd)
					os.system(cmd)

				libs = [line.strip() for line in """
				libpng15.15.dylib
				""".strip().splitlines()]
				targetdir = 'dist/vaex.app/Contents/Resources/'
				for filename in libs:
					#path = os.path.join(libpath, filename)
					cmd = "cp %s %s" % (path, targetdir)
					print(cmd)
					os.system(cmd)

			os.system("cp data/helmi-dezeeuw-2000-10p.hdf5 dist/vaex.app/Contents/Resources/")
			os.system("cd dist")
			zipname = "%s.zip" % vaex.__build_name__
			os.system("cd dist;rm %s" % zipname)
			os.system("cd dist;zip -r %s %s.app" % (zipname, vaex.__program_name__))
			retvalue = os.system("git diff --quiet")
			if retvalue != 0:
				print("WARNING UNCOMMITED CHANGES, VERSION NUMBER WILL NOT MATCH")
	cmdclass['py2app'] = my_py2app
			
#from distutils.core import setup, Extension
try:
	import numpy
	numdir = os.path.dirname(numpy.__file__)
except:
	numdir = None

if numdir is None:
	print("numpy not found, cannot install")
import sys 
import glob
sys.setrecursionlimit(10000)

APP = ["vaex_app.py"]
DATA_FILES = []
if has_py2app:
	pass
	#DATA_FILES.append(["data", ["data/disk-galaxy.hdf5"]]) #, "data/Aq-A-2-999-shuffled-1percent.hdf5"]])
	DATA_FILES.append(["data/", glob.glob("data/dist/*")] )


#print glob.glob("doc/*")
if 0:
	DATA_FILES.append(["doc/", glob.glob("docs/build/html/*.html") + glob.glob("docs/build/html/*.js")] )
	for sub in "_static _images _sources".split():
		DATA_FILES.append(["doc/" + sub, glob.glob("docs/build/html/" +sub +"/*")] )
#print DATA_FILES
OPTIONS = {'argv_emulation': False, 'excludes':[], 'resources':['python/vaex/ui/icons'],
           'matplotlib_backends':'-',
           'no_chdir':True,
		   'includes': ['h5py',
                 'h5py.defs',
                 'h5py.h5ac',
                 'h5py._errors',
                 'h5py._objects',
                 'h5py.defs',
                 'h5py.utils',
                 'h5py._proxy',
				 'six',
				 'aplus',
				 "astropy.extern.bundled",
				 ],
		   "packages": ["pygments"],
           'iconfile': 'python/vaex/ui/icons/vaex.icns'

} #, 'debug_modulegraph':True}
#, 'app':True


include_dirs = []
library_dirs = []
libraries = []
defines = []
if "darwin" in platform.system().lower():
	extra_compile_args = ["-mfpmath=sse", "-O3", "-funroll-loops"]
else:
	#extra_compile_args = ["-mfpmath=sse", "-msse4", "-Ofast", "-flto", "-march=native", "-funroll-loops"]
	extra_compile_args = ["-mfpmath=sse", "-msse4", "-Ofast", "-flto", "-funroll-loops"]
	#extra_compile_args = ["-mfpmath=sse", "-O3", "-funroll-loops"]
	extra_compile_args = ["-mfpmath=sse", "-msse4a", "-O3", "-funroll-loops"]
extra_compile_args.extend(["-std=c++0x"])

include_dirs.append(os.path.join(get_python_inc(plat_specific=1), "numpy"))
if numdir is not None:
	include_dirs.append(os.path.join(numdir, "core", "include"))

extensions = [
	Extension("vaex.vaexfast", ["src/vaex/vaexfast.cpp"],
                include_dirs=include_dirs,
                library_dirs=library_dirs,
                libraries=libraries,
                define_macros=defines,
                extra_compile_args=extra_compile_args
                )
] if numdir is not None else []

from pip.req import parse_requirements
import pip.download

session=pip.download.PipSession()
# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=session)

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]



#print "requirements", reqs
#print "ver#sion", vaex.__release__
setup(
	app=["bin/vaex"],
	name="vaex", #vaex.__program_name__,
	author="Maarten A. Breddels",
	author_email="maartenbreddels@gmail.com",
    version = "%d.%d.%d" % version.versiontuple,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    #setup_requires=['py2app'],
    #setup_requires=["sphinx"],
    includes=["vaex", "md5", "astropy", "aplus", "six", "pygments"],
    packages=["vaex", "vaex.ui", "vaex.misc", "vaex.notebook", "vaex.file", "vaex.ui.plugin", "vaex.ui.icons"],
    #install_requires=reqs,
    entry_points={ 'console_scripts': [ 'vaex=vaex.ui.main:main']  },
    ext_modules=extensions,
    package_data={'vaex': ['ui/icons/*.png']},
    package_dir={'vaex':'python/vaex'},
    cmdclass=cmdclass,
    description="Veax is a graphical tool to visualize and explore large tabular datasets.",
    url="https://www.astro.rug.nl/~breddels/vaex"
)
