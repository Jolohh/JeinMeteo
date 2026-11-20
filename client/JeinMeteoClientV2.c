// --------------------------------------------------------------------------
// Read BME280 sensor values with a Raspberry Pi Pico using the official Bosch-API
//
// Author: Bernhard Bablok
//
// https://github.com/bablokb/pico-bme280
// --------------------------------------------------------------------------

#include <hardware/gpio.h>
#include <pico/time.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>
#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "hardware/adc.h"
#include "pico/cyw43_arch.h"
#include "lwip/apps/mqtt.h"
#include "pico/unique_id.h"

//#include "user.h"
#include "bme280.h"
#include "init_sensor.h"
#include "mqttClient.h"
#include "cJson.h"

#include "config.h"

#define GPIO_DONE 11
#define BAT_ADC_CHANNEL 0
#define BAT_MEAN_N 100
#define WIFI_TIMEOUT 10000



mqtt_client_t *static_client;



// ---------------------------------------------------------------------------
// hardware-specific intialization
// SPI_* constants from CMakeLists.txt or user.h

void init_hw() {
  /*initialize GPIO Pins, set done pin to LOW*/
  gpio_init(GPIO_DONE);
  gpio_set_dir(GPIO_DONE,GPIO_OUT);
  gpio_pull_down(GPIO_DONE);
  gpio_put(GPIO_DONE,0);

  /*initialize ADC pin*/
  adc_init();
  adc_gpio_init(26);
  adc_select_input(BAT_ADC_CHANNEL);

  stdio_init_all();
  spi_init(SPI_PORT, 1000000);                // SPI with 1Mhz
  gpio_set_function(SPI_RX, GPIO_FUNC_SPI);
  gpio_set_function(SPI_SCK,GPIO_FUNC_SPI);
  gpio_set_function(SPI_TX, GPIO_FUNC_SPI);

  gpio_init(SPI_CS);
  gpio_set_dir(SPI_CS, GPIO_OUT);
  gpio_put(SPI_CS, 1);                        // Chip select is active-low
}

// ---------------------------------------------------------------------------
// get battery_level()

float get_battery_level()
{
  uint32_t raw = 0;
  for (int i = 0; i<BAT_MEAN_N; i++)
  {
    raw += adc_read();
    sleep_ms(1);
  }
  float_t voltage_at_pin = (float)raw / BAT_MEAN_N; 

  voltage_at_pin = voltage_at_pin * (3.3f / 4095.0f); // Apply linear correction factor of 0.025
  
  //printf("Raw: %d, half pin voltage: %.2fV\n", raw, voltage_at_pin);

  return (voltage_at_pin * 2);
}

// ---------------------------------------------------------------------------
// read sensor values

int8_t read_sensor(struct bme280_dev *dev, uint32_t *delay,
                   struct bme280_data *data) {
  int8_t rslt;
  rslt = bme280_set_sensor_mode(BME280_FORCED_MODE, dev);
  if (rslt != BME280_OK) {
    return rslt;
  }
  dev->delay_us(*delay,dev->intf_ptr);
  return bme280_get_sensor_data(BME280_ALL,data,dev);
}

// ---------------------------------------------------------------------------
// print sensor data to console

void print_data(struct bme280_data *data) {
  float temp, press, hum;
  float alt_fac = pow(1.0-ALTITUDE_AT_LOC/44330.0, 5.255);

  temp  = 0.01f * data->temperature;
  press = 0.01f * data->pressure/alt_fac;
  hum   = 1.0f / 1024.0f * data->humidity;
  printf("%0.1f deg C, %0.0f hPa, %0.0f%%\n", temp, press, hum);
}

// ---------------------------------------------------------------------------
// sensor data to json

