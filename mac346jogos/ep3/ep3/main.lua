class = require "class"
vector2 = require "common/vec"

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
	for k, entity in pairs(entity_list) do
		if(entity.movement ~= nil) then
			local old_position = deepcopy(entity.position.point)
			entity.position.point = entity.position.point + (entity.movement.motion * dt)
		end
	end	
	if(player ~= nil) then	
		handle_input(dt)
	end
end

function handle_input(dt)
	if(love.keyboard.isDown("up")) then
		player.movement.motion = player.movement.motion + vector2(0,  player.control.acceleration * dt)
	end
	if(love.keyboard.isDown("down")) then
		player.movement.motion = player.movement.motion + vector2(0, -player.control.acceleration * dt)
	end
	if(love.keyboard.isDown("left")) then
		player.movement.motion = player.movement.motion + vector2(-player.control.acceleration * dt, 0)
	end
	if(love.keyboard.isDown("right")) then
		player.movement.motion = player.movement.motion + vector2( player.control.acceleration * dt, 0)
	end

	camera_position = player.position.point
end

function check_collision(entity1, entity2)
	local entity1_size = 8
	local entity2_size = 8

	if(entity1.body ~= nil) then
		entity1_size = entity1.body.size
	end
	if(entity2.body ~= nil) then
		entity2_size = entity2.body.size
	end

	return distance(entity2.position.point, entity1.position.point) < entity1_size + entity2_size
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
			love.graphics.setColor(0, 1, 0, 0.7)
			love.graphics.circle("fill", ss.x, ss.y, entity.body.size)	
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
	if(new_entity.charge ~= nil and new_entity.charge.strength == nil) then
		new_entity.charge.strength = 1 
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