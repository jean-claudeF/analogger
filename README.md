# Analog / serial logger with Raspi Pico
This logger can record 4 analog channels or eventually a serial data stream

Git page: https://github.com/jean-claudeF/analogger


![Picture](/Logger.jpg)

## Features
- 4 analog inputs 0...3V with defined input impedance 1MOhm
- Real time clock
- OLED display shows the 4 voltages during wait and recording
- Recording is done on an SD card (with automatic file name generation)
- Powering over USB or LIon cell

## Hardware
- The 4 inputs are buffered by 4 OPA335 with unity gain and an input impedance of 1MOhm.
  The 4k7 resistances should protect the opamps in case of overvoltage

- The SD card is connected directly to the Pico over SPI.

- OLED, RTC (breakout board) and ADC (breakout board) are connected over I2C.
  The internal pullup resistors of the boards are used. 

- There are several switches:
    - SW1: switch between analog (voltage) and serial recording
    - SW2: switch between Wait and Record
    - SW3: switch to battery power in absence of USB connection.
      The battery is a LiIon cell that can be charged over J5

## Firmware in Micropython
The firmware is divided into several modules
- Library modules:
	- ADC_ADS1115_02.py  (slightly modified version of the ADS115 lib)
	- OLED_SH1106_02.py  (modified version of the OLED driver)
	- RTC_SD3231.py (slightly modified RTC driver)
    - sdcard.py

- Tools:
	- blink.py and i2c_scan.py say hello and check the I2C bus
	- filetools_02.py   creates unique numbered filenames according to a pattern, for example "logger_003.dat" if  "logger_002.dat" exists already.

- Main program:
	- logger_xx.py is the main logging program
	- main.py imports blink, i2c_scan and logger_xx.py, so the logging program is automatically started.

- Addon:
    - addon.py is an extension that must contain a function called addon(voltages)
      It is called in the main loop every interval time and allows actions based on the voltages or anything you want to be done regularly.
      As this piece of code is small and independant from the main program, it can easily be edited and adapted to special tasks.

## Special files / addons in the Pico file system
- info.txt contains just one line with the word "LOGGER"
  It may be used by the PC software to identify the Pico and to automatically select the right port  for the connection
  
## SD card file format
The data are recorded in a CSV file, using tabs as delimiters, so that the data can easily be imported to plotting or spreadsheat programs.

For example:

```
9.11.21
10:32:10
0	10:32:10_T_9.11.21	0.00000	0.00000	-0.00013	0.00013
1	10:32:10_T_9.11.21	0.00000	-0.00013	-0.00013	0.00025
2	10:32:11_T_9.11.21	-0.00013	0.00000	-0.00013	0.00000
```
Time is coded in the form HH:MM:SS_T_D.M.YY


## TO DO
- Allow configuration of serial baudrate and interval time (in a py file imported by logger_xx.py)



