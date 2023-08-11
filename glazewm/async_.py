import json
from typing import Any

import websockets

from .objects import (
    Dimension,
    Direction,
    GlazeWMError,
    Monitor,
    Response,
    TilingDirection,
    Window,
    WindowState,
    Workspace,
    WorkspaceType,
)


class GlazeWM:
    def __init__(self, url: str, *, raise_exception: bool = False):
        self._url = url
        self._raise_exception = raise_exception

    ################################################################################
    # STATE
    async def get_monitors(self) -> list[Monitor] | None:
        """Get information about monitors in GlazeWM."""
        res = await self.send_raw("monitors")
        assert res.data is not None and isinstance(res.data, list)

        return [Monitor(**monitor) for monitor in res.data]

    async def get_workspaces(self) -> list[Workspace] | None:
        """Get information about workspaces in GlazeWM."""
        res = await self.send_raw("workspaces")
        assert res.data is not None and isinstance(res.data, list)

        return [Workspace(**workspace) for workspace in res.data]

    async def get_windows(self) -> list[Window] | None:
        """Get information about windows in GlazeWM."""
        res = await self.send_raw("windows")
        assert res.data is not None and isinstance(res.data, list)

        return [Window(**window) for window in res.data]

    ################################################################################
    # COMMANDS
    async def binding_mode(self, mode: str) -> Response:
        """Set the binding mode."""
        return await self.command(f"binding mode {mode}")

    async def execute(self, cmd: str) -> Response:
        """Execute a command."""
        return await self.command(f"exec {cmd}")

    async def set_window_state(self, state: WindowState) -> Response:
        """Set the window state."""
        return await self.command(f"set {state}")

    async def set_window_size(self, dimension: Dimension, size: str) -> Response:
        """Set the window size."""
        assert "%" in size or "px" in size

        return await self.command(f"set {dimension} {size}")

    async def toggle_maximized(self) -> Response:
        """Toggle window maximized."""
        return await self.command("toggle maximized")

    async def toggle_floating(self) -> Response:
        """Toggle the floating window property."""
        return await self.command("toggle floating")

    async def focus(self, direction: Direction) -> Response:
        """Focus the next window in a direction."""
        return await self.command(f"focus {direction}")

    async def focus_workspace(self, workspace: WorkspaceType) -> Response:
        """Focus a workspace by name or 'recent'."""
        return await self.command(f"focus workspace {workspace}")

    async def move_to_workspace(self, workspace: WorkspaceType) -> Response:
        """Move focused window to a workspace by index."""
        return await self.command(f"move to workspace {workspace}")

    async def tiling_direction(self, direction: TilingDirection) -> Response:
        """Set or toggle the tiling direction."""
        return await self.command(f"tiling direction {direction}")

    async def reload_config(self) -> Response:
        """Reload the GlazeWM configuration."""
        return await self.command("reload config")

    async def exit_wm(self) -> Response:
        """Exit GlazeWM cleanly."""
        return await self.command("exit wm")

    async def focus_mode_toggle(self) -> Response:
        """Toggle between tiling the floating focus."""
        return await self.command("focus mode toggle")

    async def resize_borders(
        self, top: int = 0, left: int = 0, right: int = 0, bottom: int = 0
    ) -> Response:
        """Resize the border of a window."""
        return await self.command(
            f"resize borders {top}px {left}px {right}px {bottom}px"
        )

    async def ignore(self) -> Response:
        """Ignore a window, it won't be managed by GlazeWM anymore."""
        return await self.command("ignore")

    async def resize(self, dimension: Dimension, amount: str) -> Response:
        """Resizes the current window, given the dimension and the amount.

        resize <height | width> <amount in px | amount in %>
        (eg. resize height 3% or resize width 20px)
        """
        assert "%" in amount or "px" in amount
        return await self.command(f"resize {dimension} {amount}")

    ################################################################################
    # LOW LEVEL
    async def command(self, cmd: str) -> Response:
        """Send a command to GlazeWM, the input will be prefixed with 'command'."""
        return await self.send_raw(f'command "{cmd}"')

    async def send_raw(self, msg: str) -> Response:
        """Send a raw str to GlazeWM."""
        async with websockets.connect(self._url) as ws:  # type:ignore
            await ws.send(msg)

            res = json.loads(await ws.recv())
            if "success" not in res:
                e = f"Weird response received: {res}"
                raise GlazeWMError(e)

            if self._raise_exception and not res["success"]:
                raise GlazeWMError(res["error"])

            return Response(
                success=res["success"],
                message_type=res["messageType"],
                data=res["data"],
                error=res["error"],
                client_message=res["clientMessage"],
            )
