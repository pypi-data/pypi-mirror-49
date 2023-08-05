cmake_minimum_required(VERSION 2.8.12)
project(rapidrand)

add_subdirectory(lib/pybind11)
pybind11_add_module(rapidrand src/main.cpp src/genstr.cpp)

add_executable(test src/test.cpp src/genstr.cpp)