char* get_json(struct bme280_data *data, float battery_level) {
    float temp, press, hum;
    float alt_fac = pow(1.0-ALTITUDE_AT_LOC/44330.0, 5.255);

    cJSON *root = cJSON_CreateObject();
    if (root == NULL) return NULL;

    char buf[16];

    temp = 0.01f * data->temperature;
    snprintf(buf, sizeof(buf), "%.4f", temp);
    cJSON_AddRawToObject(root, "temperature", buf);

    press = 0.01f * data->pressure/alt_fac;
    snprintf(buf, sizeof(buf), "%.2f", press); 
    cJSON_AddRawToObject(root, "pressure", buf);

    hum   = 1.0f / 1024.0f * data->humidity;
    snprintf(buf, sizeof(buf), "%.2f", hum);
    cJSON_AddRawToObject(root, "humidity", buf);

    snprintf(buf, sizeof(buf), "%.4f", battery_level);
    cJSON_AddRawToObject(root, "battery_level", buf);

    char *out = cJSON_Print(root);

    cJSON_Delete(root);

    return out; // Note: The caller must free() this string!
}



// ---------------------------------------------------------------------------
// main loop: read data and send to mqtt broker


int main() {
  // init gpio pins and initialize sensor
  init_hw();
  struct bme280_dev dev;
  struct bme280_data sensor_data;
  uint32_t delay;               // calculated delay between measurements
  int8_t rslt = init_sensor(&dev,&delay);

  // get battery voltage
  sleep_ms(50); // wait for voltages to stabilize
  float battery_level = get_battery_level();

  absolute_time_t t_start = get_absolute_time();
  // connect to wifi
  if (cyw43_arch_init() != 0)
  {
    printf("error with wifi chip\n");
    sleep_ms(200);
    gpio_put(GPIO_DONE,1);
  }
  cyw43_arch_enable_sta_mode();
  cyw43_wifi_pm(&cyw43_state, CYW43_NO_POWERSAVE_MODE);
  if (cyw43_arch_wifi_connect_timeout_ms(WIFI_SSID, WIFI_PASSWORD, CYW43_AUTH_WPA2_AES_PSK,WIFI_TIMEOUT)) {
      printf("error with wifi\n");
      sleep_ms(200);
      gpio_put(GPIO_DONE,1);
  }
  printf("wifi: %lld ms\n", absolute_time_diff_us(t_start, get_absolute_time()) / 1000);

  // create unique id
  int lenidString = 2*(PICO_UNIQUE_BOARD_ID_SIZE_BYTES+1);
  char idString[lenidString];
  pico_get_unique_board_id_string(idString,lenidString);
  
  // connect to mqtt broker
  ip_addr_t broker_addr;
  ipaddr_aton(MQTT_BROKER_IP, &broker_addr);

  struct mqtt_connect_client_info_t ci = {0};
  ci.client_user = MQTT_USERNAME;
  ci.client_pass = MQTT_PASSWORD;
  ci.client_id = idString;

  static_client = mqtt_client_new();
  if (mqtt_client_connect(static_client, &broker_addr, MQTT_PORT, mqtt_connection_cb, NULL, &ci) != 0)
  {
    printf("error with mqtt\n");
    sleep_ms(200);
    gpio_put(GPIO_DONE,1);
  }
  int mqtt_timeout = 0;
  while (!mqtt_client_is_connected(static_client)) {
    sleep_ms(10);
    mqtt_timeout++;
    if (mqtt_timeout > 2000) { // 5 second timeout
        printf("mqtt connection timeout\n");
        gpio_put(GPIO_DONE, 1); 
    }
  }
  
  printf("mqtt: %lld ms\n", absolute_time_diff_us(t_start, get_absolute_time()) / 1000);
  // get data and publish
  if (rslt == BME280_OK)
  {
    //printf("Temperature, Pressure, Humidity\n"); 
    read_sensor(&dev,&delay,&sensor_data);
    //print_data(&sensor_data);
    
    // create and publish message
    char *json_str = get_json(&sensor_data, battery_level);
    char topic[32];
    snprintf(topic, sizeof(topic), "sensor/%s", idString);
 
    publish_message(static_client, topic, json_str);

    free(json_str);

  } else 
  {
    // if sensor not available send message on debug channel
    char message[64];
    snprintf(message, sizeof(message), "could not initialize sensor. RC:%d", rslt);

    char topic[32] = "debug/";
    snprintf(topic, sizeof(topic), "debug/%s", idString);

    publish_message(static_client, topic, message);
  } 

  /*put PICO to sleep*/
  sleep_ms(500);
  gpio_put(GPIO_DONE,1);
}