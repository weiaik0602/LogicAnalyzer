/*
 * myHeader.h
 *
 *  Created on: 10 Jul 2018
 *      Author: ng_we
 */
#include <stdint.h>
#include "main.h"
#include "stm32f1xx_hal.h"
#include "usb_device.h"
#include <stdio.h>
//#include "usbd_cdc_if.h"

//global variable

extern uint32_t adc[10], buffer[10];  // define variables
extern ADC_HandleTypeDef hadc1;
extern volatile uint16_t myOldCounter;
extern volatile uint16_t myCurrentCounter;
extern volatile uint16_t myOldTick;
extern volatile uint16_t myTick;
extern volatile uint8_t ADC_ReadyFlag;
extern volatile uint8_t USB_CDC_MYSTATE;
extern volatile uint8_t configBuffer[5];

//private definition
#define READY	1
#define NOT_READY	0
#define CONFIGURATION 0x22
#define SEMIHOSTING


#ifndef SEMIHOSTING
#define log(...)
#else
#define log printf
#endif
