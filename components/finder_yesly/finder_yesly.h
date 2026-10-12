#pragma once

#include "esphome/core/component.h"
#include "esphome/core/log.h"
#include <esp_gap_ble_api.h>
#include <cstring>
#include <map>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "mbedtls/ccm.h"
#include <time.h>
#include <sys/time.h>
#ifdef USE_API
#include "esphome/components/api/custom_api_device.h"
#endif

namespace esphome {
namespace finder_yesly {

class FinderYeslyComponent : public Component {
 public:
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::AFTER_WIFI; }
};

// Rolling sequence counter stored in RTC slow memory so it survives soft reboots
RTC_DATA_ATTR static uint32_t s_finder_rolling_counter = 0;

/**
 * Calculates Finder YESLY timestamp counter based on seconds since 2019-01-01 00:00:00 UTC (1546300800).
 * Matches Finder CounterUtils.GetTimestampCounter(utcnow):
 * loc1 = (utcnow - 2019/1/1)
 * loc2 = loc1 & 0x7F
 * res = (((loc1 & 0x7FFFFF80) >> 1) ^ 0x80) ^ loc2
 */
inline uint32_t get_finder_timestamp_counter() {
    time_t now = time(nullptr);
    int64_t diff = (int64_t)now - 1546300800LL;
    // Fallback baseline if NTP is not yet synchronized (approx Oct 2026 counter ~ 122,700,000)
    if (diff < 240000000LL) {
        diff = 245436000LL;
    }
    uint32_t loc2 = (uint32_t)(diff & 0x7F);
    uint32_t counter = (((uint32_t)(diff & 0x7FFFFF80) >> 1) ^ 0x80) ^ loc2;
    return counter;
}

inline void send_finder_raw(const uint8_t *payload, size_t len) {
    if (len > 24) return;
    
    uint8_t raw_adv[31];
    uint8_t idx = 0;
    
    // Flags
    raw_adv[idx++] = 0x02;
    raw_adv[idx++] = 0x01;
    raw_adv[idx++] = 0x06;
    
    // Manufacturer Specific Data
    raw_adv[idx++] = (uint8_t)(1 + 2 + len); // Type + Company ID + payload
    raw_adv[idx++] = 0xFF;                  // Manufacturer Data
    raw_adv[idx++] = 0x61;                  // Finder Company ID (0x0561) LSB
    raw_adv[idx++] = 0x05;                  // Finder Company ID (0x0561) MSB
    
    memcpy(&raw_adv[idx], payload, len);
    idx += len;
    
    esp_ble_adv_params_t adv_params = {};
    adv_params.adv_int_min = 0x20;
    adv_params.adv_int_max = 0x20;
    adv_params.adv_type = ADV_TYPE_NONCONN_IND;
    adv_params.own_addr_type = BLE_ADDR_TYPE_PUBLIC;
    adv_params.channel_map = ADV_CHNL_ALL;
    adv_params.adv_filter_policy = ADV_FILTER_ALLOW_SCAN_ANY_CON_ANY;

    ESP_LOGI("finder_tx", "Broadcasting %d bytes raw BLE frame...", idx);
    esp_err_t err = esp_ble_gap_config_adv_data_raw(raw_adv, idx);
    if (err != ESP_OK) {
        ESP_LOGE("finder_tx", "Failed to config raw adv data: %d", err);
        return;
    }
    
    err = esp_ble_gap_start_advertising(&adv_params);
    if (err != ESP_OK) {
        ESP_LOGE("finder_tx", "Failed to start advertising: %d", err);
        return;
    }
    
    // Extended adv duration to 250ms to ensure BLE mesh packet capture
    vTaskDelay(pdMS_TO_TICKS(250));
    esp_ble_gap_stop_advertising();
    ESP_LOGI("finder_tx", "Broadcast completed successfully.");
}

inline bool send_finder_mesh_packet(const uint8_t mac[6], const uint8_t key[16], uint32_t counter, uint8_t cmd_byte) {
    uint8_t nonce[13];
    memcpy(&nonce[0], mac, 6);
    nonce[6] = (uint8_t)(counter & 0xFF);
    nonce[7] = (uint8_t)((counter >> 8) & 0xFF);
    nonce[8] = (uint8_t)((counter >> 16) & 0xFF);
    nonce[9] = (uint8_t)((counter >> 24) & 0xFF);
    nonce[10] = 0x00;
    nonce[11] = 0x00;
    nonce[12] = 0x00;

    uint8_t aad[9];
    aad[0] = 0x0C;
    aad[1] = 0xFF;
    aad[2] = 0x61;
    aad[3] = 0x05;
    memcpy(&aad[4], &nonce[6], 4);
    aad[8] = cmd_byte;

    uint8_t tag[4];
    mbedtls_ccm_context ctx;
    mbedtls_ccm_init(&ctx);
    int ret = mbedtls_ccm_setkey(&ctx, MBEDTLS_CIPHER_ID_AES, key, 128);
    if (ret != 0) {
        ESP_LOGE("finder_tx", "mbedtls_ccm_setkey failed: %d", ret);
        mbedtls_ccm_free(&ctx);
        return false;
    }

    ret = mbedtls_ccm_encrypt_and_tag(&ctx, 0, nonce, sizeof(nonce), aad, sizeof(aad), NULL, NULL, tag, sizeof(tag));
    mbedtls_ccm_free(&ctx);
    if (ret != 0) {
        ESP_LOGE("finder_tx", "mbedtls_ccm_encrypt_and_tag failed: %d", ret);
        return false;
    }

    uint8_t packet[9];
    memcpy(&packet[0], &nonce[6], 4);
    packet[4] = cmd_byte;
    memcpy(&packet[5], tag, 4);

    ESP_LOGI("finder_tx", "Sending Mesh Packet: Seq=%u (0x%08X), Cmd=0x%02X, MIC=%02X%02X%02X%02X",
             (unsigned int)counter, (unsigned int)counter, cmd_byte, tag[0], tag[1], tag[2], tag[3]);

    send_finder_raw(packet, sizeof(packet));
    return true;
}

inline void send_finder_relay_click(const uint8_t mac[6], const uint8_t key[16], uint8_t channel) {
    uint32_t ts_cnt = get_finder_timestamp_counter();
    if (s_finder_rolling_counter < ts_cnt) {
        s_finder_rolling_counter = ts_cnt;
    }

    uint8_t cmd_press = (1 << channel) ^ 1;
    uint8_t cmd_release = (1 << channel) ^ 0;

    uint32_t cnt_press = ++s_finder_rolling_counter;
    ESP_LOGI("finder_cmd", "=== Step 1/2: Sending Button Press (Channel %d, Cmd 0x%02X) ===", channel, cmd_press);
    send_finder_mesh_packet(mac, key, cnt_press, cmd_press);

    vTaskDelay(pdMS_TO_TICKS(50));

    uint32_t cnt_release = ++s_finder_rolling_counter;
    ESP_LOGI("finder_cmd", "=== Step 2/2: Sending Button Release (Channel %d, Cmd 0x%02X) ===", channel, cmd_release);
    send_finder_mesh_packet(mac, key, cnt_release, cmd_release);
}

inline void send_finder_dimmer_set(const uint8_t mac[6], const uint8_t key[16], uint8_t percent) {
    uint32_t ts_cnt = get_finder_timestamp_counter();
    if (s_finder_rolling_counter < ts_cnt) {
        s_finder_rolling_counter = ts_cnt;
    }
    if (percent > 100) percent = 100;
    uint8_t cmd = 0x80 | (percent & 0x7F);

    uint32_t cnt = ++s_finder_rolling_counter;
    ESP_LOGI("finder_cmd", "=== Sending Dimmer Set Brightness: %d%% (Cmd 0x%02X) ===", percent, cmd);
    send_finder_mesh_packet(mac, key, cnt, cmd);
}

inline void send_finder_shutter_set_position(const uint8_t mac[6], const uint8_t key[16], uint8_t percent) {
    uint32_t ts_cnt = get_finder_timestamp_counter();
    if (s_finder_rolling_counter < ts_cnt) {
        s_finder_rolling_counter = ts_cnt;
    }
    if (percent > 100) percent = 100;
    uint8_t cmd = 0x80 | (percent & 0x7F);

    uint32_t cnt = ++s_finder_rolling_counter;
    ESP_LOGI("finder_cmd", "=== Sending Shutter Set Position: %d%% (Cmd 0x%02X) ===", percent, cmd);
    send_finder_mesh_packet(mac, key, cnt, cmd);
}

inline void send_finder_shutter_open(const uint8_t mac[6], const uint8_t key[16]) {
    send_finder_relay_click(mac, key, 1);
}

inline void send_finder_shutter_close(const uint8_t mac[6], const uint8_t key[16]) {
    send_finder_relay_click(mac, key, 2);
}

inline void send_finder_shutter_stop(const uint8_t mac[6], const uint8_t key[16], uint8_t channel = 1) {
    uint32_t ts_cnt = get_finder_timestamp_counter();
    if (s_finder_rolling_counter < ts_cnt) {
        s_finder_rolling_counter = ts_cnt;
    }
    uint8_t cmd_release = (1 << channel) ^ 0;
    uint32_t cnt = ++s_finder_rolling_counter;
    ESP_LOGI("finder_cmd", "=== Shutter Stop Action (Release Cmd 0x%02X) ===", cmd_release);
    send_finder_mesh_packet(mac, key, cnt, cmd_release);
}

inline bool parse_hex_mac_str(const std::string &mac_str, uint8_t out_mac[6]) {
    std::string clean = "";
    for (char c : mac_str) {
        if (c != ':' && c != '-' && c != ' ') clean += c;
    }
    if (clean.length() != 12) return false;
    for (size_t i = 0; i < 6; i++) {
        out_mac[i] = (uint8_t)strtoul(clean.substr(i * 2, 2).c_str(), nullptr, 16);
    }
    return true;
}

inline bool parse_hex_key_str(const std::string &key_str, uint8_t out_key[16]) {
    std::string clean = "";
    for (char c : key_str) {
        if (c != ' ' && c != '-') clean += c;
    }
    if (clean.length() != 32) return false;
    for (size_t i = 0; i < 16; i++) {
        out_key[i] = (uint8_t)strtoul(clean.substr(i * 2, 2).c_str(), nullptr, 16);
    }
    return true;
}

inline void send_finder_generic_click_hex(const std::string &mac_hex, const std::string &key_hex, int channel) {
    uint8_t mac[6], key[16];
    if (!parse_hex_mac_str(mac_hex, mac) || !parse_hex_key_str(key_hex, key)) {
        ESP_LOGE("finder_dyn", "Invalid MAC (%s) or Key length", mac_hex.c_str());
        return;
    }
    send_finder_relay_click(mac, key, (uint8_t)channel);
}

inline void send_finder_generic_percent_hex(const std::string &mac_hex, const std::string &key_hex, int percent) {
    uint8_t mac[6], key[16];
    if (!parse_hex_mac_str(mac_hex, mac) || !parse_hex_key_str(key_hex, key)) {
        ESP_LOGE("finder_dyn", "Invalid MAC (%s) or Key length", mac_hex.c_str());
        return;
    }
    send_finder_dimmer_set(mac, key, (uint8_t)percent);
}

inline void send_finder_generic_shutter_stop_hex(const std::string &mac_hex, const std::string &key_hex, int channel) {
    uint8_t mac[6], key[16];
    if (!parse_hex_mac_str(mac_hex, mac) || !parse_hex_key_str(key_hex, key)) {
        ESP_LOGE("finder_dyn", "Invalid MAC (%s) or Key length", mac_hex.c_str());
        return;
    }
    send_finder_shutter_stop(mac, key, (uint8_t)channel);
}

inline void on_finder_adv_received(const std::string &mac_str, int rssi, const std::string &hex_data) {
#if defined(USE_API) && defined(USE_API_HOMEASSISTANT_SERVICES)
    if (global_api_server != nullptr && global_api_server->is_connected()) {
        esphome::api::CustomAPIDevice api_dev;
        std::map<std::string, std::string> data;
        data["mac"] = mac_str;
        data["rssi"] = std::to_string(rssi);
        data["mf"] = hex_data;
        api_dev.fire_homeassistant_event("esphome.finder_ble_adv", data);
    }
#endif
}

}  // namespace finder_yesly
}  // namespace esphome
