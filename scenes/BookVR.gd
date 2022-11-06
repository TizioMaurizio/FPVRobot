extends Spatial

# The current page is the one on the left, 0 is the cover
var current_page_number = -1
# TODO: calculate this depending on book length
const MAX_PAGE = 35
const ORIGINAL_BOOK_POSITION = Vector3(0, 1.85, -1)

onready var book = $Book
# This is displayed when pages are not moving
onready var static_page = $Book/Static
# This is displayed when pages are moving
onready var turning_page = $Book/Turning
onready var turning_animation = $Book/Turning/Page/AnimationPlayer

# Pages when turning: left, animated side 1, animated side 2, right
onready var pf1 = $Book/Turning/PageLeft
onready var pf2 = $Book/Turning/Page/Front
onready var pf3 = $Book/Turning/Page/Back
onready var pf4 = $Book/Turning/PageRight

# Pages when static: left, right
onready var ps1 = $Book/Static/PageLeft
onready var ps2 = $Book/Static/PageRight

# There are 6 viewports. Current page (left) is v3, to its right is v4.
# Moreover, there are 2 pages before (v1, v2) and after (v5, v6)
onready var v1 = $Viewport1
onready var v2 = $Viewport2
onready var v3 = $Viewport3
onready var v4 = $Viewport4
onready var v5 = $Viewport5
onready var v6 = $Viewport6

onready var raycast = $ARVRCamera/RayCast
onready var tween = $Tween


func _ready():
	var arvr_interface = ARVRServer.find_interface("Native mobile")
	if arvr_interface and arvr_interface.initialize():
		get_viewport().arvr = true
	global.connect("switch_book", self, "_on_switch_book")
	global.connect("switch_environment", self, "_on_switch_environment")
