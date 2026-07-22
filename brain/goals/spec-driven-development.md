# [ craft | engineering | now ] spec-driven development

Transicionar o workspace inteiro pra SPEC-DRIVE DEVELOPMENT — todo módulo tem entradas/saídas bem definidas e verificáveis, e a spec é o contrato. Specs viram a fonte da verdade; código sem spec é dívida. Aplica a `code/`, a `core/flows`, e à árvore de loops (ver [[loop-engineering]] [[prompt-dsl]] em loop-engineering). Precede o código, não documenta depois.

> **linked work** — the `core/` agent-library pilot of this idea shipped 2026-07-18: an enforced
> per-layer frontmatter contract ([core/SCHEMA.md](../../core/SCHEMA.md)), tier unified, pilot flow
> `compare` normalized, validation in `sync-skills` + pre-commit. Sweep tracked in
> [core/ROADMAP.md](../../core/ROADMAP.md). Sibling track to the `code/` module-spec gate (pre-commit §1d).

>**signals**  
transformative · essential · thrilled

## selected next achievement
    [lock-isoroll-content] travar o 2º módulo — `code/isoroll-content` já tem "Current Workflow Contract" + SCENE-CREATION.md; destilar num SPEC.md v0 (`status: locked`, `verify: <runner>`) + `> spec:` no CONTEXT.md. Faz a catraca sair de 1→2 e valida o read-gate num módulo com código real (dsl/ é só docs).

**ease-start**  
Rodar `core/tools/spec-scan` (vê a catraca: 1/88 locked hoje). Abrir `code/isoroll-content/SCENE-CREATION.md` § contract + `SPECS.md` § Current Workflow Contract — já são spec-shaped. Copiar `code/_templates/module.SPEC.md` → `code/isoroll-content/SPEC.md`, preencher in/out/invariantes apontando pros testes existentes. 10 min.

## backlog

> [x] [protocol-v0] SPEC v0 — formato mínimo (nome/in/out/invariantes/exemplos) + 1 piloto — DONE 2026-07-17 (ver `code/SPEC-DRIVE.md` P0)  
> [x] [loop-integration] cada etapa do loop produz/consome uma spec parseável (ver [[loop-engineering]]) — DONE 2026-07-17 (Loop 0 lê / Loop 6 promove; SPEC-DRIVE P3)  
> [x] [tree-map] mapear árvore de módulos do workspace — onde falta spec — DONE 2026-07-17 (`core/tools/spec-scan`; SPEC-DRIVE P4)  
> [~] [verify-from-spec] checker que valida "saída real matche spec" por módulo — PARCIAL: conformance monta na verify:fast (modo referência); extrator de exemplos embutidos adiado até 1º consumidor (SPEC-DRIVE P2)  
> [ ] [prompt-dsl-bridge] spec como contrato entre agentes (ver [[prompt-dsl]] em loop-engineering) — dsl/ piloto já exercita a tese; próximo = checker executável  
> [ ] [lock-isoroll-content] travar 2º módulo (isoroll-content) — sai a catraca 1→2  
> [ ] [roundup-ledger] rodar `core/tools/spec-scan` no /roundup pra coverage ficar visível toda sessão  

## done

<!-- done:start -->
> [x] [enforcement-rollout] SDD virou catraca aplicada, não convenção — DONE 2026-07-17. Espinha = gate-or-injection (Princípio 1 do VERIFY). Entregue: SPEC v0 (`code/_templates/module.SPEC.md`); piloto `spacemantics/dsl` locked (verify green, 39 tests); `spec-read-gate.py` (bloqueia editar módulo spec-locked sem ler o SPEC) + pre-commit bloco 1d (novo módulo sob code/ exige `> spec:`) — testados nos 3 runtimes (Claude/opencode/copilot); Loop 0 lê spec / Loop 6 promove; `core/tools/spec-scan` ledger (baseline 1/88). Roadmap canônico: `code/SPEC-DRIVE.md`.
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-07-21  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |       2 |
| trimester   |       2 |
| semester    |       2 |
| year        |       2 |
| 2-year      |       2 |
| 4-year      |       2 |
<!-- stats:end -->
