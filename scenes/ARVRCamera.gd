extends ARVRCamera


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

var udp := PacketPeerUDP.new()
var connected = false

# Called when the node enters the scene tree for the first time.
func _ready():
	udp.connect_to_host("192.168.1.12", 1234)
	#print camera orientation
	print("Camera orientation: ", rotation)
	
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
var totDelta = 0
func _process(delta):
	totDelta = totDelta + delta
	#convert rotation to PoolByteArray
	#send rotation
	if(totDelta > 0.5):
		totDelta = 0
		udp.put_packet(var2str(rotation).to_utf8())
		print("sent")
	pass
