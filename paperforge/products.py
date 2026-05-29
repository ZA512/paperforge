from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict

from .models import NavLink, ProductOption, ProductSpec, ProjectSlot, RenderRequest, Theme


FORMAT_PRESETS = {
    "tablet_16_10": {
        "label": "Tablette 16:10",
        "width_px": 1280,
        "height_px": 800,
    },
    "tablet_tcl_nxtpaper_11_plus": {
        "label": "TCL NXTPAPER 11+",
        "width_px": 2200,
        "height_px": 1440,
    },
    "a4": {
        "label": "A4",
        "width_px": 842,
        "height_px": 595,
    },
    "a5": {
        "label": "A5",
        "width_px": 595,
        "height_px": 420,
    },
}

ORIENTATION_LABELS = {
    "landscape": "paysage",
    "portrait": "portrait",
}

COVER_STYLES = {
    "solid": "Aplat",
    "frame": "Cadre",
    "diagonal": "Diagonal",
    "terminal": "Terminal",
    "cyberpunk": "Cyberpunk",
}


PROJECT_MANAGEMENT_99 = ProductSpec(
    slug="project_management_99",
    label="Gestion de projets - 99 projets",
    template_file="products/project_management_99.html.j2",
    options=(
        ProductOption(
            key="page_format",
            label="Format",
            option_type="select",
            default="tablet_16_10",
            choices=tuple(FORMAT_PRESETS.keys()),
        ),
        ProductOption(
            key="orientation",
            label="Orientation",
            option_type="select",
            default="landscape",
            choices=tuple(ORIENTATION_LABELS.keys()),
        ),
        ProductOption(
            key="project_count",
            label="Nombre de projets",
            option_type="number",
            default=99,
            min_value=1,
            max_value=99,
        ),
        ProductOption(
            key="pages_per_project",
            label="Pages par projet",
            option_type="number",
            default=2,
            min_value=1,
            max_value=4,
        ),
        ProductOption(
            key="journal_pages",
            label="Pages journal du jour",
            option_type="number",
            default=2,
            min_value=1,
            max_value=4,
        ),
        ProductOption(
            key="radar_pages",
            label="Pages rappel",
            option_type="number",
            default=2,
            min_value=1,
            max_value=4,
        ),
        ProductOption(
            key="cover_style",
            label="Couverture",
            option_type="select",
            default="solid",
            choices=tuple(COVER_STYLES.keys()),
        ),
        ProductOption(
            key="cover_color",
            label="Couleur couverture",
            option_type="text",
            default="#176f75",
        ),
    ),
)


BASE_THEME_TOKENS = {
    "ink": "#162024",
    "muted": "#647174",
    "paper": "#f7f4ee",
    "page": "#fbf8f0",
    "line": "#cfc7b8",
    "line_soft": "#e2dbce",
    "accent": "#176f75",
    "accent_2": "#c84f35",
    "header_bg": "#eee7da",
    "header_text": "#243135",
    "footer": "#8a8580",
    "body_font": '"Segoe UI", "Helvetica Neue", Arial, sans-serif',
    "heading_font": '"Segoe UI", "Helvetica Neue", Arial, sans-serif',
}


def theme_tokens(**overrides: str) -> dict[str, str]:
    tokens = dict(BASE_THEME_TOKENS)
    tokens.update(overrides)
    return tokens


