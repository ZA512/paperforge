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
            label="Pages radar",
            option_type="number",
            default=2,
            min_value=1,
            max_value=4,
        ),
    ),
)


THEMES = {
    "pro_landscape": Theme(
        slug="pro_landscape",
        label="Pro paysage 16:10",
        css_file="themes/pro_landscape.css",
        page_size="tablet_landscape_16_10",
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
        project_count = int(options["project_count"])
        page_format = resolve_page_format(
            str(options["page_format"]),
            str(options["orientation"]),
        )
        metadata = dict(request.metadata)
        metadata["format"] = page_format["metadata_label"]
        row_counts = compute_row_counts(page_format["height_px"])
        projects = [ProjectSlot(number=index) for index in range(1, project_count + 1)]
        return {
            "product": asdict(product),
            "theme": asdict(theme),
            "title": request.title,
            "options": options,
            "metadata": metadata,
            "page_format": page_format,
            "row_counts": row_counts,
            "nav": default_nav(),
            "symbols": SYMBOLS,
            "journal_pages": range(1, int(options["journal_pages"]) + 1),
            "radar_pages": range(1, int(options["radar_pages"]) + 1),
            "extra_project_pages": range(3, int(options["pages_per_project"]) + 1),
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
    return normalized


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


def compute_row_counts(page_height: int) -> dict[str, int]:
    return {
        "journal": max(12, min(28, (page_height - 260) // 38)),
        "radar": max(12, min(30, (page_height - 220) // 36)),
        "priorities": max(12, min(30, (page_height - 220) // 36)),
        "actions": max(14, min(32, (page_height - 220) // 36)),
        "open_points": max(5, min(14, (page_height - 520) // 42)),
    }


def default_nav() -> tuple[NavLink, ...]:
    return (
        NavLink("Accueil", "home"),
        NavLink("Methode", "method"),
        NavLink("Journal", "journal-1"),
        NavLink("Radar", "radar-1"),
        NavLink("Priorites", "priorities"),
        NavLink("Index", "index-1"),
    )


def chunk(items: list[ProjectSlot], size: int) -> list[list[ProjectSlot]]:
    return [items[index : index + size] for index in range(0, len(items), size)]
