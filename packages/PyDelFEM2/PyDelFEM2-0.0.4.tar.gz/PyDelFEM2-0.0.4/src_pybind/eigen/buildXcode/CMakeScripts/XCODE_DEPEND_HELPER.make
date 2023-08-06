# DO NOT EDIT
# This makefile makes sure all linkable targets are
# up-to-date with anything they link to
default:
	echo "Do not invoke directly"

# Rules to remove targets that are older than anything to which they
# link.  This forces Xcode to relink the targets from scratch.  It
# does not seem to check these dependencies itself.
PostBuild.c_eigen.Debug:
/Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/eigen/buildXcode/Debug/c_eigen.cpython-37m-darwin.so:\
	/usr/local/lib/libGLEW.dylib
	/bin/rm -f /Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/eigen/buildXcode/Debug/c_eigen.cpython-37m-darwin.so


PostBuild.c_eigen.Release:
/Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/eigen/buildXcode/Release/c_eigen.cpython-37m-darwin.so:\
	/usr/local/lib/libGLEW.dylib
	/bin/rm -f /Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/eigen/buildXcode/Release/c_eigen.cpython-37m-darwin.so


PostBuild.c_eigen.MinSizeRel:
/Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/eigen/buildXcode/MinSizeRel/c_eigen.cpython-37m-darwin.so:\
	/usr/local/lib/libGLEW.dylib
	/bin/rm -f /Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/eigen/buildXcode/MinSizeRel/c_eigen.cpython-37m-darwin.so


PostBuild.c_eigen.RelWithDebInfo:
/Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/eigen/buildXcode/RelWithDebInfo/c_eigen.cpython-37m-darwin.so:\
	/usr/local/lib/libGLEW.dylib
	/bin/rm -f /Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/eigen/buildXcode/RelWithDebInfo/c_eigen.cpython-37m-darwin.so




# For each target create a dummy ruleso the target does not have to exist
/usr/local/lib/libGLEW.dylib:
