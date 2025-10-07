cmake_minimum_required(VERSION 3.16)
include(FetchContent)

# Find required packages
find_package(CycloneDDS QUIET)
find_package(OpenCV QUIET)
find_package(Threads REQUIRED)
FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.12.0/json.tar.xz)
FetchContent_MakeAvailable(json)


if(NOT OpenCV_FOUND)
    message(WARNING "OpenCV not found - some features may be limited")
    set(OpenCV_LIBS "")
endif()

if(NOT CycloneDDS_FOUND)
    message(WARNING "CycloneDDS not found - using stub implementation")
    set(CycloneDDS_LIBRARIES "")
    set(CycloneDDS_INCLUDE_DIRS "")
endif()


# Orchestrator executable
set(ORCHESTRATOR_SOURCES

    src/orchestrator.cpp
    src/module_manager.cpp
    src/config_manager.cpp
    src/logger.cpp
)

set(ORCHESTRATOR_HEADERS
    include/orchestrator.hpp
    include/module_manager.hpp
    include/config_manager.hpp
    include/logger.hpp
)
add_library(dashcam_orchestrator_lib STATIC
    ${ORCHESTRATOR_SOURCES}
    ${ORCHESTRATOR_HEADERS}
)
target_include_directories(dashcam_orchestrator_lib PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)
target_link_libraries(dashcam_orchestrator_lib PRIVATE
    ${CycloneDDS_LIBRARIES}
    ${OpenCV_LIBS}
    nlohmann_json::nlohmann_json
    Threads::Threads)


add_executable(dashcam_orchestrator_test src/test.cpp)

target_include_directories(dashcam_orchestrator_test PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CycloneDDS_INCLUDE_DIRS}
    ${OpenCV_INCLUDE_DIRS}
    ${CMAKE_CURRENT_BINARY_DIR}/../dds/generated
)

target_link_libraries(dashcam_orchestrator_test PRIVATE dashcam_orchestrator_lib)

# Install rules
install(TARGETS dashcam_orchestrator_test
    RUNTIME DESTINATION bin
)

# Copy configuration files
install(FILES
    config/default_config.json
    config/example_pipeline.json
    DESTINATION etc/dashcam
)