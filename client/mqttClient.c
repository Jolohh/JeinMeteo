#include"mqttClient.h"
#include<string.h>

#define QOS 1


void mqtt_connection_cb(mqtt_client_t *client, void *arg, mqtt_connection_status_t status) {
    printf("Callback called");
    if (status == MQTT_CONNECT_ACCEPTED) {
            printf("Connected to Broker!\n");
        } else {
            printf("Error: %d\n", status);
        }
};




void publish_message(mqtt_client_t *client, const char *topic, const char *payload) {
    if (mqtt_client_is_connected(client)) {
        err_t err = mqtt_publish(client, topic, payload, strlen(payload), QOS, 0, NULL, NULL);
        if (err != ERR_OK) {
            printf("Publish failed with: %d\n", err);
        } else {
            printf("Published: %s\n", payload);
            printf("on topic:%s\n",topic);
        }
    } else
    {
        printf("client not connected");
    }
};


