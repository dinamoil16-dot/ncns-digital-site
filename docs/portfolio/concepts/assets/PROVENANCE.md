# C1 original assets and licensing

These assets are for **fictional visual concept proposals**, not evidence of actual products, clients, facilities or business results. Names are tentative; no trademark/domain clearance is asserted. No rejected Sable House or NCNS-Bro material was reused.

## Images

Created specifically for this C1 review with OpenAI image generation. No stock website screenshot, customer logo or external hotlink is used. All lettering, interface content and board layouts are separate HTML/CSS.

| Local asset | Generated source retained outside checkout | Art direction |
| --- | --- | --- |
| `marine.webp` | `exec-e9b1ee9e-5e6f-42f5-b25e-3bb6e0bd26de.png` | Unbranded silver/navy yacht, quiet imagined Mediterranean refit setting, blue-hour water and architectural light |
| `industrial.webp` | `exec-3adc9daf-931b-4bda-987f-1ac638c19529.png` | Unbranded machined aluminium component, mineral studio surface, restrained orange fixture, original technical editorial still |
| `consumer.webp` | `exec-c0415c2a-bc98-44ee-bffe-a44dd521f17b.png` | Original illustrative ivory/terracotta ceramic audio objects, walnut controls, travertine and linen, warm editorial lighting |

The source PNGs remain in `/workspace/generated_images/`; they were converted to local quality-87 WebP, retaining 1536×1024 dimensions. No NCNS artwork was modified. The consumer module reuses the same image URL rather than downloading a second copy. See [manifest.json](manifest.json) for exact file sizes and hashes: approximately 201 KB marine, 148 KB industrial and 189 KB consumer.

## Fonts and icons

- Newsreader, fetched from the official `google/fonts` repository, `ofl/newsreader/Newsreader[opsz,wght].ttf`, converted to WOFF2 with FontTools/Brotli without changing glyphs. Included [SIL Open Font License](fonts/Newsreader-OFL.txt). Local WOFF2: approximately 215 KB. It is loaded only on boards that actually use the editorial serif; Kern/9 uses Manrope instead.
- Existing local Manrope is reused by relative URL; its already-committed license remains at `assets/fonts/Manrope-OFL.txt` in the repository root. The agency font files were not altered.
- The separate NCNS review index references the exact original agency emblem by relative URL, unchanged. Fictional concept names use live text; they do not redraw or impersonate the NCNS mark.
- Small directional arrows are original inline SVG paths, avoiding missing Unicode glyphs. No external icon package or script is required.

## Cost and optimisation implications

Current board subresource measurements include fonts/CSS/imagery and exclude the HTML document. These are image-first proposal artifacts, not production budgets. Later responsive image variants and a responsibly licensed/subset font strategy can reduce mobile payloads after visual approval. Preserve licensing metadata and comply with any reserved font names when subsetting. Generated product/scene art must remain labelled illustrative; new approved finish variants would be needed for a full product configurator.
