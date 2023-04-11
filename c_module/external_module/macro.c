// Include MicroPython API.
#include "py/runtime.h"

#include "tusb.h"

#if CFG_TUD_HID != 1
#warning "CFG_TUD_HID not set to 1!"
#endif

#if CFG_TUD_ENABLED != 1
#warning "CFG_TUD_ENABLED not set to 1!"
#endif

bool hid_task(void);

// This is the function which will be called from Python as cexample.add_ints(a, b).
STATIC mp_obj_t example_add_ints(mp_obj_t a_obj, mp_obj_t b_obj) {
    // Extract the ints from the micropython input objects.
    int a = mp_obj_get_int(a_obj);
    int b = mp_obj_get_int(b_obj);

    // Calculate the addition and convert to MicroPython object.
    return mp_obj_new_int(a + b);
}
// Define a Python reference to the function above.
STATIC MP_DEFINE_CONST_FUN_OBJ_2(example_add_ints_obj, example_add_ints);

// This is the function which will be called from Python as cexample.add_ints(a, b).
STATIC mp_obj_t init_usb(void) {

    tud_init(0);
    tud_task();
    
    return mp_const_none;
}

// Define a Python reference to the function above.
STATIC MP_DEFINE_CONST_FUN_OBJ_0(init_usb_obj, init_usb);

STATIC mp_obj_t key_press(void){
    tud_task();

    if (hid_task()) return mp_const_true;
    
    return mp_const_false;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(key_press_obj, key_press);

// Define all properties of the module.
// Table entries are key/value pairs of the attribute name (a string)
// and the MicroPython object reference.
// All identifiers and strings are written as MP_QSTR_xxx and will be
// optimized to word-sized integers by the build system (interned strings).
STATIC const mp_rom_map_elem_t macro_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_cexample) },
    { MP_ROM_QSTR(MP_QSTR_add_ints), MP_ROM_PTR(&example_add_ints_obj) },
    { MP_ROM_QSTR(MP_QSTR_init_usb), MP_ROM_PTR(&init_usb_obj) },
    { MP_ROM_QSTR(MP_QSTR_key_press), MP_ROM_PTR(&key_press_obj) }
};
STATIC MP_DEFINE_CONST_DICT(macro_module_globals, macro_module_globals_table);

// Define module object.
const mp_obj_module_t macro_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&macro_module_globals,
};

// Register the module to make it available in Python.
MP_REGISTER_MODULE(MP_QSTR_macro, macro_user_cmodule);


// Interface index depends on the order in configuration descriptor
enum {
  ITF_KEYBOARD = 2,
  ITF_MOUSE = 3
};

//--------------------------------------------------------------------+
// Device callbacks
//--------------------------------------------------------------------+

// Invoked when device is mounted
void tud_mount_cb(void)
{
  //blink_interval_ms = BLINK_MOUNTED;
}

// Invoked when device is unmounted
void tud_umount_cb(void)
{
  //blink_interval_ms = BLINK_NOT_MOUNTED;
}

// Invoked when usb bus is suspended
// remote_wakeup_en : if host allow us  to perform remote wakeup
// Within 7ms, device must draw an average of current less than 2.5 mA from bus
void tud_suspend_cb(bool remote_wakeup_en)
{
  (void) remote_wakeup_en;
  //blink_interval_ms = BLINK_SUSPENDED;
}

// Invoked when usb bus is resumed
void tud_resume_cb(void)
{
  //blink_interval_ms = BLINK_MOUNTED;
}

//--------------------------------------------------------------------+
// USB HID
//--------------------------------------------------------------------+

bool hid_task(void){

  /*------------- Keyboard -------------*/
  //return tud_hid_n_ready(ITF_KEYBOARD); // TODO: Never ready. Maybe because of screen?
  if ( true )
  {
    // use to avoid send multiple consecutive zero report for keyboard
    static bool has_key = false;

    if ( true )
    {
      uint8_t keycode[6] = { 0 };
      keycode[0] = HID_KEY_A;

      tud_hid_n_keyboard_report(ITF_KEYBOARD, 0, 0, keycode);

      return true;
    }else
    {
      // send empty key report if previously has key pressed
      if (has_key) tud_hid_n_keyboard_report(ITF_KEYBOARD, 0, 0, NULL);
      has_key = false;
    }
  }
  return false;
}


// Invoked when received GET_REPORT control request
// Application must fill buffer report's content and return its length.
// Return zero will cause the stack to STALL request
uint16_t tud_hid_get_report_cb(uint8_t itf, uint8_t report_id, hid_report_type_t report_type, uint8_t* buffer, uint16_t reqlen)
{
  // TODO not Implemented
  (void) itf;
  (void) report_id;
  (void) report_type;
  (void) buffer;
  (void) reqlen;

  return 0;
}

// Invoked when received SET_REPORT control request or
// received data on OUT endpoint ( Report ID = 0, Type = 0 )
void tud_hid_set_report_cb(uint8_t itf, uint8_t report_id, hid_report_type_t report_type, uint8_t const* buffer, uint16_t bufsize)
{
  // TODO set LED based on CAPLOCK, NUMLOCK etc...
  (void) itf;
  (void) report_id;
  (void) report_type;
  (void) buffer;
  (void) bufsize;
}