# Refactoring Plan: YAML Config as Single Source of Truth

## Problem Statement
The codebase has **duplicate constraint definitions** across multiple locations:
1. `models/enums.py` - `MovementConstraint` class, `SESSION_TO_DISCIPLINE_MAPPING`, `DB_VALID_DISCIPLINES`
2. `config/program_building_config.yaml` - `movement_query_disciplines`, `session_discipline_mapping`, `movement_enum_values`
3. `services/enhanced_program_service.py` - Inline `BlockConstraints` in `_create_warmup_block()`, `_create_main_block()`, `_create_cooldown_block()`

**Critical Issue:** `BlockConstraints` created by `EnhancedProgramService` are **IGNORED** by `MovementPopulationService` (lines 150-161).

**Goal:** Establish YAML config (`config/program_building_config.yaml`) as the **single source of truth** for all constraint definitions.

---

## Phase 1: Add Block Constraints to YAML Config
Add a new `block_constraints` section to the YAML config file.

### Task 1.1: Define Warmup Block Constraints
**File:** `config/program_building_config.yaml`
**Location:** After `movement_query_disciplines` section (line ~862)

- [ ] Add `block_constraints.warmup` section with:
  - `compound: false`
  - `spinal_compression: ["none", "low"]`
  - `disciplines: ["mobility", "stretch", "athletic"]`
  - `movement_name_patterns: ["jump", "leap", "hop", "mobility", "stretch"]`

### Task 1.2: Define Cooldown Block Constraints
**File:** `config/program_building_config.yaml`

- [ ] Add `block_constraints.cooldown` section with:
  - `compound: false`
  - `spinal_compression: ["none", "low"]`
  - `disciplines: ["mobility", "stretch"]`
  - `movement_name_patterns: ["stretch", "mobility", "foam_roll"]`

### Task 1.3: Define Main Block Constraints by Session Type
**File:** `config/program_building_config.yaml`

- [ ] Add `block_constraints.main` section with constraints for each session type:
  - `resistance_accessory`:
    - `compound: true`
    - `disciplines: ["resistance training"]`
    - `compound_filter: true`
  - `resistance_circuits`:
    - `compound: true`
    - `disciplines: ["resistance training", "crossfit"]`
    - `compound_filter: null`
  - `hyrox_style`:
    - `compound: true`
    - `disciplines: ["resistance training", "cardio", "athletic"]`
    - `compound_filter: null`
  - `mobility_only`:
    - `compound: false`
    - `disciplines: ["mobility", "stretch"]`
    - `compound_filter: false`
  - `cardio_only`:
    - `compound: false`
    - `disciplines: ["cardio", "athletic"]`
    - `compound_filter: false`

---

## Phase 2: Add ConfigLoader Methods
Add methods to `ConfigLoader` for retrieving block constraints.

### Task 2.1: Add `get_warmup_constraints()` Method
**File:** `utils/config_loader.py`

- [ ] Create method returning warmup constraint dict from config

### Task 2.2: Add `get_cooldown_constraints()` Method
**File:** `utils/config_loader.py`

- [ ] Create method returning cooldown constraint dict from config

### Task 2.3: Add `get_main_block_constraints()` Method
**File:** `utils/config_loader.py`

- [ ] Create method accepting `session_type: str` parameter
- [ ] Return constraints dict for specified session type
- [ ] Include fallback to empty dict if session type not found

### Task 2.4: Add `get_block_constraints()` Unified Method
**File:** `utils/config_loader.py`

- [ ] Create unified method accepting `block_type: str` and optional `session_type: str`
- [ ] Route to appropriate constraint getter based on block_type
- [ ] Return constraints dict suitable for `BlockConstraints` model

---

## Phase 3: Update MovementPopulationService
Make `MovementPopulationService` respect `BlockConstraints` from config.

### Task 3.1: Add ConfigLoader Dependency
**File:** `services/movement_population_service.py`

- [ ] Import `ConfigLoader` from `utils.config_loader`
- [ ] Add `config_loader: ConfigLoader` parameter to `__init__`
- [ ] Initialize `self.config_loader` in constructor

