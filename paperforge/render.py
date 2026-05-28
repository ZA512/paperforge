from __future__ import annotations

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .models import RenderRequest
from .products import build_context, get_product, get_theme


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "templates"


def load_request(path: Path) -> RenderRequest:
    data = json.loads(path.read_text(encoding="utf-8"))
    return RenderRequest(
        product=data["product"],
        theme=data["theme"],
        title=data["title"],
        options=data.get("options", {}),
        metadata=data.get("metadata", {}),
    )


def render_html(request: RenderRequest) -> str:
    product = get_product(request.product)
    theme = get_theme(request.theme)
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_ROOT)),
        autoescape=select_autoescape(("html", "xml", "j2")),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(product.template_file)
    css = (TEMPLATE_ROOT / theme.css_file).read_text(encoding="utf-8")
    return template.render(**build_context(request), inline_css=css)


def write_output(request: RenderRequest, output: Path, html_only: bool = False) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    html = render_html(request)
    if html_only or output.suffix.lower() == ".html":
        output.write_text(html, encoding="utf-8")
        return

    try:
        from weasyprint import HTML
    except (ImportError, OSError) as exc:
        raise RuntimeError(
            "WeasyPrint cannot start. Use --html-only, install Python dependencies, "
            "and make sure native WeasyPrint libraries are available on this system."
        ) from exc

    HTML(string=html, base_url=str(TEMPLATE_ROOT)).write_pdf(str(output))
