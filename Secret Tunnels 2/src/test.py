import os
import sys
import traceback
import atexit

import asyncio
import wizsdk
from wizsdk import Client, register_clients, XYZYaw, unregister_all

__DIR__ = os.path.dirname(os.path.abspath(__file__))
FIGHT = XYZYaw(x=-4.377, y=780.019, z=0.0, yaw=0.0)
KROKARENA = XYZYaw(x=-1.654, y=6000.268, z=-1051.56, yaw=3.097)
AZTECAARENA = XYZYaw(x=0.235, y=-500.183, z=420.436, yaw=1.244)
PIGSWICKARENA = XYZYaw(x=17.526, y=-0.908, z=81.02, yaw=3.141)
AVALONARENA = XYZYaw(x=3318.952, y=15210.904, z=-632.432, yaw=3.095)
BAZAARDESK = XYZYaw(x=-80.343, y=817.222, z=-0.046, yaw=3.153)
CELESTIAARENA = XYZYaw(x=-3046.454, y=-153.12, z=-616.795, yaw=1.635)
ZAFARIAARENA = XYZYaw(x=-122.312, y=6000.97, z=-958.024, yaw=3.254)
GRIZZLEHEIMARENA = XYZYaw(x=337.594, y=500.911, z=-384.321, yaw=0.168)
ARENA = XYZYaw(x=53.042, y=1000.181, z=-17.618, yaw=0.086)

async def test():
  try:
    client = register_clients(-1,["Player1", "P2","P3","P4"])
    p1 = client[0]
    await asyncio.gather(*[p.activate_hooks() for p in client])

    await p1.press_x()
    await p1.wait(5)
    await p1.finish_loading()
    print("loaded")
    await p1.send_key("W",1)
    await p1.wait(2)
    await print(p1.find_enemy('./icons/loremaster.png'))

    # await p1.teleport_to(ZAFARIAARENA)
  except Exception:
    traceback.print_exc()
  finally:
    await unregister_all()

if __name__=="__main__":
  asyncio.run(test())