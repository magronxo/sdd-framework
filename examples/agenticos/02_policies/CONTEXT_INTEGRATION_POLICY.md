# Context Integration Policy

> **Estat:** Actiu  
> **Data:** 2026-04-04  
> **Abast:** Ús del `context-engine` dins del desenvolupament extern del Kernel

---

## 1. Propòsit

El `context-engine` no és un substitut de pensament arquitectònic. És una eina de recuperació semàntica per reduir punts cecs quan el volum de fitxers o la dispersió del coneixement fan insuficient la lectura directa.

Aquest document defineix **quan és obligatori**, **quan és recomanat** i **quan no cal**.

---

## 2. Principi General

**Metadata > embeddings > intuïció.**

L'ordre correcte és:

1. entendre el problema
2. saber quin context falta
3. llançar cerca semàntica acotada
4. contrastar amb lectura directa dels fitxers retornats

No al revés.

### Regla de complementarietat

El `context-engine` és millor per a **descobriment**.

La cerca textual (`grep`, `rg`, `Select-String`) és millor per a **localització precisa**.

**Regla:** el `context-engine` no substitueix `grep`. El complementa.

---

## 3. Ús Obligatori

S'ha d'intentar usar `04_tools/context.ps1 search "..."` abans de:

- canvis significatius de governança (>3 fitxers o >100 línies)
- refactors transversals de flux o procés
- redefinir skills, context o integracions externes
- re-auditories de specs a escala
- mapejar relacions entre documents i implementació

---

## 4. Ús Recomanat

És recomanat quan:

- hi ha massa documents relacionats amb el mateix concepte
- s'intueix que hi ha contradiccions documentals
- cal localitzar una capacitat sense saber a quin fitxer viu
- es comparen marcs externs amb primitives internes

---

## 5. Ús No Necessari

No cal quan:

- el canvi és local i ben delimitat
- el fitxer objectiu ja és conegut
- s'està fent una revisió petita d'un document concret
- el problema és conceptual i encara no cal recuperar corpus

---

## 6. Flux Operatiu

### Pas 1. Formular la consulta

La query ha de descriure el problema, no només paraules soltes.

**Bé:**
- `"external kernel development workflow skills context integration"`
- `"ticket lifecycle archive processing validation"`

**Malament:**
- `"skills"`
- `"context"`

### Pas 2. Revisar resultats

El resultat del context-engine no es considera font final. Només és una guia de localització.

### Pas 3. Confirmar amb lectura directa

Els fitxers retornats s'han de llegir abans de proposar canvis.

### Pas 3b. Localitzar amb cerca textual

Quan ja s'ha identificat el fitxer o la zona probable, s'ha d'usar cerca textual o lectura directa per trobar:

- símbols
- línies concretes
- camps exactes
- punts de contradicció

### Pas 4. Documentar limitacions

Si la cerca falla per entorn, proxy, índex obsolet o embeddings no disponibles, s'ha de deixar constància i continuar amb lectura directa.

---

## 7. Política de Fallback

Si el `context-engine` falla:

1. no inventar context
2. continuar amb lectura directa i cerca textual
3. deixar constància que la cerca semàntica s'ha intentat
4. no bloquejar tot el flux per una incidència d'infraestructura externa

---

## 8. Context de Desenvolupament vs Context de Runtime

### Context de Desenvolupament

Inclou:

- docs del projecte
- specs, tasks, auditories
- skills
- marcs externs
- decisions de governança

### Context de Runtime

Inclou:

- prompts interns
- context builder del runtime
- tickets actius
- memòria del sistema
- estat operatiu del Kernel

**Regla:** Les dues capes poden compartir conceptes, però no s'han de confondre.

---

## 9. Anti-Patrons

- usar embeddings per evitar llegir els fitxers reals
- usar el context-engine per justificar canvis que ja estaven decidits
- fer cerques enormes i vagues
- convertir qualsevol tasca petita en dependència del context-engine

---

## 10. Criteri d'Èxit

La política de context funciona quan:

- el context-engine redueix soroll en canvis grans
- no substitueix la lectura directa
- les consultes estan justificades
- el sistema continua sent operable si la infraestructura semàntica falla
