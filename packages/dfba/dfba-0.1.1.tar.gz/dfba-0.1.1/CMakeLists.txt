cmake_minimum_required(VERSION 2.8.3)

project(dynamic-fba)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "-Wno-deprecated-register" )

################### Find python packages

FIND_PACKAGE(PythonInterp 3)

if (PYTHONINTERP_FOUND)
  if (UNIX AND NOT APPLE)
    if (PYTHON_VERSION_MAJOR EQUAL 3)
        FIND_PACKAGE(Boost COMPONENTS python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} REQUIRED)
        FIND_PACKAGE(PythonInterp 3)
        FIND_PACKAGE(PythonLibs 3)
    else()
	message("Python3 not found")
    endif()
  else()
    if (PYTHON_VERSION_MAJOR EQUAL 3)
        FIND_PACKAGE(Boost COMPONENTS python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} REQUIRED)
        FIND_PACKAGE(PythonInterp 3)
        FIND_PACKAGE(PythonLibs 3)
    else()
	message("Python3 not found")
    endif()
  endif()
else()
    message("Python not found")
endif()


message(STATUS "PYTHON_LIBRARIES = ${PYTHON_LIBRARIES}")
message(STATUS "PYTHON_EXECUTABLE = ${PYTHON_EXECUTABLE}")
message(STATUS "PYTHON_INCLUDE_DIRS = ${PYTHON_INCLUDE_DIRS}")
message(STATUS "Boost_LIBRARIES = ${Boost_LIBRARIES}")

################### Set path for custom FindModules

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

################### Find glpk packages

FIND_PACKAGE(GLPK REQUIRED)
message(STATUS "GLPK_LIBRARIES = ${GLPK_LIBRARIES}")
message(STATUS "GLPK_INCLUDE_DIRS = ${GLPK_INCLUDE_DIRS}")

################### Find sundials packages

FIND_PACKAGE(SUNDIALS REQUIRED)
message(STATUS "SUNDIALS_LIBRARIES = ${SUNDIALS_LIBRARIES}")
message(STATUS "SUNDIALS_INCLUDE_DIR = ${SUNDIALS_INCLUDE_DIR}")

################### Include directories and libraries

#ENABLE_TESTING()
INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS} ${GLPK_INCLUDE_DIRS} ${SUNDIALS_INCLUDE_DIR})
LINK_LIBRARIES(${Boost_LIBRARIES} ${PYTHON_LIBRARIES} ${GLPK_LIBRARIES} ${SUNDIALS_LIBRARIES})

################### Source files

set(SRC ./src/extension/)
AUX_SOURCE_DIRECTORY(${SRC}/emblp/ EMBLP_FILES)
AUX_SOURCE_DIRECTORY(${SRC}/methods/ METHOD_FILES)
set(MODULE_FILES ${SRC}dfba_utils.cpp ${EMBLP_FILES} ${METHOD_FILES})

################### Build module

PYTHON_ADD_MODULE(dfba_utils ${MODULE_FILES})
