# [ craft | engineering | now ] spec-driven development

Transicionar o workspace inteiro pra SPEC-DRIVE DEVELOPMENT — todo módulo tem entradas/saídas bem definidas e
verificáveis, e a spec é o contrato. Specs viram a fonte da verdade; código sem spec é dívida. Aplica a `code/`, a
`core/flows`, e à árvore de loops (ver [[craft-flows]] e [[prompt-dsl]]). Precede o código, não documenta depois.

> **linked work** — the `core/` agent-library pilot of this idea lives in an enforced
> per-layer frontmatter contract ([core/SCHEMA.md](../../core/SCHEMA.md)), tier unified, pilot flow
> `compare` normalized, validation in `sync-skills` + pre-commit. Sweep tracked in
> [core/ROADMAP.md](../../core/ROADMAP.md). Sibling track to the `code/` module-spec gate (pre-commit §1d).

>**signals**  
transformative · essential · thrilled

>**owns**  
`core/tools/wos/spec-scan` · `core/tools/wos/spec-contract-check` · `code/spacemantics/dsl`

## selected next achievement
    [lock-isoroll-content] travar o 2º módulo — `code/isoroll-content` já tem "Current Workflow Contract" +
    SCENE-CREATION.md; destilar num SPEC.md v0 (`status: locked`, `verify: <runner>`) + `> spec:` no CONTEXT.md. Faz a
    catraca sair de 1→2 e valida o read-gate num módulo com código real (dsl/ é só docs).

**ease-start**  
Rodar `core/tools/wos/spec-scan` (vê a catraca: 1/88 locked hoje). Abrir `code/isoroll-content/SCENE-CREATION.md` §
contract + `SPECS.md` § Current Workflow Contract — já são spec-shaped. Copiar `code/_templates/module.SPEC.md` →
`code/isoroll-content/SPEC.md`, preencher in/out/invariantes apontando pros testes existentes. 10 min.

## backlog

> [x] [protocol-v0] SPEC v0 — formato mínimo (nome/in/out/invariantes/exemplos) + 1 piloto — DONE 2026-07-17 (ver
> `code/ROADMAP-spec-drive.md` P0)  
> [x] [loop-integration] cada etapa do loop produz/consome uma spec parseável (ver [[craft-flows]]) — DONE 2026-07-17
> (Loop 0 lê / Loop 6 promove; SPEC-DRIVE P3)  
> [x] [tree-map] mapear árvore de módulos do workspace — onde falta spec — DONE 2026-07-17 (`core/tools/wos/spec-scan`;
> SPEC-DRIVE P4)  
> [~] [verify-from-spec] checker que valida "saída real matche spec" por módulo — PARCIAL: conformance monta na
> verify:fast (modo referência); extrator de exemplos embutidos adiado até 1º consumidor (SPEC-DRIVE P2)  
> [ ] [prompt-dsl-bridge] spec como contrato entre agentes (ver [[prompt-dsl]] em [[craft-flows]]) — dsl/ piloto já
> exercita a tese; próximo = checker executável  
> [ ] [lock-isoroll-content] travar 2º módulo (isoroll-content) — sai a catraca 1→2  
> [ ] [roundup-ledger] rodar `core/tools/wos/spec-scan` no /roundup pra coverage ficar visível toda sessão  

## done

<!-- done:start -->
> [x] [enforcement-rollout] SDD virou catraca aplicada, não convenção — DONE 2026-07-17. Espinha = gate-or-injection
>   (Princípio 1 do VERIFY). Entregue: SPEC v0 (`code/_templates/module.SPEC.md`); piloto `spacemantics/dsl` locked
>   (verify green, 39 tests); `spec-read-gate.py` + pre-commit bloco 1d; Loop 0 lê spec / Loop 6 promove;
>   `core/tools/wos/spec-scan` ledger (baseline 1/88). Roadmap canônico: `code/ROADMAP-spec-drive.md`.
<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-08-29  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |       9 |
| trimester   |      18 |
| semester    |      18 |
| year        |      18 |
| 2-year      |      18 |
| 4-year      |      18 |
<!-- stats:end -->
