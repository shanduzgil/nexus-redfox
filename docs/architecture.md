# Architecture

NEXUS is organized as a pure-Python core plus static web assets.

The scanner loads a rule pack, filters rules by language and prefilter needles, then scans files concurrently. The indexer uses SQLite and file hashes so repeated work is incremental. The graph builder extracts symbols and imports and produces a stable architecture graph. The SBOM layer parses common package manifests. The capsule layer bundles analysis artifacts and SHA-256 checksums. The MCP adapter exposes read-only inspection tools.
