from paperforge.models import RenderRequest
from paperforge.products import build_context, resolve_options, PROJECT_MANAGEMENT_99


def test_project_management_context_matches_expected_page_blocks():
    request = RenderRequest(
        product="project_management_99",
        theme="pro_landscape",
        title="Carnet",
        options={"project_count": 99, "journal_pages": 2, "radar_pages": 2},
    )

    context = build_context(request)

    assert len(context["projects"]) == 99
    assert len(context["index_groups"]) == 4
    assert context["index_groups"][0][0].code == "01"
    assert context["index_groups"][-1][-1].code == "99"
    assert (
        context["layout"]["header_h"]
        + (context["layout"]["index_row_h"] * context["row_counts"]["index"])
        <= context["layout"]["table_h"]
    )


def test_number_options_are_bounded():
    try:
        resolve_options(PROJECT_MANAGEMENT_99.options, {"project_count": 100})
    except ValueError as exc:
        assert "project_count" in str(exc)
    else:
        raise AssertionError("Expected project_count validation to fail")
