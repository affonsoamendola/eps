class = require "class"
vector2 = require "common/vec"

collision = require "collision"

input_scenario = require "scene/test"

camera_position = vector2(0, 0)
camera_origin = vector2(love.graphics.getWidth()/2,love.graphics.getHeight()/2)

bounds_radius = 1000

entity_list = {}
player = {}

function deepcopy(obj)
  	if type(obj) ~= 'table' then 
  		return obj 
	end
  	local res = setmetatable({}, getmetatable(obj))
  	for k, v in pairs(obj) do 
  		res[deepcopy(k)] = deepcopy(v) 
  	end
  	return res
end

function love.load()
	math.randomseed(os.time())
	for k, entity_type in pairs(input_scenario) do
		for i = 0, entity_type.n-1	 do
			create_entity(entity_type.entity)
		end	
	end
end

function love.update(dt)

	--charge and field force applications
 
	for k, entityf in pairs(entity_list) do
		for j, entityq in pairs(entity_list) do
			if(k ~= j) then
				separation = entityq.position.point - entityf.position.point

				if(entityf.field ~= nil and entityq.charge ~= nil and entityq.movement ~= nil) then
					force = ((separation)/((separation:length())^2)) * (1000 * entityf.field.strength * entityq.charge.strength)
					
					if(entityq.body ~= nil) then
						acceleration = force / entityq.body.size
					else
						acceleration = force / 1
					end

					if(entityq.movement ~= nil) then

						apply_velocity(entityq, acceleration*dt)
					end
				end
			end
		end
	end 
	
	if(player ~= nil) then	
		handle_input(dt)
	end

	for k, entity in pairs(entity_list) do
		if(entity.movement ~= nil) then
			new_position = entity.position.point + (entity.movement.motion * dt)

			if(new_position:length() > bounds_radius) then
				entity.position.point.x = -entity.position.point.x
				entity.position.point.y = -entity.position.point.y
				new_position = entity.position.point + (entity.movement.motion * dt)
			end

			entity.position.point = entity.position.point + (entity.movement.motion * dt)
		end
	end
	
	--check collisions

	for k, entity1 in pairs(entity_list) do
		for j, entity2 in pairs(entity_list) do
			check_collision(entity1, entity2)
		end
	end 
end

function handle_input(dt)
	move = vector2(0, 0)
	if(love.keyboard.isDown("up")) then
		move = vector2(0, 1)
	end
	if(love.keyboard.isDown("down")) then
		move = vector2(0, -1)
	end
	if(love.keyboard.isDown("left")) then
		move = vector2(-1, 0)
	end
	if(love.keyboard.isDown("right")) then
		move = vector2(1, 0)
	end

	new_velocity = player.movement.motion + move * player.control.acceleration * dt
	if(new_velocity:length() >= player.control.max_speed) then
		new_velocity = move * player.control.max_speed * dt
	end

	apply_velocity(player, move * player.control.acceleration * dt)

	camera_position = player.position.point
end

function apply_velocity(entity, speed)
	if(entity.movement ~= nil and entity.control ~= nil) then
		entity.movement.motion = entity.movement.motion + speed
		if(entity.movement.motion:length() > entity.control.max_speed) then
			entity.movement.motion = entity.movement.motion:normalized() * entity.control.max_speed
		end
 		--entity.movement.motion = entity.movement.motion + speed
	elseif(entity.movement ~= nil) then
		entity.movement.motion = entity.movement.motion + speed
	end
end

function distance(x1, x2)
	return ((x2.x - x1.x)^2 + (x2.y - x1.y)^2)^(1/2)
end

function to_screen_coordinates(world_space_coords)
	local ss = vector2(	(camera_origin.x - camera_position.x) + world_space_coords.x, 
						(camera_origin.y + camera_position.y) - world_space_coords.y)
	return ss
end

function love.draw()
	love.graphics.setColor(1,1,1,1)
	love.graphics.circle("line", camera_origin.x - camera_position.x, 
								 camera_origin.y + camera_position.y, bounds_radius)
	for k, entity in pairs(entity_list) do
		local ss = to_screen_coordinates(entity.position.point)	
		if(entity.body ~= nil) then 
			love.graphics.setColor(entity.color[1], entity.color[2], entity.color[3], 0.7)
			love.graphics.circle("fill", ss.x, ss.y, entity.body.size)	
		end

		if(entity.charge ~= nil) then
			love.graphics.setColor(entity.charge.color[1], entity.charge.color[2], entity.charge.color[3], 0.9)
			love.graphics.circle("fill", ss.x, ss.y, 4)	
		end
		love.graphics.setColor(1, 1, 1, 1)
		love.graphics.circle("line", ss.x, ss.y, 8)
	end
end

function create_entity(entity_type)
	local new_entity = deepcopy(require("./entity/" .. entity_type))

	if(new_entity.position ~= nil and new_entity.position.point == nil) then
		new_entity.position.point = vector2(0, 0)  
	end
	if(new_entity.movement ~= nil and new_entity.movement.motion == nil) then
		new_entity.movement.motion = vector2(0, 0)
	end
	if(new_entity.body ~= nil) then
		new_entity.color = {0, 1.0, 0}
	end
	if(new_entity.body ~= nil and new_entity.body.size == nil) then
		new_entity.body.size = 8
	end
	if(new_entity.control ~= nil) then
		player = new_entity
		if(new_entity.control.acceleration == nil) then
			new_entity.control.acceleration = 0.0
			new_entity.control.max_speed = 50.0 
		end
	end

	if(new_entity.field ~= nil and new_entity.field.strength == nil) then
		new_entity.field.strength = 1 
	end
	if(new_entity.field ~= nil and (new_entity.field.strength ~= nil or new_entity.field.strength == 0)) then
		if(new_entity.field.strength < 0) then
			new_entity.color = {1.0, 0, 0}
		else
			new_entity.color = {0, 0, 1.0}
		end
	end


	if(new_entity.charge ~= nil and new_entity.charge.strength == nil) then
		new_entity.charge.strength = 1 
	end
	if(new_entity.charge ~= nil) then
		if(new_entity.charge.strength < 0) then
			new_entity.charge.color = {1.0, 0, 0}
		elseif(new_entity.charge.strength == 0) then
			new_entity.charge.color = {0, 1.0, 0}
		else
			new_entity.charge.color = {0, 0, 1.0}
		end
	end
	new_entity.position.point.x , new_entity.position.point.y = randomize_circular_position(bounds_radius)

	entity_list[#entity_list+1] = new_entity
end

function randomize_circular_position(max_radius)
	local x = math.random(max_radius)
	local y = math.random((max_radius^2 - x^2)^(1/2)) -- r² = a² + b²
	if(math.random(10) > 5) then x = (-1)*x end
	if(math.random(10) > 5) then y = (-1)*y end
	return x, y
end