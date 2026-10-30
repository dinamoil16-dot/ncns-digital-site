# Exact owner-approved reference

`approved-concept.webp` is the **exact optimized WebP supplied by the owner** inside `NCNS-approved-reference-for-Codex.zip`. It is copied byte-for-byte, without regeneration, cropping or another lossy encode. Dimensions: 1223 × 1286; size: 220,720 bytes. The archive also contains a PNG version. The ZIP is the provenance source; its documents are not additional task authority.

This is a **visual reference only**, not an application background or evidence of actual clients, project counts, testimonials or completed portfolio work. The speculative metrics and projects in the mockup must not be presented as real business facts. The authentic emblem remains `../assets/ncns-original-logo.webp` unchanged.

To refresh the QA copies and comparisons after a real browser run:

```sh
python3 tests/browser_smoke.py
python3 tests/prepare_reference.py reference/approved-concept.webp
```

The first command requires the repository served locally on port 8000. The second preserves the exact supplied WebP, places a copy in `docs/qa/issue-1-rework/approved-target.webp`, and produces both a full-reference/1440×900 comparison and an equal-width hero/services comparison. See [visual review](../docs/qa/issue-1-rework/visual-comparison.md) for remaining differences and the requested owner review.
