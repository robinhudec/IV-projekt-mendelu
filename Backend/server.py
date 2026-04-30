import serial
import time
import threading


class Server:
    def __init__(self, com_port='/dev/ttyACM0', baud_rate=9600):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.arduino = None
        self.automatic_mode_on = False
        self.running = True

        self.pripoj_arduino()

        self.auto_thread = threading.Thread(target=self.auto_mode_loop, daemon=True)
        self.auto_thread.start()

    def pripoj_arduino(self):
        try:
            self.arduino = serial.Serial(self.com_port, self.baud_rate, timeout=2)
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

    def ziskej_svetlo(self):
        odpoved = self.posli_prikaz("LIGHT")

        if odpoved.startswith("LIGHT:"):
            try:
                return int(odpoved[6:])
            except ValueError:
                return None

        return None

    def auto_mode_loop(self):
        while self.running:
            if self.automatic_mode_on:
                svetlo = self.ziskej_svetlo()

                if svetlo is not None:
                    print(f"[AUTO] Intenzita světla: {svetlo}")

                    if svetlo < 400:
                        odpoved = self.posli_prikaz("1")
                        print(f"[AUTO] Tma → LED ON: {odpoved}")
                    else:
                        odpoved = self.posli_prikaz("0")
                        print(f"[AUTO] Světlo → LED OFF: {odpoved}")
                else:
                    print("[AUTO] Nepodařilo se přečíst intenzitu světla")

            time.sleep(1)

    def stop(self):
        self.running = False

        if self.arduino:
            self.arduino.close()