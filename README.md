# Logic Analyzer
This project is to probe signals from the STM32, send them through USB and display them in PC using Python 3.6

## Getting Started

### Environment
* Windows10
* [Python 3.6](https://www.python.org/downloads/release/python-366/)

#### Python Packages Used
* [pyusb](https://github.com/pyusb/pyusb)
* [numpy](http://www.numpy.org/)
* [matplotlib](https://matplotlib.org/)
* [pytest](https://pytest.org/)

#### Hardware Used
* STM32F103C8T6

#### Software Used
* [STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html)
* [System Workbench for STM32](https://www.st.com/en/development-tools/sw4stm32.html)
* [PyCharm](https://www.jetbrains.com/pycharm/)

## How to use it?
* Clone this project
* Open the .project file inside this project (Make sure that it is opened using System Workbench for STM32)
* Upload the code to your STM32F103
* Open up PyCharm, include the folder LogicAnalyzer/python (python should automatically install all the packages inside the       requirements.txt)
* Connect the STM32F103 to PC by using 1 USB cable
* Run the python code

## Respective Port to Pin
AP0 -> PA0  
AP1 -> PA1  
AP2 -> PA2  
AP3 -> PA3  
AP4 -> PA4  
AP5 -> PA5  
AP6 -> PA6  
AP7 -> PA7  
AP8 -> PB0  
AP9 -> PB1  
  
DP0 -> PB2  
DP1 -> PB3  
DP2 -> PB4  
DP3 -> PB5  
DP4 -> PB6  
DP5 -> PB7  
DP6 -> PA8  
DP7 -> PA9  
DP8 -> PA10 
DP9 -> PA15 
