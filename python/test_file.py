import animated
from animated import breakTimeData,breakDataForAP,breakDataForDP,updateData


def test_breakTimeDataExpected2010152():
    value = [0x80, 0x28, 0xD8, 0xFA]
    # |1|0x7A|  |1|0x58|    |0|0x28|
    x = breakTimeData(value)
    #the data is placed starting at value[-4]
    assert x == -4
    assert animated.timeDiff == 2010152

def test_breakTimeDataExpected110():
    value = [0x80, 0x6E]
    # |0|0x6E|
    x = breakTimeData(value)
    #the data is placed starting at value[-2]
    assert x == -2
    assert animated.timeDiff == 0x6E

def test_breakDataForAPSet1():
    # for adc 1 0xD11(3345)
    # for adc 3 0x848(2120)
    # for adc 5 0x309(777)
    # for adc 7 0xC92(3218)
    # for adc 8 0xFFF(4095)
    # for adc 9 0x1(1)
    USBData=[0x11,0xD,0x48,0x8,0x9,0x3,0x92,0xC,0xFF,0xF,0x1,0x0,0x28,0xD8,0xFA]
    #APPortArray=[1,3,5,7,8,9]
    breakDataForAP(USBData)
    assert animated.APData[0] == 0xD11
    assert animated.APData[1] == 0x848
    assert animated.APData[2] == 0x309
    assert animated.APData[3] == 0xC92
    assert animated.APData[4] == 0xFFF
    assert animated.APData[5] == 0x1

def test_breakDataForAPSet2():
    # for adc 1 0x832(2098)
    # for adc 3 0x2FA(762)
    # for adc 5 0x1C9(457)
    # for adc 7 0x252(594)
    # for adc 8 0x41E(1054)
    # for adc 9 0xBB8(3000)
    USBData=[0x32,0x8,0xFA,0x2,0xC9,0x1,0x52,0x2,0x1E,0x4,0xB8,0xb,0x28,0xD8,0xFA]
    #APPortArray=[1,3,5,7,8,9]
    breakDataForAP(USBData)
    assert animated.APData[0] == 0x832
    assert animated.APData[1] == 0x2FA
    assert animated.APData[2] == 0x1C9
    assert animated.APData[3] == 0x252
    assert animated.APData[4] == 0x41E
    assert animated.APData[5] == 0xBB8

def test_breakDataForDPSet1():
    # 0x3E
    #0x11 1110
    USBData=[0x3E,0x28,0xD8,0xFA]
    breakDataForDP(USBData)
    assert animated.DPData[0] == 0
    assert animated.DPData[1] == 1
    assert animated.DPData[2] == 1
    assert animated.DPData[3] == 1
    assert animated.DPData[4] == 1
    assert animated.DPData[5] == 1



