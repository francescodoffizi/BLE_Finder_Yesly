# Changelog - BLE_Finder_Yesly

Tutte le modifiche degne di nota al componente ESPHome per il controllo dei dispositivi Finder YESLY sono documentate in questo file.

## [Unreleased]

- **Mitigazione Tempesta RF BLE & Passaggio a Scansione Passiva (`active: false`)**:
  - Convertita la modalità di scansione di `esp32_ble_tracker` da attiva a passiva (`active: false`), eliminando l'invio continuo di pacchetti `SCAN_REQ` da parte dei proxy ESP32 che saturavano l'etere a 2.4 GHz e collassavano la mesh YESLY.
- **Deduplicazione Hardware e Rate Limiting Telemetria (`s_adv_cache`)**:
  - Introdotta cache LRU in RAM (`AdvCacheEntry`) su ESP32 per sopprimere payload duplicati entro 2500 ms e imporre un rate-limit massimo di 1 pacchetto/sec per MAC, abbattendo il carico di eventi verso Home Assistant da >6000/min a soli frame effettivi di stato.
- **Interruttore di Emergenza Telemetria (`switch.finder_telemetry_forwarding`)**:
  - Esporto switch template in Home Assistant per silenziare/riattivare istantaneamente l'inoltro di eventi `esphome.finder_ble_adv` senza ricompilare o riavviare i nodi.
- **Licenza Ufficiale MIT**:
  - Introdotto file `LICENSE` con titolarità `Copyright (c) 2026 Francesco D'Offizi`.
- **Bonifica Documentazione e Interoperabilità**:
  - Revisionato `README.md` focalizzando la descrizione del progetto su interoperabilità di rete BLE, standard crittografici e controllo offline diretto.
  - Normalizzati gli script di test interni e validazione protocollo AES-CCM.
- **Sincronizzazione Dinamica del Sequence Counter con Epoch UTC 2019-01-01**:
  - Allineata la formula del contatore rolling alla logica proprietaria Finder (`CounterUtils.GetTimestampCounter(utcnow)`).
  - Previene che i frame BLE vengano rigettati come comandi replay/stale dai relè fisici YESLY.
- **Estensione Durata Advertising Burst a 250 ms**:
  - Aumentato il tempo di trasmissione in raw advertising (`ADV_TYPE_NONCONN_IND`) da 100 ms a 250 ms con intervallo tra Press e Release di 50 ms per garantire una ricezione affidabile da parte dei nodi riceventi.

---

## [1.0.0] - 2026-10-10
- Componente nativo ESPHome `finder_yesly` per ESP32.
- Supporto crittografia hardware AES-CCM a 128 bit per frame radio compatibili Finder YESLY.
- Azioni native `finder_mesh_click` e `finder_mesh_set_percent`.
