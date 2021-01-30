from wizsdk import Client, XYZYaw, unregister_all
import asyncio
import os
import traceback


async def go_to_potions(player):

    # Go home
    await player.mouse.click(649, 584)
    await player.finish_loading()

    # Press X at the world door
    try:
        await asyncio.wait_for(player.press_x(), timeout=2)
    except asyncio.TimeoutError:
        await player.hold_key("s", 1.2)
        await player.press_x()

    # Wait for page to be opened
    while not player.pixel_matches_color((221, 547), ((132, 36, 66)), 20):
        await asyncio.sleep(1)

    # Choose Arcanum
    [await player.mouse.click(643, 492, duration=0.2) for i in range(3)]

    await asyncio.sleep(0.5)
    arcanum = player.locate_on_screen("icons/arcanum.png")

    if arcanum:
        await player.mouse.click(arcanum[0], arcanum[1] - 29, duration=0.2)
    else:
        raise Exception("COULDN'T FIND THE ARCANUM!!!")

    # Go to world
    await player.mouse.click(590, 546, duration=0.2)

    await player.finish_loading()

    # go to vendor
    await player.teleport_to(XYZYaw(x=-522.909, y=1574.476, z=-20.594, yaw=2.436))
    await player.hold_key("W", 0.6)


async def buy_potions(player):
    await player.press_x()

    while not player.pixel_matches_color((679, 527), (173, 1, 1), 20):
        await asyncio.sleep(1)
    # Fill all potions
    await player.mouse.click(547, 301, duration=0.2)
    # buy
    await player.mouse.click(269, 483, duration=0.2)
    # use
    await player.mouse.click(510, 468, duration=0.2)
    await player.click_confirm()
    # Fill all potions
    await player.mouse.click(547, 301, duration=0.2)
    # buy
    await player.mouse.click(269, 483, duration=0.2)

    # Close
    await player.mouse.click(687, 533, duration=0.2)


if __name__ == "__main__":

    async def main():
        player = Client.register()
        await player.activate_hooks()

        await go_to_potions(player)
        # await buy_potions(player)

    async def run():
        try:
            await main()
        except Exception:
            traceback.print_exc()
        finally:
            # IMPORTANT
            await unregister_all()

    asyncio.run(run())
