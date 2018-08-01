/*
 * myHeader.h
 *
 *  Created on: 10 Jul 2018
 *      Author: ng_we
 */
#include <stdint.h>
#include <stdio.h>
#include "MyFunction.h"
#include "main.h"
#include "stm32f1xx_hal.h"
#include "usb_device.h"
#include "usbd_cdc_if.h"

//global variable
// define variables
extern uint32_t adc[10], buffer[10];
extern ADC_HandleTypeDef hadc1;
extern volatile uint16_t myOldCounter;
extern volatile uint16_t myCurrentCounter;
extern volatile uint32_t myOldTick;
extern volatile uint32_t myCurrentTick;
extern volatile uint8_t ADC_ReadyFlag;
extern volatile uint8_t USB_CDC_MYSTATE;
extern volatile uint8_t configBuffer[5];
extern volatile uint8_t sizeofDP;
extern uint8_t DPPortArray[];
extern uint8_t DPDataArray[];
extern volatile uint16_t counterDiff;
extern volatile uint32_t tickDiff;
extern volatile uint8_t DPUpData;
extern volatile uint8_t DPDownData;
extern volatile uint8_t DPUpTable[256];
extern volatile uint8_t DPDownTable[256];
extern volatile uint8_t time[];
extern uint8_t sizeofTimeArray;
//private definition
#define SEMIHOSTING


#ifndef SEMIHOSTING
#define log(...)
#else
#define log printf
#endif
