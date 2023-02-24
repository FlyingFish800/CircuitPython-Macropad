cmake_minimum_required(VERSION 3.13)

# Init pico sdk
include(../../../../pico_c/pico-sdk/pico_sdk_init.cmake)

project(usb_lib)

pico_sdk_init()

add_executable(usb_lib usb_lib.c)

#target_include_directories(usb_lib PUBLIC ${CMAKE_CURRENT_LIST_DIR})

target_link_libraries(usb_lib pico_stdlib)# tinyusb_device tinyusb_board)

# Disable
pico_enable_stdio_usb(usb_lib 1)
pico_enable_stdio_uart(usb_lib 0)

# Disable
pico_add_extra_outputs(usb_lib)