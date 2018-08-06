/*
 * myHeader.h
 *
 *  Created on: 10 Jul 2018
 *      Author: ng_we
 */
#include <stdint.h>
#include <stdio.h>
#include "MyFunction.h"

//global variable
 // define variables
extern uint16_t adc[10], buffer[10];
extern volatile uint16_t myOldCounter;
extern volatile uint16_t myCurrentCounter;
extern volatile uint32_t myOldTick;
extern volatile uint32_t myCurrentTick;
extern volatile uint8_t ADC_DataFlag;
extern volatile uint8_t USB_CDC_MYSTATE;
extern volatile uint8_t configBuffer[5];
extern volatile uint8_t sizeofDP;
extern volatile uint8_t sizeofAP;
extern uint8_t DPPortArray[];
extern uint8_t DPDataArray[];
extern volatile uint16_t counterDiff;
extern volatile uint32_t tickDiff;
extern volatile uint8_t DPUpData;
extern volatile uint8_t DPDownData;
extern volatile uint8_t DPPortATable[256];
extern volatile uint8_t DPPortBTable[256];
extern volatile uint8_t time[];
extern uint8_t sizeofTimeArray;
extern uint16_t DPData;
extern uint8_t packet[256];
extern volatile uint8_t stateMachine_State;
extern uint8_t USB_SendData[];
extern uint8_t indexCounter;
extern uint8_t APPortArray[];
extern uint8_t APDataArray[];
extern volatile uint8_t isConfigReady;
// definition

#define SEMIHOSTING


#ifndef SEMIHOSTING
#define log(...)
#else
#define log printf
#endif
