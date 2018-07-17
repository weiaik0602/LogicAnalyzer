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
#include "usbd_cdc_if.h"

//global variable
extern uint16_t myTick;
extern uint32_t adc[10], buffer[10];  // define variables
extern ADC_HandleTypeDef hadc1;
extern volatile uint8_t ADC_ReadyFlag;


//private defination
#define READY	1
#define NotREADY	0
