#include "unity.h"
#include "MyFunction.h"
#include "mock_mockFunc.h"
#include "FunctionHeaderTest.h"

void setUp(void)
{
}

void tearDown(void)
{
}


void test_AssignPortToArrayDP02468(void){
  /*Put in 0xXX 0x1 0x55 0xXX 0xXX
  into the configBuffer*/
  //activate DP0,2,4,6,8
  configBuffer[1]=1;
  configBuffer[2]=0x55;
  AssignPortToArray();
  TEST_ASSERT_EQUAL(DPPortArray[0],0);
  TEST_ASSERT_EQUAL(DPPortArray[1],2);
  TEST_ASSERT_EQUAL(DPPortArray[2],4);
  TEST_ASSERT_EQUAL(DPPortArray[3],6);
  TEST_ASSERT_EQUAL(DPPortArray[4],8);
}

void test_AssignPortToArrayDP14678(void){
  /*Put in 0xXX 0x1 0xD2 0xXX 0xXX
  into the configBuffer*/
  //activate DP1,4,6,7,8
  configBuffer[1]=1;
  configBuffer[2]=0xD2;
  AssignPortToArray();
  TEST_ASSERT_EQUAL(DPPortArray[0],1);
  TEST_ASSERT_EQUAL(DPPortArray[1],4);
  TEST_ASSERT_EQUAL(DPPortArray[2],6);
  TEST_ASSERT_EQUAL(DPPortArray[3],7);
  TEST_ASSERT_EQUAL(DPPortArray[4],8);
}
void test_TimeDiffCalculate(void){
  //Ccounter=0x156  Ctick=30
  //OldCounter=0    Oldtick=0
  __HAL_TIM_GetCounter_ExpectAndReturn(&htim2,0x156);
  myCurrentTick=30;
  myOldCounter=0;
  myOldTick=0;
  TimeDiffCalculate();
  TEST_ASSERT_EQUAL(tickDiff,30);
  TEST_ASSERT_EQUAL(counterDiff,0x156);

}
void test_GenerateDownTableAccordingDPPortArray_GivenDP02467(void){
  DPPortArray[0]=0;
  DPPortArray[1]=2;
  DPPortArray[2]=4;
  DPPortArray[3]=6;
  DPPortArray[4]=7;
  sizeofDP=5;
  GenerateDownTableAccordingDPPortArray();
  /*This table is only for the lower part of DP,
  which is from DP0 to DP5(B2 to B7)
  | B7 | B6 | B5 | B4 | B3 | B2 | B1 | B0 |  correspond to
  | D5 | D4 | D3 | D2 | D1 | D0 | XX | XX |*/
  //The wanted port is 0,2,4(6 and 7 dont care)
  //0x3e = 0011 1110
  //DP0 2 and 4=B2 B4 B6
  //011=3
  TEST_ASSERT_EQUAL(DPDownTable[0x3e],3);
  //0x45 =0100 0101
  //DP0 2 and 4=B2 B4 B6
  //101=5
  TEST_ASSERT_EQUAL(DPDownTable[0x45],5);
  //0x98 =1001 1000
  //DP0 2 and 4=B2 B4 B6
  //010=2
  TEST_ASSERT_EQUAL(DPDownTable[0x98],2);
  //0xe5 =1110 0101
  //DP0 2 and 4=B2 B4 B6
  //101=5
  TEST_ASSERT_EQUAL(DPDownTable[0xe5],5);
  //0xf8 =1111 1000
  //DP0 2 and 4=B2 B4 B6
  //110=6
  TEST_ASSERT_EQUAL(DPDownTable[0xf8],6);
}
void test_GenerateDownTableAccordingDPPortArray_GivenDP012345(void){
  DPPortArray[0]=0;
  DPPortArray[1]=1;
  DPPortArray[2]=2;
  DPPortArray[3]=3;
  DPPortArray[4]=4;
  DPPortArray[5]=5;
  sizeofDP=6;
  GenerateDownTableAccordingDPPortArray();
  /*This table is only for the lower part of DP,
  which is from DP0 to DP5(B2 to B7)
  | B7 | B6 | B5 | B4 | B3 | B2 | B1 | B0 |  correspond to
  | D5 | D4 | D3 | D2 | D1 | D0 | XX | XX |*/
  //The wanted port is 0,1,2,3,4,5
  //0xf7 = 1111 0111
  //DP0 1 2 3 4 5 = B 2 3 4 5 6 7
  //111101=3D
  TEST_ASSERT_EQUAL(DPDownTable[0xf7],0x3d);
  //0x9c =1001 1100
  //DP0 1 2 3 4 5 = B 2 3 4 5 6 7
  //100111=0x27
  TEST_ASSERT_EQUAL(DPDownTable[0x9c],0x27);
  //0xea=1110 1010
  //DP0 1 2 3 4 5 = B 2 3 4 5 6 7
  //111010=0x3a
  TEST_ASSERT_EQUAL(DPDownTable[0xea],0x3a);
  //0x0b=0000 1011
  //DP0 1 2 3 4 5 = B 2 3 4 5 6 7
  //000010=2
  TEST_ASSERT_EQUAL(DPDownTable[0x0b],2);
  //0x01=0000 0001
  //DP0 1 2 3 4 5 = B 2 3 4 5 6 7
  //000000
  TEST_ASSERT_EQUAL(DPDownTable[0x01],0);
}

