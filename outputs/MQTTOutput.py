##
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <t3kpunk@gmail.com> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Widmar 
# ----------------------------------------------------------------------------
##

import PluginLoader
from datetime import datetime
import paho.mqtt.client as mqtt

class MQTTOutput(PluginLoader.Plugin):
    """Outputs the data from the Omnik inverter to an MQTT server """

    def process_message(self, msg):
        # New Paho client syntax for Python 3
        # use CallbackAPIVersion.VERSION1 for compatibility
        try:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Omnik Solar Inverter")
        except AttributeError:
            # Voor oudere paho-mqtt versies
            client = mqtt.Client("Omnik Solar Inverter")

        client.username_pw_set(self.config.get('mqtt', 'user'),
                               self.config.get('mqtt', 'pass'))
        
        # 3. CRUCIAAL: poort moet een 'int' zijn, geen tekst
        port = int(self.config.get('mqtt', 'port'))
        host = self.config.get('mqtt', 'host')
        
        client.connect(host, port)

        # Berichten publiceren
        client.publish("power/solar/e_total", msg.e_total)
        client.publish("power/solar/e_today", msg.e_today)
        client.publish("power/solar/h_total", msg.h_total)
        client.publish("power/solar/power", msg.power)
        client.publish("power/solar/temp", msg.temperature)

        for x in [1, 2, 3]:
            # Gebruik str(x) voor de topic naam
            client.publish("power/solar/v_pv" + str(x), msg.v_pv(x))
            client.publish("power/solar/v_ac" + str(x), msg.v_ac(x))
            client.publish("power/solar/i_ac" + str(x), msg.i_ac(x))
            client.publish("power/solar/f_ac" + str(x), msg.f_ac(x))
            client.publish("power/solar/p_ac" + str(x), msg.p_ac(x))

        client.loop(1)
        client.disconnect()
