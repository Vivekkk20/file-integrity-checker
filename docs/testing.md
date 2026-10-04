# Testing & Quality Assurance Documentation

## 1. Testing Philosophy

The **File Integrity Checker** test suite adheres to strict isolation and security standards:
- **Temporary Files Only**: All tests create ephemeral files using `pytest`'s `tmp_path` fixture. The user's real personal files are never touched.
- **Deterministic Vectors**: Standard NIST SHA-256 test vectors (including empty string hash) verify mathematical accuracy.
- **Full Spectrum Coverage**: Unit tests, database transactional tests, REST API mock tests, and end-to-end lifecycle verification.

---

## 2. Test Suite Architecture

```text
tests/
├── __init__.py
├── test_hasher.py          # Cryptographic hashing & streaming buffer tests
├── test_file_handler.py    # Path sanitization, quotes stripping, metadata
├── test_database.py        # SQLite schema, upsert, query, history, stats
├── test_comparator.py      # Deterministic verdict logic (MATCHED, MODIFIED, etc.)
├── test_reporter.py        # Text & JSON audit report generation
├── test_api.py             # Flask test client HTTP API endpoints
└── test_end_to_end.py      # Complete 7-step lifecycle integration workflow
```

---

## 3. Test Cases Inventory

### 3.1 Hash Engine (`test_hasher.py`)
- `test_known_empty_file_hash`: Validates against NIST empty string SHA-256 digest (`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
- `test_known_content_hash`: Validates standard pangram ASCII string digest.
- `test_same_file_produces_identical_hash`: Verifies deterministic reproducibility.
- `test_modified_file_produces_different_hash`: Verifies avalanche effect on single-character mutation.
- `test_chunking_with_large_payload`: Validates correct checksum across 16KB chunk buffer boundaries for 200KB payload.
- `test_missing_file_raises_filenotfound`: Verifies clean exception handling.
- `test_directory_raises_isadirectoryerror`: Prevents attempting to hash directories.

### 3.2 File Handler (`test_file_handler.py`)
- `test_format_bytes_human`: Validates byte conversion to B, KB, MB, GB.
- `test_validate_path_valid`: Validates normal resolution.
- `test_validate_path_strips_quotes`: Ensures command-line or drag-and-drop quotes are cleanly stripped.
- `test_validate_path_null_byte_rejected`: Blocks null-byte injection attacks.
- `test_validate_path_empty_rejected`: Rejects blank inputs.
- `test_get_metadata_existing_file`: Checks size, timestamps, readability, and name.
- `test_get_metadata_missing_file`: Checks graceful error return.
- `test_get_metadata_directory`: Distinguishes directories from regular files.

### 3.3 Database Manager (`test_database.py`)
- `test_save_and_retrieve_baseline`: Validates baseline persistence and retrieval by path and ID.
- `test_baseline_upsert_updates_existing`: Verifies `ON CONFLICT` updates without duplicate entries.
- `test_delete_baseline`: Verifies record removal and return codes.
- `test_update_baseline_last_verified`: Verifies timestamp tracking.
- `test_log_and_filter_verification_history`: Tests status filtering and query limits.
- `test_dashboard_stats`: Tests aggregation counts (total baselines, verifications, status breakdown).

### 3.4 Comparison Engine (`test_comparator.py`)
- `test_evaluate_status_matched`: Tests identical hash match (including case normalization).
- `test_evaluate_status_modified`: Tests hash divergence.
- `test_evaluate_status_missing`: Tests missing file detection.
- `test_evaluate_status_error_on_message`: Tests error propagation.
- `test_verify_file_lifecycle`: Real disk operations verifying progression from un-baselined -> MATCHED -> MODIFIED -> MISSING.

### 3.5 Report Generator (`test_reporter.py`)
- `test_to_text_report_contains_key_elements`: Checks headers, dividers, status, and advisory notes.
- `test_to_json_report_is_valid_json`: Validates JSON schema and deserialization.
- `test_to_history_summary_text`: Tests tabular ASCII audit logging format.

### 3.6 API Endpoints (`test_api.py`)
- `test_index_route`: Verifies single-page UI loads with HTTP 200.
- `test_api_stats`: Validates metrics payload.
- `test_api_analyze_valid_file`: Tests file inspection endpoint.
- `test_api_analyze_missing_file`: Tests 404 response for nonexistent paths.
- `test_api_baseline_and_verify`: Tests full REST API lifecycle (baseline creation, verification, history logging, report export).
- `test_api_upload`: Tests multipart file upload and SHA-256 calculation.

### 3.7 Master End-to-End Workflow (`test_end_to_end.py`)
Executes the full required lifecycle:
```text
1. Create test file `critical_asset.conf`
2. Generate baseline in SQLite
3. Verify unchanged file -> MATCHED
4. Modify test file
5. Verify again -> MODIFIED
6. Delete test file
7. Verify again -> MISSING
8. Validate 3 corresponding audit log records in database
9. Validate text and JSON audit report generation
```

---

## 4. Running the Tests

To execute the entire test suite:

```bash
# Activate virtual environment
.\.venv\Scripts\activate

# Run pytest with verbose output
pytest
```

Output:
```text
============================= 54 passed in 1.28s ==============================
```

---

## 5. Verification & Browser Testing Evidence

- **Automated Test Execution**: All 54 unit, API, file handler, and end-to-end integration tests execute cleanly in 1.28s with 100% pass rate.
- **Local Browser UI Verification**: In addition to programmatic endpoint testing, the running Flask application on `http://127.0.0.1:5000` was verified using local Google Chrome automation via Playwright (`channel="chrome"`).
- **Photographic UI Evidence**: 12 authentic raw and annotated screenshots were captured directly from the live running application interface and embedded into the 15-page master documentation report.


