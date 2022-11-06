def connect(ssid):
    import network
    sta_if = network.WLAN(network.STA_IF)
    print('connecting to network...')
    sta_if.active(True)
    sta_if.disconnect()
    if ssid == 'TIM-37482183-5G':
        password = 'HnbD76SPtLs7G8vS'
    if ssid == 'Xiaomi 11T Pro':
        password = 'HnbD76SPtLs7G8vS'
    if ssid == 'RedmiMau':
        password = 'mau12397'
    if ssid == 'LenovoTizio':
        password = 'tizio1234'
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        pass
    print('network config:', sta_if.ifconfig())

def list():
    print('- TIM-37482183-5G')
    print('- Xiaomi 11T Pro')
    print('- RedmiMau')
    print('- LenovoTizio')