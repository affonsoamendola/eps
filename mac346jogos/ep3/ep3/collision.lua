function check_collision(entity1, entity2)
	local entity1_size = 8
	local entity2_size = 8

	if(entity1.body ~= nil) then
		entity1_size = entity1.body.size
	end
	if(entity2.body ~= nil) then
		entity2_size = entity2.body.size
	end

	distance = (entity2.position.point - entity1.position.point):length()

	if(distance < entity2_size + entity1_size) then

		l = (entity2_size + entity1_size) - distance

		d = (entity2.position.point - entity1.position.point):normalized()

		entity2.position.point = entity2.position.point + (d * l)
		
		if(entity2.movement ~= nil) then
			entity2.movement.motion = entity2.movement.motion - d*(d:dot(entity2.movement.motion))
		end
	end
end

