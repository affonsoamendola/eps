local SIMULATOR = {}

function fight(scenario_input, attacker, defender)
	attacker_wpn = scenario_input.weapons[attacker.weapon]

	defender_wpn = scenario_input.weapons[defender.weapon]
	defender_atk_speed = defender.spd - math.max(0, defender_wpn.wt - defender.str)

	accuracy = attacker_wpn.hit + attacker.skl * 2 + attacker.lck + triangle_bonus[attacker_wpn.kind][defender_wpn.kind] * 10
	avoid = (defender.spd*2) + defender.lck

	hit_chance = math.max(0, math.min(100, accuracy - avoid))

	if(random_value() < hit_chance) then
		print("HIT")

		crit_rate = attacker_wpn.crt + (attacker.skl / 2)
		dodge = defender.lck

		crit_chance = math.max(0, math.min(100, crit_rate - dodge))

		crit_bonus = 1

		print("Crit chance ", crit_chance)
		if(math.random(100) < crit_chance) then
			print("CRIT")
			crit_bonus = 3
		end

		eff = 1

		if((attacker_wpn.eff ~= nil) and attacker_wpn.eff == defender.trait) then
			print("EFF BONUS")
			eff = 2
		end

		if(attacker_wpn.kind == 'sword' or attacker_wpn.kind == 'axe' or attacker_wpn.kind == 'lance' or attacker_wpn.kind == 'bow') then
			print("Physical weapon")
			relevant_skill_atk = attacker.str
			relevant_skill_def = defender.def
		else
			print("Magical Attack")
			relevant_skill_atk = attacker.mag
			relevant_skill_def = defender.res
		end
	
		power = relevant_skill_atk + ((attacker_wpn.mt + triangle_bonus[attacker_wpn.kind][defender_wpn.kind]) * eff)
		dmg = (power - relevant_skill_def) * crit_bonus

		defender.hp = math.max(0, defender.hp - dmg)			
	else print("MISS") end
end

function SIMULATOR.run(scenario_input)
	math.randomseed(scenario_input.seed)	
	for i, fight_n in pairs(scenario_input.fights) do
		local left = scenario_input.units[fight_n[1]]
		local right = scenario_input.units[fight_n[2]]

		left_atk_speed = left.spd - math.max(0, scenario_input.weapons[left.weapon].wt - left.str)
		right_atk_speed = right.spd - math.max(0, scenario_input.weapons[right.weapon].wt - right.str)

		print("Fight ", i)
		print("Attack")
		fight(scenario_input, left, right)
		if(right.hp > 0) then
			print("Counter attack")
			fight(scenario_input, right, left)

			if(left_atk_speed - right_atk_speed >= 4 and right.hp) then
				print("Double Attack Left")
				fight(scenario_input, left, right)
			end
			if(right_atk_speed - left_atk_speed >= 4 and left.hp) then
				print("Double Attack Right")
				fight(scenario_input, right, left)
			end
		end
	end
	return scenario_input.units
end

function random_value()
	a = math.random(100)
	b = math.random(100)
	return (a + b)/2
end

triangle_bonus = {	['sword'] =   { ['sword'] = 0, ['axe'] = 1, ['lance'] =-1, ['bow'] = 0, ['wind'] = 0, ['thunder'] = 0, ['fire'] = 0,},
					['axe']   =   { ['sword'] =-1, ['axe'] = 0, ['lance'] = 1, ['bow'] = 0, ['wind'] = 0, ['thunder'] = 0, ['fire'] = 0,},
					['lance'] =   { ['sword'] = 1, ['axe'] =-1, ['lance'] = 0, ['bow'] = 0, ['wind'] = 0, ['thunder'] = 0, ['fire'] = 0,},
					['bow'] =     { ['sword'] = 0, ['axe'] = 0, ['lance'] = 0, ['bow'] = 0, ['wind'] = 0, ['thunder'] = 0, ['fire'] = 0,},
					['wind']   =  { ['sword'] = 0, ['axe'] = 0, ['lance'] = 0, ['bow'] = 0, ['wind'] = 0, ['thunder'] = 1, ['fire'] =-1,},
					['thunder'] = { ['sword'] = 0, ['axe'] = 0, ['lance'] = 0, ['bow'] = 0, ['wind'] =-1, ['thunder'] = 0, ['fire'] = 1,},
					['fire']   =  { ['sword'] = 0, ['axe'] = 0, ['lance'] = 0, ['bow'] = 0, ['wind'] = 1, ['thunder'] =-1, ['fire'] = 0,}
}

return SIMULATOR
