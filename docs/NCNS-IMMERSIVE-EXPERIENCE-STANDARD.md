# NCNS Digital — immersive experience & product-demo standard
**Owner direction approved 2026-10-31** · Applies to future agency experiences and all six planned interactive portfolio demos.

## North star
**Cinematic impact + useful interaction + credible business value.**
Not six normal websites. Do not mistake motion for innovation: each signature gesture must help explain a feature, product, buying decision, workflow, or measurable operational improvement. NCNS's approved original-logo hero (Milestones A/B in main) is the untouched foundation, not a candidate for redesign.

The owner specifically likes physically convincing interactive gestures: selecting a house in a catalog makes an architectural visualization open and reveal floors; opening a fashion item makes a jacket unzip or unfold; clicking an item changes camera/object/materials; interactive catalogs feel alive, not static. These are EXAMPLES to develop creatively, not instructions to include a jacket or house in every demo.

## Creative design standard
- Give each demo a signature **WOW moment within the opening 5–10 seconds**, then a real meaningful interaction within the first 20–30 seconds. No forced full-screen intro that traps users.
- A **Before → Interactive action → Revealed internal mechanism → Business output** sequence.
- Use spatial storytelling: progressive object reveals, precise camera movement, exploded views, material/lighting variations, realistic physical transformations, interactive hotspots and true data-driven motion.
- User controls the experience: click/tap/drag/scroll with clear handles and a "Reset" action. Functional states, keyboard alternatives, no puzzle navigation to reach pricing or contact.
- Original conceptual imagery, licensed 3D assets, editorial type, cinematic composition. Protect identity and visual coherence; no excessive particles, unreadable text, fake neon or cloned templates.
- Build the product with native HTML for menus/commerce/quotes and 3D/animation for visuals. No screenshot-as-webpage or sham "working" visuals.
- Different demos need different signatures. CRM/analytics should not become pointless rotating 3D spheres; show business data moving between components.

## Six experience signatures (approved direction / details to refine visually)

### 1 — Growth OS: THE CONTROL ROOM (currently prototyped in draft PR #9)
**WOW:** an interactive end-to-end view of lead acquisition → qualification → opportunity → won sale, with animated flows and transparent conversion breakdown. On selection, the system zooms into the operator view; metric changes visibly propagate through charts and the recommended action plan.
**Real function:** filter synthetic channels/periods, manage in-memory sample pipeline, simulate follow-up handling/opt-outs, edit conversion assumptions and see calculated revenue vs estimated margin contribution. Export real local plan.
**Value sold:** connected decision-making, operational oversight and monthly optimization, not dashboards for their own sake.
**Constraint:** NO hollow abstract 3D. Keep numbers, context, data provenance and keyboard access paramount.

### 2 — Demand Engine: FROM ATTENTION TO QUALIFIED LEAD
**WOW:** one incoming customer "journey thread" moves through SEO search result / social creative / landing offer / qualification / CRM assignment — every stage responds to user-selected channel, audience, content and offer. Reveal a mini simulation of a campaign landing page and operator attribution.
**Real function:** sample lead quality and source math, campaign comparison, opt-in/gated outbound examples, tested hypotheses. No actual prospect messaging.
**Value sold:** full-funnel marketing, conversion and approved lead acquisition operations, not "likes".

### 3 — AI Front Desk: THE TRANSFORMATION FROM CHAT TO ACTION
**WOW:** visitor types in the simulated customer messenger; the UI branches to a second live operator panel and shows the structured intent, urgency, knowledge-base source or "uncertain → human review" and a prepared customer brief.
**Real function:** deterministic, documented knowledge-assistant simulation until a real authorized model and knowledge base exist. Clear escalation, recoverable errors, user-visible source and no hallucinated capabilities.
**Value sold:** less repetitive support work, better lead routing and human control. No unsupported real-world deployment claims.

