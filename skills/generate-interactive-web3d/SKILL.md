---
name: generate-interactive-web3d
description: Generate a polished, responsive, single-file interactive 3D experience directly from any natural-language subject or scene prompt. Use for procedural WebGL/Three.js models, interactive landmarks, machines and products, vehicles, scientific visualizations, explodable assemblies, mechanism simulations, educational 3D exhibits, and visually impressive browser-based 3D micro-apps produced in one response without tools or external model assets.
---

# Generate Interactive Web3D

Create a subject-specific interactive 3D instrument, not a generic orbiting model. Infer what is distinctive, inspectable, and operable about the requested subject, then express those qualities through procedural geometry, meaningful views, causal interactions, and an exhibition-grade interface.

Reason silently. Return only one complete HTML document from `<!DOCTYPE html>` through `</html>`. Never return Markdown fences, commentary, omitted-code placeholders, or a plan.

## Honor the one-response contract

● Produce one self-contained HTML file with embedded CSS and JavaScript.
● Do not use searches, tools, local files, build steps, APIs, generated assets, or a second response.
● Do not load GLTF/OBJ models, images, external textures, HDRIs, fonts, JSON, or other subject data.
● Build the subject from procedural geometry and CSS-drawn interface elements. Runtime-generated CanvasTexture assets are allowed for paper text, gauges, labels, diagrams, subtle material patterns, and other prompt-relevant details; keep them deterministic, correctly color-spaced, and inexpensive.
● Allow only a version-pinned Three.js CDN dependency. Use this import map unless the user provides another compatible pin:

```html
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.183.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.183.0/examples/jsm/"
  }
}
</script>
```

● Import three and addons such as OrbitControls from the map inside `<script type="module">`.
● Prefer a complete, reliable, high-detail experience over excessive scope. Never truncate the document.
● Keep JavaScript readable and non-minified. Use descriptive local variables, line breaks, and small functions. Token savings never justify compressed one-line construction code that hides scope or lifecycle defects.

## Design the experience before coding

Silently derive a compact experience specification from the prompt.

### 1. Classify the subject

Choose the closest behavior family, combining families when appropriate:
● Architecture or landmark: spatial hierarchy, construction, circulation, structure, light, cutaways.
● Machine or product: housings, subassemblies, controls, moving linkages, input/output, service access.
● Vehicle: body, propulsion, steering, suspension, doors, controls, airflow or travel state.
● Scientific or abstract system: layers, fields, cycles, parameters, scale changes, time evolution.
● Natural form or organism: anatomy, growth, articulation, layers, environmental response.
● Scene or environment: composition, atmosphere, time of day, paths, focal events, spatial storytelling.

Do not expose this classification in the output.

### 2. Derive a subject signature

Identify:
● The unmistakable silhouette and proportions;
● 6–12 semantic component families;
● Characteristic colors, materials, finishes, repeated motifs, and construction logic;
● 2–6 actions or state changes that reveal how the subject works;
● 5–10 camera views that best explain this particular subject;
● One visual environment and interface language appropriate to its era and function.

Define 3–7 critical identity features that must not be lost even if the output must be simplified. Reject the silent plan if any critical feature is represented only by a generic box, cylinder, or unrelated decoration.

Assume the user's prompt may be only one sentence naming the subject and one or two behaviors. Do not wait for the user to specify materials, camera views, mechanisms, component counts, history, or interface design. Infer these from the subject signature and spend the output budget on the details that make the named object unmistakable.

Perform a silent Hero-view occlusion check: every critical feature must be visible, correctly layered, and large enough to read. Lower or reshape housings, decks, walls, and shells that hide the very controls or mechanism the subject is known for.

Do not copy control names from an unrelated subject. Derive every control from the named object's real construction, operation, inspection, or explanatory state.

### 3. Set a quality budget

Prioritize in this order:
1. Complete valid HTML and working imports.
2. Recognizable silhouette and correct major proportions.
3. Meaningful subject-specific interaction or mechanism.
4. Semantic parts, selection, and readable state transitions.
5. Medium structural detail and repeated motifs.
6. Premium lighting, materials, UI, labels, and subtle motion.
7. Optional secondary mechanisms.

If output length becomes risky, simplify tiny decoration before removing the defining mechanism, view system, selection, responsiveness, or error handling.

## Build a convincing procedural model

