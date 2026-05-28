from __future__ import annotations

import json
import subprocess
import tempfile
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

    executable = ROOT / "weasyprint.exe"
    if executable.is_file():
        write_pdf_with_executable(executable, html, output)
        return

    try:
        from weasyprint import HTML
    except (ImportError, OSError) as exc:
        raise RuntimeError(
            "WeasyPrint cannot start. Use --html-only, install Python dependencies, "
            "make sure native WeasyPrint libraries are available on this system, "
            "or put weasyprint.exe at the project root."
        ) from exc

    HTML(string=html, base_url=str(TEMPLATE_ROOT)).write_pdf(str(output))


def write_pdf_with_executable(executable: Path, html: str, output: Path) -> None:
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".html",
        encoding="utf-8",
        delete=False,
        dir=ROOT / "dist",
    ) as handle:
        handle.write(html)
        html_path = Path(handle.name)

    try:
        result = subprocess.run(
            [str(executable), str(html_path), str(output)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        html_path.unlink(missing_ok=True)

    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"weasyprint.exe failed with exit code {result.returncode}: {details}")
