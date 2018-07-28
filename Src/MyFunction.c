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
uint8_t DPPortArray[];
uint8_t DPDataArray[];
volatile uint8_t sizeofDP;
volatile uint8_t sizeofAP;
volatile uint16_t counterDiff;
volatile uint32_t tickDiff;
volatile uint8_t DPUpData;
volatile uint8_t DPDownData;
volatile uint8_t DPUpTable[256];
volatile uint8_t DPDownTable[256];
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
void GenerateDownTableAccordingDPPortArray(){
  /*This table is only for the lower part of DP(port B),
  which is from DP0 to DP5(B2 to B7)
  | B7 | B6 | B5 | B4 | B3 | B2 | B1 | B0 |  correspond to
  | D5 | D4 | D3 | D2 | D1 | D0 | XX | XX |*/
  uint8_t data[8];

  for(int i=0;i<0xFF;i++){
    uint8_t result=0;
    for(int y=0;y<8;y++){
      data[y]=(i>>y)&1;
    }
    uint8_t counter=0;
    for(int z=0;z<sizeofDP;z++){
      if(DPPortArray[z]<6){
      result=((data[DPPortArray[z]+2])<<(counter))|result;
      counter++;
      }
    }
    DPDownTable[i]=result;
  }
}
void GenerateUpTableAccordingDPPortArray(){
  /*This table is only for the upper part of DP(port A),
  which is from DP6 to DP9(A8 A9 A10 A15)
  | A15 | A14 | A13 | A12 | A11 | A10 | A9  | A8  |  correspond to
  | DP9 | xxx | xxx | xxx | xxx | DP8 | DP7 | DP6 |*/
  uint8_t data[8];

  for(int i=0;i<0xFF;i++){
    uint8_t result=0;
    for(int y=0;y<8;y++){
      data[y]=(i>>y)&0x01;

    }
    uint8_t counter=0;
    for(int z=0;z<sizeofDP;z++){
      if(DPPortArray[z]>5){
        if(DPPortArray[z]==9){
          result=((data[7])<<(counter))|result;
          counter++;
        }
        else{
          result=((data[DPPortArray[z]-6])<<(counter))|result;
          counter++;
        }
      }
    }
    DPUpTable[i]=result;
  }
}
void ArrangeTimeArray(){

}
