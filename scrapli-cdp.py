from urllib import response
from scrapli.driver.core import IOSXEDriver
from devicelist import devices
from rich import print as rp


for device in devices:
    with IOSXEDriver(**device) as conn:
        response = conn.send_command("show cdp neighbor detail")
        structured_response = response.genie_parse_output()
        cdp_index = structured_response['index']
        rp(f"********** Sending Configurations to {device['host']} **********\n")
        for id in cdp_index:
            remote_device = cdp_index[id]['device_id'].split('.')[0]
            remote_port = cdp_index[id]['port_id']
            local_port = cdp_index[id]['local_interface']
            config_commands = [f"interface {local_port}", f"description Connected to {remote_device}'s {remote_port}"]
            results = conn.send_configs(config_commands)
            rp(results.result)
        rp("\n")