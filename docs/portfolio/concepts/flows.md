# Concrete future demo flows — definitions, not C1 implementations

C1 boards are static visual states. The following client-side flows are proposed for a later owner-approved development task. None is represented as working now. All numerical fixtures are invented demonstration data, not real supplier/product information.

## 01 / Asterwake — refit scope and estimate model

**Commercial problem:** a premium-service enquiry often starts with an aspiration but little structured scope. The demonstration should help a visitor understand what they have and have not specified, rather than promise a real survey or quotation.

**Customer workflow:** choose vessel type and length → select work packages → choose an approximate planning window → review a transparent sample model → copy/download a structured brief for human discussion.

Proposed state: `{vesselType, lengthMetres, packages[], planningWindow, notes, assumptionsVersion}`. Keep it in memory; no enquiry is sent. Timing can remain “to discuss” and is not a reservation.

### Deterministic illustrative calculation

| Fixture | Sample value |
| --- | --- |
| Motor-vessel base | €20,000 |
| Sailing-vessel base | €16,000 |
| Length coefficient | €1,500 per metre |
| Deck restoration | €10,000 |
| Interior refresh | €18,000 |
| Technical systems | €25,000 |

`subtotal = base[vesselType] + lengthMetres × 1500 + sum(selectedPackageRates)`.

`low = roundToNearest1000(subtotal × 0.93)`; `high = roundToNearest1000(subtotal × 1.13)`.

The pictured motor yacht / 28m / deck + interiors gives `20,000 + 42,000 + 10,000 + 18,000 = 90,000`; the deliberately invented range rounds to **€84,000–€102,000**. These coefficients are a transparent toy model, not market research. A future UI must expose them and say “fictional model, nonbinding, no supplier quote”; rounding is display-only and should not hide assumptions.

### Validation and meaningful acceptance

- Require a known vessel type, finite length between 10 and 60m and at least one package. These are model bounds, not actual business acceptance criteria. Unsupported/unknown requests get “outside this illustrative model — human review”, not a fabricated exact quote.
- Display units and reject blank, negative, NaN, infinite or unreasonable input. A narrow locale-normalisation rule may accept one decimal comma; ambiguous formats must be explained rather than guessed.
- The example above yields the pictured range. Adding technical systems produces subtotal €115,000 and rounded range €107,000–€130,000. Back/edit preserves choices and recalculates; reset removes them.
- Export includes inputs, assumptions version, calculation and simulation disclaimer. Native clipboard plus manual-selection fallback; optional local `.txt` download. No customer account, booking, supplier survey, email or backend.
- Keyboard can complete all steps; invalid input receives visible field errors and focus; the range changes without excessive screen-reader announcements. Test reduced motion and mobile field visibility.

**Potential value to test:** task completion, missing-scope count and comprehension of the estimate assumptions in moderated usability tasks. No conversion uplift or actual customer outcome is claimed.

**Indicative later scope:** 4–6 focused working days for this single local flow, responsive states, transparent rates, copy/export and QA; excludes commercial pricing research, supplier processes and integrations. Main risk: a convincing-looking estimate being mistaken for a real quote. Keep the model label and assumptions next to the result.

## 02 / Kern/9 — specification to simulated human-review queue

**Commercial problem:** a request can be incomplete or internally inconsistent before an engineer sees it. Show a careful interface that makes uncertainty visible and assembles a usable packet, not an automated promise of manufacturability.

**Customer workflow:** pick a sample geometry → specify material, quantity, tolerance and finish → see completeness/constraint flags → explicitly run a local routing simulation → inspect the RFQ packet and a follow-up-message preview → copy/export locally.

Proposed state: `{samplePartId, material, quantity, requestedToleranceMm, finish, notes, ruleFlags[], queuePreview}`. Bundled sample geometry/metadata is illustrative. If an optional future file picker is approved, validate extension and a 10MiB local size limit, read only filename/size, and state **“geometry not analysed”**. CAD parsing, uploads and real production feasibility are not included.

### Bounded rules and simulation boundary

