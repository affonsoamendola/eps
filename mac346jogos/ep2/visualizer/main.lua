require "love"

world_layers = {}
world_file = {}
layer_count = 0

camera_position = {0, 0}

backgroundcolor = {0, 0, 0}

function love.load(arg)

	if(arg[1] == nil) then
		print("You must provide a world file to visualize.")
		love.event.quit()
		return
	end

	load_world("./maps/" .. arg[1])

	backgroundcolor = {world_file.backgroundcolor[1]/255, world_file.backgroundcolor[2]/255, world_file.backgroundcolor[3]/255 }
	tileset_image = love.graphics.newImage("maps/tilesheet_complete.png")
end

function load_world(filename)
	world_file = require(filename)

	for k, layer in pairs(world_file.layers) do
		if layer.type == "tilelayer" then
			layer_count = layer_count + 1
			world_layers[layer_count] = layer
		end
	end
end

function love.draw()
	love.graphics.setBackgroundColor(backgroundcolor)

	for l = 1, layer_count do
		for x = 1, world_file.width do
			for y = 1, world_file.height do
				local ss_x, ss_y = ws_to_ss(x, y, 	world_layers[l].offsety, 
													world_file.tilewidth, world_file.tileheight)
			
				local current_tile = world_layers[l].data[(y-1) * world_file.width + x]
				if current_tile ~= 0 then
					draw_tile(ss_x, ss_y, current_tile)
				end
			end
		end
	end
end

function draw_tile(ss_x, ss_y, tile_id)
	love.graphics.draw(tileset_image, get_tile_quad(tile_id), ss_x, ss_y)
end

function get_tile_quad(tile_id)
	local quad = love.graphics.newQuad(	world_file.tilewidth * ((tile_id % 21) - 1), 
										world_file.tileheight * 2 * math.floor(tile_id / 21), 
										world_file.tilewidth, world_file.tileheight * 2, 
										tileset_image:getDimensions())
	
	return quad
end

function ws_to_ss(x, y, z, w, h)
	local ss_x = (x - y) * (w/2) + camera_position[1]
	local ss_y = (x + y) * (h/2) + z + camera_position[2]
	return ss_x, ss_y
end