THEMES = {
    "pro_landscape": Theme(
        slug="pro_landscape",
        label="Pro clair",
        css_file="themes/pro_landscape.css",
        page_size="tablet_landscape_16_10",
        preview_class="preview-pro",
        tokens=theme_tokens(),
    ),
    "ledger_blue": Theme(
        slug="ledger_blue",
        label="Bleu registre",
        css_file="themes/pro_landscape.css",
        page_size="tablet_landscape_16_10",
        preview_class="preview-ledger",
        tokens=theme_tokens(
            ink="#152532",
            muted="#5b7180",
            paper="#edf4f7",
            page="#f8fcfd",
            line="#bfd0d8",
            line_soft="#d7e5ea",
            accent="#2f6f8f",
            accent_2="#bf6f4a",
            header_bg="#dcebf0",
            header_text="#183447",
            footer="#6f8792",
            body_font='"Candara", "Segoe UI", sans-serif',
            heading_font='"Georgia", "Cambria", serif',
        ),
    ),
    "sage_focus": Theme(
        slug="sage_focus",
        label="Sauge focus",
        css_file="themes/pro_landscape.css",
        page_size="tablet_landscape_16_10",
        preview_class="preview-sage",
        tokens=theme_tokens(
            ink="#1e2a24",
            muted="#69736a",
            paper="#eef1e7",
            page="#fbfbf4",
            line="#c6cfbb",
            line_soft="#dfe5d6",
            accent="#4f765f",
            accent_2="#a15e4f",
            header_bg="#e2eadb",
            header_text="#203328",
            footer="#788070",
            body_font='"Trebuchet MS", "Segoe UI", sans-serif',
            heading_font='"Cambria", "Georgia", serif',
        ),
    ),
    "graphite_lime": Theme(
        slug="graphite_lime",
        label="Graphite lime",
        css_file="themes/pro_landscape.css",
        page_size="tablet_landscape_16_10",
        preview_class="preview-graphite",
        tokens=theme_tokens(
            ink="#151719",
            muted="#656a6d",
            paper="#f1f1ec",
            page="#fbfaf5",
            line="#c8c8bd",
            line_soft="#deded5",
            accent="#30363c",
            accent_2="#b7c847",
            header_bg="#e5e4df",
            header_text="#111315",
            footer="#777974",
            body_font='"Segoe UI", "Helvetica Neue", Arial, sans-serif',
            heading_font='"Constantia", "Cambria", serif',
        ),
    ),
    "copper_workshop": Theme(
        slug="copper_workshop",
        label="Atelier cuivre",
        css_file="themes/pro_landscape.css",
        page_size="tablet_landscape_16_10",
        preview_class="preview-copper",
        tokens=theme_tokens(
            ink="#241d18",
            muted="#77695f",
            paper="#f3eadb",
            page="#fffaf1",
            line="#d2bfa6",
            line_soft="#eadcc8",
            accent="#8c4a2f",
            accent_2="#27646f",
            header_bg="#ead9c2",
            header_text="#2f241c",
            footer="#8a7a68",
            body_font='"Georgia", "Cambria", serif',
            heading_font='"Georgia", "Cambria", serif',
        ),
    ),
    "terminal_green": Theme(
        slug="terminal_green",
        label="Terminal vert",
        css_file="themes/pro_landscape.css",
        page_size="tablet_landscape_16_10",
        preview_class="preview-terminal",
        tokens=theme_tokens(
            ink="#0d1c14",
            muted="#4e6f5e",
            paper="#edf3ea",
            page="#fbfff8",
            line="#a9c6b0",
            line_soft="#d9eadb",
            accent="#1f8f4d",
            accent_2="#89ff9b",
            header_bg="#dcebdd",
            header_text="#102417",
            footer="#5f7f67",
            body_font='"Lucida Console", Consolas, "Courier New", monospace',
            heading_font='Consolas, "Lucida Console", monospace',
        ),
    ),
    "cyberpunk_neon": Theme(
        slug="cyberpunk_neon",
        label="Cyberpunk neon",
        css_file="themes/pro_landscape.css",
        page_size="tablet_landscape_16_10",
        preview_class="preview-cyberpunk",
        tokens=theme_tokens(
            ink="#161524",
            muted="#6f6587",
            paper="#f4f1fb",
            page="#fffaff",
            line="#c9b9e6",
            line_soft="#eadff8",
            accent="#d12a8c",
            accent_2="#00a7b5",
            header_bg="#efe0ff",
            header_text="#20152d",
            footer="#7f6b91",
            body_font='"Segoe UI", "Helvetica Neue", Arial, sans-serif',
            heading_font='"Trebuchet MS", "Segoe UI", sans-serif',
        ),
    ),
    "midnight_ops": Theme(
        slug="midnight_ops",
        label="Midnight ops",
        css_file="themes/pro_landscape.css",
        page_size="tablet_landscape_16_10",
        preview_class="preview-midnight",
        tokens=theme_tokens(
            ink="#dce6e8",
            muted="#9aadb3",
            paper="#101719",
            page="#151d20",
            line="#38474d",
            line_soft="#243238",
            accent="#77d9d4",
            accent_2="#f0b35e",
            header_bg="#223137",
            header_text="#edf7f6",
            footer="#8fa3a8",
            body_font='"Segoe UI", "Helvetica Neue", Arial, sans-serif',
            heading_font='"Segoe UI Semibold", "Segoe UI", sans-serif',
        ),
    ),
}


PRODUCTS = {
    PROJECT_MANAGEMENT_99.slug: PROJECT_MANAGEMENT_99,
}