### 4 — Kern/9: THE EXPLODING PRODUCT / TECHNICAL RFQ
**WOW:** realistic industrial machined assembly in a 3D viewer. User clicks/rotates, selected part separates with an engineered exploded view; changing material or tolerance reveals annotations and potential exception flags. When ready, it folds into an exportable technical RFQ and operator review queue.
**Real function:** actual form validation, bounded rule checking, stage status, sample spec export; no CAD feasibility analysis or manufacturing certification.
**Value sold:** reduce incomplete RFQs and technician back-and-forth.

### 5 — Asterwake: YACHT EXPERIENCE / SPATIAL SERVICE CONFIGURATION
**WOW:** yacht rotates in a restrained moonlit marina. User chooses a clickable part of the vessel; scene moves into that work zone (deck/interior/technical) and reveals work layers/material options. Selection drives a nonbinding sample estimator and structured enquiry.
**Real function:** working scoped configurator and explicitly fictional assumptions; exportable operator brief.
**Value sold:** premium brand trust + fewer vague high-ticket enquiries.

### 6 — Auven / OPTIONAL RECONCEPT: BRAND IN MOTION
**WOW:** instead of a generic storefront, show an original branded 3D object that the user can truly open/unfold/customize; candidate **fashion garment zipper/materials**, **architectural house unfolding**, **premium consumer packaging unfolding**, or refined audio object. This is an owner-inspired variant to visually compare; NO irreversible swap before creative review.
**Real function:** interaction affecting colors/materials, editable set/brand direction and local export of a visual/creative requirements brief; gallery of 100% original brand and AI-assisted campaign assets with honest labels.
**Value sold:** brand/commerce digital experiences and continuous content production, not a pretty portfolio thumbnail.

**Six total flagship demos.** More internal microexamples are possible, but avoid quietly increasing the approved main project count.

## Engineering / browser standards

- Prefer one carefully implemented hero-level spatial interaction per demo + real useful workflow. Do not ship a museum of competing effects.
- Suitable tools when justified: **Blender → optimized glTF/GLB**, **Three.js** for 3D, **GSAP/ScrollTrigger** or Web Animations for choreography. Choose simpler CSS/SVG/Canvas2D or video-sequence fallback if it solves the interaction more efficiently.
- Prefer deferred loading for heavy scenes, optimized geometries/textures, compression and image responsive sources. Respect device GPU limits; test integrated graphics and mobile, including fallback when WebGL unsupported.
- Visible loading states, failure/fallback paths, explicit reduced-motion and pause, pointer/touch/keyboard controls, readable native HTML UI, semantic accessibility.
- Defend useful rendering performance; measure actual input latency, transfer and layout shift in real browser tests. Set budgets per project after reviewing asset demands rather than pretending all complex 3D can be weightless.
- Track asset origin/license and any AI-generated elements.
- Do not make the working system depend on massive, unverified renders on a modest machine; an approved simplified model or pre-rendered fallback is better than a broken showpiece.
- Before approving a build: 1440, 1024, 768, 390, 360 screenshots; real desktop/mobile motion recording; actual pointer/scroll/click tests; keyboard; reduced motion; fast-fail JS checks; check scene does not obstruct CTA or confuse offer.
- Maintain no fake clients, awards, results, AI processing, checkout, delivery, financial gains or real connected integrations when not built.

## Approval milestones
1. **Creative treatment** for each flagship: 3–6 meaningful storyboard frames + actual 3D interaction proof-of-concept or short motion capture (not just static typography page). User selects one direction.
2. **Interactive vertical slice**: one working wow interaction + one real customer/operator workflow, responsive.
3. **Functional case**: validation, accessible flows, commercial proof, real sample export, QA.
4. **Integration and launch**: only after final user review and separate deployment decision.

## Commercial evaluation
Every visual interaction should pass: "Would this help the customer understand/buy something, or is it just decoration?" Demos must clearly answer:
- Who pays?
- What problem costs them time or money?
- What exactly would NCNS deliver?
- What moves, opens, changes or gets calculated?
- What does the customer or employee get out?
- Why work with NCNS month after month?

Any old C1 concepts in draft PR #7 were rejected as brochure-like; do not merge or rebuild them as-is. Existing Growth OS prototype is only an early vertical slice. This standard supersedes weaker descriptions where they conflict, **without authorizing merging production PRs**.
