docker run \
    -it \
    --rm \
    --network host \
    --env mdns_service_name=portainer \
    --env mdns_port=9000 \
    docker-mdns