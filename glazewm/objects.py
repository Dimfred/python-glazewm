from typing import Any, Literal, Union

from pydantic import BaseModel, model_validator


class GlazeWMError(Exception):
    pass


Direction = Literal["left", "down", "up", "right"]
WorkspaceType = Union[int, Literal["recent"]]
WindowState = Literal["maximized", "minimized", "floating", "tiling"]
TilingDirection = Literal["horizontal", "vertical", "toggle"]
Dimension = Literal["width", "height"]


class Response(BaseModel):
    success: bool
    data: str | list | None
    error: str | None
    message_type: str
    client_message: str


################################################################################
# WINDOW
class FloatingPlacement(BaseModel):
    left: int
    top: int
    right: int
    bottom: int
    x: int
    y: int
    width: int
    height: int


class BorderDelta(BaseModel):
    left: int
    top: int
    right: int
    bottom: int


class Window(BaseModel):
    id: str  # noqa: A003
    type: str  # noqa: A003
    handle: int
    x: int
    y: int
    width: int
    height: int
    focus_index: int
    floating_placement: FloatingPlacement
    border_delta: BorderDelta
    children: list

    @model_validator(mode="before")
    @classmethod
    def to_snake_case(cls, data: dict[str, Any]) -> dict[str, Any]:
        data["floating_placement"] = data["floatingPlacement"]
        data["border_delta"] = data["borderDelta"]
        data["focus_index"] = data["focusIndex"]

        return data


################################################################################
# WORKSPACE
class Workspace(BaseModel):
    id: str  # noqa: A003
    type: str  # noqa: A003
    name: str
    layout: str
    x: int
    y: int
    width: int
    height: int
    focus_index: int
    size_percentage: int
    children: list[Window]

    @model_validator(mode="before")
    @classmethod
    def to_snake_case(cls, data: dict[str, Any]) -> dict[str, Any]:
        data["focus_index"] = data["focusIndex"]
        data["size_percentage"] = data["sizePercentage"]
        return data


################################################################################
# MONITOR
class Monitor(BaseModel):
    id: str  # noqa: A003
    type: str  # noqa: A003
    device_name: str
    x: int
    y: int
    width: int
    height: int
    focus_index: int
    children: list[Workspace]

    @model_validator(mode="before")
    @classmethod
    def to_snake_case(cls, data: dict[str, Any]) -> dict[str, Any]:
        data["device_name"] = data["deviceName"]
        data["focus_index"] = data["focusIndex"]
        return data
