#ifndef _MYFUNCTION_H
#define _MYFUNCTION_H
#include <stdint.h>
#include <string.h>
// #include "stm32f1xx_hal.h"

uint8_t countSetBits(uint16_t PortsAvailable);
void AssignPortToArray();
void TimeDiffCalculate();
void GeneratePortBToSelectedPinsTable(uint16_t config);
void GeneratePortAToSelectedPinsTable(uint16_t config);
uint8_t GenerateVariableSizeTime(int Diff,uint8_t* timeA);
uint16_t ReadGpioxIDR(char choose);
void PackingDataForDP();
uint8_t PackingDataForAP(uint16_t config);
void InterpretCommand();
void ReceivePacket(uint8_t* Buf, uint32_t Len);


#define LOBYTE(x)  ((uint8_t)(x & 0x00FF))
#define HIBYTE(x)  ((uint8_t)((x & 0xFF00) >>8))

#define A 0
#define B 1

#define STATE_READY	1
#define STATE_NOT_READY	0
#define STATE_SEND_DP 0xa
#define STATE_SEND_AP 0xb
#define STATE_CONFIG 0xc
#define STATE_SEND_ACK 0xd
#define STATE_IDLE 0xF

#define USED 0
#define NOT_USED 1
#define READY 1
#define NOT_READY 0
#endif // _MYFUNCTION_H
