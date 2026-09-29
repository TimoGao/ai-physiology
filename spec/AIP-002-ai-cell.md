# AIP-002: AI Cell

**Status:** Draft  
**Version:** 0.1

## Definition

An **AI Cell** is the smallest autonomous operational unit within a defined AI Organism that:
1. performs a localized function,
2. consumes resources,
3. exchanges internal signals,
4. has an identifiable lifecycle,
5. can be created, replaced, or terminated without necessarily terminating the organism.

## Scale dependence

"Cell" is relative to the organism boundary. A server, local model, controller, process, or agent may qualify in one architecture and not another.

## Required properties

- `cell_id`
- `organism_id`
- `function`
- `state`
- `health`
- `resource_use`
- `inputs`
- `outputs`
- `lifecycle_state`
