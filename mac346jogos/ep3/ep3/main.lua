class = require "class"
vector2 = require "common/vec"

input_scenario = require "scene/test"

camera_center = vector2(0,100)
camera_origin = vector2(love.graphics.getWidth()/2,love.graphics.getHeight()/2)

bounds_radius = 200

entity_list = {}

function default_entity() 
	return 
	{
		position = 
		{
	    	point = vector2(0, 0)
	  	},
	  	movement = 
	  	{
	    	motion = vector2(0, 0)
	  	},
	  	body = 
	  	{
	    	size = 8
	  	},
	  	control = 
	  	{
	    	acceleration = 0.0,
	    	max_speed = 50.0,
	  	},
	  	field = 
	  	{
	    	strength = 1
	  	},
	  	charge = 
  		{
    		strength = 1
  		}
	}
end

function love.load()
	for k, entity_type in pairs(input_scenario) do
		for i = 0, entity_type.n do
			create_entity(entity_type.entity)
		end	
	end
end 

function love.draw()
	love.graphics.circle("line", camera_origin.x-camera_center.x, 
								 camera_origin.y-camera_center.y, bounds_radius)
	for entity in entity_list do
		love.graphics.circle("line", camera_origin.x-entity.position.point.x)
	end
end

function create_entity(entity_type)
	default_entity = default_entity()
	print(default_entity.position.point)
	new_entity = require("./entity/" .. entity_type)
	for k, v in pairs(new_entity) do default_entity[k] = v end
	default_entity.position.point.x , default_entity.position.point.y = randomize_circular_position(bounds_radius - default_entity.body.size)
	table.insert(entity_list, default_entity)
end

function randomize_circular_position(max_radius)
	x = math.random(max_radius)
	y = math.random(max_radius^2 - x^2) -- r² = a² + b²
	return x, y
end