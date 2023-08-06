# DO NOT EDIT
# This makefile makes sure all linkable targets are
# up-to-date with anything they link to
default:
	echo "Do not invoke directly"

# Rules to remove targets that are older than anything to which they
# link.  This forces Xcode to relink the targets from scratch.  It
# does not seem to check these dependencies itself.
PostBuild.c_core.Debug:
/Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/core/buildXcode/Debug/c_core.cpython-37m-darwin.so:
	/bin/rm -f /Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/core/buildXcode/Debug/c_core.cpython-37m-darwin.so


PostBuild.c_core.Release:
/Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/core/buildXcode/Release/c_core.cpython-37m-darwin.so:
	/bin/rm -f /Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/core/buildXcode/Release/c_core.cpython-37m-darwin.so


PostBuild.c_core.MinSizeRel:
/Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/core/buildXcode/MinSizeRel/c_core.cpython-37m-darwin.so:
	/bin/rm -f /Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/core/buildXcode/MinSizeRel/c_core.cpython-37m-darwin.so


PostBuild.c_core.RelWithDebInfo:
/Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/core/buildXcode/RelWithDebInfo/c_core.cpython-37m-darwin.so:
	/bin/rm -f /Users/nobuyuki/projects/Aerodynamics3D/delfem2/src_pybind/core/buildXcode/RelWithDebInfo/c_core.cpython-37m-darwin.so




# For each target create a dummy ruleso the target does not have to exist
