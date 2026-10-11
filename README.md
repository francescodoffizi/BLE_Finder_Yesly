# BLE Finder Yesly (Local Offline Bridge)

Progetto per il controllo diretto e 100% offline degli attuatori **Finder YESLY** (tapparelle `13S2`, relè/dimmer `1322`) tramite Bluetooth Low Energy (BLE) ed ESPHome, bypassando interamente il cloud Finder (`you-api.iot.findernet.com`) e il gateway hardware ufficiale (1Y.GU).

---

## 1. Obiettivi del Progetto

1. **Zero Cloud Dependency**: Eliminare le disconnessioni, la demotion silenziosa dell'app e la latenza dei server gRPC Finder.
2. **Controllo Diretto BLE**: Utilizzare le chiavi simmetriche AES-128 e i MAC address estratti dal dump dell'impianto (`GetPlant`) per inviare comandi radio cifrati direttamente agli attuatori.
3. **Integrazione ESPHome / Home Assistant**: Creare un componente personalizzato ESPHome per gestire entità cover e switch locali da Home Assistant con risposta immediata.

---

## 2. Architettura

```text
+-------------------------------------------------------------+
|                        HOME ASSISTANT                       |
|          (Entità Cover / Switch tramite API ESPHome)         |
+-------------------------------------------------------------+
                              |
                              | Native ESPHome API (WiFi / Ethernet)
                              v
+-------------------------------------------------------------+
|                 ESP32 NODE (ESPHome Firmware)               |
|  - Componente Custom: ble_finder_yesly                      |
|  - Tabella Dispositivi: MAC, Device UUID, AES-128 Key       |
|  - Radio BLE: Invio frame crittografati AES-128             |
+-------------------------------------------------------------+
                              |
                              | BLE Direct Radio (2.4 GHz)
                              v
+-------------------------------------------------------------+
|                ATTUATORI FINDER YESLY (Locale)               |
|  - 13S2 (Tapparelle motorizzate)                            |
|  - 1322 (Relè / Dimmer luci)                                |
+-------------------------------------------------------------+
```

---

## 3. Struttura del Repository

- `components/`: Componenti personalizzati ESPHome per Finder YESLY.
- `tools/`: Script Python per estrazione chiavi, analisi catture e PoC di invio pacchetti BLE.
- `docs/`: Documentazione di reverse engineering del protocollo radio BLE.
- `finder_yesly_bridge.yaml`: Esempio di configurazione firmware ESPHome.

---

## Integrazione con Home Assistant (homeassistant-finder-you)

Questo progetto lavora in stretta sinergia con [`homeassistant-finder-you`](https://github.com/francescodoffizi/homeassistant-finder-you):
- Fornisce l'encoder crittografico AES-128 / CCM per i comandi radio e i template ESPHome per il broadcasting BLE diretto.
- L'integrazione `homeassistant-finder-you` implementa un'architettura **Local-First con fallback su Cloud**: invia i comandi prima in locale tramite il proxy/bridge BLE definito in questo repo, garantendo latenza zero e resilienza offline, e ricorre ai server cloud Finder solo in caso di mancata copertura radio.

---

## 4. Licenza
MIT License

