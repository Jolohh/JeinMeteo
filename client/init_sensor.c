#include "user.h"
#include "bme280.h"
#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "init_sensor.h"


int8_t init_sensor(struct bme280_dev *dev, uint32_t *delay) {
  int8_t rslt = BME280_OK;
  uint8_t settings;

  // give sensor time to startup
  sleep_ms(5);                    // datasheet: 2ms

  // basic initialization
  dev->intf_ptr = SPI_PORT;       // SPI_PORT is an address
  dev->intf     = BME280_SPI_INTF;
  dev->read     = user_spi_read;
  dev->write    = user_spi_write;
  dev->delay_us = user_delay_us;
  rslt = bme280_init(dev);
#ifdef DEBUG
  printf("[DEBUG] chip-id: 0x%x\n",dev->chip_id);
#endif
  if (rslt != BME280_OK) {
    return rslt;
  }
  // configure for forced-mode, indoor navigation
  dev->settings.osr_h = BME280_OVERSAMPLING_1X;
  dev->settings.osr_p = BME280_OVERSAMPLING_16X;
  dev->settings.osr_t = BME280_OVERSAMPLING_2X;
  dev->settings.filter = BME280_FILTER_COEFF_16;

  settings = BME280_OSR_PRESS_SEL | BME280_OSR_TEMP_SEL | BME280_OSR_HUM_SEL | BME280_FILTER_SEL;
  if (rslt != BME280_OK) {
    return rslt;
  }
  rslt   = bme280_set_sensor_settings(settings,dev);
  *delay = bme280_cal_meas_delay(&dev->settings);
  #ifdef DEBUG
    printf("[DEBUG] delay: %u µs\n",*delay);
  #endif
  return rslt;
}