# BSR Map Integration — TODO

## Completed

- [x] TSR2→BSR state mapping (2044 states)
- [x] Manual decisions: 1954/1954 applied, 0 invalid
  - Phase 1: 304 new_bsr_state → `keep_bsr`
  - Phase 2-3: 786 split/merge (conf≥1.0) → `approve_selected`
  - Phase 4a: 371 owner/core conflict (conf≥0.8) → `approve_selected`
  - Phase 4b+4c: 468 owner/core + resource/building → `approve_selected`
  - Phase 5: 25 low-conf → `approve_selected`
- [x] Proportional manpower distribution (2044/2044 = 100%)
- [x] Proportional resources distribution (807/2044 = 39.5%)
- [x] Proportional buildings distribution (1984/2044 = 97.1%)
- [x] Province buildings preserved with `BSR_REVIEW` markers (348 states)
- [x] staged_state_validation: errors=3, warnings=0

## Remaining Work

### 1. Province building province ID remap (348 states, 3 errors)

Province buildings (naval_base, bunker, coastal_bunker, naval_supply_hub) reference
TSR2 province IDs. These must be remapped to the corresponding BSR province IDs.

- 3 validation errors: province 13255 is not land (states 44, 1045, 1510)
- `BSR_REVIEW province id needs remap` comments mark affected blocks
- Requires TSR2→BSR province mapping or manual reassignment

### 2. Owner / controller / cores review (321 merge states)

Merge states adopt TSR2 political setup. Where TSR2 and BSR differ, manual review
is needed to confirm the correct owner/controller/core assignment.

- `owner_core_conflicts.csv` lists all conflicts
- `manual_review_priority_europe_russia.md` covers the highest-risk 872 states
- Key: verify that merge overlays don't assign wrong country ownership

### 3. Victory point reassignment

VPs referencing provinces absent from the BSR state are omitted from staged output.
These need manual placement onto valid BSR provinces.

- `omitted_victory_points.csv` lists all omitted VPs
- `missing_victory_point_provinces.csv` tracks missing provinces

### 4. Railway / supply node migration

TSR2 railways and supply nodes use TSR2 province IDs. These must be rebuilt for
the BSR map.

- `tsr_railways_vs_bsr_definition_validation.csv` — compatibility check done
- `tsr_supply_nodes_vs_bsr_definition_validation.csv` — compatibility check done
- Actual railway network reconstruction is TODO

### 5. Copy to live map/ and history/states/

After staged files pass review, copy to production paths.

- `staged_history/states/` → `history/states/`
- BSR map files (`map/definition.csv`, `map/provinces.bmp`, etc.) → `map/`
- Requires full game-load test before merge to `develop`

### 6. Strategic regions, adjacencies, map network

- Strategic region boundaries need adjustment for new BSR provinces
- `bsr_strategicregions_validation.csv` — validation done
- Water connections, adjacencies, impassable borders need review
- `bsr_adjacencies_validation.csv`, `bsr_adjacency_rules_validation.csv` — done

## Key generated files

| File | Purpose |
|------|---------|
| `manual_decisions.csv` | All 1954 manual decisions |
| `applied_manual_decisions.csv` | Decisions applied by the tool |
| `staged_history/states/` | Draft merged state files (2044) |
| `staged_overlay_decisions.csv` | Selected TSR2 overlay per BSR state |
| `staged_merge_review.csv` | All issues in staged output |
| `owner_core_conflicts.csv` | Owner/controller/core mismatches |
| `omitted_victory_points.csv` | VPs dropped due to missing provinces |
| `split_merge_resources.csv` | Resources needing manual distribution |
| `manual_building_distribution.csv` | Buildings needing manual allocation |
