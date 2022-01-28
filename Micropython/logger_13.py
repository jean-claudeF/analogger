import blink
import i2c_scan
from machine import Pin, I2C, UART
import time
from OLED_SH1106_02 import SH1106_I2C
from RTC_DS3231 import DS3231
from ADC_ADS1115_02 import ADS1115
from filetools_02 import SD
from generate_filename import  get_next_filename
import sys
#-----------------------------------------------------------------
# Initialisations

file_pattern = 'logger_000.dat'
t_interval = 1

# OLED + RTC + ADC on I2C
i2c = I2C(0, scl=Pin(9), sda=Pin(8))
oled = SH1106_I2C(128, 64, i2c)
rtc = DS3231(0, 9, 8)
adc = ADS1115(i2c, address = 72, gain = 1)

# SD card on SPI
sdfolder = "/SD"
SPIselect = 0                  # 0/1 for SPI0 or SPI1
SD_CS = 5                      # Chip select for SD  (may be any GP pin)
sd = SD(SPIselect, SD_CS, sdfolder)

#switches
sw1 = Pin(14, Pin.IN, Pin.PULL_UP)
sw2 = Pin(15, Pin.IN, Pin.PULL_UP)

# output
trigger_out = Pin(17, Pin.OUT)
led_measure = Pin(16, Pin.OUT)

# supplementary output for actions:
'''
d18 = Pin(18, Pin.OUT)
d19 = Pin(19, Pin.OUT)
d20 = Pin(20, Pin.OUT)
d21 = Pin(21, Pin.OUT)
'''
#----------------------------------------------------------------------------------

def check_sdcard():
    
    if sd.error:
        print(sd.error)
        oled.print_s("SD card ERROR!")
        sys.exit()
    else:
        print("SD card OK")
        oled.print_s("SD card OK")
        print("SD folder: ", sd.sdfolder)
        
        #l = sd.listfiles()
        #print("Files on SD: ", l)
        print()

def init_file():
    files = sd.listfiles()
    name = get_next_filename(files, file_pattern)
    print("File name: ", name)
    oled.print(name)
    sd.print(name, "# " + name)
    
    return name
# ------------------------------------------------------
def printall(s, filename):
    print(s)
    oled.print(s)
    sd.print(filename, s)
    oled.show()

def print_time(filename):
    print("LOGGER")
    s = rtc.get_date()
    printall(s, filename)
    s = rtc.get_time()
    printall(s, filename)
    
def end_program():
    sd.unmount()
    print("END")
    oled.clear()
    oled.print("END")
    
def start_program():
    check_sdcard()
    filename = init_file()
    print_time(filename)
    return filename
#-----------------------------------------------------

def analog_loop():
    
    # wait for record switch -> 0
    while (sw2.value()) == 1:
        v = adc.read_all_as_string()
        s = "WAITING" + '\t' + v
        oled.print_s(s)
        print(s, end = '\r')
        time.sleep(0.5)
        
    
    # debounce
    time.sleep(0.1)
    trigger_out.value(1)
    
    # Record until record switch -> 0
    i = 0
    while (sw2.value()) == 0:
        led_measure.value(1)
        t0 = time.time()
        
        v = adc.read_all_as_string()
        
        # print and file
        s = str(i) +'\t' + rtc.get_time() + '_T_' + rtc.get_date() + '\t' + v
        print(s)
        sd.print(filename, s )
        
        # OLED must be shorter!
        s = str(i) +'\t' + rtc.get_time() +  '\t' + v
        #s = str(i) +'\t'  + v
        oled.print_s(s)
        led_measure.value(0)
        
        while (time.time() - t0 < t_interval):
            pass
        
        i += t_interval
        
        # for the extension: read voltages as array
        voltages = adc.read_all()
        addon(voltages)
    
    trigger_out.value(0)
    end_program()
    
#-----------------------------------------------------------------
def serial_loop():
    
    uart = UART(0, baudrate=19200, timeout = 5)
    
   # wait for record switch -> 0
    while (sw2.value()) == 1:
        s = "WAITING" 
        oled.print_s(s)
        s = uart.readline()
        if s:
            s = s.decode('utf-8')
            print(s, end = '\r')
            oled.print_s(s)
            time.sleep(0.1)
        
    
    # debounce
    time.sleep(0.1)
    trigger_out.value(1)
    
   
    while (sw2.value()) == 0:
        s = uart.readline()
        
        if s:
            #print(s)
            s = s.decode('utf-8')
            s = s.replace('\r', '')
            print(s, end = '')
            sd.print(filename, s)
            oled.print_s(s)
        time.sleep(0.5)

    trigger_out.value(0)
    end_program()
#---------------------------------------------------------    
filename = start_program()

''' try to import addon extension from filesystem'''
try:
    from addon import addon
except:
    def addon():
        pass
    
''' Main: analog or serial loop until stopped by user  '''   
if sw1.value():
    analog_loop()
else:
    serial_loop()
