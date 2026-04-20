# put in place for python2 vs python3 compatibility
import PluginLoader
import datetime
import urllib.parse   # Required for urllib.parse.urlencode
import urllib.request as urllib2  # Replaces the old urllib2



class PVoutputOutput(PluginLoader.Plugin):
    """Sends the data from the Omnik inverter to PVoutput.org"""

    def process_message(self, msg):
        now = datetime.datetime.now()

        if (now.minute % 5) == 0:  # # Only run at every 5 minute interval
            self.logger.info('Uploading to PVoutput')
            url = "http://pvoutput.org/service/r2/addstatus.jsp"

            # always provided data
            get_data = {
                'key': self.config.get('pvout', 'apikey'),
                'sid': self.config.get('pvout', 'sysid'),
                'd': now.strftime('%Y%m%d'),
                't': now.strftime('%H:%M'),
                'v1': msg.e_today * 1000,
                'v2': msg.p_ac(1),
                'v6': msg.v_ac(1)
            }
            
            # optionally provided data
            if self.config.getboolean('inverter', 'use_temperature'):
                get_data['v5'] = msg.temperature

            try:
                get_data_encoded = urllib.parse.urlencode(get_data)
                request_object = urllib2.Request(url + '?' + get_data_encoded)
                response = urllib2.urlopen(request_object)
                
               # Reading and decoding the bytes to text
                result = response.read().decode('utf-8')
                self.logger.info(f"PVOutput result: {result}")
            except Exception as e:
                self.logger.error(f"Error during upload: {e}")

        else:
            self.logger.info('not at a 5 minute interval')
