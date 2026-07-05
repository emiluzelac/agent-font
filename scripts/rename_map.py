"""Style data and license/copyright text for the TASA Orbiter -> Agent rename."""

STATIC_WEIGHTS = {
    "Text": ["Regular", "Medium", "SemiBold", "Bold"],
    "Deck": ["Regular", "Medium", "SemiBold", "Bold"],
    "Display": ["Regular", "Medium", "SemiBold", "Bold", "Black"],
}

# opsz values (8/32/60) match the named instances upstream actually shipped;
# wght ranges are capped to what upstream shipped as static instances per optical.
SPLIT_VF_AXES = {
    "Text": {"opsz_pin": 8, "wght_range": (400, 700)},
    "Deck": {"opsz_pin": 32, "wght_range": (400, 700)},
    "Display": {"opsz_pin": 60, "wght_range": (400, 900)},
}

COPYRIGHT_NOTICE = (
    "Copyright © 2023 Local Remote (https://localremote.co/). Portions "
    "Copyright © 2026 Emil Uzelac. Renamed \"Agent\"; based on TASA "
    "Orbiter, used and modified under the SIL Open Font License, Version 1.1."
)

OFL_HEADER = (
    "Copyright (c) 2023, Local Remote (https://localremote.co/).\n"
    "Portions Copyright (c) 2026, Emil Uzelac.\n"
    "\n"
    "This is a modified version, renamed \"Agent\", based on TASA Orbiter\n"
    "from the TASA Typeface Collection\n"
    "(https://github.com/localremotetw/TASA-Typeface-Collection), used and\n"
    "redistributed under the SIL Open Font License, Version 1.1.\n"
    "\n"
    "This Font Software is licensed under the SIL Open Font License, Version 1.1.\n"
    "This license is copied below, and is also available with a FAQ at:\n"
    "http://scripts.sil.org/OFL\n"
    "\n"
)
