# Mapa del Projecte: AgenticOS

> **Actualitzat:** 2026-04-05
> **Estat:** Mapa operatiu resumit i alineat amb l'estat actual del repo

## Propòsit

Aquest document descriu **com s'ha de llegir el repositori avui**.
No substitueix:

- [README.md](/K:/AgenticOsGen/README.md) com a entrada humana curta
- [SDD_GUIDE.md](/K:/AgenticOsGen/00_project_documentation/SDD/SDD_GUIDE.md) com a flux de treball
- el codi a [02_implementation](/K:/AgenticOsGen/02_implementation/) com a veritat executable

## Estructura principal

```text
AgenticOsGen/
├── 00_project_documentation/   # Documentació viva del projecte
├── 01_design/                  # Memòria arquitectònica legacy i baseline
├── 02_implementation/          # Codi i runtime de desenvolupament
├── 03_deployments/             # Bootstrap i llavor inicial per plantar instàncies
├── 04_tools/                   # Eines de desenvolupament (context-engine, scripts)
├── AGENTS.md                   # Governança de comportament dels agents
└── README.md                   # Entrada humana curta
```

## Lectura correcta per carpeta

### `00_project_documentation/`

La capa documental principal del projecte.

Conté:

- manifest i glossari
- parking lot i ADRs
- metodologia SDD
- documents de governança externa del Kernel

Subcarpeta clau:

- [SDD/](/K:/AgenticOsGen/00_project_documentation/SDD/) = contracte de desenvolupament, specs, tasks, re-auditories i polítiques de flux

### `01_design/`

No és la font de veritat actual.

És:

- memòria arquitectònica
- baseline històrica
- exploració de futur

S'ha de llegir com a referència útil, no com a contracte vigent.

### `02_implementation/`

El codi executable i el runtime de desenvolupament.

Inclou:

- [cmd/](/K:/AgenticOsGen/02_implementation/cmd/) = binaries Go
- [internal/](/K:/AgenticOsGen/02_implementation/internal/) = core backend
- [agentic-ide/](/K:/AgenticOsGen/02_implementation/agentic-ide/) = dashboard React
- [agenticos_data/](/K:/AgenticOsGen/02_implementation/agenticos_data/) = sandbox local i dades de prova

### `03_deployments/`

No és runtime viu.

És:

- kit de bootstrap
- scripts de plantació
- seed base

La seed desplegada real ha de viure **fora del repo**.

### `04_tools/`

Utilitats de desenvolupament, no governança.

Inclou:

- [context.ps1](/K:/AgenticOsGen/04_tools/context.ps1)
- [context-engine/](/K:/AgenticOsGen/04_tools/context-engine/)

## Components principals del codi

### Backend Go

- [internal/kernel/](/K:/AgenticOsGen/02_implementation/internal/kernel/) = event loop, router, guardian, executor, worker pool
- [internal/api/](/K:/AgenticOsGen/02_implementation/internal/api/) = API REST i WebSocket
- [internal/contextbuilder/](/K:/AgenticOsGen/02_implementation/internal/contextbuilder/) = composició de prompt i eines
- [internal/engram/](/K:/AgenticOsGen/02_implementation/internal/engram/) = memòria persistent
- [internal/llm/](/K:/AgenticOsGen/02_implementation/internal/llm/) = integració amb models
- [internal/session/](/K:/AgenticOsGen/02_implementation/internal/session/) = Session Tree

### Frontend

- [02_implementation/agentic-ide/](/K:/AgenticOsGen/02_implementation/agentic-ide/) = dashboard React/Vite

## Regles de lectura

1. Per entendre el projecte: `README.md` → `00_project_documentation/` → `SDD/`
2. Per entendre decisions passades: `01_design/` i `05_ADR_DECISION_LOG.md`
3. Per entendre el comportament real: `02_implementation/`
4. Per idees o gaps: `04_PARKING_LOT.md`
5. Per utilitats: `04_tools/`

## Notes útils

- `02_implementation/agenticos_data` és per a proves locals, no per a desplegament final
- `03_deployments/setup.ps1` encara arrossega topologia legacy i no s'ha de confondre amb el runtime vigent
- `06_USER_MANUAL.md` existeix però avui no és un document fiable per onboarding final
