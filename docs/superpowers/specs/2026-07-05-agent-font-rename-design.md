# Agent font: rename of TASA Orbiter — design

## Goal

Produce a font family named **Agent**, derived from **TASA Orbiter** (from the
[TASA Typeface Collection v1.001](https://github.com/localremotetw/TASA-Typeface-Collection/releases/tag/v1.001)),
by renaming all family/style/PostScript identifiers throughout the compiled
font binaries. TASA Explorer is out of scope.

## Background

The v1.001 release ships TASA Orbiter as compiled binaries only — no UFO,
Glyphs, or designspace source is included. What exists:

- 13 static OTFs across three optical-size sub-families:
  - **Text**: Regular, Medium, SemiBold, Bold
  - **Deck**: Regular, Medium, SemiBold, Bold
  - **Display**: Regular, Medium, SemiBold, Bold, Black
- 1 variable WOFF2 (`TASAOrbiterVF.woff2`) with axes `wght` (400–900) and
  `opsz` (8–60), carrying all 13 styles above as named instances.

Licensed under **OFL 1.1**, with **"TASA Orbiter" as a Reserved Font Name**.
Under OFL, a Reserved Font Name may not be used to name a Modified Version —
renaming to "Agent" is exactly the license's intended path for a fork, not a
gray area. The original copyright notice must be retained; the family name
itself is free to change everywhere (name table, CFF names, file names).

Attribution in the original: designer **Weizhong Zhang**, foundry **Local
Remote** (localremote.co), vendor tag `Loca`.

Because there's no design source, "building" Agent means editing metadata in
the existing compiled binaries with a script — not recompiling outlines.

v1.001 is pinned deliberately, not just "whatever's latest": the collection
is no longer maintained, and this original design is preferred over TASA's
2025 revision. `vendor/` holds exactly this release, permanently — Agent is
a fork of v1.001, not a tracker of upstream's future changes.

## Scope

- **In scope**: TASA Orbiter → Agent (Text/Deck/Display sub-families, all
  13 static weights, plus the variable font).
- **Out of scope**: TASA Explorer (untouched).
- **Deliverables**: same binary types the upstream release ships — 13 static
  OTFs + 1 variable WOFF2 — **plus** one added artifact: a variable **TTF**
  decompressed from the WOFF2, since a `.woff2` isn't directly installable as
  a system font on macOS/Windows, and a variable TTF is useful for design
  apps (Figma, Illustrator) and OS installation. Everything else mirrors
  upstream 1:1.

## Naming scheme

| Original | Renamed |
|---|---|
| TASA Orbiter Text | Agent Text |
| TASA Orbiter Deck | Agent Deck |
| TASA Orbiter Display | Agent Display |
| TASA Orbiter VF (typographic family) | Agent VF |
| `TASAOrbiterText-Bold` (PostScript) | `AgentText-Bold` |
| `TASAOrbiterVF-TextRegular` (PostScript) | `AgentVF-TextRegular` |

Weight/style names (Regular/Medium/SemiBold/Bold/Black) and the
Text/Deck/Display optical-size split are unchanged — only the "TASA
Orbiter" → "Agent" substitution is applied, consistently, everywhere it
appears (family name, full name, PostScript name, unique ID, typographic
family/subfamily, CFF `FontName`/`FullName`).

File names follow the same pattern:
`AgentText-Regular.otf`, `AgentDeck-Bold.otf`, `AgentVF.woff2`, `AgentVF.ttf`, etc.

## What gets changed in each font (technical)

For every static OTF and the variable font:

- **`name` table** — nameIDs 1, 2, 3, 4, 6, 16, 17: replace `TASA Orbiter` →
  `Agent` and `TASAOrbiter` → `Agent` (PostScript-safe form, no space).
  NameID 3 (unique identifier, e.g. `1.000;Local Remote;TASAOrbiterText-Regular`)
  gets its PostScript-name segment updated to match.
- **CFF table** (static OTFs only) — `FontName` and `FullName` in the CFF
  top dict get the same substitution (this is what Font Book/macOS actually
  reads on some code paths, independent of the `name` table).
- **NameID 0 (copyright)** — the original notice is **retained** (OFL
  requirement), with a modification notice appended:
  > Copyright © 2023 Local Remote (https://localremote.co/). Portions
  > Copyright © 2026 Emil Uzelac. Renamed "Agent"; based on TASA Orbiter,
  > used and modified under the SIL Open Font License, Version 1.1.
- **NameID 9 (Designer), NameID 13/14 (license text/URL), `OS/2.achVendID`
  (`Loca`), NameID 11 (vendor URL, stays `localremote.co`)** — left
  unchanged; the underlying design and license don't change, only the
  brand name does.
- **STAT table, `fvar` axes/instances, OS/2 weight class, `head.macStyle`,
  glyph outlines, hinting** — untouched. These don't reference the brand
  name and don't need to change for a rename.
- A new **`OFL.txt`** is generated for the Agent build: same OFL 1.1 license
  body, header updated to show it's a modified/renamed version, retaining
  Local Remote's original copyright line above the new one. "Agent" is not
  declared as a new Reserved Font Name (keeps it simple; can be added later
  if you ever want to prevent further downstream renaming).

## Implementation approach

A small, data-driven **Python script using `fontTools`**, not a font-editor
GUI edit and not a from-scratch `fontmake`/AFDKO rebuild (there's no source
to rebuild from, and outlines aren't changing).

```
Font/
  vendor/
    TASA-Orbiter-v1.001/         # pristine upstream files, never hand-edited
      OFL.txt
      otf (static)/*.otf         # 13 files
      woff2 (VF)/TASAOrbiterVF.woff2
  scripts/
    rename_map.py                 # data: old->new strings, copyright text
    build_agent.py                 # fontTools pipeline: vendor/ -> dist/
  dist/
    Agent/
      otf/AgentText-Regular.otf, ...   (13 files)
      webfonts/AgentVF.woff2
      variable/AgentVF.ttf
      OFL.txt
  LICENSE                          # copy of dist/Agent/OFL.txt, for GitHub's license detection
  README.md
```

`build_agent.py` is re-runnable: if TASA ships a new Orbiter release later,
drop the new files into `vendor/` and re-run the script to regenerate `dist/`.

## Hosting & README

- **Repo**: public, `https://github.com/emiluzelac/agent-font` (name checked
  available). Chosen over the bare `agent` to avoid ambiguity with
  agent/AI-agent projects, and easy to rename later since GitHub keeps a
  redirect from the old name.
- **README.md** covers:
  - What Agent is and why it exists (a preserved/renamed fork of TASA
    Orbiter v1.001, from a now-unmaintained collection whose original
    2023 design is preferred here over TASA's later revision).
  - **Designed by Local Remote, Weizhong Zhang** — credited explicitly,
    with a link to the original
    [TASA Typeface Collection](https://github.com/localremotetw/TASA-Typeface-Collection)
    and the v1.001 release.
  - License: SIL Open Font License 1.1, linking `LICENSE`.
  - Family/style list (Agent Text/Deck/Display × weights, Agent VF) and
    where to find the built files in `dist/Agent/`.
  - Basic install/usage instructions (desktop install of the OTFs or the
    variable TTF; `@font-face` snippet for `AgentVF.woff2` on the web).

## Verification plan

- `fontTools ttx`/Python dump of the `name` table on a sample from each
  sub-family (Text/Deck/Display + the VF) confirming no "TASA" or "Orbiter"
  string remains anywhere, and that copyright/designer/license fields match
  the intended values above.
- Install a couple of the generated OTFs plus the variable TTF locally and
  confirm they appear as "Agent Text", "Agent Deck", "Agent Display" (and
  "Agent VF") in Font Book/system font list, with the expected weight
  instances.
- Render a sample string with each installed style as a quick visual sanity
  check that outlines/hinting are unaffected by the metadata edit.

## Decisions (confirmed)

1. Modification copyright holder: **Emil Uzelac**.
2. "Agent" is **not** declared a new Reserved Font Name.
3. Vendor URL (nameID 11) stays `localremote.co`.
4. Repo: public, `github.com/emiluzelac/agent-font`, with a README crediting
   Local Remote / Weizhong Zhang as the original designer.