● Model the complete subject rather than a symbolic placeholder or a few stacked primitives.
● Work from large silhouette to medium structure to repeated detail.
● Use small reusable helpers for boxes, cylinders, lathed profiles, extruded outlines, beams between points, radial arrays, grids, curved tubes, panels, gears, keys, ribs, fasteners, and trim.
● Use LatheGeometry, ExtrudeGeometry, ShapeGeometry, curves/tubes, and custom BufferGeometry when basic primitives cannot express a defining contour.
● Align elongated members from actual endpoints with direction vectors or quaternions. Never guess rotations that make beams, rods, rails, rafters, or cables pierce adjacent surfaces.
● Place parts according to plausible support and connection logic. Avoid floating decoration and intersecting assemblies.
● Use bevels, layered edges, seams, collars, caps, recessed panels, and material changes to prevent a toy-block appearance.
● For revolved closed profiles, order profile points so the outward surface has outward normals. If winding is uncertain, use a deliberate double-sided material for that shell. Never let a decorative underside replace or occlude the primary exterior surface.
● Make repeated features visible at the initial camera distance. Avoid geometry too small to affect the image.
● Target roughly 120–500 visible objects and smooth interaction on a laptop. Use InstancedMesh for repeated non-selectable detail; use regular meshes when individual motion or identification is required.
● Reuse geometries and materials where safe. Never mutate a shared material for one selection or mode without isolating or restoring all consumers.
● Silently build in passes: blockout → structure → form → materials → detail → interaction. At each pass, preserve the critical identity features established earlier. Do not spend output on micro-detail until the silhouette and component hierarchy are convincing.
● Never silently replace an unsupported defining shape with a box. Choose a supported procedural approximation—profile, lathe, extrusion, curve sweep, fitted shell, tapered network, or custom buffer geometry—and simplify noncritical regions instead.
● Make every construction helper self-contained: all geometry dimensions, loop indexes, materials, parent groups, and metadata it uses must be parameters or declared locals. Before returning, silently trace one real call to every custom helper and reject any reference to a name that exists only in another loop or function.

### Geometry strategies by subject

● Historic architecture: build foundation, load-bearing frame, enclosure, roof/facade system, circulation, ornament, and surrounding datum. Generate curved roofs from revolved or sampled profiles rather than finished cones. Make tile/rib lines follow the surface.
● Mechanical products: build the outer case and the visible mechanism. Include shafts, pivots, linkages, keys, levers, rollers, gears, springs, guides, fasteners, and material breaks when relevant. Design moving parts around real pivot axes.
● Vehicles: establish wheelbase and body proportions first, then glazing, wheels, lights, cabin, drivetrain cues, and articulated controls.
● Scientific systems: use clear scale, color encoding, reference axes, layers, field lines, particles, and time controls. Do not substitute random decorative motion for an explanatory relationship.
● Natural subjects: preserve organic silhouette with profiles, curves, tapered segments, layered surfaces, and coherent articulation. Avoid perfect primitive repetition where natural variation matters.

## Create a semantic scene architecture

Build one root assembly and maintain explicit registries such as parts, selectables, animatedParts, and viewPresets. Use one manifest-like object as the source of truth for part identity, mesh binding, exploded offsets, annotations, mechanism channels, and optional telemetry/status. Keep geometry construction separate from interaction and presentation logic.

Use scene-graph parents as real pivots, sockets, and articulation roots. Parent related children to a frame or module so local motion remains simple and other assembly transforms propagate correctly.

Give each meaningful part or part group stable metadata:
● partName: concise human-readable name;
● category: semantic family;
● description: one useful explanatory sentence;
● originalPosition, originalQuaternion, and optionally originalScale;
● explodeOffset or group-level exploded transform;
● mechanism data such as pivot, axis, travel range, phase, or parent channel when applicable.
● annotation anchors and optional status/telemetry bindings when they materially explain the subject.

Keep one appState object for view, explode amount, active mechanism, selection, labels, material mode, auto-rotation, and domain-specific parameters. All UI must reflect this state.

## Make interaction reveal the subject

### Provide prompt-specific views

● Create 5–10 concise view presets named for the subject, not merely Camera 1/2/3.
● Include a strong Hero view plus explanatory views such as elevation, underside, interior, mechanism close-up, operator view, material close-up, cutaway, top, or rear when relevant.
● Smoothly interpolate camera position and OrbitControls.target; do not teleport.
● Interrupt camera interpolation when the user starts orbiting.
● Frame each view intentionally. Never aim through geometry or crop the defining feature.

### Implement a readable exploded assembly