### Task 3.2: Update `_populate_warmup_block()` to Use Config
**File:** `services/movement_population_service.py`

- [ ] Get warmup constraints via `self.config_loader.get_warmup_constraints()`
- [ ] Pass disciplines from config to query service
- [ ] Apply spinal_compression filter from config

### Task 3.3: Update `_populate_cooldown_block()` to Use Config
**File:** `services/movement_population_service.py`

- [ ] Get cooldown constraints via `self.config_loader.get_cooldown_constraints()`
- [ ] Pass disciplines from config to query service
- [ ] Apply spinal_compression filter from config

### Task 3.4: Update `_populate_main_block()` to Use Config
**File:** `services/movement_population_service.py`

- [ ] Get main block constraints via `self.config_loader.get_main_block_constraints(session_type)`
- [ ] Use `session.session_type` to determine constraints
- [ ] Pass disciplines from config to query service
- [ ] Apply compound_filter from config

### Task 3.5: Respect Existing BlockConstraints if Provided
**File:** `services/movement_population_service.py`

- [ ] Check if `block.constraints` is not None
- [ ] If `block.constraints` has disciplines defined, use those
- [ ] Otherwise fall back to config-based constraints
- [ ] This allows EnhancedProgramService constraints to still work if explicitly set

---

## Phase 4: Remove Duplicate Definitions from enums.py
Clean up legacy code that duplicates YAML config.

### Task 4.1: Remove `DB_VALID_DISCIPLINES` Set
**File:** `models/enums.py`
**Lines:** 78-90

- [ ] Delete `DB_VALID_DISCIPLINES` set definition
- [ ] Update any code referencing this set to use `config_loader.get_enum_values("discipline")`

### Task 4.2: Remove `validate_discipline_value()` Function
**File:** `models/enums.py`
**Lines:** 163-165

- [ ] Delete `validate_discipline_value()` function
- [ ] Replace usages with `config_loader.validate_enum_value("discipline", value)`

### Task 4.3: Remove `MovementConstraint` Class
**File:** `models/enums.py`
**Lines:** 173-216

- [ ] Delete entire `MovementConstraint` class including:
  - `WARMUP_CONSTRAINTS`
  - `COOLDOWN_CONSTRAINTS`
  - `MAIN_BLOCK_CONSTRAINTS`

### Task 4.4: Remove `SESSION_TO_DISCIPLINE_MAPPING` Dict
**File:** `models/enums.py`
**Lines:** 219-226

- [ ] Delete `SESSION_TO_DISCIPLINE_MAPPING` dictionary
- [ ] Update any code referencing this to use `config_loader.get_session_discipline_mapping(session_type)`

### Task 4.5: Remove or Mark `DisciplineType.HYPERTROPHY`
**File:** `models/enums.py`
**Line:** 70

- [ ] Option A: Remove `HYPERTROPHY = "hypertrophy"` (not in DB)
- [ ] Option B: Add comment marking it as internal-only (not valid for DB queries)
- [ ] Update any code using `DisciplineType.HYPERTROPHY` to use `DisciplineType.RESISTANCE_TRAINING`

---

## Phase 5: Update Imports and References
Fix any imports/references to removed code.

### Task 5.1: Search for `MovementConstraint` References
**Command:** `grep -rn "MovementConstraint" --include="*.py"`

- [ ] Identify all files importing or using `MovementConstraint`
- [ ] Update each to use config-based approach

### Task 5.2: Search for `SESSION_TO_DISCIPLINE_MAPPING` References
**Command:** `grep -rn "SESSION_TO_DISCIPLINE_MAPPING" --include="*.py"`

- [ ] Identify all files importing or using this mapping
- [ ] Update each to use `config_loader.get_session_discipline_mapping()`

### Task 5.3: Search for `DB_VALID_DISCIPLINES` References
**Command:** `grep -rn "DB_VALID_DISCIPLINES" --include="*.py"`

