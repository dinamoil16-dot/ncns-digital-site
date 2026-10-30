# Scenic assets and provenance

These are original AI-generated illustrative assets created for this NCNS redesign with OpenAI image generation on 2026-10-30. They are not photographs of a real location, customer deliverables, or the owner's approved reference image. No third-party stock images, customer logos or hotlinks were used.

- `obsidian-lake-1942.webp` and `obsidian-lake-1280.webp`: the same generated environment plate, optimized at two sizes. Prompt: realistic obsidian alpine ridges, a narrow central peak, wet reflective lake, silver haze and a muted dark planet at upper right; empty upper-left space; no text, rings, logos or UI. Generated source: `exec-712da4af-246a-41c7-9f1d-498bc9ace9b1.png`.
- `service-studio.webp`: generated three-panel studio atlas (laptop mockup, embossed black stationery, glass circuitry module). No client identities, project claims or legible brand lettering. Source: `exec-bb12e740-531c-4fd6-9f20-adb3fd50b3d9.png`. CSS selects each panel locally without additional requests.

Original generated PNGs remain outside the checkout in `/workspace/generated_images/`; optimized WebP files are committed. The scene has no baked-in website text, buttons or NCNS logo. The authentic NCNS emblem remains `../ncns-original-logo.webp`, unchanged, and is independently composited in HTML. The subtle reflection reuses that same asset.

Fonts are separately hosted under `../fonts/`: Michroma (Google Fonts `ofl/michroma`) and Manrope (Google Fonts `ofl/manrope`), fetched from the official google/fonts repository. Their SIL Open Font Licenses are included as `Michroma-OFL.txt` and `Manrope-OFL.txt`. FontTools/Brotli was used only to encode WOFF2 without altering glyphs. Browser rendering does not require external font services or build tools.

See `asset-manifest.json` for dimensions and byte sizes. No runtime image generation or image-processing dependency is required.
