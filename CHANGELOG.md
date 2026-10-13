# Changelog - BLE_Finder_Yesly

Tutte le modifiche degne di nota al componente ESPHome per il controllo dei dispositivi Finder YESLY sono documentate in questo file.

## [Unreleased]

### Aggiunto / Ottimizzato
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
