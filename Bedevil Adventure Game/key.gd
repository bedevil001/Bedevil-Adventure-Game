extends Area2D


func _on_Coins_body_entered(body):
	queue_free()
