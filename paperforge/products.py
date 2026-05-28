from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict

from .models import NavLink, ProductOption, ProductSpec, ProjectSlot, RenderRequest, Theme


PROJECT_MANAGEMENT_99 = ProductSpec(
    slug="project_management_99",
    label="Gestion de projets - 99 projets",
    template_file="products/project_management_99.html.j2",
    options=(
        ProductOption(
            key="project_count",
            label="Nombre de projets",
            option_type="number",
            default=99,
            min_value=1,
            max_value=99,
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
        project_count = int(options["project_count"])
        projects = [ProjectSlot(number=index) for index in range(1, project_count + 1)]
        return {
            "product": asdict(product),
            "theme": asdict(theme),
            "title": request.title,
            "options": options,
            "metadata": request.metadata,
            "nav": default_nav(),
            "symbols": SYMBOLS,
            "journal_pages": range(1, int(options["journal_pages"]) + 1),
            "radar_pages": range(1, int(options["radar_pages"]) + 1),
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
        elif option.choices and value not in option.choices:
            raise ValueError(f"{option.key} must be one of {option.choices}")
        resolved[option.key] = value
    return resolved


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
