# Python-Arduino-Serial-Communication
A Basic Data Link between a Python Program (on Windows) and an Arduino via Serial exchanging Data in Both ways

Data Rates of serial:   High Datacount (integers floats strings etc )but low Refresh rate about 3Hz Max maybe upgradeable
Data Rates of Hardware: Mikrocontrollers with different Chips may require different Looprates in the Python Code
                                    Tested:
                                    Arduino UNO 0.4s  Python Looprate
                                    Arduino MEGA 0.8s Python Looprate


to be useable by Linux or Mac: the Serial variables in the Python program need to be changed to their specific Serial port connection Path 
to be useable by Windows: just change "COM12" in the Python file to your com port of the arduino
