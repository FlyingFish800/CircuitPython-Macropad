add_library(usbmod INTERFACE)

target_sources(usbmod INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/macro.c
    ${CMAKE_CURRENT_LIST_DIR}/usb_descriptors.c
)

target_include_directories(usbmod INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/../../../../micropy/micropython/lib/tinyusb/src
)

target_link_libraries(usermod INTERFACE usbmod)