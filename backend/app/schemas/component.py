from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ComponentTemplate(BaseModel):
    id: int | str
    component_key: str
    name: str
    name_en: str | None = None


class ComponentMeta(BaseModel):
    id: int | str
    component_key: str
    name: str
    category_id: int | str = 0
    icon: str | None = None
    tpl_id: int | str | None = None
    templates: list[ComponentTemplate] = Field(default_factory=list)
    schema_data: dict[str, Any] = Field(default_factory=dict, alias="schema_json")
    default_data: dict[str, Any] = Field(default_factory=dict)
    enabled: int = 1
    sort: int = 0

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class DesignComponent(BaseModel):
    id: str
    component_key: str
    component_title: str
    template_id: int | str
    remote_data: dict[str, Any] = Field(default_factory=dict)
    tasks: list["DesignComponent"] = Field(default_factory=list)
    invalid: bool | None = None
    invalidReason: str | None = None
