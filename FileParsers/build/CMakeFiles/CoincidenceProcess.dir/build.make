# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.20

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/petsys/PETsysUtils/FileParsers

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/petsys/PETsysUtils/FileParsers/build

# Include any dependencies generated for this target.
include CMakeFiles/CoincidenceProcess.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/CoincidenceProcess.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/CoincidenceProcess.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/CoincidenceProcess.dir/flags.make

CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.o: CMakeFiles/CoincidenceProcess.dir/flags.make
CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.o: ../CoincidenceProcess.cpp
CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.o: CMakeFiles/CoincidenceProcess.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/petsys/PETsysUtils/FileParsers/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.o -MF CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.o.d -o CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.o -c /home/petsys/PETsysUtils/FileParsers/CoincidenceProcess.cpp

CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/petsys/PETsysUtils/FileParsers/CoincidenceProcess.cpp > CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.i

CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/petsys/PETsysUtils/FileParsers/CoincidenceProcess.cpp -o CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.s

# Object files for target CoincidenceProcess
CoincidenceProcess_OBJECTS = \
"CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.o"

# External object files for target CoincidenceProcess
CoincidenceProcess_EXTERNAL_OBJECTS =

CoincidenceProcess: CMakeFiles/CoincidenceProcess.dir/CoincidenceProcess.cpp.o
CoincidenceProcess: CMakeFiles/CoincidenceProcess.dir/build.make
CoincidenceProcess: CMakeFiles/CoincidenceProcess.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/petsys/PETsysUtils/FileParsers/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable CoincidenceProcess"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/CoincidenceProcess.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/CoincidenceProcess.dir/build: CoincidenceProcess
.PHONY : CMakeFiles/CoincidenceProcess.dir/build

CMakeFiles/CoincidenceProcess.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/CoincidenceProcess.dir/cmake_clean.cmake
.PHONY : CMakeFiles/CoincidenceProcess.dir/clean

CMakeFiles/CoincidenceProcess.dir/depend:
	cd /home/petsys/PETsysUtils/FileParsers/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/petsys/PETsysUtils/FileParsers /home/petsys/PETsysUtils/FileParsers /home/petsys/PETsysUtils/FileParsers/build /home/petsys/PETsysUtils/FileParsers/build /home/petsys/PETsysUtils/FileParsers/build/CMakeFiles/CoincidenceProcess.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/CoincidenceProcess.dir/depend
