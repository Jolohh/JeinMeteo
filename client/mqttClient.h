#pragma once
#include "lwip/apps/mqtt.h"


void mqtt_connection_cb(mqtt_client_t *client, void *arg, mqtt_connection_status_t status);

void publish_message(mqtt_client_t *client, const char *topic, const char *payload);