SYMBOLS = (
    {"symbol": "•", "label": "Action", "rule": "Quelque chose que je peux executer."},
    {"symbol": "-", "label": "Note", "rule": "Information utile, contexte, detail."},
    {"symbol": "?", "label": "Question", "rule": "Point a clarifier."},
    {"symbol": "!", "label": "Important", "rule": "Risque ou point a ne pas oublier."},
    {"symbol": "W", "label": "Attente", "rule": "Reponse ou entree attendue."},
    {"symbol": "B", "label": "Blocage", "rule": "Sujet immobilise ou fortement ralenti."},
    {"symbol": "D", "label": "Decision", "rule": "Decision actee a conserver."},
)


def build_context(request: RenderRequest) -> dict:
    product = get_product(request.product)
    theme = get_theme(request.theme)
    options = resolve_options(product.options, request.options)

    if product.slug == PROJECT_MANAGEMENT_99.slug:
        options = normalize_legacy_options(options)
        options["cover_color"] = normalize_hex_color(str(options.get("cover_color", "#176f75")))
        project_count = int(options["project_count"])
        page_format = resolve_page_format(
            str(options["page_format"]),
            str(options["orientation"]),
        )
        metadata = dict(request.metadata)
        metadata["format"] = page_format["metadata_label"]
        layout = compute_layout(page_format["width_px"], page_format["height_px"])
        projects = [ProjectSlot(number=index) for index in range(1, project_count + 1)]
        return {
            "product": asdict(product),
            "theme": asdict(theme),
            "title": request.title,
            "options": options,
            "metadata": metadata,
            "page_format": page_format,
            "layout": layout,
            "theme_tokens": theme.tokens,
            "cover_text_color": contrast_text_color(str(options["cover_color"])),
            "row_counts": layout["row_counts"],
            "nav": default_nav(),
            "symbols": SYMBOLS,
            "journal_pages": range(1, int(options["journal_pages"]) + 1),
            "radar_pages": range(1, int(options["radar_pages"]) + 1),
            "extra_project_pages": range(3, int(options["pages_per_project"]) + 1),
            "project_page_numbers": range(1, int(options["pages_per_project"]) + 1),
            "index_groups": chunk(projects, 25),
            "projects": projects,
        }

    raise ValueError(f"Unsupported product: {product.slug}")


def get_product(slug: str) -> ProductSpec:
    try:
        return PRODUCTS[slug]
    except KeyError as exc:
        raise ValueError(f"Unknown product: {slug}") from exc


def get_theme(slug: str) -> Theme:
    try:
        return THEMES[slug]
    except KeyError as exc:
        raise ValueError(f"Unknown theme: {slug}") from exc


def resolve_options(schema: Iterable[ProductOption], values: dict) -> dict:
    resolved = {}
    for option in schema:
        value = values.get(option.key, option.default)
        if option.option_type == "number":
            value = int(value)
            if option.min_value is not None and value < option.min_value:
                raise ValueError(f"{option.key} must be >= {option.min_value}")
            if option.max_value is not None and value > option.max_value:
                raise ValueError(f"{option.key} must be <= {option.max_value}")
        elif option.option_type == "boolean":
            value = bool(value)
        elif option.option_type == "select":
            if value not in option.choices:
                raise ValueError(f"{option.key} must be one of {option.choices}")
        elif option.choices and value not in option.choices:
            raise ValueError(f"{option.key} must be one of {option.choices}")
        resolved[option.key] = value
    return resolved


def normalize_legacy_options(options: dict) -> dict:
    normalized = dict(options)
    legacy_format = normalized.get("page_format")
    if legacy_format == "a4_portrait":
        normalized["page_format"] = "a4"
        normalized["orientation"] = "portrait"
    elif legacy_format == "a5_portrait":
        normalized["page_format"] = "a5"
        normalized["orientation"] = "portrait"
    normalized.setdefault("orientation", "landscape")
    normalized.setdefault("cover_style", "solid")
    normalized.setdefault("cover_color", "#176f75")
    return normalized


def normalize_hex_color(value: str) -> str:
    cleaned = value.strip()
    if len(cleaned) == 7 and cleaned.startswith("#"):
        digits = cleaned[1:]
        if all(char in "0123456789abcdefABCDEF" for char in digits):
            return f"#{digits.lower()}"
    return "#176f75"


