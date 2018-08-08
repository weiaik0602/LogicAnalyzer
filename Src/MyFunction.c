#include "MyFunction.h"
#include "mockFunc.h"
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
//place the global variable//
uint16_t adc[10], buffer[10];
volatile uint16_t myOldCounter;
volatile uint16_t myCurrentCounter;
volatile uint32_t myOldTick;
volatile uint32_t myCurrentTick;
volatile uint8_t ADC_DataFlag;
volatile uint8_t USB_CDC_MYSTATE;
volatile uint8_t stateMachine_State;
volatile uint8_t configBuffer[10];
uint8_t DPPortArray[0];
uint8_t DPDataArray[2];
uint8_t APPortArray[0];
uint8_t APDataArray[20];
volatile uint8_t sizeofDP;
volatile uint8_t sizeofAP;
volatile uint16_t counterDiff;
volatile uint32_t tickDiff;
volatile uint8_t DPUpData;
volatile uint8_t DPDownData;
volatile uint8_t DPPortATable[256];
volatile uint8_t DPPortBTable[256];
uint8_t DPUpSize=0;
uint8_t DPDownSize=0;
volatile uint8_t time[5];
uint8_t sizeofTimeArray;
uint16_t DPData;
volatile uint8_t packet[256];
uint8_t USB_SendData[256];
uint8_t indexCounter;

volatile uint8_t isConfigReady=0;
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
  uint16_t configAP=(configBuffer[3]<<8)|configBuffer[4];
  uint8_t APortNum=0;
	int x=0;
	while(configAP){
		if(configAP&1){
			APPortArray[x]=APortNum;
			x++;
		}
		configAP >>= 1;
		APortNum+=1;
	 }
}
void TimeDiffCalculate()
{
	//get current counter
	myCurrentCounter=GetCurrentCounterTim2();
	counterDiff=myCurrentCounter-myOldCounter;
	tickDiff=myCurrentTick-myOldTick;
  myOldCounter=myCurrentCounter;
	myOldTick=myCurrentTick;
}
void GeneratePortBToSelectedPinsTable(uint16_t config){
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
    DPDownSize=0;
    uint16_t counter =0;
    uint16_t newconfig=(config&(0x3F));
    while(newconfig){
      if(newconfig&0x01){
        result=(data[counter+2]<<DPDownSize)|result ;
        DPDownSize++;
      }
      counter++;
      newconfig>>=1;
    }
    DPPortBTable[i]=result;
  }
}
void GeneratePortAToSelectedPinsTable(uint16_t config){
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
    DPUpSize=0;
    uint16_t counter =0;
    uint16_t newconfig=(config&(~0x3F))>>6;
    uint8_t buffForA15=newconfig>>3;
    while(newconfig){
      if(counter<3){
        if(newconfig&0x01){
          result=(data[counter]<<DPUpSize)|result ;
          DPUpSize++;
        }
      }
      counter++;
      newconfig>>=1;
    }
    if(buffForA15){
      result=(data[7]<<DPUpSize)|result ;
      DPUpSize++;
    }
    DPPortATable[i]=result;
  }
}

uint8_t GenerateVariableSizeTime(uint32_t Diff,uint8_t* timeA){
  memset((void*)&time, 0, 5);
  if(Diff<128)  //7bit
    sizeofTimeArray=1;
  else if(Diff<16384) //14bit
    sizeofTimeArray=2;
  else if(Diff<2097152) //21bit
    sizeofTimeArray=3;
  else if(Diff<268435456) //28bit
    sizeofTimeArray=4;
  else if(Diff<4294967296)  //32bit (max)
    sizeofTimeArray=5;

  for(int i=0;i<sizeofTimeArray;i++){
    //the last byte, dont add anything('0')
    if(i==0){
      timeA[i]=((Diff>>i*7)&0x7F);
    }
    //not last byte, add '1' flag infront
    else
      timeA[i]=((Diff>>i*7)&0x7F)|0x80;
  }
  return sizeofTimeArray;
}
void PackingDataForDP(){
  uint8_t DPUpData=(ReadGpioxIDR(A)>>8)&0xFF;
  uint8_t DPDownData=ReadGpioxIDR(B)&0xFF;
  DPData=((DPPortATable[DPUpData])<<DPDownSize)|DPPortBTable[DPDownData];
}

uint8_t PackingDataForAP(uint16_t config){
  int even=0;
  int odd=1;
  uint8_t counter=0;
  uint8_t size=countSetBits(config);
  while(config){
    if(config&0x01){
      APDataArray[even]=LOBYTE(adc[counter]);
      APDataArray[odd]=HIBYTE(adc[counter]);
      even+=2;
      odd+=2;
    }
    counter++;
    config>>=1;
  }
  return size;
}

void InterpretCommand(){
  switch(stateMachine_State){
    case STATE_CONFIG:
      isConfigReady=NOT_READY;
      memcpy((void*)configBuffer,(void*)packet,10);
      sizeofDP=countSetBits(configBuffer[2]<<8|configBuffer[3]);
      AssignPortToArray();
      GeneratePortAToSelectedPinsTable(configBuffer[2]<<8|configBuffer[3]);
      GeneratePortBToSelectedPinsTable(configBuffer[2]<<8|configBuffer[3]);
      //memset((void*)&packet[0], 0, 256);
      stateMachine_State=STATE_IDLE;
      isConfigReady=READY;
      break;
    case STATE_SEND_DP:
      TimeDiffCalculate();
      GenerateVariableSizeTime(tickDiff,(uint8_t*)&time[0]);
      PackingDataForDP();
      uint8_t DPA[]={LOBYTE(DPData),HIBYTE(DPData)};
      uint8_t *Sdata=(uint8_t*)&USB_SendData;
      memcpy(Sdata,DPA, 2);
      memcpy(Sdata+2, (const void*)time, sizeofTimeArray);
      USB_SendData[sizeofTimeArray+2]=STATE_SEND_DP;

      CDC_Transmit_FS((uint8_t*)&USB_SendData,(sizeofTimeArray+3));
      stateMachine_State=STATE_IDLE;
      break;

    case STATE_SEND_AP:
    	if(ADC_DataFlag==NOT_USED){
				TimeDiffCalculate();
				sizeofTimeArray=GenerateVariableSizeTime(tickDiff,(uint8_t*)&time[0]);
				sizeofAP=PackingDataForAP(configBuffer[4]<<8|configBuffer[5]);
				int size=sizeofAP*2;
				uint8_t *SAPdata=(uint8_t*)&USB_SendData;
				memcpy(SAPdata,APDataArray,size );
				memcpy((SAPdata+size), (const void*)time, sizeofTimeArray);
				USB_SendData[sizeofTimeArray+size]=STATE_SEND_AP;
				CDC_Transmit_FS((uint8_t*)&USB_SendData,(sizeofTimeArray+size+1));
				ADC_DataFlag=USED;
    	}
    	stateMachine_State=STATE_IDLE;
      break;

    case STATE_SEND_ACK:
      USB_SendData[0]=STATE_SEND_ACK;
      USB_SendData[1]=0;
      CDC_Transmit_FS((uint8_t*)&USB_SendData,2);
      stateMachine_State=STATE_IDLE;
      break;

    case STATE_IDLE:
      break;

  }
}
void ReceivePacket(uint8_t* Buf, uint32_t Len)
{
  memcpy(((void*)&packet[0]+indexCounter),Buf,Len);
  indexCounter=indexCounter+(uint32_t)Len;
  if(indexCounter==(packet[1]+2)){
    stateMachine_State=packet[0];
    indexCounter=0;
  }
}
