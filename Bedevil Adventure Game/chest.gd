extends AnimatedSprite
var emmited= false
func _physics_process(delta):
	if Input.is_action_just_pressed("ui_accept"):
		frame = 1
		if emmited==false:
			get_parent().get_node("CoinSpread").emmited = true
			emmited = true
