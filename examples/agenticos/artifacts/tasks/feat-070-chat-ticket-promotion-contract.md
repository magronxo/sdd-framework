# Tasks: feat-070 — Chat Ticket Promotion Contract

## Phase 1: Types (Infrastructure)

- [ ] 1.1 Afegir `RequestedMode string` a `ChatRequest` struct a `internal/api/types.go`
- [ ] 1.2 Crear `TicketPromotionResponse` struct a `internal/api/types.go` (ticket_id, tracking_url, status, timestamp)

## Phase 2: Core Implementation

- [ ] 2.1 Modificar `handleLLMChat` a `internal/api/handlers_dashboard.go` per evaluar `requested_mode` abans de logica LLM
- [ ] 2.2 Implementar validacio requested_mode (400 si invalid)
- [ ] 2.3 Implementar cami interactive (200 si permisos OK)
- [ ] 2.4 Implementar cami ticketed (201 si permisos OK, revalidacio)
- [ ] 2.5 Implementar cami auto (intenta interactive, fallback 202 si denegat)
- [ ] 2.6 Integrar revalidacio guardian (GetMode) + backpressure (Check) abans de crear ticket
- [ ] 2.7 Mapar `llm_chat` a `NetworkSurface` a `02_implementation/internal/kernel/mode.go`

## Phase 3: Testing

- [ ] 3.1 Afegir `TestLLMChat_WithInvalidRequestedMode_Returns400`
- [ ] 3.2 Afegir `TestLLMChat_WithTicketedMode_Returns201Or400`
- [ ] 3.3 Afegir `TestLLMChat_WithAutoMode_ITOP_Returns202Or400`
- [ ] 3.4 Afegir `TestLLMChat_RequestedModeAbsent_DefaultsToAuto`
- [ ] 3.5 Afegir `TestLLMChat_InteractiveMode_ReadOnlyDenied`
- [ ] 3.6 Afegir `TestLLMChat_AutoMode_ReadOnlyFallbackReturns403`
- [ ] 3.7 Afegir `TestLLMChat_AutoMode_MonitorFallbackReturns403`
- [ ] 3.8 Afegir `TestLLMChat_InteractiveMode_OverlaySafeModeDenied`
- [ ] 3.9 Actualitzar tests existents per compatibilitat (sense breaking change)

## Phase 4: Verification

- [ ] 4.1 Executar `go test ./internal/api/... -count=1` — verificar tots tests passen
- [ ] 4.2 Verificar que `go build ./...` compila sense errors

## Phase 5: Documentation

- [ ] 5.1 Documentar canvis a feature record JSON
- [ ] 5.2 Generar audit report
