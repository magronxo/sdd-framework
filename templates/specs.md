# Spec: {{feature_name}}

**Versió:** 1.0
**Estat:** Esborrany
**Design de referència:** `artifacts/design/{{feature}}.md`

---

## Context
<!-- Per què existeix aquesta especificació? Quina necessitat resol? -->

---

## Goals
- [ ] Goal 1: mesurable
- [ ] Goal 2: mesurable

---

## Non-Goals
- ❌ No s’inclou X
- ❌ No s’integra amb Y

---

## Requirements

### Funcionals
**RF-01:** El sistema DEURÀ [comportament] quan [condició].
**RF-02:** El sistema PODRÀ [comportament opcional] si [condició].
**RF-03:** El sistema NO DEURÀ [comportament prohibit].

### No Funcionals
**RNF-01 (Rendiment):** La resposta DEURÀ ser < X ms sota càrrega Y.
**RNF-02 (Seguretat):** Totes les credencials DEURAN emmagatzemar-se xifrades.
**RNF-03 (Fiabilitat):** El sistema DEURÀ recuperar-se de fallades transients en X intents.

---

## Type Definitions

Defineix els tipus de dades propis d'aquesta feature (structs, enums, unions):

```
Type: ModelStatus
  Values: PENDING | DOWNLOADING | READY | FAILED | ARCHIVED

Type: DownloadConfig
  Fields:
    - model_id: string (format: "org/model-name")
    - quantization: string | null
    - max_workers: int (default: 1, max: 8)
    - resume: boolean (default: true)
```

---

## Inputs

| Camp | Tipus | Font | Validació | Exemple |
|------|-------|------|-----------|---------|
| `user_id` | `string (UUID)` | Header HTTP | Format UUID, no buit | `"550e8400-..."` |
| `action` | `enum` | Body JSON | Valors: `[start, stop]` | `"start"` |

---

## Outputs

| Camp | Tipus | Condició d’emissió | Exemple |
|------|-------|-------------------|---------|
| `status` | `string` | Èxit | `"ok"` |
| `error` | `object` | Qualsevol error | `{"code": "E001", "message": "..."}` |

---

## Concurrency Model (Opcional)

Omple aquesta secció si la feature implica més d'un fil d'execució.

| Aspecte | Decisió |
|---------|---------|
| **Model** | [sequential / parallel / actor / CSP / async-await / thread-pool] |
| **Max parallelism** | X workers / goroutines / threads |
| **Shared state** | [Què es comparteix i com es protegeix: mutex, channel, atomics, etc.] |
| **Ordering guarantees** | [FIFO / LIFO / unordered / priority queue] |
| **Cancellation** | [Com es cancel·len tasques en curs: context, signals, etc.] |

---

## Performance Budget (Opcional)

Omple aquesta secció si la feature té requisits de rendiment estrictes.

| Mètrica | Límit | Com es mesura |
|---------|-------|---------------|
| **Latency (p50)** | < X ms | [Benchmark / test unitari / endpoint] |
| **Latency (p99)** | < X ms | [Benchmark / test unitari / endpoint] |
| **Throughput** | > X req/s | [Load test] |
| **Memory (steady)** | < X MB | [pprof / runtime metric] |
| **Memory (peak)** | < X MB | [pprof / runtime metric] |
| **CPU (steady)** | < X% core | [perf / runtime metric] |

---

## Invariants (Opcional)

> **Inspirat en TLA+**: propietats que sempre han de ser certes, independentment del camí d'execució.

Omple aquesta secció si la feature té propietats que mai es poden trencar.

| ID | Invariant | Com es verifica |
|----|-----------|----------------|
| **INV-01** | `[Propietat que sempre és certa]` | `[Test / assert / monitor]` |
| **INV-02** | `[Propietat que sempre és certa]` | `[Test / assert / monitor]` |

**Exemples**:
- "Un usuari mai pot tenir saldo negatiu"
- "El sistema sempre respon en < 100ms"
- "No hi pot haver dos processos actius amb el mateix ID"

---

## Errors

| Codi | Condició | Missatge al log | Acció del sistema | Notificació? |
|------|----------|-----------------|-------------------|--------------|
| `E001` | Input invàlid | `"Invalid action: <valor>"` | Retornar 400, no persistir | ❌ |
| `E002` | Timeout extern | `"Timeout after Xms"` | Retry 3x, fallback mode degradat | ⚠️ |

---

## Edge Cases

- **Fallada de xarxa:** El sistema DEURÀ reintentar 3 cops amb backoff exponencial. Després, marcar com a `FAILED` i notificar.
- **Input inesperat:** Si la resposta no compleix l’esquema, el sistema DEURÀ reintentar 3 cops. Si encara falla, marcar com a `FAILED`.
- **Reinici inesperat:** El sistema DEURÀ recuperar l’estat anterior a partir de l’estat persistent i reprocessar les tasques actives.

---

## Acceptance Criteria (Gherkin)

```gherkin
Scenario: <Nom del cas principal>
  Given <estat inicial>
  When  <acció>
  Then  <resultat observable>

Scenario: Error E001 – Input invàlid
  Given una sol·licitud amb camp `action` buit
  When  el sistema valida l’input
  Then  retorna error 400 amb codi E001
  And   no persisteix cap canvi
```

---

## Dependencies

- [Dependency 1]
- [Dependency 2]

---

**SDT Scenarios:**
- Happy Path: [descripció]
- Edge Case: [descripció]
- Failure Mode: [descripció]
