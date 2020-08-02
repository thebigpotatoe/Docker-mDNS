# Docker-mDNS

This image aims to be a very simple way of broadcasting mDNS information on a local network. Since docker does not broadcast the service name of services or containers to the local network, the motivation behind this was to allow users to broadcast where docker services are on their network with very little effort or setup.

The image is build using `python:3.8-alpine` as its base for space, but this can be changed to anything desired. Simply, the container runs a single python script which uses [python-zeroconf](https://pypi.org/project/zeroconf/) to broadcast mDNS service information to a local network.

## Quick start

To advertise where a portainer instance might be use:

``` bash
docker run \
    --network host \
    --env mdns_service_name=portainer \
    --env mdns_port=9000 \
    thebigpotatoe/docker-mdns
```

Then naviagate to your service using your browswer at :

```
http://portainer.local:9000/
```

## Build from Source

Download the repo into a know location:

``` bash
git clone https://github.com/thebigpotatoe/Docker-mDNS.git
```

To build the container from this repo simply run:

``` bash
/bin/sh scripts/build.sh
```

## Usage

### Environmental Variables

Each container is designed to broadcast and respond to one mDNS service only. Simply spawn more than one container to publish more than one service. Services are customised through environmental variables at run time, each are optional but allow users to customise their setup. These environmental variables can be input via the command line when running a docker. Please see the docker documentation for more info. A complete list is:

- mdns_hostname - The hostname to broadcast (defaults to the hostname of the container or host)
- mdns_ip_address - The IP address to broadcast (defaults to the container IP address)
- mdns_port - The port to advertise for the service (defaults to `80`)
- mdns_service_type - The mDNS service type to broadcast (defaults to `_http._tcp.local.`)
- mdns_service_name - The service name to broadcast as (defaults to mdns_hostname)
- mdns_text_services - A JSON object of service text data entries (defaults to `None`)

### Host Network

The container also needs to be run on the host network using `--network host` to both obtain the correct IP to broadcast automatically and to be able to respond to mDNS packets

### Service Texts

To supply the mDNS service with text entries, you may supply a single level JSON object as a string to be parsed. For example adding a text entry to state weather the service is production or development is as easy as:

``` bash
docker run \
    --network host \
    --env mdns_text_services={\"production\":false} \
    docker-mdns
```

## TODO

- [ ] Add ability to supply multiple services via config file

## Contributing

This image isn't perfect, so if there is anything the can be optised, pull requests are most welcome :smile:
