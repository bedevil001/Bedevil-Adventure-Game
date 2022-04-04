extends Node2D

func _on_LeftButton_pressed():
	Input.action_press("ui_left")
func _on_LeftButton_released():
	Input.action_release("ui_left")
func _on_RightButton_pressed():
	Input.action_press("ui_right")
func _on_RightButton_released():
	Input.action_release("ui_right")
func _on_JumpButton_pressed():
	Input.action_press("ui_up")
func _on_JumpButton_released():
	Input.action_release("ui_up")
#func _on_AttackRightButton_pressed():
#	Input.action_press("ui")
#func _on_AttackRightButton_released():
#	pass # Replace with function body.
#func _on_AttackLeftButton_pressed():
#	pass # Replace with function body.
#func _on_AttackLeftButton_released():
#	pass # Replace with function body.
