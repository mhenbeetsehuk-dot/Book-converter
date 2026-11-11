# DARK FRONTIER — Visual Design Specification V1

Status: Proposed visual direction, pending first rendered benchmark.
Reference: photorealistic cinematic CGI, with an original production identity. Do not copy copyrighted characters, sets, frames, or proprietary assets.

## Visual canon
- Realistic anatomy and restrained performance; no exaggerated cartoon proportions.
- Spacecraft: functional industrial engineering, layered panels, visible mechanisms, believable wear.
- Planet: lifeless dark basalt, mineral dust, deep shadows; no Earth-like vegetation, blue skies or habitable terrain.
- Palette: charcoal #10141A, steel #303A46, slate #536C7D, rust #874838, cyan #4CA6B0, silver #C4CCD0.
- Motivated lighting: ship lamps, thrusters, instrumentation and sparse mineral luminescence.
- Cameras: cinematic tracking and deliberate cuts; physically credible scale, lensing and movement.
- Materials: rough rock, worn metal, polymer, glass, pressure-suit fabric; use PBR textures where available.
- Audio: low mechanical hum, thruster rumble, landing-gear impacts, near-silence; avoid copyrighted sound recordings.

## Render tiers
| Tier | Resolution | Engine | Purpose |
| --- | --- | --- | --- |
| Draft | 640x360 | Eevee | Blocking and continuity |
| Preview | 1280x720 | Eevee | Materials and camera approval |
| Final | 1920x1080 | Cycles selectively | Approved shots only |

All tiers target 24 fps. Use resumable frame-range rendering, compressed assets and per-shot jobs. Free Colab GPU/CPU availability is limited and not guaranteed.

## Benchmark scene TEST-001 — The First Descent
Length: 30 seconds, 720 frames at 24 fps.
This is an original technical demonstration, not yet a manuscript-adapted scene.

| Shot | Seconds | Frames | Action |
| --- | --- | --- | --- |
| 01 Orbital approach | 0-6 | 1-144 | Craft approaches black barren planet, wide tracking |
| 02 Descent systems | 6-11 | 145-264 | Thruster and panel close-ups |
| 03 Surface approach | 11-18 | 265-432 | Searchlights illuminate fractured basalt and dust |
| 04 Touchdown | 18-24 | 433-576 | Landing gear contacts surface, dust disperses |
| 05 Silence | 24-30 | 577-720 | Engines quiet, static wide shot, fade to black |

## Minimum assets
- One reusable spacecraft model with thruster, lights and landing gear.
- One modular basalt terrain patch with scattered rocks and dust shader.
- One rigged camera path per shot.
- Emissive lamps and thruster effects.
- Optional procedural dust; avoid costly volumetrics in draft mode.

## Acceptance tests
1. Same spacecraft mesh and material IDs across five shots.
2. No Earth-like terrain, vegetation or daylight.
3. All 720 frames accounted for, without duplicated or missing ranges.
4. Preview and final use the same camera and animation data.
5. Outputs include render logs, frame metadata and recoverable checkpoints.
6. Benchmark must be actually rendered and visually reviewed before marked complete.

## Current state
Specification and shot plan only. No TEST-001 assets, animations or render outputs have been produced or validated yet.
