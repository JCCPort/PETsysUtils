project(PETsysParsers)
cmake_minimum_required(VERSION 3.20)

set (CMAKE_CXX_STANDARD 20)


if (CMAKE_BUILD_TYPE STREQUAL "Debug")
    set(CMAKE_C_FLAGS "-O0 -pthread -DISDEBUG -Wall -Wextra -pedantic")
    set(CMAKE_CXX_FLAGS "-O0 -pthread -DISDEBUG -Wall -Wextra -pedantic")
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



EXECUTE_PROCESS(COMMAND uname -m COMMAND tr -d '\n' OUTPUT_VARIABLE ARCHITECTURE)
if (CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
else ()
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -march=native")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif ()

set(MAKE_PROFILE FALSE)
set(USE_PROFILE FALSE)

if (MAKE_PROFILE)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fprofile-generate -fprofile-dir=.")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-generate -fprofile-dir=.")
endif ()

if (USE_PROFILE)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fprofile-use -fprofile-dir=.")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-use -fprofile-dir=.")
endif ()



find_package(Boost COMPONENTS serialization REQUIRED)

#set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -lboost_serialization --verbose")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -lboost_serialization --verbose")


file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cpp)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh, ${PROJECT_SOURCE_DIR}/include/*.h, ${PROJECT_SOURCE_DIR}/include/*.icc)

message("${sources}")
message("${PROJECT_SOURCE_DIR}")


###########################

include_directories(${Boost_INCLUDE_DIRS})


add_executable(sort SortBinaries.cpp ${sources} ${headers})
add_executable(CoincidenceProcess CoincidenceProcess.cpp ${sources} ${headers})
add_executable(MultithreadSort include/MultithreadSort.h)
set_target_properties(MultithreadSort PROPERTIES LINKER_LANGUAGE CXX)

target_link_libraries(sort ${Boost_LIBRARIES})
target_link_libraries(sort boost_serialization)

target_link_libraries(CoincidenceProcess ${Boost_LIBRARIES})
target_link_libraries(CoincidenceProcess boost_serialization)