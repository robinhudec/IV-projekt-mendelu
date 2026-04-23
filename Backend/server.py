import serial
import time


class Server:
    def __init__(self, com_port='/dev/ttyACM0', baud_rate=9600):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.arduino = None
        self.automatic_mode_on = False #False = arduino je rizeno manualne z frontendu

        self.pripoj_arduino()

    def pripoj_arduino(self):
        try:
            self.arduino = serial.Serial(self.com_port, self.baud_rate)
            time.sleep(2)

            print(f"✓ Připojeno k Arduinu na {self.com_port}")

            uvital = self.arduino.readline().decode().strip()
            print(f"✓ Arduino: {uvital}")

        except Exception as e:
            print(f"✗ Chyba připojení: {e}")
            self.arduino = None

    def posli_prikaz(self, prikaz):
        if not self.arduino:
            return "ERROR: Arduino není připojeno"

        try:
            while self.arduino.in_waiting:
                self.arduino.readline()

            self.arduino.write((prikaz + '\n').encode())
            return self.arduino.readline().decode().strip()

        except Exception as e:
            return f"ERROR: {str(e)}"

    def prepni_rezim(self):
        self.automatic_mode_on = not self.automatic_mode_on
        return self.automatic_mode_on

    def stav(self):
        return {
            "arduino": "connected" if self.arduino else "disconnected",
            "automatic_mode_on": self.automatic_mode_on
        }