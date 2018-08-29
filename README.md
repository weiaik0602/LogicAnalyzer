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
