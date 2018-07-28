#include "MyFunction.h"
#include "mockFunc.h"
#include <stdio.h>
#include <stdint.h>
//place the global variable//
//need to be remove after this//
volatile uint16_t myOldCounter;
volatile uint16_t myCurrentCounter;
volatile uint32_t myOldTick;
volatile uint32_t myCurrentTick;
volatile uint8_t ADC_ReadyFlag;
volatile uint8_t USB_CDC_MYSTATE;
volatile uint8_t configBuffer[]={0};
volatile uint8_t DPPortArray[];
volatile uint8_t DPDataArray[];
volatile uint8_t sizeofDP;
volatile uint8_t sizeofAP;
volatile uint16_t counterDiff;
volatile uint32_t tickDiff;
/////////////////////////////////////////



uint8_t countSetBits(uint16_t PortsAvailable)
{
  unsigned int count = 0;
  while (PortsAvailable)
  {
    count += PortsAvailable & 1;
    PortsAvailable >>= 1;
  }
  return count;
}

void AssignPortToArray(){
  uint16_t configDP=(configBuffer[1]<<8)|configBuffer[2];
	uint8_t PortNum=0;
	int i=0;
	while(configDP){
		if(configDP&1){
			DPPortArray[i]=PortNum;
			i++;
		}
		configDP >>= 1;
		PortNum+=1;
	 }
}



void TimeDiffCalculate()
{
	//get current counter
	myCurrentCounter=__HAL_TIM_GetCounter(&htim2);
	counterDiff=myCurrentCounter-myOldCounter;
	tickDiff=myCurrentTick-myOldTick;
  myOldCounter=myCurrentCounter;
	myOldTick=myCurrentTick;
}

void AssignReadDataToArray(){
	for(int i=0;i<sizeofDP;i++){
		switch(DPPortArray[i]){
		// case 0:
		// 			DPDataArray[i]=HAL_GPIO_ReadPin(DP0_GPIO_Port,DP0_Pin);
		// 			break;
		// case 1:
		// 			DPDataArray[i]=HAL_GPIO_ReadPin(DP1_GPIO_Port,DP1_Pin);
		// 			break;
		// case 2:
		// 			DPDataArray[i]=HAL_GPIO_ReadPin(DP2_GPIO_Port,DP2_Pin);
		// 			break;
		// case 3:
		// 			DPDataArray[i]=HAL_GPIO_ReadPin(DP3_GPIO_Port,DP3_Pin);
		// 			break;
		// case 4:
		// 			DPDataArray[i]=HAL_GPIO_ReadPin(DP4_GPIO_Port,DP4_Pin);
		// 			break;
		// case 5:
		// 			DPDataArray[i]=HAL_GPIO_ReadPin(DP5_GPIO_Port,DP5_Pin);
		// 			break;
		// case 6:
		// 			DPDataArray[i]=HAL_GPIO_ReadPin(DP6_GPIO_Port,DP6_Pin);
		// 			break;
		// case 7:
		// 			DPDataArray[i]=HAL_GPIO_ReadPin(DP7_GPIO_Port,DP7_Pin);
		// 			break;
		// case 8:
		// 			DPDataArray[i]=HAL_GPIO_ReadPin(DP8_GPIO_Port,DP8_Pin);
		// 			break;
		// case 9:
		// 			DPDataArray[i]=HAL_GPIO_ReadPin(DP9_GPIO_Port,DP9_Pin);
		// 			break;
		}
	}
}