void test_GenerateUpTableAccordingDPPortArray_GivenDP6789(void){
  DPPortArray[0]=6;
  DPPortArray[1]=7;
  DPPortArray[2]=8;
  DPPortArray[3]=9;
  sizeofDP=4;
  GenerateUpTableAccordingDPPortArray();
  /*This table is only for the upper part of DP(port A),
  which is from DP6 to DP9(A8 A9 A10 A15)
  | A15 | A14 | A13 | A12 | A11 | A10 | A9  | A8  |  correspond to
  | DP9 | xxx | xxx | xxx | xxx | DP8 | DP7 | DP6 |*/
  //The wanted port is DP 6 7 8 9
  //0xf7 = 1111 0111
  //1111=0xF
  TEST_ASSERT_EQUAL(DPUpTable[0xf7],0xf);
  //0x9c =1001 1100
  //1100=0xc
  TEST_ASSERT_EQUAL(DPUpTable[0x9c],0xc);
  //0xea=1110 1010
  //1010=0xa
  TEST_ASSERT_EQUAL(DPUpTable[0xea],0xa);
  //0x0b=0000 1011
  //0011=3
  TEST_ASSERT_EQUAL(DPUpTable[0x0b],3);
  //0x01=0000 0001
  //0001
  TEST_ASSERT_EQUAL(DPUpTable[0x01],1);
}

void test_GenerateUpTableAccordingDPPortArray_GivenDP02468(void){
  DPPortArray[0]=0;
  DPPortArray[1]=2;
  DPPortArray[2]=4;
  DPPortArray[3]=6;
  DPPortArray[4]=8;
  sizeofDP=5;
  GenerateUpTableAccordingDPPortArray();
  /*This table is only for the upper part of DP(port A),
  which is from DP6 to DP9(A8 A9 A10 A15)
  | A15 | A14 | A13 | A12 | A11 | A10 | A9  | A8  |  correspond to
  | DP9 | xxx | xxx | xxx | xxx | DP8 | DP7 | DP6 |*/
  //The wanted port is DP 6 8
  //0x3e = 0011 1110
  //10=2
  TEST_ASSERT_EQUAL(DPUpTable[0x3e],2);
  //0x45 =0100 0101
  //11=3
  TEST_ASSERT_EQUAL(DPUpTable[0x45],3);
  //0x98 =1001 1000
  //00
  TEST_ASSERT_EQUAL(DPUpTable[0x98],0);
  //0xe5 =1110 0101
  //11
  TEST_ASSERT_EQUAL(DPUpTable[0xe5],3);
  //0xf8 =1111 1000
  //00
  TEST_ASSERT_EQUAL(DPUpTable[0xf8],0);
}

void test_ArrangeTimeArrayExpect1byte(void){
  tickDiff=33;
  ArrangeTimeArray();
  //When the diff is <128,1 byte is enough
  TEST_ASSERT_EQUAL(time[0],33);
  TEST_ASSERT_EQUAL(time[1],0);
}
void test_ArrangeTimeArrayExpect3byte(void){
  tickDiff=1564852;
  ArrangeTimeArray();
  //When the 16384<diff<2097152,3 byte is enough
  //1st byte will be 0(lower 7-bit)
  //1564852=0001 0111 1110 0000 1011 0100
  TEST_ASSERT_EQUAL(time[0],0x34);
  //2nd byte = 1(medium 7-bit)
  TEST_ASSERT_EQUAL(time[1],0xC1);
  //3rdbyte =1(higher 7-bit)
  TEST_ASSERT_EQUAL(time[2],0xDF);
  //4th byte =0
  TEST_ASSERT_EQUAL(time[3],0);
}
void test_ArrangeTimeArrayExpect2byte(void){
  tickDiff=15780;
  ArrangeTimeArray();
  //When the 128<diff<16384,2 byte is enough
  //1st byte will be 0(lower 7-bit)
  //15780=0011 1101 1010 0100
  TEST_ASSERT_EQUAL(time[0],0x24);
  //2nd byte = 1(higher 7-bit)
  TEST_ASSERT_EQUAL(time[1],0xFB);
  //3rdbyte =0
  TEST_ASSERT_EQUAL(time[2],0);
}
void test_PackingDataForDP(void){
  //assuming these are the port we wanted
  //DP 0 2 4 6 8
  DPPortArray[0]=0;
  DPPortArray[1]=2;
  DPPortArray[2]=4;
  DPPortArray[3]=6;
  DPPortArray[4]=8;
  sizeofDP=5;
  //Assuming GPIOA will return 0xefc8
  //Assuming GPIOB will return 0xc6a9
  ReadGpioxIDR_ExpectAndReturn(A,0xefc8);
  ReadGpioxIDR_ExpectAndReturn(B,0x98a2);
  //generate both table
  GenerateUpTableAccordingDPPortArray();
  GenerateDownTableAccordingDPPortArray();
  //pack data
  PackingDataForDP();
  //DP 6 and 8 from GPIOA 8 10
  //1 1
  //DP0 2 4 from GPIOB 2 4 6
  //0 0 0
  TEST_ASSERT_EQUAL(DPData,0x18);
}
