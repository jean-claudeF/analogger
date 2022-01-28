from machine import Pin, I2C
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
addresses = i2c.scan()
print("I2C addresses:")
for a in addresses:
    print(hex(a), '\t', a)
print()    