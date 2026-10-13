# BLE Finder Yesly (Local Offline Bridge)

Progetto per il controllo diretto e 100% offline degli attuatori **Finder YESLY** (tapparelle `13S2`, relè/dimmer `1322`) tramite Bluetooth Low Energy (BLE) ed ESPHome, bypassando interamente il cloud Finder (`you-api.iot.findernet.com`) e il gateway hardware ufficiale (1Y.GU).

---

## 1. Obiettivi del Progetto

1. **Zero Cloud Dependency**: Eliminare le disconnessioni, la demotion silenziosa dell'app e la latenza dei server gRPC Finder.
2. **Controllo Diretto BLE**: Utilizzare le chiavi simmetriche AES-128 e i MAC address configurati nell'impianto per inviare comandi radio cifrati direttamente agli attuatori.
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

- `packages/finder_yesly_mesh.yaml`: Package standard ESPHome pronto all'uso da includere in qualsiasi proxy ESP32.
- `finder_sender.h`: Motore crittografico AES-128-CCM e gestore advertising radio BLE raw.
- `bluetooth-proxy-sara.yaml`: Esempio di firmware nodo proxy reale ripulito e modulare.
- `tools/`: Script e utility Python per analisi del protocollo radio, diagnostica telemetria e PoC.

---

## 4. Come installare il supporto Finder YESLY su qualsiasi ESP32

Per abilitare il controllo diretto Finder YESLY su qualsiasi nodo ESP32 (senza modifiche custom locali o pulsanti fittizi):

Nel file di configurazione YAML del tuo ESP32 (tramite ESPHome Dashboard su Home Assistant):

```yaml
packages:
  finder_yesly:
    url: https://github.com/francescodoffizi/BLE_Finder_Yesly
    ref: main
    files: [ packages/finder_yesly_mesh.yaml, finder_sender.h ]
    refresh: 1d
```

*(Oppure scaricando `finder_sender.h` e includendo `packages/finder_yesly_mesh.yaml` localmente).*

Una volta compilato e caricato, l'ESP esporrà automaticamente via Home Assistant API i 3 servizi universali:
- `esphome.<nome_nodo>_finder_mesh_click`
- `esphome.<nome_nodo>_finder_mesh_set_percent`
- `esphome.<nome_nodo>_finder_mesh_shutter_stop`

L'integrazione Home Assistant [`homeassistant-finder-you`](https://github.com/francescodoffizi/homeassistant-finder-you) rileverà automaticamente tutti gli ESP che espongono questi servizi e instraderà ogni comando verso il nodo con il segnale radio BLE ottimale.

---

## 5. Licenza
MIT License