def contrast_text_color(hex_color: str) -> str:
    digits = hex_color.lstrip("#")
    red = int(digits[0:2], 16)
    green = int(digits[2:4], 16)
    blue = int(digits[4:6], 16)
    luminance = (red * 0.299 + green * 0.587 + blue * 0.114) / 255
    return "#162024" if luminance > 0.62 else "#fffaf0"


def resolve_page_format(slug: str, orientation: str) -> dict:
    preset = FORMAT_PRESETS[slug]
    width = int(preset["width_px"])
    height = int(preset["height_px"])
    if orientation == "portrait" and width > height:
        width, height = height, width
    elif orientation == "landscape" and height > width:
        width, height = height, width
    orientation_label = ORIENTATION_LABELS[orientation]
    return {
        "slug": slug,
        "orientation": orientation,
        "label": preset["label"],
        "metadata_label": f"{preset['label']} {orientation_label} - {width} x {height} px",
        "width_px": width,
        "height_px": height,
    }


def compute_layout(page_width: int, page_height: int) -> dict:
    short_side = min(page_width, page_height)
    long_side = max(page_width, page_height)
    scale = short_side / 800

    pad_x = round(max(36, min(78, short_side * 0.045)))
    pad_top = round(max(34, min(72, page_height * 0.04)))
    pad_bottom = round(max(34, min(72, page_height * 0.04)))
    topbar_h = round(max(28, min(44, page_height * 0.022)))
    title_h = round(max(58, min(104, page_height * 0.052)))
    footer_h = round(max(22, min(36, page_height * 0.018)))
    gap = round(max(16, min(34, page_height * 0.018)))
    table_h = page_height - pad_top - pad_bottom - topbar_h - title_h - footer_h - (gap * 2)

    row_h = round(max(52, min(112, page_height * 0.052)))
    project_row_h = round(max(34, min(70, page_height * 0.032)))
    header_h = round(max(30, min(52, row_h * 0.48)))
    project_header_h = round(max(26, min(42, project_row_h * 0.58)))
    table_h = max(row_h * 8, table_h)
    index_row_h = max(18, (table_h - header_h) // 25)

    def rows(extra_reserved: int = 0, minimum: int = 8, maximum: int = 28) -> int:
        available = max(row_h * minimum, table_h - extra_reserved - header_h)
        return max(minimum, min(maximum, available // row_h))

    project_summary_reserved = (
        project_row_h
        + round(max(120, min(230, page_height * 0.105)))
        + h3_height(short_side)
        + (gap * 4)
    )

    return {
        "pad_x": pad_x,
        "pad_top": pad_top,
        "pad_bottom": pad_bottom,
        "topbar_h": topbar_h,
        "title_h": title_h,
        "footer_h": footer_h,
        "gap": gap,
        "table_h": table_h,
        "row_h": row_h,
        "project_row_h": project_row_h,
        "index_row_h": index_row_h,
        "header_h": header_h,
        "project_header_h": project_header_h,
        "font_base": round(max(13, min(22, 14 * scale))),
        "font_small": round(max(10, min(16, 11 * scale))),
        "h1": round(max(42, min(82, short_side * 0.05))),
        "h2": round(max(28, min(54, short_side * 0.036))),
        "h3": round(max(17, min(28, short_side * 0.018))),
        "lead": round(max(16, min(28, short_side * 0.018))),
        "home_card_h": round(max(120, min(260, long_side * 0.12))),
        "summary_note_h": round(max(120, min(230, page_height * 0.105))),
        "note_line": round(max(34, min(64, row_h * 0.58))),
        "row_counts": {
            "journal": rows(),
            "radar": rows(minimum=8, maximum=28),
            "priorities": rows(minimum=8, maximum=28),
            "actions": max(12, min(44, (table_h - project_header_h) // project_row_h)),
            "open_points": max(
                8,
                min(
                    28,
                    (table_h - project_summary_reserved - project_header_h)
                    // project_row_h,
                ),
            ),
            "index": 25,
        },
    }


def h3_height(short_side: int) -> int:
    return round(max(17, min(28, short_side * 0.018)))


def default_nav() -> tuple[NavLink, ...]:
    return (
        NavLink("Accueil", "home"),
        NavLink("Methode", "method"),
        NavLink("Journal", "journal-1"),
        NavLink("Rappel", "radar-1"),
        NavLink("Priorites", "priorities"),
        NavLink("Index", "index-1"),
    )


def chunk(items: list[ProjectSlot], size: int) -> list[list[ProjectSlot]]:
    return [items[index : index + size] for index in range(0, len(items), size)]
