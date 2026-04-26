
---

## 3. `templates/spec.md` (plantilla d’especificació)

```markdown
# Spec: {{feature_name}}

**Versió:** 1.0
**Estat:** Esborrany
**Design de referència:** `SDD/artifacts/design/{{feature}}.md`

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
**RNF-01 (Rendiment):** La resposta DEURÀ ser < X ms en hardware Orange Pi sota càrrega Y.
**RNF-02 (Seguretat):** Totes les credencials DEURAN emmagatzemar-se xifrades.
**RNF-03 (Fiabilitat):** El sistema DEURÀ recuperar-se de fallades transients en X intents.

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

## Errors

| Codi | Condició | Missatge al log | Acció del sistema | Notificació? |
|------|----------|-----------------|-------------------|--------------|
| `E001` | Input invàlid | `"Invalid action: <valor>"` | Retornar 400, no persistir | ❌ |
| `E002` | LLM timeout | `"LLM timeout after Xms"` | Retry 3x, fallback mode degradat | ⚠️ |

---

## Edge Cases

- **Fallada de xarxa:** El sistema DEURÀ reintentar 3 cops amb backoff exponencial. Després, marcar el ticket com a `FAILED` i notificar.
- **Al·lucinació LLM:** Si la resposta no compleix l’esquema, el Kernel DEURÀ reintentar 3 cops (Self-Healing). Si encara falla, marcar com a `FAILED`.
- **Reinici inesperat:** El sistema DEURÀ recuperar l’estat anterior a partir de `kernel.state.json` i reprocessar els tickets actius.

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
