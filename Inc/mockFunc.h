#ifndef _MOCKFUNC_H
#define _MOCKFUNC_H
#include <stdint.h>
int htim2;
uint16_t __HAL_TIM_GetCounter(int* address);
uint16_t ReadGpioxIDR(char choose);
#endif // _MOCKFUNC_H
