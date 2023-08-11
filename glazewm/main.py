import asyncio as aio

from .async_ import GlazeWM as Async
from .sync import GlazeWM as Sync


async def main():
    client = Async("ws://192.168.144.1:6123", raise_exception=True)

    # res = await client.send_raw("subscribe window_focus")
    # print(res)

    # res = await client.get_monitors()
    # print(res)

    # res = await client.get_workspaces()
    # print(res)

    # while True:
    #     s = input("Input: ")
    #     res = await client.send_raw(s)
    #     print(res)

    # res = await client.binding_mode("base")
    # print(res)

    # res = await client.execute("echo test")
    # print(res)

    # res = await client.set_window_state("floating")
    # res = await client.set_window_state("minimized")
    # res = await client.set_window_state("maximized")
    # res = await client.set_window_state("tiling")

    # res = await client.toggle_maximized()
    # res = await client.toggle_floating()

    # res = await client.focus("left")
    # res = await client.focus("right")
    # res = await client.focus("up")
    # res = await client.focus("down")

    # res = await client.focus_workspace(1)
    # res = await client.move_to_workspace(1)

    # res = await client.tiling_direction("vertical")
    # res = await client.tiling_direction("horizontal")

    res = await client.reload_config()


# client = Sync("ws://192.168.144.1:6123", raise_exception=True)
# res = client.binding_mode("base")
# print(res)


if __name__ == "__main__":
    aio.run(main())
