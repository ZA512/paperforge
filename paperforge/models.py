from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


PageSize = Literal["tablet_landscape_16_10", "a4_portrait", "a5_portrait"]


@dataclass(frozen=True)
class Theme:
    slug: str
    label: str
    css_file: str
    page_size: PageSize = "tablet_landscape_16_10"


@dataclass(frozen=True)
class ProductOption:
    key: str
    label: str
    option_type: Literal["text", "number", "select", "boolean"]
    default: Any
    min_value: int | None = None
    max_value: int | None = None
    choices: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProjectSlot:
    number: int
    title: str = ""
    domain: str = ""
    state: str = ""

    @property
    def code(self) -> str:
        return f"{self.number:02d}"


@dataclass(frozen=True)
class ProductSpec:
    slug: str
    label: str
    template_file: str
    options: tuple[ProductOption, ...]


@dataclass
class RenderRequest:
    product: str
    theme: str
    title: str
    options: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NavLink:
    label: str
    target: str
