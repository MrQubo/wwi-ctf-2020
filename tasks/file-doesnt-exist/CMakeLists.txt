cmake_minimum_required(VERSION 3.16)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS_RELEASE "-O2 -Werror -W -Wall -Wextra -pedantic -Wno-catch-value -fanalyzer")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_RELEASE} -g -fsanitize=address -fsanitize=leak -fsanitize=undefined -fstack-protector-strong")

# set the project name
project(main)

# https://fmt.dev/
find_package(fmt)

# add the executable
add_executable(main main.cpp)

target_link_libraries(main fmt::fmt)
