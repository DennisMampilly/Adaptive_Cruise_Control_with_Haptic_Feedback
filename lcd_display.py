import I2C_LCD_driver

lcd = I2C_LCD_driver.lcd()

def show_message(message):

    lcd.lcd_clear()

    lcd.lcd_display_string(
        message.center(16),
        1
    )
