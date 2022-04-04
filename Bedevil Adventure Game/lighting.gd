extends Node2D
onready var sprite_texture= [	preload("res://storm/lightning1.png"),
						preload("res://storm/lightning2.png"),
						preload("res://storm/lightning3.png")]
func _ready():
	$Sprite/Timer.wait_time=rand_range(3,15)
	$Sprite/Timer.start()
func lighting():
	$Sprite.texture = sprite_texture[randi() % 3]
	position.x = rand_range(0,640)
	$Sprite/AnimationPlayer.play("light")
	$Sprite/Timer.wait_time=rand_range(3,15)
	$Sprite/Timer.start()

func _on_Timer_timeout():
	lighting()
