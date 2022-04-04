extends CanvasLayer


func _ready():
	connect("pressed",self,"_on_pressed")

func _on_pressed():
	var player = run.get_main_node("player")
	if player:
		player.set_state(player.run)
	hide()
