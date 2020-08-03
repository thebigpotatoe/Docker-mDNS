#!/usr/bin/env python3

import os, subprocess, logging, socket, json, platform
from time import sleep
from zeroconf import IPVersion, ServiceInfo, Zeroconf

if __name__ == '__main__':
    try:
        # Start logging
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Starting python mDNS responder")

        # Create the global variables 
        zeroconf = None

        # Import environmental settings
        mdns_hostname = os.environ.get('mdns_hostname', None)
        mdns_ip_address = os.environ.get('mdns_ip_address', None)
        mdns_port = int(os.environ.get('mdns_port', 80))
        mdns_service_type = os.environ.get('mdns_service_type', "_http._tcp.local.")
        mdns_service_name = os.environ.get('mdns_service_name', None)
        mdns_text_services = os.environ.get('mdns_text_services', None)

        # Check and get the host name of the service
        if mdns_hostname is None: mdns_hostname = socket.gethostname()
        logging.info("Using hostname of: {}".format(mdns_hostname))

        # Check and get the IP address for the service
        if mdns_ip_address is None: 
            # mdns_ip_address = socket.gethostbyname(hostname)
            # mdns_ip_address = subprocess.getoutput("ifconfig eth0 | grep \"inet \" | awk \'{print $2}\'") # For ubuntu
            mdns_ip_address = subprocess.getoutput("ifconfig eth0 | grep \"inet \" | awk \'{print $2}\' | awk -F':' '{print $2}'") # For Alpine
        logging.info("Using IP address of: {}".format(mdns_ip_address))

        # Check the port 
        if mdns_port is not None:
            logging.info("Using Port of: {}".format(mdns_port))
        else:
            raise RuntimeError("mDNS service port not passed in environmental variables")

        # Check the service type
        if mdns_service_type is not None:
            logging.info("Using service type of: {}".format(mdns_service_type))
        else:
            raise RuntimeError("mDNS service type not passed in environmental variables")

        # Get and check the service name
        if mdns_service_name is not None:
            _mdns_service_name = mdns_service_name + '.' + mdns_service_type
            logging.info("Using service name of: {}".format(mdns_service_name))
        elif mdns_hostname is not None:
            mdns_service_name = mdns_hostname
            _mdns_service_name = mdns_hostname + '.' + mdns_service_type
            logging.warning("No service name passed, instead using host of {}".format(mdns_service_name))
        else:
            raise RuntimeError("mDNS service name was None")
            
        # Get and add text descriptions to service
        service_text_object = {}
        service_text_object["hostname"] = mdns_hostname
        if mdns_text_services is not None:
            service_text_object = json.loads(mdns_text_services)
            logging.info("Using service texts of: {}".format(service_text_object))
        else:
            logging.warning("No additional service text descriptions passed, using default of: {}".format(service_text_object))

        # Create the service info object
        info = ServiceInfo(
            mdns_service_type,
            _mdns_service_name,
            addresses=[socket.inet_aton(mdns_ip_address)],
            port=mdns_port,
            properties=service_text_object,
            server=mdns_service_name + '.local.'
        )

        # Start the mDNS reponder
        zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
        logging.info("Successfully started mDNS responder, try http://{}.local:{}/".format(mdns_service_name, mdns_port))

        # Add service texts to responder
        zeroconf.register_service(info)
        logging.info("Successfully added service info to mDNS responder")

        # Burn time forever
        while True: sleep(0.1)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.exception(e)
    finally:
        try:
            if zeroconf is not None:
                logging.info("Unregistering mDNS service")
                zeroconf.unregister_service(info)
                zeroconf.close()
                logging.info("Successfully stopped and unregistered mDNS service")
            else :
                logging.info("Stopping mDNS service")
        except Exception as e:
            logging.error("Failed to stop mDNS responder on shutdown")
            logging.exception(e)