extends Button


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

var udp := PacketPeerUDP.new()
var connected = false

# Called when the node enters the scene tree for the first time.
func _ready():
	udp.connect_to_host("192.168.1.12", 1234)
	print("Hello World")
	#change color of this object to red
	self.modulate = Color(1,0,0,1)
	pass # Replace with function body.

# when Button2 is pressed change color of Button to yellow
func _pressed():
	#change color of this object to yellow
	self.modulate = Color(1,1,0,1)
	udp.put_packet("stop".to_utf8())
	#change label of this button to ciao
	self.text = "stopped"
	#udp send to localhost ciao

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
