STATUS: TRANSITIONAL
AUTHORITY: NON-CANONICAL

This document is transitional context. It is not a source of truth for the SDD pipeline.
If it conflicts with `00_core/SDD_RUNTIME.md` (execution contract) or validated specs/ADRs, those win.

---

# Context Engine Environment Diagnosis

> **Estat:** Actiu
> **Data:** 2026-04-04
> **Abast:** Incidencia d'entorn detectada durant l'ús de `04_tools/context.ps1` des de Codex Desktop

---

## 1. Resum

El `context-engine` funciona en entorns on la sortida cap a OpenAI embeddings està disponible, i ara també degrada de forma segura a embeddings deterministes quan aquesta sortida falla.

Des de la sessió actual de Codex Desktop, la cerca semàntica falla de forma consistent amb aquest error:

`proxyconnect tcp: dial tcp 127.0.0.1:9`

La troballa més important és que això apunta a **proxy injectat per l'entorn d'execució**, no a un error estructural del repositori.

---

## 2. Evidència Observada

- `04_tools/context.ps1 search "..."` arriba fins a la fase d'OpenAI embeddings
- la petició falla abans de rebre resposta de l'API
- l'error recurrent és:
  - `Post "https://api.openai.com/v1/embeddings": proxyconnect tcp: dial tcp 127.0.0.1:9`
- en OpenCode, segons validació de l'usuari, el mateix índex i el mateix `context-engine` funcionen correctament
- a la sessió actual, després de la normalització del binari, la reindexació i la cerca continuen amb `DummyEmbedder` quan OpenAI cau

---

## 3. Diagnòstic

### El que sembla clar

- el problema **no** apunta al `chunker`
- el problema **no** apunta al `search`
- el problema **no** apunta al path actual del store
- el problema **sí** apunta a una política de xarxa/proxy de l'entorn que executa processos Go dins Codex Desktop
- el problema **ja no bloqueja l'operació** perquè el motor té fallback deterministic

### Lectura operativa

Hi ha dos comportaments diferents:

1. **OpenCode**
   - embeddings funcionals
   - cerca semàntica operativa

2. **Codex Desktop (sessió actual)**
   - embeddings remots bloquejats per proxy efectiu `127.0.0.1:9`
   - cerca semàntica no fiable quan depèn d'OpenAI

---

## 4. Impacte

- la governança que exigeix una cerca semàntica prèvia continua sent correcta
- però en aquest entorn concret s'ha d'acceptar un **fallback documentat**
- no s'ha de confondre aquesta incidència amb un defecte del model arquitectònic del `context-engine`

---

## 5. Solució Operativa Actual

Quan es treballa des d'aquest entorn:

1. intentar la cerca semàntica igualment
2. si falla amb el mateix error de proxy, deixar-ne constància
3. continuar amb lectura directa + `grep`/`Select-String`
4. el motor completarà la reindexació/cerca amb embeddings deterministes
5. si cal contrast amb OpenAI real, executar-lo des d'OpenCode o un entorn amb xarxa

---

## 6. Millores Recomanades

Aquest incident justifica millores futures al `context-engine` extern:

1. mode d'embedder explícit, no només automàtic per API key
2. mantenir el fallback local com a camí estable de primera classe
3. evitar reindexació destructiva si falla l'embedder remot
4. permetre configurar la dimensió del fallback en funció de l'índex existent

---

## 7. Conclusió

El problema actual és d'**entorn d'execució**, no de concepte del `context-engine`.

Per tant:

- no cal reobrir ara l'arquitectura del motor
- sí que convé fer-lo més resilient per a entorns restringits
