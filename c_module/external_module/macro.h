#ifndef MACRO_H
#define MACRO_H
#include "tusb.h"

uint8_t const * tud_hid_descriptor_report_cb(uint8_t instance);

void tud_hid_set_report_cb(uint8_t instance, uint8_t report_id, hid_report_type_t report_type, uint8_t const* buffer, uint16_t bufsize);

#endif