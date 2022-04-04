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
			
func play_sound(sound: String):
	var player = AudioStreamPlayer2D.new()
	player.stream = load(sound)
	player.connect("finished", player, "queue_free")
	add_child(player)
	player.play()
func _on_Coin_body_entered(body):
	$Collision.call_deferred("set", "disabled", true)
	$Sound.play()
	hide()
	emit_signal("get_coin")
