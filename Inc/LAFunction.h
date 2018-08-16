#ifndef _LAFUNCTION_H
#define _LAFUNCTION_H
#include <stdint.h>
#include <string.h>

uint8_t countSetBits(uint16_t PortsAvailable);
void AssignPortToArray();
void TimeDiffCalculate();
void GeneratePortBToSelectedPinsTable(uint16_t config);
void GeneratePortAToSelectedPinsTable(uint16_t config);
uint8_t GenerateVariableSizeTime(uint32_t Diff,uint8_t* timeA);
uint16_t ReadGpioxIDR(char choose);
void PackingDataForDP();
uint8_t PackingDataForAP(uint16_t config);
void InterpretCommand();
int ReceivePacket(uint8_t* Buf, uint32_t Len);
int RemovePacket(int indexCounter);
//global variable
 // define variables
extern uint16_t adc[10], buffer[10];
extern volatile uint16_t myOldCounter;
extern volatile uint16_t myCurrentCounter;
extern volatile uint32_t myOldTick;
extern volatile uint32_t myCurrentTick;
extern volatile uint8_t ADC_DataFlag;
extern volatile uint8_t USB_CDC_MYSTATE;
extern volatile uint8_t configBuffer[];
extern volatile uint8_t sizeofDP;
extern volatile uint8_t sizeofAP;
extern uint8_t DPPortArray[];
extern uint8_t DPDataArray[];
extern volatile uint16_t counterDiff;
extern volatile uint32_t tickDiff;
extern volatile uint8_t DPUpData;
extern volatile uint8_t DPDownData;
extern volatile uint8_t DPPortATable[];
extern volatile uint8_t DPPortBTable[];
extern volatile uint8_t time[];
extern uint8_t sizeofTimeArray;
extern uint16_t DPData;
extern volatile uint8_t packet[];
extern volatile uint8_t stateMachine_State;
extern uint8_t USB_SendData[];
extern uint8_t APPortArray[];
extern volatile uint8_t APDataArray[];
extern volatile uint8_t isConfigReady;
extern int indexCounter;
extern volatile uint32_t analogTick;

#define LOBYTE(x)  ((uint8_t)(x & 0x00FF))
#define HIBYTE(x)  ((uint8_t)((x & 0xFF00) >>8))

#define A 0
#define B 1

#define STATE_READY	1
#define STATE_NOT_READY	0
#define STATE_CHANGE_APP  0x9
#define STATE_SEND_DP 0xa
#define STATE_SEND_AP 0xb
#define STATE_CONFIG 0xc
#define STATE_SEND_ACK 0xd
#define STATE_SEND_APP 0xe

#define STATE_IDLE 0xF

#define USED 0
#define NOT_USED 1
#define READY 1
#define NOT_READY 0



#endif // _LAFUNCTION_H
