<p align="center">

  <img src="assets/logo.png" alt="NEXUS REDFOX" width="260">
</p>

# NEXUS

NEXUS REDFOX 0.2.0 is a local-first codebase intelligence and security workspace. It builds an architecture graph, keeps an incremental SQLite index, performs deterministic security checks, generates SPDX and CycloneDX SBOMs, exports SARIF, creates tamper-evident project manifests, produces portable analysis capsules, exposes an MCP-compatible server, serves an offline web dashboard, and optionally talks to a local Ollama instance.

## Core commands

```text
nexus init .
nexus index .
nexus scan . --format html --out nexus-report.html
nexus scan . --deep --format sarif --out nexus.sarif.json
nexus graph . --out nexus-graph.json
nexus impact authentication .
nexus sbom . --out sbom.json
nexus snapshot .
nexus verify .nexus/snapshot.json .
nexus capsule . --out nexus.nexus.zip
nexus capsule-verify nexus.nexus.zip
nexus serve .
nexus mcp .
nexus ask "Explain the authentication flow" .
nexus explain NXS101
```

## Operating model

The deterministic core does not require a cloud API. Source files are read locally. The default dashboard binds to loopback. Remote dashboards and remote AI endpoints require explicit opt-in. NEXUS never executes repository code during scan, graph, SBOM, or capsule operations.

## Local AI

Ollama can be used for optional natural-language analysis. NEXUS sends only the selected project facts needed for the request. The default endpoint is loopback.

## Differentiating capabilities

NEXUS combines architecture graph, incremental local indexing, impact traversal, security scanning, SBOM generation, reproducible manifests, portable analysis capsules, and MCP access in one offline workflow.

## Security posture

The repository contains a threat model, security policy, release workflow, dependency review configuration, CodeQL configuration, and a workflow that produces build provenance attestations on GitHub.

## License

Apache-2.0 for source code. The NEXUS name and brand are reserved by the project owner; see TRADEMARKS.md.

## Supported platforms

The core is pure Python and targets Windows, macOS, and Linux with Python 3.11 or newer. The release workflow builds and tests the package on all three platform families. Native mobile operating systems are not claimed as supported targets.

## Release integrity

Use the SHA-256 manifest for release artifacts and verify GitHub build provenance before distribution. The project also provides content manifests and analysis capsules with embedded checksums.
