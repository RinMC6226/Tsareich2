# BSR map integration tooling

Run from the repository root:

```sh
python3 tools/map_bsr/bsr_map_tool.py all
```

The default BSR source is `/Users/eightman/Desktop/HOI4_modding/2640808954`.
The command writes generated artifacts under `tools/map_bsr/generated/` and
does not modify live `map/` or `history/states/` files.

Manual review decisions can be supplied with:

```sh
python3 tools/map_bsr/bsr_map_tool.py all --decisions tools/map_bsr/manual_decisions.csv
```

If `tools/map_bsr/manual_decisions.csv` is absent, the command ignores it and
emits `generated/manual_decision_template.csv` for reviewers to fill. Supported
`manual_decision` values are:

- `approve_selected`: keep the currently selected TSR2 overlay for that BSR
  state.
- `keep_bsr`: use the BSR state without TSR2 overlay.
- `override_tsr`: use `manual_tsr_state_id`, which must be one of that BSR
  state's mapping rows.

Important outputs:

- `input_snapshot.csv`: checksums, dimensions, and source counts.
- `state_mapping.csv`: machine-readable TSR2-to-BSR state mapping table.
- `manual_review_mappings.csv`: mappings that need human review.
- `new_bsr_states.csv` and `retired_tsr_states.csv`: unmapped state reports.
- `rejected_overlap_mappings.csv`: province-overlap rows rejected from
  automatic staging because state id/name and political tags did not line up.
- `staged_history/states/`: generated draft merged state files.
- `staged_overlay_decisions.csv`: one selected TSR2 overlay candidate per BSR
  state used to generate the staged files.
- `staged_state_validation.csv`: state/province validation report.
- `omitted_victory_points.csv`: TSR2 victory points omitted from staged output
  because the province is not in the mapped BSR state.
- `omitted_province_buildings.csv`: province building entries omitted for the
  same reason.
- `missing_victory_point_provinces.csv`: TSR2 victory point provinces missing
  from BSR `definition.csv`.
- `invalid_building_provinces.csv`: TSR2 per-province building references
  missing from BSR `definition.csv`.
- `manual_building_distribution.csv`: split/merge state buildings that were
  not duplicated into staged states and need manual allocation.
- `owner_core_conflicts.csv`: mapped states where TSR2 and BSR political setup
  differs.
- `split_merge_resources.csv`: resources attached to split/merge mappings that
  need explicit distribution or summing decisions.
- `manual_review_priority_europe_russia.csv`: first-pass manual review queue
  for Europe and Russia-sensitive mappings.
- `manual_review_priority_europe_russia_grouped.csv`: the same queue grouped
  by BSR state with selected overlay and issue counts.
- `manual_review_priority_europe_russia.md`: readable first-pass review packet
  for the highest-risk grouped Europe/Russia states.
- `review_decisions.csv`: all BSR states with a conservative decision status.
- `auto_approved_review_decisions.csv`: clean mappings that can be treated as
  reviewed by tooling heuristics.
- `unresolved_review_decisions.csv`: states still requiring manual decision
  before live import.
- `manual_decision_template.csv`: fillable template for
  `tools/map_bsr/manual_decisions.csv`.
- `applied_manual_decisions.csv` and `invalid_manual_decisions.csv`: audit
  reports for supplied manual decisions.
- `bsr_*_validation.csv`: BSR map-network reference checks.
- `tsr_railways_vs_bsr_definition_validation.csv` and
  `tsr_supply_nodes_vs_bsr_definition_validation.csv`: compatibility checks for
  retaining TSR2 1.19 railways and supply nodes with BSR province IDs.
