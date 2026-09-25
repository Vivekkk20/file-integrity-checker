# Security Architecture & Threat Model

## 1. Security Overview

**File Integrity Checker** is engineered with a strict principle of least privilege, defensive path parsing, and a 100% local execution model. It provides reliable cryptographic verification while preventing common vulnerabilities associated with handling user-supplied filesystem targets.

---

## 2. Threat Model & Mitigations

| Threat Vector | Potential Impact | Defensive Mitigation |
| :--- | :--- | :--- |
| **Path Traversal / Poisoning** | Accessing sensitive files or directories outside user intent via `../` or null bytes. | All inputs are canonicalized via `pathlib.Path.resolve()`. Raw strings are rejected if null-byte characters (`\x00`) are found. |
| **Arbitrary Code Execution** | Malicious binaries or scripts being run during analysis. | The application **never executes** files. Target files are accessed strictly as passive binary streams via read-only file handles (`open(path, 'rb')`). |
| **Command Injection** | Execution of shell commands via unsanitized file paths. | Zero use of `os.system()`, `subprocess.Popen()`, or shell interpolations on file inputs across the entire codebase. |
| **SQL Injection** | Manipulation of the local SQLite database via crafted file names or paths. | 100% of database queries utilize SQLite parameter binding (`?`). No SQL statement is constructed using string concatenation. |
| **Memory Exhaustion (DoS)** | Crashing the system by loading multi-gigabyte files into RAM. | The hashing engine streams data in fixed **64 KB chunks**, maintaining constant $O(1)$ memory consumption regardless of file size. |
| **Data Leakage / Telemetry** | Exposure of confidential file names, paths, or checksums to the cloud. | Complete local operation. Zero third-party telemetry, tracking analytics, or external API endpoints. |
| **Unsafe File Uploads** | Malicious file uploads overwriting critical system files. | Uploads through the web interface are passed through `secure_filename()` and restricted to an isolated `staged_files/` directory. |

---

## 3. Cryptographic Integrity Guarantees

### 3.1 SHA-256 Collision Resistance
The Federal Information Processing Standard (FIPS 180-4) SHA-256 algorithm produces a 256-bit hash. 
- The probability of finding two distinct files that produce the same SHA-256 digest is $2^{-128}$ (approx. $1$ in $3.4 \times 10^{38}$), which is computationally infeasible.
- Single-bit alterations in a target file trigger the **avalanche effect**, causing approximately 50% of the output hash bits to change pseudo-randomly.

### 3.2 What `MATCHED` Means (and Does NOT Mean)
- **What it Proves**: A `MATCHED` verdict proves beyond cryptographic doubt that the target file on disk is bit-for-bit identical to the file state when the baseline was created.
- **What it Does NOT Prove**: A `MATCHED` verdict **does NOT guarantee the file is free of malware**. If an already compromised binary or trojan horse is initially baselined, subsequent verifications will report `MATCHED`. File integrity checking must be paired with anti-malware and vulnerability scanning as part of defense-in-depth.

---

## 4. Hashing vs. Encryption

A core educational objective of this project is clarifying the fundamental distinction between hashing and encryption:

```text
+---------------------------------------------------------------------------------+
|                                    HASHING                                      |
|  * One-Way Mathematical Transformation                                         |
|  * Irreversible: Plaintext cannot be computed from digest                      |
|  * Fixed-length output (SHA-256 is always 64 hexadecimal characters)           |
|  * Primary Goal: INTEGRITY VERIFICATION (Detecting tampering)                 |
+---------------------------------------------------------------------------------+

                                     VERSUS

+---------------------------------------------------------------------------------+
|                                  ENCRYPTION                                     |
|  * Two-Way Mathematical Transformation                                         |
|  * Reversible: Requires a cryptographic secret key to decrypt                  |
|  * Variable-length output proportional to plaintext length                      |
|  * Primary Goal: CONFIDENTIALITY (Preventing unauthorized reading)             |
+---------------------------------------------------------------------------------+
```

---

## 5. Secret Hygiene & Code Audit

- No hardcoded passwords, tokens, API keys, or certificates exist in the codebase.
- `.gitignore` explicitly prevents accidental commit of virtual environments (`.venv/`), test databases (`*.db`), temporary files, or environment configurations.