● Store immutable base transforms after construction.
● Drive explosion with normalized explodeTarget and smoothly damped explodeCurrent.
● Recompute each transform from its base on every frame. Never add offsets cumulatively.
● Explode in assembly order rather than as a particle burst. Keep related parts clustered and preserve the subject silhouette at 100%.
● Prefer group-aware paths: housings open first, functional modules separate next, fine linkages move last; or foundations remain low while structural and roof layers separate upward.
● Keep the full exploded bounding box near 1.6–1.9 times assembled width and at most about 2.2 times assembled height unless the subject demands another axis.
● Pair explosion with framing. Define an Exploded camera preset or compute the expanded Box3 after transforms and smoothly dolly the camera/target to include the complete assembly with 10–18% margin. On reassembly, return to the prior explanatory view. A 100% exploded state with cropped parts fails the experience.
● Fit against the actual unobstructed 3D viewport, not the browser window. On desktop, prefer a layout that reserves physical width for the control rail (grid-template-columns: minmax(0,1fr) railWidth) so the renderer canvas and camera aspect describe only the visible stage. If the rail overlays the canvas, subtract its occupied width and shift the camera/target so the subject is centered in the remaining safe rectangle. A model hidden under a translucent panel is still cropped.
● Treat this framing as mandatory, not optional. Implement either a generously distant subject-specific Exploded preset or a fit routine equivalent to:

```js
root.updateMatrixWorld(true);
box.setFromObject(root);
box.getCenter(center);
box.getSize(size);
const vFov = THREE.MathUtils.degToRad(camera.fov);
const fitHeight = size.y / (2 * Math.tan(vFov / 2));
const fitWidth = size.x / (2 * Math.tan(vFov / 2) * camera.aspect);
const distance = Math.max(fitHeight, fitWidth) * 1.25;
const direction = camera.position.clone().sub(controls.target).normalize();
// Tween controls.target to center and camera.position to center + direction * distance.
```

● Run the fit after exploded transforms have updated, or precompute bounds from base transforms plus full offsets. Switching to 100% explosion must also switch to this framing; switching back must restore the prior view.
● Because explosion is damped over time, do not fit only on the button click while parts are still assembled. Either fit continuously while explodeCurrent changes, refit once it is within a small epsilon of explodeTarget, or compute the final bounds analytically. Re-run the fit after resize, control-rail collapse, orientation change, and mobile breakpoint changes.
● Never approximate animation completion with a short fixed setTimeout such as 60–500 ms; damping duration depends on frame timing and the final parts may continue beyond the fitted box. Keep a needsFinalExplodeFit flag. In the animation loop, after transforms update, when Math.abs(explodeCurrent - explodeTarget) < 0.005, run the fit exactly once and clear the flag. Set it again whenever the target, stage size, rail state, or widest-pose parameter changes. Alternatively compute the 100% bounds from immutable bases plus full offsets without waiting.
● The bounds source must include the finial/crown, antennas, stairs, railing, handles, exhausts, vessels, labels intended to remain visible, and every exploded child. Do not fit only a handpicked subset or omit a small top/bottom identity feature because it has no selection metadata.
● Validate the result geometrically: project all eight corners of the final world-space Box3 through the active camera and require them to remain inside a normalized safe frame (approximately x/y ±0.82, adjusted for intentional ground contact). Include tall vessels, antennas, eaves, stairs, plinths, shadows, and labels that communicate identity. Do not judge framing only by whether the central mass is visible.
● Connect a slider and Explode/Assemble action to the same state, update labels live, and support repeated reversal without drift.

### Simulate causal mechanisms

● Derive actions from the requested subject and implement at least one convincing causal chain when it has moving parts.
● Animate around correct pivots and axes. Use parent groups for articulated components.
● Show cause and effect: a key press moves its key, linkage, striker and output; a crank rotates connected gears; a door handle unlatches before the door opens; a control surface changes orientation and airflow indication.
● Accept the most natural input when feasible: keyboard events for a keyed text machine or instrument, drag/slider for a translating assembly or valve, click for doors or levers, and time control for a scientific process.
● Make mechanisms reversible, bounded, and interruptible. Avoid perpetual unrelated motion.
● Keep secondary animation channels independent so changing the camera or explode amount does not corrupt mechanism state.

### Identify parts

● Use Raycaster.setFromCamera() with pointer coordinates from the renderer canvas rectangle.
● Raycast only selectable parts, using a dedicated array or Three.js layer. Exclude ground, helpers, labels, and environment.
● Distinguish click from orbit drag using pointer travel or timing.
● On hover, show a compact tooltip and pointer cursor.
● On click, persist selection, highlight safely, and populate a part panel with name, category, and description.
● Restore the prior material correctly, including arrays and shared materials.
● Add a projected HTML marker or leader line for the selected part.
● Provide Clear Selection and optional Labels controls. Curate labels; do not cover the screen with every part name.

