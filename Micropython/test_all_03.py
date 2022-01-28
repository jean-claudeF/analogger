import blink
import i2c_scan
from machine import Pin, I2C
import time

from OLED_SH1106_JCF import SH1106_I2C
from RTC_DS3231 import DS3231
from ADC_ADS1115_02 import ADS1115
from filetools_02 import SD
from generate_filename import  get_next_filename

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


#----------------------------------------------------------------------------------

def test_oled():
    s = "Hello \t world \t ! \t 3.14     \t The answer is \t 42"
    oled.print_s(s)
    

def test_rtc():
    print("RTC:")
    print(rtc.get_time(), '\t', rtc.get_date())
    print()




def test_adc():
    print("ADS1115 voltages:")
    v = adc.read_all_as_string()
    print(v)
    print()

def test_sdcard():
    
    if sd.error:
        print(sd.error)
    else:

        print("SD folder: ", sd.sdfolder)
        
        l = sd.listfiles()
        print("Files on SD: ", l)
        print()
             
        #sd.unmount()

def test_newfile():
    files = sd.listfiles()
    pattern = 'logger_000.dat'
    name = get_next_filename(files, pattern)
    print(name)
    sd.print(name, name)

def test_switches():
    v1 = sw1.value()
    v2 = sw2.value()
    print(v1, "\t", v2)

#----------------------------------------------------------
def test_all():
    test_oled()
    test_rtc()
    test_adc()
    test_sdcard()
    test_newfile()
    test_switches()

while (True):
    test_switches()
    time.sleep(0.1)
    

if __name__ == "__main__":
    test_all()
    
    