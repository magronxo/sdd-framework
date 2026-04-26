# Spec Re-Audit feat-013

> **Estat:** Actiu
> **Data:** 2026-04-04
> **Abast:** `feat-013-session-tree`

## Resum

`feat-013-session-tree` no s'ha de tancar encara.

La spec i el design ja descriuen un contracte coherent per a Session Tree, però el task file mostra que encara queden punts vius de producte i validació. Això la converteix en una spec activa, no en un cas de normalització documental tancada.

## Fitxers revisats

- `00_project_documentation/SDD/specs/feat-013-session-tree.md`
- `00_project_documentation/SDD/design/feat-013-session-tree.md`
- `00_project_documentation/SDD/tasks/feat-013-session-tree.md`
- `00_project_documentation/SDD/features_for_specs/feat-013.json`

## Observacions

- El feature record continua en `SPEC`, que és coherent amb l'estat actual
- El task file indica `IMPLEMENTING (MVP Parcial)` i encara té pendents
- El design encara conté preguntes obertes que no s'han de forçar a fals tancament
- L'ecosistema documental de `feat-013` és consistent com a bloc actiu

## Conclusions

- `feat-013-session-tree` és el següent cas viu
- No es marca `DONE`
- No cal tocar runtime ni reescriure el contracte ara mateix

## Criteri de sortida

Aquest cas només s'haurà de reobrir per normalització documental si apareix una contradicció real entre:

- `spec`
- `design`
- `tasks`
- `feature record`

Mentrestant, `feat-013` s'ha de tractar com a MVP parcial actiu. Els fitxers fonamentals del projecte no s'han de modificar per aquest cas tret que el feedback extern aporti una regla nova de governança o un conflicte estructural verificable.

## Notes

- Aquest cas és útil com a benchmark per comparar el feedback de Gemini i altres auditors
- Les properes passes haurien de centrar-se en tancar pendents reals, no en normalitzar per aparença
