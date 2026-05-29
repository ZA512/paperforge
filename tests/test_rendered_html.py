from html.parser import HTMLParser

from paperforge.models import RenderRequest
from paperforge.render import render_html


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.sections = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "section":
            self.sections += 1
        if "id" in attrs_dict:
            self.ids.append(attrs_dict["id"])


def test_project_management_html_has_expected_pages_and_anchors():
    html = render_html(
        RenderRequest(
            product="project_management_99",
            theme="pro_landscape",
            title="Carnet",
            options={"project_count": 99, "journal_pages": 2, "radar_pages": 2},
        )
    )
    parser = IdCollector()
    parser.feed(html)

    assert parser.sections == 209
    assert "home" in parser.ids
    assert "index-4" in parser.ids
    assert "project-01-summary" in parser.ids
    assert "project-99-actions" in parser.ids
    assert "&#34" not in html
    assert 'font-family: "Segoe UI"' in html
    assert "clamp(" not in html
    assert "var(--" not in html


def test_page_format_changes_pdf_css_size():
    html = render_html(
        RenderRequest(
            product="project_management_99",
            theme="pro_landscape",
            title="Carnet",
            options={
                "page_format": "a4",
                "orientation": "portrait",
                "project_count": 1,
                "pages_per_project": 2,
                "journal_pages": 1,
                "radar_pages": 1,
            },
        )
    )

    assert "size: 595px 842px;" in html
    assert "height: 842px;" in html
    assert "width: 595px;" in html
    assert 'class="format-a4 orientation-portrait"' in html


def test_pages_per_project_controls_project_page_count():
    html = render_html(
        RenderRequest(
            product="project_management_99",
            theme="pro_landscape",
            title="Carnet",
            options={
                "project_count": 3,
                "pages_per_project": 3,
                "journal_pages": 1,
                "radar_pages": 1,
            },
        )
    )
    parser = IdCollector()
    parser.feed(html)

    assert parser.sections == 15
    assert "project-01-summary" in parser.ids
    assert "project-01-actions" in parser.ids
    assert "project-01-extra-3" in parser.ids


def test_tcl_tablet_format_uses_exact_pixels():
    html = render_html(
        RenderRequest(
            product="project_management_99",
            theme="pro_landscape",
            title="Carnet",
            options={
                "page_format": "tablet_tcl_nxtpaper_11_plus",
                "orientation": "landscape",
                "project_count": 1,
                "pages_per_project": 1,
                "journal_pages": 1,
                "radar_pages": 1,
            },
        )
    )

    assert "size: 2200px 1440px;" in html
    assert "TCL NXTPAPER 11+ paysage - 2200 x 1440 px" in html
