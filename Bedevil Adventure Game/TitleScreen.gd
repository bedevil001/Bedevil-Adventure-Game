extends Node2D


func _ready():
	$MarginContainer2/VBoxContainer2/TextureButton3.grab_focus()

func _process(delta):
	if $MarginContainer2/VBoxContainer2/TextureButton.is_hovered() == true:
		$MarginContainer2/VBoxContainer2/TextureButton.grab_focus()
	if $MarginContainer2/VBoxContainer2/TextureButton2.is_hovered() == true:
		$MarginContainer2/VBoxContainer2/TextureButton2.grab_focus()
	if $MarginContainer2/VBoxContainer2/TextureButton3.is_hovered() == true:
		$MarginContainer2/VBoxContainer2/TextureButton3.grab_focus()
