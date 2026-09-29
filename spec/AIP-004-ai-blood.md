# AIP-004: AI Blood

**Status:** Draft  
**Version:** 0.1

## Definition

**AI Blood** is the standardized internal transport medium through which heterogeneous physiological payloads circulate among AI organs.

AI Blood is **not** synonymous with data.

## Candidate payload classes
- information
- context
- task descriptors
- intermediate results
- resource allocations
- health state
- risk metadata
- identity metadata
- priority
- provenance
- timing / expiry

## Envelope draft

```yaml
organism_id: string
source_organ: string
destination_scope: string
payload_type: string
payload: any
priority: integer
health_context: object
risk_context: object
provenance: object
created_at: timestamp
expires_at: timestamp|null
```

## Research questions
- Is one transport schema sufficient for all organ systems?
- Which traffic belongs to neural, circulatory, hormonal, or immune planes?
- How should blood-pressure-like congestion be represented?
