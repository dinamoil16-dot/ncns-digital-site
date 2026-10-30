# Owner-approved design reference

The exact approved reference is the full-page dark NCNS mockup attached to the owner's redesign request (originally named `a_high_end_dark_cinematic_futuristic_website_lan.png`). It was visually inspected in the conversation. It is a **visual reference only**, not a website asset or evidence of clients, metrics, testimonials or completed projects. Do not display the whole mockup as the page background.

**Source-file blocker:** the attachment is visible in the conversation, but its original downloadable pixel file was not exposed to the execution workspace. Therefore `approved-concept.webp` has not been fabricated, regenerated or substituted. Its exact optimized copy and the approved-versus-actual image collage remain pending the actual file. The generated scenery under `assets/scenery/` is independent illustrative artwork, not the approved reference.

When the original file is made available, run `python3 tests/prepare_reference.py /path/to/original.png` from the repository root. The script preserves the full original composition in an optimized WebP, copies it alongside QA, and produces the required two-column approved-versus-actual collage from the real 1440px browser screenshot. Review the collage visually and revise the site before declaring the reference gate complete.

See `design-direction.md` and `../docs/qa/issue-1-rework/visual-comparison.md` for the visual direction and current review notes.