- [ ] Identify all files importing or using this set
- [ ] Update each to use `config_loader.get_enum_values("discipline")`

### Task 5.4: Search for `validate_discipline_value` References
**Command:** `grep -rn "validate_discipline_value" --include="*.py"`

- [ ] Identify all files using this function
- [ ] Update each to use `config_loader.validate_enum_value()`

---

## Phase 6: Update EnhancedProgramService (Optional)
Optionally refactor `EnhancedProgramService` to use config for block creation.

### Task 6.1: Review `_create_warmup_block()` Method
**File:** `services/enhanced_program_service.py`
**Lines:** ~768-780

- [ ] Review current inline BlockConstraints
- [ ] Decide: keep inline or refactor to use config
- [ ] If refactoring: use `config_loader.get_warmup_constraints()`

### Task 6.2: Review `_create_main_block()` Method
**File:** `services/enhanced_program_service.py`

- [ ] Review current inline BlockConstraints
- [ ] Decide: keep inline or refactor to use config
- [ ] If refactoring: use `config_loader.get_main_block_constraints(session_type)`

### Task 6.3: Review `_create_cooldown_block()` Method
**File:** `services/enhanced_program_service.py`
**Lines:** ~810-829

- [ ] Review current inline BlockConstraints
- [ ] Decide: keep inline or refactor to use config
- [ ] If refactoring: use `config_loader.get_cooldown_constraints()`

---

## Phase 7: Testing and Verification

### Task 7.1: Run Existing Test Suite
**Command:** `pytest`

- [ ] Verify all 121 existing tests still pass
- [ ] Document any test failures and their causes

### Task 7.2: Add Unit Tests for New ConfigLoader Methods
**File:** `tests/test_config_loader.py` (create if needed)

- [ ] Test `get_warmup_constraints()` returns expected values
- [ ] Test `get_cooldown_constraints()` returns expected values
- [ ] Test `get_main_block_constraints()` for each session type
- [ ] Test `get_block_constraints()` routing logic

### Task 7.3: Add Integration Tests for MovementPopulationService
**File:** `tests/test_movement_population_service.py`

- [ ] Test warmup block population uses config disciplines
- [ ] Test cooldown block population uses config disciplines
- [ ] Test main block population uses session-type-specific disciplines
- [ ] Test that BlockConstraints from skeleton override config when present

### Task 7.4: Manual End-to-End Test
- [ ] Run program generation with different session types
- [ ] Verify movements match expected disciplines
- [ ] Verify no "hypertrophy" discipline queries (would fail)

---

## Phase 8: Documentation and Cleanup

### Task 8.1: Update Code Comments
- [ ] Add docstring to new ConfigLoader methods explaining source of truth
- [ ] Add comments in MovementPopulationService explaining constraint hierarchy

### Task 8.2: Update YAML Config Metadata
**File:** `config/program_building_config.yaml`

- [ ] Update `version` in metadata section
- [ ] Add changelog entry for block_constraints addition

### Task 8.3: Remove This Document (Optional)
- [ ] Once refactoring is complete, archive or delete this instruction file

---

## Summary of Files to Modify

| File | Action |
|------|--------|
| `config/program_building_config.yaml` | Add `block_constraints` section |
| `utils/config_loader.py` | Add 4 new constraint getter methods |
| `services/movement_population_service.py` | Use config for constraints |
| `models/enums.py` | Remove duplicate definitions |
| `services/enhanced_program_service.py` | Optional refactor |
| `tests/test_config_loader.py` | Add new tests |
| `tests/test_movement_population_service.py` | Add integration tests |

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Breaking existing tests | Run tests after each phase |
| Invalid discipline queries | Ensure all disciplines in config exist in DB |
| Regression in program generation | Manual E2E testing after completion |
| Circular import issues | Import ConfigLoader in functions, not at module level |

---

## Rollback Plan
If critical issues arise:
1. Revert changes using `git checkout` for affected files
2. Keep `models/enums.py` legacy code as fallback
3. Feature flag the config-based approach via environment variable
