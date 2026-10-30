# Codex brief — NCNS Digital flagship website

## Mission
Develop a production-quality international AI & digital agency website under a **new independent** repository called `ncns-digital-site`, not `NCNS-Bro`. Use the starter and owner-approved visual reference, improving the fidelity significantly. The user approved a mix of two visual styles: *Cinematic Luxury* (strong hero, scenic dark mountains/reflective surface, large luminous NCNS ring) + *Premium Minimalism* (clean typography and restrained layout). **No neon/acid green, no bright gradient gimmicks.**

## Visual references and assets
- `assets/ncns-original-logo.webp`: the actual approved owner logo (chrome NCNS text inside a circular ice-blue halo). Preserve the geometry, lettering and identity. Do not substitute generated letterforms.
- `reference/approved-combined-concept.webp`: a generated layout reference only, not a source of client facts or assets. DO NOT display it as a background image for the full site.
- Colors: #03070C/#070D16 near black; #EAF2FC silver white; #98AABB graphite/silver; cool-blue glints #9AC6FF used *sparingly*.
- Typography: high-end bold technology wordmark combined with modern restrained reading body. Be precise in spacing.
- Atmosphere: nuanced scenic mountains / water reflections, photographic-real feeling where appropriate, with an animated 3D ring or layered CSS/Canvas/Three.js object. Ensure performant degradation on mobile.

## Motion requirements (must work, not animated screenshots)
1. Hero: breathe/glow ring, subtle slow highlight moving along circle; very mild parallax; intro typography reveals.
2. Services: card border accent light traces pointer movement; icons/art move subtly; no bouncing UI.
3. Page scroll: staggered reveals only when visible; reduced-motion support.
4. Portfolio: add real interactive portfolio items only when finished, tagged 'Concept' if fictional.
5. Navigation: working anchors, mobile accessible menu, smooth scroll with focus management.
6. Performance: prefer CSS & lightweight SVG/WebGL as needed; avoid huge dependencies and oversized video. Target good Core Web Vitals and no layout shift.

## Content structure
- Header: logo, Services, Work, Process, About, Contact.
- Hero: “DIGITAL SOLUTIONS THAT WORK.” Clear positioning, 'Start a project' and 'Explore our approach' CTAs.
- Services: Websites & Digital Products; Branding & Digital Identity; AI & Automation.
- Interactive capabilities demo — client-side only, explicitly labeled as such until real integrations exist.
- Selected Work — temporarily an honest work-in-progress section; no made-up client results or logos.
- Process, about (international studio, no fabricated team claims), project enquiry/contact.
- Footer: original brand and legal/social placeholders only after confirmed links.

## Functional implementation
- Mobile-first accessible responsive layout at 360, 390, 768, 1440px widths.
- Keyboard focus visible; heading hierarchy; proper labels and alt text; contrast; prefers-reduced-motion.
- No fake form submission; either verified contact URL/email or clearly offline brief copy action until backend is connected.
- Avoid copying entire hero-image screenshot into page. Rebuild as HTML/CSS/JS and asset layers.
- Test desktop/mobile visually in actual Chromium; test navigation, all buttons, selectors and copy fallback; report limitations truthfully.

## Delivery / review gates
Milestone A: high-fidelity hero/header/services with working motion, screenshot at desktop and mobile. Owner reviews before expanding visual system.
Milestone B: full pages and functional interactions, accessible and mobile-tested.
Milestone C: add concept portfolio experiences individually and label accurately.
Milestone D: deploy to preview URL, connect verified contact and finally connect the domain after owner approval.

## Don't do
- No acid lime / fluorescent yellow-green.
- No fake client testimonials, revenue or '50+ projects' counters seen in inspirational generated images.
- No use of another brand's logo as a client without permission.
- No claims of deployed production site or active connected AI agent without verification.
- Do not modify `NCNS-Bro` repository.