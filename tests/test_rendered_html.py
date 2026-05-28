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
    assert 'font-family: "Inter"' in html
