//#include "tusb_config.h"
//#include "tusb.h"
#include "pico/stdlib.h"
#include "stdio.h"

int main(void){
    stdio_init_all();
    while (1) {
        printf("Hello World!\n");
        sleep_ms(1000);
    }
    return 0;
}