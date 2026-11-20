# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.2.0)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.2.0-a4)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
set(PICO_BOARD pico2_w CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(JeinMeteoClientV2 C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1

add_executable(JeinMeteoClientV2 JeinMeteoClientV2.c mqttClient.c bme280.c user.c init_sensor.c cJson.c)

add_compile_definitions(SPI_PORT=spi1)
add_compile_definitions(SPI_RX=12)
add_compile_definitions(SPI_CS=13)
add_compile_definitions(SPI_SCK=14)
add_compile_definitions(SPI_TX=15)
add_compile_definitions(ALTITUDE_AT_LOC=520)
add_compile_definitions(BME280_32BIT_ENABLE)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
  set(CMAKE_VERBOSE_MAKEFILE 1)
  add_compile_definitions(DEBUG)
  add_compile_definitions(UPDATE_INTERVAL=10)
else()
  add_compile_definitions(UPDATE_INTERVAL=60)
endif()

pico_set_program_name(JeinMeteoClientV2 "JeinMeteoClientV2")
pico_set_program_version(JeinMeteoClientV2 "0.1")

# Modify the below lines to enable/disable output over UART/USB
pico_enable_stdio_usb(JeinMeteoClientV2 1)
pico_enable_stdio_uart(JeinMeteoClientV2 0)


# Add the standard library to the build
target_link_libraries(JeinMeteoClientV2
        pico_stdlib)

# Add the standard include files to the build
target_include_directories(JeinMeteoClientV2 PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}
)

# Add any user requested libraries
target_link_libraries(JeinMeteoClientV2
        hardware_spi
        hardware_adc
        pico_lwip_mqtt
        pico_cyw43_arch_lwip_threadsafe_background
        pico_unique_id
        )



# target_link_libraries(JeinMeteoClientV2 pico_stdlib)

pico_add_extra_outputs(JeinMeteoClientV2)

