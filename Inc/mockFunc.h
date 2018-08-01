#ifndef _MOCKFUNC_H
#define _MOCKFUNC_H
#include <stdint.h>
int htim2;
uint16_t GetCurrentCounterTim2();
uint16_t ReadGpioxIDR(char choose);
uint8_t CDC_Transmit_FS(uint8_t* Buf, uint16_t Len);
#endif // _MOCKFUNC_H