## Build a domain-adaptive control console

Treat the page as a polished interactive exhibit or simulation, not a generic dashboard.
● Keep the 3D viewport dominant. Use a narrow translucent control rail, compact segmented controls, small uppercase section labels, and quiet status readouts.
● On desktop, reserve a real stage region for the model and a separate rail region for controls whenever the rail is wider than about 22% of the page. Overlay treatments may look elegant, but they must not consume the model's framing space. On mobile, use a compact bottom sheet or collapsible rail with a guaranteed stage height; never leave only a thin strip of canvas behind a full-height panel.
● Organize controls by intent: Views, Mechanisms/Actions, Parameters, Display, and Selection.
● Generate only controls that produce real behavior. Never include decorative toggles.
● Use the subject's terminology in control names.
● Add a short title, subject subtitle, current state indicator, control hint, and part information area.
● Provide Reset and a concise audit/status readout when useful.
● Use semantic buttons, labels, visible focus states, and keyboard-operable controls.
● Prevent interface pointer events from reaching the canvas.
● On narrow screens, collapse secondary descriptions and control groups while preserving core interaction and a large usable viewport.
● Include a loading overlay that clears only after initialization and a visible fatal-error panel for unsupported WebGL or initialization failure.

## Compose an exhibition-grade visual scene

● Match the environment to the subject: bright architectural study, dark product studio, technical laboratory, atmospheric landscape, or another justified treatment.
● Use a perspective camera with a purposeful three-quarter Hero composition and sensible orbit limits.
● Fit the subject using Box3 or derived dimensions. Keep the full subject comfortably inside the viewport and offset it away from the control rail.
● Perform two framing audits: one for the initial Hero state and one for the maximum-extent state (fully exploded, cut away, doors open, articulated, or animated to its widest pose). The full critical silhouette must remain inside the safe stage in both states; check every preset that materially changes bounds.
● Use antialiasing, capped pixel ratio, SRGBColorSpace, ACESFilmicToneMapping, and tuned exposure.
● Combine hemisphere/ambient fill, a shadow-casting key light, and a softer rim/accent. Use PCFShadowMap, not deprecated PCFSoftShadowMap.
● Add a receiving ground or plinth, subtle fog when appropriate, and a procedural CSS or scene background. Avoid empty default black and avoid overpowering scenery.
● Use plausible roughness, metalness, transparency, and emissive accents. Provide neutral/look-development material modes only when they help inspect form.
● Design materials as a system, not a color table. For every critical material family, combine: (1) appropriate geometry scale and seams, (2) physically plausible PBR response, (3) small deterministic variation, and (4) lighting that produces readable grazing highlights. A uniformly colored MeshStandardMaterial on one large shell is not a convincing tiled roof, lacquered case, stone terrace, skin layer, or machined metal assembly.
● Preserve a clear material hierarchy. The dominant identity surface should retain roughly 70–85% of its authored base family, with accent metals or contrasting trim confined to structurally plausible edges and details. Never alternate an accent color across every repeated rib, blade, key, tile, or panel merely to create visual activity.
● Keep dielectric materials such as ceramic, paint, wood, stone, paper, rubber, and skin at or near metalness: 0. Use MeshPhysicalMaterial selectively for coated surfaces: clearcoat and low clearcoat roughness can express glazed ceramic or lacquer, while transmission is reserved for real glass or fluid-like shells. Do not make ceramics look metallic merely to create highlights.
● Runtime procedural textures are encouraged when a flat material would erase identity. Generate compact deterministic CanvasTexture color, roughness, stripe, grain, speckle, print, patina, or wear maps; set color maps to SRGBColorSpace, leave roughness/normal-like data in NoColorSpace, set sensible wrapping/repeat, and cap anisotropy from renderer.capabilities.getMaxAnisotropy(). Do not update static textures every frame.
● Prefer geometry for silhouette-changing and close-up details—tile courses, ribs, panel gaps, key legends, fasteners, mortar joints, stitched seams—and textures for sub-surface variation. A painted line cannot replace a raised roof rib, and hundreds of invisible micro-meshes cannot replace tonal variation.
● Repeated surface details require a continuous substrate. Roof tiles, louvers, grilles, scales, feathers, shingles, cooling fins, and panel seams must sit on or overlap a readable base surface unless the real object is genuinely open. Never let decorative linework turn a solid identity surface into a wireframe cage or transparent grid.
● Create environment reflections without external HDR files when coated or metallic materials need them. A small RoomEnvironment/PMREMGenerator setup or deliberate large area-like lights is acceptable; dispose temporary PMREM resources. Keep reflection strength restrained so the subject's base color remains legible.
● Audit highlight clipping under the final exposure and environment. White stone, paper, chrome, glazed ceramic, and polished paint must retain midtone variation and edge definition rather than becoming flat white or pastel. If reflections wash out the base color, reduce environment intensity/exposure, increase roughness slightly, or deepen the base value before adding more lights.
● Include at least one material or grazing-light close-up when finish quality is central to the subject. If a Look-dev toggle is shown, it must switch between a neutral inspection setup and the authored presentation materials rather than merely changing the background.
● Preserve shadow detail. Black housings still need readable planes, seams, controls, and edge highlights; use fill/rim lighting and nonzero roughness rather than crushing large regions to featureless black.
● Include slow optional auto-rotation for static exhibits; pause it on user interaction. Do not auto-rotate operator-driven machines while they are being used.
● When useful, expose a small performance/status audit derived from renderer.info and actual app state; never fabricate metrics.

