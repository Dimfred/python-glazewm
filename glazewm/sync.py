import asyncio as aio

from .async_ import (
    Dimension,
    Direction,
    Response,
    TilingDirection,
    WindowState,
    WorkspaceType,
)
from .async_ import GlazeWM as GlazeWMAsync


class GlazeWM:
    def __init__(self, url: str, *, raise_exception: bool = False):
        self._client = GlazeWMAsync(url, raise_exception=raise_exception)

    ################################################################################
    # COMMANDS
    def binding_mode(self, mode: str) -> Response:
        """Set the binding mode."""
        return aio.run(self._client.binding_mode(mode))

    def execute(self, cmd: str) -> Response:
        """Execute a command."""
        return aio.run(self._client.execute(cmd))

    def set_window_state(self, state: WindowState) -> Response:
        """Set the window state."""
        return aio.run(self._client.set_window_state(state))

    def set_window_size(self, dimension: Dimension, size: str) -> Response:
        """Set the window size."""
        return aio.run(self._client.set_window_size(dimension, size))

    def toggle_maximized(self) -> Response:
        """Toggle window maximized."""
        return aio.run(self._client.toggle_maximized())

    def toggle_floating(self) -> Response:
        """Toggle the floating window property."""
        return aio.run(self._client.toggle_floating())

    def focus(self, direction: Direction) -> Response:
        """Focus the next window in a direction."""
        return aio.run(self._client.focus(direction))

    def focus_workspace(self, workspace: WorkspaceType) -> Response:
        """Focus a workspace by name or 'recent'."""
        return aio.run(self._client.focus_workspace(workspace))

    def move_to_workspace(self, workspace: WorkspaceType) -> Response:
        """Move focused window to a workspace by index."""
        return aio.run(self._client.move_to_workspace(workspace))

    def tiling_direction(self, direction: TilingDirection) -> Response:
        """Set or toggle the tiling direction."""
        return aio.run(self._client.tiling_direction(direction))

    def reload_config(self) -> Response:
        """Reload the GlazeWM configuration."""
        return aio.run(self._client.reload_config())

    def exit_wm(self) -> Response:
        """Exit GlazeWM cleanly."""
        return aio.run(self._client.exit_wm())

    def focus_mode_toggle(self) -> Response:
        """Toggle between tiling the floating focus."""
        return aio.run(self._client.focus_mode_toggle())

    def resize_borders(
        self, top: int = 0, left: int = 0, right: int = 0, bottom: int = 0
    ) -> Response:
        """Resize the border of a window."""
        return aio.run(self._client.resize_borders(top, left, right, bottom))

    def ignore(self) -> Response:
        """Ignore a window, it won't be managed by GlazeWM anymore."""
        return aio.run(self._client.ignore())

    def resize(self, dimension: Dimension, amount: str) -> Response:
        """Resizes the current window, given the dimension and the amount.

        resize <height | width> <amount in px | amount in %>
        (eg. resize height 3% or resize width 20px)
        """
        return aio.run(self._client.resize(dimension, amount))

    ################################################################################
    # LOW LEVEL
    async def command(self, cmd: str) -> Response:
        """Send a command to GlazeWM, the input will be prefixed with 'command'."""
        return aio.run(self._client.command(cmd))

    async def send_raw(self, msg: str) -> Response:
        """Send a raw str to GlazeWM."""
        return aio.run(self._client.send_raw(msg))
