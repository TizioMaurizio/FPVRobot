extends Spatial

onready var viewport = $Viewport
onready var pivot = $Viewport/Spatial/Pivot


func _process(_delta):
	if goat.ENABLE_INVENTORY_ICON_ROTATION:
		var seconds = OS.get_ticks_msec() * 0.001
		pivot.rotation_degrees.y = (
			360.0 * seconds / goat.INVENTORY_ICON_ROTATION_PER_SECOND
		)


func make_icon_texture(model_scene_path):
	var scene = load(model_scene_path).instance()
	scene.set_script(null)
	for c in pivot.get_children():
		pivot.remove_child(c)
	pivot.add_child(scene)
	return viewport.get_texture()