## Resist benchmark specialization

● Do not assume the prompt belongs to a known evaluation set, even when its wording seems familiar.
● Do not embed named landmark dimensions, fixed component counts, signature colors, model-specific mechanisms, or a canned list of views for any particular object.
● Infer those facts from the current subject using the subject-signature process. If uncertain, preserve the most widely recognizable form and construction logic while avoiding fabricated precision.
● Generalize every quality correction to a reusable invariant. For example: preserve a continuous substrate under repeated surface units; keep accent materials subordinate to the dominant material family; explode repeated fine parts with their semantic parent; fit the camera only after the widest state converges.
● Let the current subject determine whether repeated units form courses, rings, grids, scales, blades, keys, feathers, panels, fins, or another topology. Never reuse a topology simply because it worked for a prior object.
● Evaluation prompts and their expected visual facts belong outside this skill. The generation model must not receive hidden benchmark answers.

## Animate efficiently and safely

● Use one requestAnimationFrame loop and THREE.Timer or a timestamp-derived delta. Prefer timer.connect(document) so hidden tabs do not create large deltas. Avoid deprecated THREE.Clock in Three.js 0.183+.
● Clamp delta after background-tab pauses.
● Update camera interpolation, controls, explosion, mechanism channels, selection marker, subtle ambient motion, and rendering in that loop.
● Avoid allocating geometries, materials, or many temporary vectors per frame.
● Handle resize by updating camera aspect/projection and renderer size/pixel ratio.
● Use renderer.localClippingEnabled only when a real section control is implemented.
● Keep the core page functional if an optional effect fails.

## Audit the final document silently

Before returning, verify the actual code:
● The document begins with `<!DOCTYPE html>` and ends with `</html>`.
● HTML tags, strings, template literals, braces, and parentheses are closed.
● Every queried DOM ID exists and every identifier is declared before use.
● Imports exactly match the pinned import map; no legacy global THREE assumption is mixed with modules.
● No external subject asset, image, texture, font, or undocumented variable is referenced.
● The renderer is appended, the animation loop starts once, loading clears, resize works, and damping calls controls.update().
● Initial framing shows the complete recognizable subject.
● Hero and maximum-extent framing are computed against the unobstructed stage, not the full window; no critical feature sits under the control rail or outside the safe frame.
● Every custom helper is called with valid arguments and references only its parameters, declared locals, or intentional module-level state. Pay special attention to loop indexes used by nested helpers.
● Every visible control changes real state and can be reversed or reset.
● View presets animate to valid compositions.
● Explode works repeatedly without drift and remains readable at 100%.
● Causal mechanisms use correct pivots, stay bounded, and do not fight explosion or camera state.
● Selectable parts contain metadata; selection ignores non-parts and restores highlights correctly.
● Desktop and mobile layouts remain usable.
● No deprecated Three.js API warning is knowingly introduced.
● Critical material families remain distinguishable in both Hero and close-up views: their highlight width, roughness, coating, joints, scale detail, and color variation match what they are meant to represent. No major identity surface is just a smooth flat-colored primitive.
● Any displayed part count, renderer statistic, status, or progress value is derived after construction and matches actual state; no metric remains zero, stale, or placeholder unless zero is truthful.

Return only the complete HTML.
