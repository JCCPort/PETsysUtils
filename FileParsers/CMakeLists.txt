project(PETsysParsers)
cmake_minimum_required(VERSION 3.20)

set (CMAKE_CXX_STANDARD 17)

if (CMAKE_BUILD_TYPE STREQUAL "Debug")
    set(CMAKE_C_FLAGS "-O0 -pthread -DISDEBUG")
    set(CMAKE_CXX_FLAGS "-O0 -pthread -DISDEBUG")
    set(ISDEBUG)
elseif (CMAKE_BUILD_TYPE STREQUAL "Release")
    set(CMAKE_C_FLAGS "-O3 -pthread -flto")
    set(CMAKE_CXX_FLAGS "-O3 -pthread -flto")
    #    set(ISDEBUG 0)
elseif (CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo")
    set(CMAKE_C_FLAGS "-O2 -pthread -fprofile-arcs -DISDEBUG")
    set(CMAKE_CXX_FLAGS "-O2 -pthread -fprofile-arcs -DISDEBUG")
    set(ISDEBUG)
endif ()

file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cpp)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh, ${PROJECT_SOURCE_DIR}/include/*.h, ${PROJECT_SOURCE_DIR}/include/*.icc)

message("${sources}")
message("${PROJECT_SOURCE_DIR}")


###########################

add_executable(sort SortBinaries.cpp ${sources} ${headers})

add_executable(CoincidenceProcess CoincidenceProcess.cpp ${sources} ${headers})