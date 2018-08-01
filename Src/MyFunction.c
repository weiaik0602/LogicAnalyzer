#include "MyFunction.h"
#include "mockFunc.h"
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
//place the global variable//
uint32_t adc[10], buffer[10];
volatile uint16_t myOldCounter;
volatile uint16_t myCurrentCounter;
volatile uint32_t myOldTick;
volatile uint32_t myCurrentTick;
volatile uint8_t ADC_ReadyFlag;
volatile uint8_t USB_CDC_MYSTATE;
volatile uint8_t stateMachine_State;
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
uint8_t DPUpSize=0;
uint8_t DPDownSize=0;
volatile uint8_t time[];
uint8_t sizeofTimeArray;
uint16_t DPData;
volatile uint8_t packet[256];
uint8_t USB_SendData[];
uint8_t packetCounter;
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
	myCurrentCounter=GetCurrentCounterTim2();
	counterDiff=myCurrentCounter-myOldCounter;
	tickDiff=myCurrentTick-myOldTick;
  myOldCounter=myCurrentCounter;
	myOldTick=myCurrentTick;
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
    DPDownSize=0;
    for(int z=0;z<sizeofDP;z++){
      if(DPPortArray[z]<6){
      result=((data[DPPortArray[z]+2])<<(DPDownSize))|result;
      DPDownSize++;
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
    DPUpSize=0;
    for(int z=0;z<sizeofDP;z++){
      if(DPPortArray[z]>5){
        if(DPPortArray[z]==9){
          result=((data[7])<<(DPUpSize))|result;
          DPUpSize++;
        }
        else{
          result=((data[DPPortArray[z]-6])<<(DPUpSize))|result;
          DPUpSize++;
        }
      }
    }
    DPUpTable[i]=result;
  }
}

void ArrangeTimeArray(){
  memset((void*)&time[0], 0, sizeofTimeArray);
  if(tickDiff<128)  //7bit
    sizeofTimeArray=1;
  else if(tickDiff<16384) //14bit
    sizeofTimeArray=2;
  else if(tickDiff<2097152) //21bit
    sizeofTimeArray=3;
  else if(tickDiff<268435456) //28bit
    sizeofTimeArray=4;
  else if(tickDiff<4294967296)  //32bit (max)
    sizeofTimeArray=5;

  for(int i=0;i<sizeofTimeArray;i++){
    //the last byte, dont add anything('0')
    if(i==0){
      time[i]=((tickDiff>>i*7)&0x7F);
    }
    //not last byte, add '1' flag infront
    else
      time[i]=((tickDiff>>i*7)&0x7F)|0x80;
  }
}
void PackingDataForDP(){
  uint8_t DPUpData=(ReadGpioxIDR(A)>>8)&0xFF;
  uint8_t DPDownData=ReadGpioxIDR(B)&0xFF;
  DPData=((DPUpTable[DPUpData])<<DPDownSize)|DPDownTable[DPDownData];
}


void InterpretCommand(){
  switch(stateMachine_State){
    case STATE_CONFIG:
      configBuffer[0]=packet[0];
      configBuffer[1]=packet[2];
      configBuffer[2]=packet[3];
      configBuffer[3]=packet[4];
      configBuffer[4]=packet[5];
      sizeofDP=countSetBits(configBuffer[1]<<8|configBuffer[2]);
      AssignPortToArray();
      GenerateUpTableAccordingDPPortArray();
      GenerateDownTableAccordingDPPortArray();
      memset((void*)&packet[0], 0, 256);
      stateMachine_State=STATE_SEND_ACK;
      break;
    case STATE_SEND_DP:
      TimeDiffCalculate();
      ArrangeTimeArray();
      PackingDataForDP();
      uint8_t DPA[]={LOBYTE(DPData),HIBYTE(DPData)};
      uint8_t *Sdata=(uint8_t*)malloc((sizeofTimeArray+2) );
      Sdata=(uint8_t*)&USB_SendData;
      memcpy(Sdata,DPA, 2);
      memcpy(Sdata+2, (const void*)time, sizeofDP);
      CDC_Transmit_FS((uint8_t*)&USB_SendData,(sizeofTimeArray+2));
      stateMachine_State=STATE_SEND_ACK;
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
void ReceivePacket(uint8_t* Buf, uint32_t *Len)
{
  memcpy((&packet[0]+packetCounter),Buf,(uint32_t)Len);
  packetCounter=packetCounter+(uint32_t)Len;
  if(packetCounter==(packet[1]+2)){
    stateMachine_State=packet[0];
    packetCounter=0;
  }
}
