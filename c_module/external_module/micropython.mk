USB_MOD_DIR := $(USERMOD_DIR)

# Add all C files to SRC_USERMOD.
SRC_USERMOD += $(USB_MOD_DIR)/macro.c
SRC_USERMOD += $(USB_MOD_DIR)/usb_descriptors.c

# We can add our module folder to include paths if needed
# This is not actually needed in this example.
CFLAGS_USERMOD += -I$(USB_MOD_DIR)/../../../../micropy/micropython/lib/tinyusb/src