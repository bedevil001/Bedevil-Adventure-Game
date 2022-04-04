extends Area2D

func _physics_process(delta):
	var bodies = get_overlapping_bodies()
	for body in bodies:
		if body.name=="player":
			$AnimatedSprite.play("taken")
			yield($AnimatedSprite,"animation_finished")
			queue_free()
		else:
			$AnimatedSprite.play("idle")
