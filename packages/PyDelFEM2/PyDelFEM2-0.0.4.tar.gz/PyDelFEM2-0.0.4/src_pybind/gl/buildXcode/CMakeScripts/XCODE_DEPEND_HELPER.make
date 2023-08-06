# DO NOT EDIT
# This makefile makes sure all linkable targets are
# up-to-date with anything they link to
default:
	echo "Do not invoke directly"

# Rules to remove targets that are older than anything to which they
# link.  This forces Xcode to relink the targets from scratch.  It
# does not seem to check these dependencies itself.
PostBuild.c_gl.Debug:
/Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/gl/buildXcode/Debug/c_gl.cpython-37m-darwin.so:\
	/usr/local/lib/libGLEW.dylib
	/bin/rm -f /Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/gl/buildXcode/Debug/c_gl.cpython-37m-darwin.so


PostBuild.c_gl.Release:
/Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/gl/buildXcode/Release/c_gl.cpython-37m-darwin.so:\
	/usr/local/lib/libGLEW.dylib
	/bin/rm -f /Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/gl/buildXcode/Release/c_gl.cpython-37m-darwin.so


PostBuild.c_gl.MinSizeRel:
/Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/gl/buildXcode/MinSizeRel/c_gl.cpython-37m-darwin.so:\
	/usr/local/lib/libGLEW.dylib
	/bin/rm -f /Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/gl/buildXcode/MinSizeRel/c_gl.cpython-37m-darwin.so


PostBuild.c_gl.RelWithDebInfo:
/Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/gl/buildXcode/RelWithDebInfo/c_gl.cpython-37m-darwin.so:\
	/usr/local/lib/libGLEW.dylib
	/bin/rm -f /Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/gl/buildXcode/RelWithDebInfo/c_gl.cpython-37m-darwin.so




# For each target create a dummy ruleso the target does not have to exist
/usr/local/lib/libGLEW.dylib:
