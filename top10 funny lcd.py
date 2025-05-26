from RPLCD.i2c import CharLCD
import datetime
import time


lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)

lcd.close(clear=True)
society = False
if society:
    lcd.write_shift_mode(0)
    lcd.write(0b11110100)
    lcd.cursor_pos = (1, 7)
    lcd.write(0b11110110)


a = True
while a:
    y = datetime.datetime.now().time().isoformat('seconds')
    #lcd.clear()
    lcd.cursor_pos = (0, 3)
    lcd.write_string(y) 
    #time.sleep(1)
#7355608
bomb = False
while bomb:
    lcd.clear()
    lcd.write_string("tick-tock tick-tock")
    lcd.cursor_pos = (0, 1)
    time.sleep(10)
    lcd.clear()

    lcd.write_string("BOOM UR DED")
    bomb = False





exit()