# Ticket Contract Audit 2026-04-05
**Data:** 2026-04-05  
**Tipus:** Auditoria curta de contracte vs runtime  
**Abast:** flux real de ticket a `02_implementation` contrastat amb manifest, SDD operating flow i baseline legacy `01_design/02_TICKET_SYSTEM.md`  
**Resultat Global:** WARN  
**Risc Global:** Alt si es tracta el ticket system com a contracte universal ja consolidat

## Resum Executiu
El runtime actual **sí processa tickets** de punta a punta, però el contracte real és avui un **pipeline mínim executable**, no una màquina d'estats universal rica i persistent.

La lectura correcta és aquesta:
- hi ha flux usable per tickets directes i `llm_agent`
- no hi ha encara correspondència forta entre el contracte documental i el contracte runtime
- el gap crític no és "falta una feature menor"
- el gap crític és que **el model de ticket vigent no està congelat**

## Mapa del Flux Actual
1. Entrada a `tickets/incoming` via scheduler, API o bridge.
2. `EventLoop` detecta fitxers `.json` i dispara `OnNewTicket`.
3. `LoadBalancer` decideix `ALLOW`, `DELAY`, `SPOOL` o `REJECT`.
4. `Router.AcquireTicket()` mou el fitxer a `tickets/processing` i persisteix `PROCESSING`.
5. `WorkerPool` processa el ticket en memòria.
6. Ruta A, ticket directe: validar tool, validar path si existeix, executar tool, completar o fallar.
7. Ruta B, `llm_agent`: construir context, cridar LLM, parsejar JSON, validar tool/path per iteració, executar eina, continuar loop o tancar.
8. Tancament binari: `tickets/success` amb `COMPLETED` o `tickets/failed` amb `FAILED`.

## Matriu Contracte vs Runtime
| Àrea | Contracte documental esperat | Runtime actual | Gap real | Severitat | Decisió |
|---|---|---|---|---|---|
| Schema del ticket | Ticket ric amb `metadata`, `request`, `steps`, `final_resolution`, `metrics`, `hash` | Struct curt amb `id`, `type`, `status`, `created_at`, `payload`, `result`, `error` | El contracte universal no està implementat | CRÍTICA | Congelar schema runtime vigent abans de continuar |
| FSM persistent | 11 estats de repòs i transicions explícites | Persistència real sobretot de `PROCESSING`, `COMPLETED`, `FAILED` | La FSM prometuda no governa el runtime | CRÍTICA | Definir FSM mínima real i fer-la persistent |
| Auditoria del loop | `steps[]` com a traça de reasoning/audit/result | El loop existeix però la traça no queda cristal·litzada al ticket | Sense glass box real | CRÍTICA | Persistir passos per iteració |
| HITL / approvals | `REQUIRES_HUMAN`, `.approval.json`, retorn `APPROVED/REJECTED` | API/dashboard d'approval existeixen, però no hi ha cablejat clar al kernel de ticket | Capacitat promesa però no operativa | ALTA | O connectar-la o treure-la del contracte actiu |
| Load shedding | `REJECT` o espera controlada amb conseqüència sobre el ticket | `REJECT` al `LoadBalancer` però al `main` queda com `TODO` | Sobrecàrrega sense tancament coherent | ALTA | Tancar el cas `REJECT` amb error explícit |
| Recovery/staleness | Tickets zombis detectats i recuperats amb contracte clar | `StaleDetector` usa estructura de directoris que no coincideix amb la real; `WorkerPool` reencola tickets mínims | Recuperació potencialment corruptora | ALTA | Redissenyar recovery contra el contracte real |
| Context/memòria | Context rellevant per topic/agent/departament | `FetchMemory` llista engrams globals i ignora `topicKeys` | Soroll contextual, poca utilitat productiva | ALTA | Filtrar memòria per topic i àmbit |
| Routing departamental | Ticket com a RPC robust entre departaments/seeds | Hi ha resolució agent/departament per `llm_agent`, però sense contracte ric de delegació/callback | Delegació parcial, no universal | MITJA | Deferir fins congelar schema base |
| Observabilitat | Estat de ticket com a font única per UI i auditoria | API/TUI observen directoris bàsics i estats simples | Observabilitat depèn d'un model massa pobre | MITJA | Millorar després d'estabilitzar FSM |
| Legacy baseline | Document legacy com a baseline, no contracte vigent | El document encara conté llenguatge de "font de veritat" | Pot generar implementacions equivocades | MITJA | Reclassificar-lo explícitament com a baseline no vigent |

## Riscos
- **Risc de contracte fals:** nous canvis poden implementar el document legacy en lloc del runtime real.
- **Risc d'operació opaca:** sense `steps`, l'operador no pot reconstruir què ha passat dins d'un ticket LLM.
- **Risc de recovery defectuós:** la reencolada de tickets encallats pot recrear tickets incoherents.
- **Risc de governança buida:** approvals, auditing i waiting existeixen més com a intenció que com a comportament executable.
- **Risc de qualitat del producte:** la memòria injectada és global i sorollosa just on hauria de donar precisió.

## Prioritat de Treball
### P0. Congelar el contracte runtime del ticket
- Decidir quin schema és vigent de debò.
- Alinear documentació viva i codi.
- Aturar expansió funcional fins tancar aquesta decisió.

### P1. Fer real una FSM mínima usable
- Persistir com a mínim `PENDING -> PROCESSING -> AUDITING -> EXECUTING -> COMPLETED/FAILED`.
- Introduir `WAITING` i `REQUIRES_HUMAN` només si es connecten de debò.

### P2. Persistir traça del loop agentic
- Guardar `steps` amb intenció, validació i resultat.
- Fer que el ticket sigui auditable sense dependre del log de consola.

### P3. Corregir recoverability
- Tancar la branca `REJECT`.
- Redissenyar stale detection perquè parli amb l'estructura real.
- Eliminar la reencolada de tickets mínims sense payload complet.

### P4. Fer la memòria realment útil
- Aplicar filtratge per `topic_keys`.
- Separar memòria per departament/agent o scope equivalent.

## Veredicte
El ticket system actual és **base funcional de processament**, però **encara no és el contracte universal d'AgenticOS**.

La següent decisió correcta no és afegir més comportaments damunt del model actual. La decisió correcta és **fixar el contracte runtime del ticket** i fer que la documentació deixi d'explicar un sistema més avançat del que existeix.
