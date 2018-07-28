#include "unity.h"
#include "MyFunction.h"
#include "mock_mockFunc.h"
#include "myFunctionHeader.h"

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
