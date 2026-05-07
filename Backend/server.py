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
        self.threshold = 400
    def set_threshold(self, treshold):
        if treshold <0:
            return
        else:
            self.threshold = treshold


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

    def nastav_rgb(self, r, g, b):
        try:
            r = max(0, min(255, int(r)))
            g = max(0, min(255, int(g)))
            b = max(0, min(255, int(b)))
        except ValueError:
            return {
                "status": "error",
                "message": "RGB hodnoty musí být čísla"
            }

        prikaz = f"RGB {r} {g} {b}"
        print(prikaz)
        odpoved = self.posli_prikaz(prikaz)

        return {
            "status": "ok",
            "rgb": {
                "r": r,
                "g": g,
                "b": b
            },
            "arduino_response": odpoved
        }
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
                print(odpoved[6:])
                return int(odpoved[6:])
            except ValueError:
                return None

        return None
    def ziskej_teplotu(self):
        odpoved = self.posli_prikaz("TEMP")
        print("odpoved" + odpoved)

        if odpoved.startswith("teplota: "):
            try:
                print("teplotka" + odpoved[9:])
                return int(odpoved[9:])
            except ValueError:
                return None

        return None

    def ziskej_svetlo_status(self):
        odpoved = self.posli_prikaz("LIGHT")

        if odpoved is None:
            return None

        odpoved = odpoved.strip().upper()

        if odpoved in ["ON", "LIGHT:ON", "1", "LIGHT:1", "TRUE"]:
            return "ON"

        if odpoved in ["OFF", "LIGHT:OFF", "0", "LIGHT:0", "FALSE"]:
            return "OFF"

        return None
    def auto_mode_loop(self):
        while self.running:
            if self.automatic_mode_on:
                print("auto mode loop")

                svetlo = self.ziskej_svetlo()
                print("testovac"+str(svetlo))
                print(self.threshold)
                print("svetlo")
                if svetlo is not None:
                    print(f"[AUTO] Intenzita světla: {svetlo}")

                    if svetlo > self.threshold:
                        self.nastav_rgb(0, 0, 0)
                    else:
                        self.nastav_rgb(255, 255, 255)
                else:
                    print("[AUTO]  se přečíst intenzitu světla")

            time.sleep(1)

    def stop(self):
        self.running = False

        if self.arduino:
            self.arduino.close()