- Materials: sample Aluminium 6061, Stainless 304 and POM; quantity: integer 1–5000; tolerance: positive decimal in mm.
- A deliberately limited fixture matrix permits anodising only for the aluminium sample. Invalid combinations get a review flag. Requested tolerance below 0.05mm goes to manual review, not “supported” or “impossible” engineering advice. These are illustrative software rules, not a supplier capability table.
- Missing sample geometry, unknown material, invalid quantity or blank required fields blocks “prepare packet” with concrete errors. A valid but tight/unsupported request remains exportable as **review required**, with its flags preserved.
- The explicit “Run local simulation” control walks through `draft → completeness checked → human review`. A visible “simulated CRM queue” is just an in-memory object/preview. No actual CRM record, API call or email is created.
- A follow-up text preview may explain missing fields; do not say it was sent. Use a reserved example address such as `buyer@example.test` only if an address is needed; do not solicit real customer data for the simulation.

### Meaningful acceptance

- Pictured sample part / Aluminium 6061 / 50 units / ±0.10mm / bead-blasted produces a complete packet marked **sample / unassessed geometry / human review**, not a guaranteed production quote.
- Quantity 0, fractional values and values over 5000 show model-bound errors. Tolerance 0.02mm preserves the request and clearly flags manual review. POM + anodising cannot silently pass the fixture compatibility check.
- Running the simulation creates one local preview packet; rerunning updates/replaces it without duplicate pretend “leads”. Back/edit invalidates stale statuses. Reset clears the in-memory preview and any attachment metadata.
- Copy/JSON export contains all entered values, flags and the simulation disclaimer. No outbound write requests, real uploads, authentication, CRM or mail SDK.
- Accessible step navigation, keyboard review of rule messages and understandable mobile tables. Under reduced motion, status transitions update immediately without losing meaning.

**Potential value to test:** specification completeness, time to identify exceptions and whether a reviewer can explain the next handoff. Measure these in test tasks; do not invent operational savings.

**Indicative later scope:** 6–9 focused working days for one specification wizard, sample rule table, in-memory routing preview, packet export and QA. Risk is expansion into CAD analysis, real CRM or engineering claims; keep these outside the demo. This is the recommended first direction because it demonstrates the strongest operational thinking alongside visual craft.

## 03 / Auven — a transparent fictional product configuration

**Commercial problem:** a shopper needs to understand a combination and its price without hidden arithmetic. Demonstrate a coherent brand experience and deterministic local state, not a pretend working shop.

**Customer workflow:** choose finish → choose 1–4 sample objects → toggle one optional display base → inspect itemised total → copy/download the configuration. No checkout or payment CTA.

Proposed state: `{finish, quantity, includeBase, catalogueVersion}`. Finishes are Ivory, Clay and Night palette directions; Night would need approved original product imagery before a complete visual configurator is built. Do not claim an exact product renderer from only colour swatches. Existing C1 images show the ivory/clay visual direction.

### Explicit sample pricing

Use integer cents: each fictional object is `18000`; one optional walnut display base is `4800`; all three finishes use the same sample price. `totalCents = quantity × 18000 + (includeBase ? 4800 : 0)`.

The pictured pair + one base is **€408**. One object without a base is €180; four with one base is €768. All values are invented. Tax, delivery, inventory, discounts, checkout and payment are not modelled. The demo does not manufacture an actual order or claim hardware/audio specifications.

### Meaningful acceptance

- Only known finishes and integer quantity 1–4 are accepted. Never display NaN or a negative price; invalid state blocks export with a useful error.
- Every option change updates the itemised total correctly. Removing the base subtracts exactly €48; finish changes do not add hidden charges. Back/reset states are predictable.
- Future product imagery changes must match the selected, approved finish. Until a render exists, show a clearly labelled palette study, not an inaccurate physical-product preview.
- Native labelled radio groups for swatches, descriptive selected text, keyboard-operable quantity controls and a polite total announcement. No colour-only selection or hover-only information. Motion remains optional.
- Copy/export contains fictional product identity, chosen finish, quantity, line items and “sample prices / no order created”. No cart service, checkout, payment, shipping or email request is made.

**Potential value to test:** price comprehension, successful configuration completion and option-state clarity. No sales uplift, customer reviews or inventory claims.

**Indicative later scope:** 3–5 focused working days for one local configurator, itemised sample calculation, copy/export and QA. Extra product renders and production commerce infrastructure are separate. This is the clearest, smallest commerce proof, but has less workflow depth than Kern/9.

## Shared approval boundary

These definitions are intended to make later development testable, not to authorise it. First approve the visual direction(s), tentative identity, representative module and stated scope. Only then build the chosen flow in a separate task with its own browser tests and review gate. No backend, deployment, real integrations or completed portfolio cases are produced during C1.
