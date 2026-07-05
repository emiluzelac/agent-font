# Agent

**Agent** is a renamed, redistributed fork of **TASA Orbiter**, from the
[TASA Typeface Collection v1.001](https://github.com/localremotetw/TASA-Typeface-Collection/releases/tag/v1.001).

That collection is no longer maintained, and this original v1.001 design is
preferred here over TASA's later 2025 revision — Agent preserves it rather
than tracking upstream's future changes.

**Designed by Local Remote, Weizhong Zhang.** All credit for the original
design goes to them; see the
[TASA Typeface Collection](https://github.com/localremotetw/TASA-Typeface-Collection)
for their other work.

## What's in this repo

`dist/Agent/` contains the built font files:

- **`otf/`** — 13 static OTFs across three optical-size families:
  - Agent Text: Regular, Medium, SemiBold, Bold
  - Agent Deck: Regular, Medium, SemiBold, Bold
  - Agent Display: Regular, Medium, SemiBold, Bold, Black
- **`variable/`** and **`webfonts/`** — four variable fonts, each as `.ttf`
  (desktop/design-app install) and `.woff2` (web):
  - **Agent VF** — the full range: `wght` 400–900, `opsz` 8–60, covering
    all three opticals in one file. Use this if you want to scrub
    continuously across optical size.
  - **Agent Text VF**, **Agent Deck VF**, **Agent Display VF** — the same
    three opticals split into independent, single-purpose variable fonts
    (`wght` only), for when you only need one of them.

## Install

Double-click any `.otf` or `.ttf` file to install on macOS/Windows, or drop
the whole `otf/` and/or `variable/` folder into your system fonts directory.

## Use on the web

```css
@font-face {
  font-family: "Agent Text VF";
  src: url("AgentTextVF.woff2") format("woff2-variations");
  font-weight: 400 700;
}
```

## License

Licensed under the [SIL Open Font License, Version 1.1](LICENSE) — the same
license TASA Orbiter itself was released under. "Agent" is not a Reserved
Font Name.
