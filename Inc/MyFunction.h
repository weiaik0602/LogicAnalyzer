#ifndef _MYFUNCTION_H
#define _MYFUNCTION_H
#include <stdint.h>
#include <string.h>
// #include "stm32f1xx_hal.h"

uint8_t countSetBits(uint16_t PortsAvailable);
void AssignPortToArray();
void TimeDiffCalculate();
void GenerateDownTableAccordingDPPortArray();
void GenerateUpTableAccordingDPPortArray();
void ArrangeTimeArray();
uint16_t ReadGpioxIDR(char choose);
void PackingDataForDP();

#define A 0
#define B 1
#endif // _MYFUNCTION_H
