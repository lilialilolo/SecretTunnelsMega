import asyncio
from farmlogic import farm

# async def pass_turn_dead(self) -> None:
#   """
#   Clicks `pass` while in a battle
#   """
#   await self.mouse.click(300, 300, duration=0.2, delay=0.5)
#   await self.wait(0.5)

async def fight(name, p1, p2, p3, p4):

  hitter_pos = 7 # 6 for 3, 7 for 4
  
  battle = p2.get_battle(name)
  if (name == "mobs"):
    while await battle.loop():
      m_feint = await p1.find_spell('mass-feint')
      if m_feint:
        await m_feint.cast()
      else:
        await p1.pass_turn()

      r_ele = await p2.find_spell('elemental-blade')
      r_sharpen = await p2.find_spell('sharpened-blade')
      if r_ele and r_sharpen:
        e_r_blade = await r_sharpen.enchant(r_ele)
        await e_r_blade.cast(target=hitter_pos)
      else:
        await p2.pass_turn()
      
      ele_blade = await p3.find_spell('elemental-blade')
      if ele_blade:
        await ele_blade.cast(target=hitter_pos)
      else:
        await p3.pass_turn()

      tempest = await p4.find_spell('tempest')
      epic = await p4.find_spell('epic')

      if tempest and epic:
        e_hit = await epic.enchant(tempest)
        await e_hit.cast()
      else:
        await p4.pass_turn()



asyncio.run(farm(fight))