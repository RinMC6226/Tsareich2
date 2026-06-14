# BSR map integration plan

## Premise

- Working branch: `feature/_map_bsr_integration_plan`
- Base branch at creation: `fix/map-1.19`
- BSR source: `/Users/eightman/Desktop/HOI4_modding/2640808954`
- Current TSR2 state count: 1103
- BSR state count: 2044
- Current TSR2 `provinces.bmp`: 5632 x 2048
- BSR `provinces.bmp`: 5120 x 2560

The previous direct import broke the map workflow because BSR map geometry and BSR state data were copied as one unit. This plan separates geometry import from gameplay/history preservation.

## Goal

Use BSR as the draft map geometry, while preserving TSR2 state content wherever a reliable mapping exists.

In practice:

- BSR wins for physical map geometry and province identifiers.
- TSR2 wins for state history content and gameplay intent.
- Generated bridge data must record every mapping decision so state content is not silently lost.

## Precedence Rules

### BSR Priority

Use BSR as source of truth for files whose values are tied to province colors, pixel layout, or BSR-only province IDs:

- `map/provinces.bmp`
- `map/definition.csv`
- province lists inside `history/states/*.txt`
- BSR state boundaries as the first draft
- strategic region province membership, after compatibility review
- adjacency data only after validating against BSR provinces

### TSR2 Priority

Use current TSR2 state files as source of truth for state gameplay content:

- `history = { owner = ... }`
- `controller`
- `add_core_of`
- `victory_points`
- `buildings`
- `resources`
- `manpower`
- `state_category`
- `local_supplies`
- impassable and special state flags when they represent TSR2 design intent
- comments that explain TSR2 design decisions

### Compatibility Priority

Keep `fix/map-1.19` structure unless a BSR file is proven necessary. Do not blindly copy older BSR map scaffolding such as `default.map`, `supplyareas/`, or cosmetic bitmap files into the 1.19 map branch.

Files requiring explicit 1.19 review:

- `map/railways.txt`
- `map/supply_nodes.txt`
- `map/buildings.txt`
- `map/adjacencies.csv`
- `map/adjacency_rules.txt`
- `map/strategicregions/`
- `map/unitstacks.txt`

## Integration Method

1. Snapshot inputs

   Record checksums and counts for current TSR2 map/state files and BSR map/state files before editing.

2. Build state mapping table

   Create a machine-readable table, for example `tools/map_bsr/state_mapping.csv`, with these columns:

   - `tsr_state_id`
   - `tsr_state_name`
   - `bsr_state_id`
   - `bsr_state_name`
   - `mapping_type`
   - `confidence`
   - `notes`

   Mapping types:

   - `same_id_same_area`
   - `same_name`
   - `province_overlap`
   - `manual`
   - `split`
   - `merge`
   - `new_bsr_state`
   - `retired_tsr_state`

3. Generate draft merged states

   Start each output state from the BSR state file so the state ID, name, and `provinces = {}` match BSR geometry.

   Then overlay TSR2 content for mapped states:

   - owner/controller
   - cores
   - buildings and victory points, remapped to BSR province IDs where needed
   - resources
   - manpower and state category
   - local supplies and special flags

   For unmapped or low-confidence states, keep BSR province geometry but mark the state for manual review.

4. Handle split and merge cases explicitly

   If one TSR2 state maps to several BSR states:

   - distribute owner and cores to all mapped BSR states
   - keep victory points only where the referenced province/city can be remapped
   - divide resources/buildings only by explicit rule or manual decision

   If several TSR2 states map to one BSR state:

   - prefer TSR2 owner/controller from the largest overlap or manual decision
   - union cores only when politically valid
   - sum resources only if the BSR state truly covers both old areas

5. Preserve review artifacts

   Generate review lists:

   - unmapped TSR2 states
   - unmapped BSR states
   - TSR2 victory points whose province no longer exists
   - buildings assigned to invalid BSR provinces
   - resources from split/merge states
   - owner/core conflicts

6. Validate before replacing working files

   Required checks:

   - no duplicate state IDs
   - no duplicate province assignments
   - no state references a province missing from `definition.csv`
   - all land provinces are assigned to a state, except province `0`
   - `victory_points` and per-province buildings reference valid land provinces
   - strategic regions reference valid provinces
   - railways and supply nodes reference valid provinces

7. Only then write repo files

   Replace `map/provinces.bmp` and `map/definition.csv` with BSR draft geometry only after the generated states and validation reports are ready.

## Manual Review Order

1. Europe and Russia, because TSR2 political setup is most likely to be custom there.
2. Middle East and North Africa, because cores and ownership are usually sensitive.
3. Asia and colonial regions.
4. Americas and remote islands.
5. Strategic regions, railways, and supply nodes.

## Stop Conditions

Do not continue with a bulk import if any of these are true:

- generated states have missing province references
- generated states have duplicate province assignments
- more than a small reviewable number of TSR2 states cannot be mapped
- victory points or buildings cannot be remapped without manual decisions
- the map utility cannot open the generated draft cleanly

## First Implementation Tasks

1. Add a validation script for state/province consistency.
2. Add a mapping extractor that compares TSR2 and BSR states by ID, name, and province overlap.
3. Generate `state_mapping.csv` and review reports without modifying `map/` or `history/states/`.
4. Review high-risk mappings manually.
5. Generate draft merged states into a staging directory.
6. Validate staging output.
7. Copy staged files into the mod only after validation passes.

