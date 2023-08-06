from .submaker import Submaker
from inception.generators.wpasupplicantconf import WPASupplicantConfGenerator
import os
import logging

logger = logging.getLogger(__name__ )
class WifiSubmaker(Submaker):
    def make(self, workDir):
        aps = self.getValue("aps", [])

        if not len(aps):
            return

        wpaSupplicantData= {
            "mode": "0660",
            "gid": "1010",
            "uid": "1010",
            "context": "u:object_r:wifi_data_file:s0"
        }
        wifiDirData = {
            "mode": "0770",
            "mode_dirs": "0770",
            "gid": "1010",
            "uid": "1010",
            "context": "u:object_r:wifi_data_file:s0"
        }

        self.setValue("update.files.add./data/misc/wifi", wifiDirData)
        self.setValue("update.files.add./data/misc/wifi/wpa_supplicant\.conf", wpaSupplicantData)

        gen = WPASupplicantConfGenerator()
        gen.setWorkDir(workDir)

        for ap in aps:
            ssid = ap["ssid"]
            key = ap["key"] if "key" in ap else None
            security = ap["security"] if "security" in ap else None
            security = "WPA-PSK" if key and not security else security
            hidden = ap["hidden"] if "hidden" in ap else False
            prioriy = ap["priority"] if "priority" in ap else 1

            logger.debug("Adding SSID %s" % ssid)

            if security == "WPA-EAP":
                gen.add_eap_tls_network(
                    ssid,
                    ap["eap"],
                    ap["identity"],
                    ap["ca_cert"],
                    ap["client_cert"],
                    ap["key_id"],
                    engine_id=ap["engine_id"] if "engine_id" in ap else None,
                    hidden=hidden
                )
            else:
                gen.addNetwork(ssid, security, key, hidden, prioriy)

        generated = gen.generate()

        if not os.path.exists(workDir):
            os.makedirs(workDir)

        wpaSupplicantFilePath = os.path.join(workDir, "wpa_supplicant.conf")
        wpaSupplicantFile = open(wpaSupplicantFilePath, "w")
        wpaSupplicantFile.write(generated.encode("utf-8"))
        wpaSupplicantFile.close()