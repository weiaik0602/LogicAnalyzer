#ifndef _MYFUNCTION_H
#define _MYFUNCTION_H
#include <stdint.h>
// #include "stm32f1xx_hal.h"

uint8_t countSetBits(uint16_t PortsAvailable);
void AssignPortToArray();
void TimeDiffCalculate();
void AssignReadDataToArray();
void GenerateDownTableAccordingDPPortArray();
void GenerateUpTableAccordingDPPortArray();
#endif // _MYFUNCTION_H
