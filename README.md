# Serial-Data-read-from-arduino-and-bandpower-calculation

When Arduino is connected to system and data acquisition is taking place through serial communication between Arduino and system,SerialData.py file can be used to store serial data from 2 channels (2 analog pins of arduino) and calculate bandpower.
# 1) Bandpower will be calculated for last 4000 samples(Bandpower for data in 25 Hz to 450 Hz). A butterworth filter has been used.
# 2)You have to rename Serialdata.csv file created after every session in order to avoid adding data to same file.
# 3)Can increase no. of samples for which bandpower to be calculated by changing "samples=4000".
