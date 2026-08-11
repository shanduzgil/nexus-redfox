# Threat Model

Assets include source code, local credentials, index data, generated reports, and agent context.

Trust boundaries are the project workspace, the local NEXUS process, optional local model runtimes, optional remote model runtimes, the browser dashboard, and CI runners.

Primary risks are secret disclosure, arbitrary command execution, malicious repository content, unsafe agent context, path traversal in generated artifacts, and supply-chain tampering.

Controls include loopback defaults, no shell execution in scans, explicit user invocation for process execution, bounded file reads, ignored build directories, content hashing, SHA-256 manifests, capsule checksums, CI security scanning, and GitHub build provenance attestations.
