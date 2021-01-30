import os
import sys
import traceback
import atexit
import random
import asyncio
import wizsdk
from wizsdk import Client, register_clients, XYZYaw, unregister_all, finish_all_loading

# ====================================
# Potion buying
from get_potions import go_to_potions, buy_potions

# ====================================


__DIR__ = os.path.dirname(os.path.abspath(__file__))

"""
Handler controlling login/client

"""
FIGHT_1 = XYZYaw(x=1085.361, y=-2914.182, z=0.195, yaw=5.417)
FIGHT_2 = XYZYaw(x=5718.185, y=-4054.871, z=0.195, yaw=4.598)
EXIT = XYZYaw(x=174.189, y=1067.975, z=0.556, yaw=3.021)
ENTRANCE = XYZYaw(x=7972.952, y=1821.296, z=-15.707, yaw=1.632)

RUN_TIMEOUT = 6 * 60  # 6 minutes

# HELPER FUNCTIONS
async def teleport_party(players):
    loading_task = asyncio.create_task(finish_all_loading(*players))
    for p in players:
        await p.teleport_to_friend(__DIR__ + "icons/green_gem.png")

    await loading_task


async def join_fight(player, delay, run_duration=2):
    await asyncio.sleep(delay)
    await player.send_key("W", run_duration)


async def join_fight_in_order(players, delay_between=0.5, run_duration=1.5):
    await asyncio.gather(
        *[
            join_fight(player, i * delay_between, run_duration)
            for i, player in enumerate(players)
        ]
    )


async def go_through_dialogs(players):
    await asyncio.gather(*[player.go_through_dialog() for player in players])


async def mass_logout_login(players):
    await asyncio.gather(*[player.logout_and_in() for player in players])


async def mass_teleport_to(location, players):
    await asyncio.gather(*[player.teleport_to(location) for player in players])


async def check_all_potions(players):
    for p in players:
        await p.use_potion_if_needed()


async def backup_to_x(player):
    await player.send_key("S", 0.5)
    while not player.is_press_x():
        await player.send_key("S", 0.2)
        await player.wait(0.2)


async def farm(fight=None):
    try:
        clients = register_clients(-1, ["P1", "P2", "P3", "P4"])
        teammates = clients[1:]
        notHitters = clients[:3]

        p1, p2, p3, p4 = [*clients, None][:4]  # """, p3, p4"""
        await asyncio.gather(*[p.activate_hooks() for p in clients])

        async def run_once():
            # sigil
            [await p.press_x() for p in clients]

            # load?
            await finish_all_loading(*clients)
            await p1.send_key("W", 1)
            await go_through_dialogs(clients)
            await p1.wait(2)
            await mass_teleport_to(FIGHT_1, clients)
            await p1.wait(3)
            await join_fight_in_order(clients)
            await fight("mobs", *clients)
            await go_through_dialogs(clients)
            await mass_teleport_to(FIGHT_2, clients)
            await p1.wait(3)
            await go_through_dialogs(clients)
            await join_fight_in_order(clients)
            await fight("mobs", *clients)
            await go_through_dialogs(clients)
            await mass_teleport_to(EXIT, clients)

            # Start a loading task that finishes after confirming the exit prompts
            loading_task = asyncio.create_task(finish_all_loading(*clients))
            [await p.click_confirm() for p in clients]
            await loading_task

            # Back up to X
            await asyncio.gather(*[backup_to_x(p) for p in clients])

            # use potions for every player
            have_to_buy_potions = False
            for player in clients:
                await player.use_potion_if_needed(health=2000, mana=120)

                if await player.get_health() < 2000 or await player.get_mana() < 50:
                    have_to_buy_potions = True

            # Buy potions if needed
            if have_to_buy_potions:
                print("Going to buy potions")
                # Mark location
                await p1.mouse.click(675, 584)
                await go_to_potions(p1)
                # teleport to player that is there
                await teleport_party(teammates)
                # everyone buys potions
                [await buy_potions(p) for p in clients]

                # go to set location
                await p1.mouse.click(698, 567)
                await p1.finish_loading()
                # teleport to player that is there
                await teleport_party(teammates)

        async def reset_dungeon():
            # Code to reset if something went wrong
            [await p.logout_and_in(confirm=True) for p in clients]
            await mass_teleport_to(ENTRANCE, clients)

        while True:
            try:
                await asyncio.wait_for(run_once(), timeout=RUN_TIMEOUT)
            except asyncio.TimeoutError:
                await reset_dungeon()

    # Error handling
    except Exception:
        traceback.print_exc()
    finally:
        # ALWAYS UNREGISTER!
        await unregister_all()


if __name__ == "__main__":
    asyncio.run(farm())

