extends KinematicBody2D

const GRAVITY = 10
const SPEED = 30
const FLOOR = Vector2(0,-1)

var velocity = Vector2()

var direction = 1
#enum states {IDLE, ATTACKING}
#var state = IDLE
var is_attack=false 
var is_dead = false
export var strength = 6
onready var target = get_parent().get_node("player")

func _ready():
	pass

func attack():
	is_attack=true
	velocity = Vector2(0,0)
	$AnimatedSprite.play("attack")
func dead():
	is_dead=true
	velocity = Vector2(0,0)
	$AnimatedSprite.play("dead")
func _process(delta: float) -> void:
	if is_dead==false:
		velocity.x = SPEED * direction
	if direction==1:
		$AnimatedSprite.flip_h=false
	else:
		$AnimatedSprite.flip_h=true
	$AnimatedSprite.play("walk")
	
	velocity.y += GRAVITY
	velocity = move_and_slide(velocity, FLOOR)
	
	if is_on_wall():
		direction= direction * -1
		$RayCast2D.position.x *= -1
	
	if $RayCast2D.is_colliding()==false:
		direction=direction * -1
		$RayCast2D.position.x *= -1
		
func _on_Timer_timeout():
	damage_target(target, strength)
	#if not target:
	#	$Timer.stop()
	#	return
	#if state != IDLE:
	#	return

	#state = ATTACKING
	#$AnimationPlayer.play("anticipate")
func damage_target(target, damage):
	target.take_damage(damage)
