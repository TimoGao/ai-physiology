# AIP-006: Organ Interface

**Status:** Draft  
**Version:** 0.1

## Purpose

Defines the minimum observable interface for an AI Organ.

## Draft interface

```yaml
organ_id: string
organ_type: string
organism_id: string
capabilities: []
health:
  status: healthy|degraded|critical|offline
  metrics: {}
inputs: []
outputs: []
neural_interface: {}
circulatory_interface: {}
hormonal_receptors: []
immune_interface: {}
lifecycle:
  created_at: timestamp
  version: string
  replaceable: boolean
```

## Design principle

An organ should expose enough state to be monitored, regulated, isolated, repaired, and replaced without requiring full knowledge of its internal implementation.
