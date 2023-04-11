#include "py/dynruntime.h"
#include "tusb.c"
#include "device/usbd.c"
#include "tusb.h"

STATIC mp_int_t factorial_recursive(mp_int_t x){
	if (x==0){
		return 1;
	}
	return x * factorial_recursive(x-1);
}

// Initialize USB hardware
STATIC mp_obj_t usb_init(void){
	// Init tinyusb
	return mp_const_none;
}

STATIC MP_DEFINE_CONST_FUN_OBJ_0(usb_init_obj, usb_init);

// Called from python 
STATIC mp_obj_t factorial(mp_obj_t x_obj){
	// Extract int, run through C code, and return python int obj
	mp_int_t x = mp_obj_get_int(x_obj);
	mp_int_t result = factorial_recursive(x);
	return mp_obj_new_int(result);
}

// Define python reference to above function
STATIC MP_DEFINE_CONST_FUN_OBJ_1(factorial_obj, factorial);

// This is the entry point and is called when the module is imported
mp_obj_t mpy_init(mp_obj_fun_bc_t *self, size_t n_args, size_t n_kw, mp_obj_t *args) {
    // This must be first, it sets up the globals dict and other things
    MP_DYNRUNTIME_INIT_ENTRY

    // Make the function available in the module's namespace
    mp_store_global(MP_QSTR_factorial, MP_OBJ_FROM_PTR(&factorial_obj));
    mp_store_global(MP_QSTR_usb_init, MP_OBJ_FROM_PTR(&usb_init_obj));

    // This must be last, it restores the globals dict
    MP_DYNRUNTIME_INIT_EXIT
}
