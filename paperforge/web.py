from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .models import RenderRequest
from .products import (
    COVER_STYLES,
    FORMAT_PRESETS,
    ORIENTATION_LABELS,
    PRODUCTS,
    THEMES,
    get_product,
    get_theme,
    resolve_options,
)
from .render import ROOT, write_output


WEB_ROOT = ROOT / "templates" / "web"
DIST_ROOT = ROOT / "dist"


def serve(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = ThreadingHTTPServer((host, port), PaperforgeHandler)
    print(f"Paperforge web app running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Paperforge web app")
    finally:
        server.server_close()


class PaperforgeHandler(BaseHTTPRequestHandler):
    env = Environment(
        loader=FileSystemLoader(str(WEB_ROOT)),
        autoescape=select_autoescape(("html", "xml", "j2")),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.render_app()
            return
        if parsed.path.startswith("/static/"):
            self.serve_static(parsed.path)
            return
        if parsed.path.startswith("/dist/"):
            self.serve_dist(parsed.path)
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/generate":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(length).decode("utf-8")
        form = {key: values[-1] for key, values in parse_qs(payload).items()}
        result = handle_generation(form)
        self.render_app(result=result, values=form)

    def render_app(self, result: dict | None = None, values: dict | None = None) -> None:
        template = self.env.get_template("app.html.j2")
        html = template.render(
            products=[product_view(product) for product in PRODUCTS.values()],
            themes=[asdict(theme) for theme in THEMES.values()],
            default_product=next(iter(PRODUCTS.values())).slug,
            default_theme=next(iter(THEMES.values())).slug,
            choice_labels={
                "page_format": {
                    slug: f"{preset['label']} ({preset['width_px']} x {preset['height_px']} px)"
                    for slug, preset in FORMAT_PRESETS.items()
                },
                "orientation": ORIENTATION_LABELS,
                "cover_style": COVER_STYLES,
            },
            cover_styles=COVER_STYLES,
            values=values or {},
            result=result,
        )
        self.send_text(html, "text/html; charset=utf-8")

    def serve_static(self, request_path: str) -> None:
        relative = request_path.removeprefix("/static/").replace("/", "\\")
        path = (WEB_ROOT / "static" / relative).resolve()
        if not path.is_file() or WEB_ROOT.resolve() not in path.parents:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content_type = "text/css; charset=utf-8" if path.suffix == ".css" else "text/plain"
        self.send_bytes(path.read_bytes(), content_type)

    def serve_dist(self, request_path: str) -> None:
        relative = request_path.removeprefix("/dist/").replace("/", "\\")
        path = (DIST_ROOT / relative).resolve()
        if not path.is_file() or DIST_ROOT.resolve() not in path.parents:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        if path.suffix == ".html":
            content_type = "text/html; charset=utf-8"
        elif path.suffix == ".pdf":
            content_type = "application/pdf"
        else:
            content_type = "application/octet-stream"
        self.send_bytes(path.read_bytes(), content_type)

    def send_text(self, body: str, content_type: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_bytes(body.encode("utf-8"), content_type, status)

    def send_bytes(
        self, body: bytes, content_type: str, status: HTTPStatus = HTTPStatus.OK
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return


def handle_generation(form: dict[str, str]) -> dict:
    action = form.get("action", "command")
    request = request_from_form(form)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = f"generated_{request.product}_{request.theme}_{timestamp}"
    config_output = ROOT / "configs" / f"{stem}.json"
    html_output = DIST_ROOT / f"{stem}.html"
    pdf_output = DIST_ROOT / f"{stem}.pdf"
    command_output = pdf_output if action == "pdf" else html_output
    write_generated_config(request, config_output)
    command = build_command(config_output, command_output, html_only=action != "pdf")

    result = {
        "status": "ready",
        "message": "Commande preparee.",
        "command": command,
        "html_url": None,
        "pdf_url": None,
    }

    if action == "command":
        return result

    try:
        if action == "html":
            write_output(request, html_output, html_only=True)
            result.update(
                status="success",
                message="HTML genere.",
                html_url=f"/dist/{html_output.name}",
            )
        elif action == "pdf":
            write_output(request, pdf_output, html_only=False)
            result.update(
                status="success",
                message="PDF genere.",
                pdf_url=f"/dist/{pdf_output.name}",
            )
        else:
            raise ValueError(f"Action inconnue: {action}")
    except Exception as exc:
        result.update(status="error", message=str(exc))

    return result


def request_from_form(form: dict[str, str]) -> RenderRequest:
    product_slug = form.get("product", next(iter(PRODUCTS)))
    theme_slug = form.get("theme", next(iter(THEMES)))
    product = get_product(product_slug)
    get_theme(theme_slug)
    option_values = {
        option.key: form.get(option.key, option.default) for option in product.options
    }
    options = resolve_options(product.options, option_values)
    title = form.get("title") or "Carnet de pilotage projets"
    return RenderRequest(
        product=product_slug,
        theme=theme_slug,
        title=title,
        options=options,
        metadata={
            "subtitle": form.get("subtitle")
            or "Capture rapide, radar de relance, index hyperlie et 99 projets en deux pages.",
        },
    )


def write_generated_config(request: RenderRequest, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "product": request.product,
        "theme": request.theme,
        "title": request.title,
        "options": request.options,
        "metadata": request.metadata,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_command(config_path: Path, output: Path, html_only: bool) -> str:
    config_arg = config_path.relative_to(ROOT)
    output_arg = output.relative_to(ROOT)
    flag = " --html-only" if html_only else ""
    command = (
        ".\\.venv\\Scripts\\python.exe -m paperforge.cli render "
        f"--config {config_arg} --output {output_arg}{flag}"
    )
    return command.replace("/", "\\")


def product_view(product) -> dict:
    data = asdict(product)
    data["options"] = [asdict(option) for option in product.options]
    return data
