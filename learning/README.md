# Capability learning system — stage 1

Book-converter can record techniques found in external applications and research whether they can be integrated legally and safely.

## Workflow
1. **Discover** documented methods, permissively accessible source code, or public APIs.
2. **Evaluate** the license, prerequisites, compute cost, and potential output quality.
3. **Prototype** a small isolated implementation; never run untrusted third-party code automatically.
4. **Test** the result against known input/output samples.
5. **Approve** only with recorded evidence and human review.
6. **Reuse** approved workflows through production adapters.

## Current implementation
`registry.py` provides a JSON-backed research registry, URL and license checks, and explicit approval gates. It does **not** autonomously browse applications, reverse engineer proprietary products, train models, execute downloaded code, or modify production code. Those capabilities require separate implementations and permissions.

## Future modules
- Documentation and public GitHub source ingestion
- AI-assisted technique comparison and workflow synthesis
- Sandboxed test runner with resource quotas and network restrictions
- Benchmarks for 3D modelling, rigging, animation, voice, and rendering
- Versioned, reviewable GitHub pull requests for approved capability adapters
- Source attribution, license compatibility, and provenance records

Never collect passwords, bypass paywalls, circumvent DRM, or imitate proprietary services through unauthorized access.
