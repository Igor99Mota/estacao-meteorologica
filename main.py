# Importação das bibliotecas necessárias
from machine import Pin, ADC, SoftI2C
import ssd1306  # Controle do display OLED via I2C
import time
import dht      # Sensor de temperatura e umidade

# ========== Inicialização dos Componentes ==========

# Inicializa comunicação I2C com o display OLED
i2c = SoftI2C(sda=Pin(14), scl=Pin(15))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Sensores ambientais
sensor_dht = dht.DHT11(Pin(16))     # Sensor de temperatura/umidade DHT11
mq135 = ADC(Pin(28))                # Sensor MQ-135 de qualidade do ar (leitura analógica)

# Sensor de vento (HC-020K) - contador de pulsos
encoder_pin = Pin(17, Pin.IN, Pin.PULL_UP)
pulsos = 0
def contar_pulso(pin):
    global pulsos
    pulsos += 1
encoder_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=contar_pulso)

# Joystick analógico e botão central
adc_x = ADC(Pin(27))
adc_y = ADC(Pin(26))
joystick_button = Pin(22, Pin.IN, Pin.PULL_UP)

# Botões adicionais
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

# LED RGB para indicar qualidade do ar
led_r = Pin(13, Pin.OUT)
led_g = Pin(12, Pin.OUT)
led_b = Pin(11, Pin.OUT)

# ========== Variáveis de Estado ==========

menu_items = [
    "Temperatura",
    "Umidade",
    "Qualidade do Ar",
    "Vento (RPM)",
    "Vento (km/h)"
]
menu_index = 0        # índice do menu atual
rgb_on = True         # controle do LED RGB
last_move = time.ticks_ms()
last_button_a = 1
ultima_leitura_rpm = time.ticks_ms()
rpm = 0

# ========== Funções ==========

# Define a cor do LED RGB
def set_rgb_color(r, g, b):
    if rgb_on:
        led_r.value(r)
        led_g.value(g)
        led_b.value(b)
    else:
        led_r.value(0)
        led_g.value(0)
        led_b.value(0)

# Converte RPM em km/h com base no diâmetro da hélice
def calcular_kmh(rpm):
    diametro_cm = 3  # diâmetro da hélice em centímetros
    circ = 3.1416 * diametro_cm / 100  # circunferência em metros
    return round((rpm * circ / 60) * 3.6, 1)  # m/s para km/h

# Lê temperatura do DHT11
def read_temperature():
    try:
        sensor_dht.measure()
        return sensor_dht.temperature()
    except:
        return "--"

# Lê umidade do DHT11
def read_humidity():
    try:
        sensor_dht.measure()
        return sensor_dht.humidity()
    except:
        return "--"

# Lê qualidade do ar (valor analógico entre 0 e 65535)
def read_air_quality():
    return mq135.read_u16()

# Calcula RPM a partir dos pulsos lidos no sensor de vento
def read_rpm():
    global pulsos, ultima_leitura_rpm, rpm
    agora = time.ticks_ms()
    if time.ticks_diff(agora, ultima_leitura_rpm) >= 1000:
        rotacoes = pulsos / 20  # 20 pulsos por rotação
        rpm = int(rotacoes * 60)
        pulsos = 0
        ultima_leitura_rpm = agora
    return rpm

# Define status da qualidade do ar e muda cor do LED RGB
def air_quality_status(val):
    if val < 15000:
        set_rgb_color(0, 1, 0)  # verde
        return "Boa"
    elif val < 30000:
        set_rgb_color(1, 1, 0)  # amarelo
        return "Moderada"
    elif val < 45000:
        set_rgb_color(1, 0, 0)  # vermelho
        return "Ruim"
    else:
        set_rgb_color(1, 0, 0)  # vermelho intenso
        return "Péssima"

# Desenha o menu e exibe os dados no display OLED
def draw_menu():
    oled.fill(0)
    title = menu_items[menu_index]
    oled.text(title, 0, 0)

    if title == "Temperatura":
        temp = read_temperature()
        oled.text(f"{temp} C", 0, 20)

    elif title == "Umidade":
        hum = read_humidity()
        oled.text(f"{hum} %", 0, 20)

    elif title == "Qualidade do Ar":
        val = read_air_quality()
        status = air_quality_status(val)
        oled.text(status, 0, 20)
        oled.text(f"{val}", 0, 40)

    elif title == "Vento (RPM)":
        valor_rpm = read_rpm()
        oled.text(f"{valor_rpm} RPM", 0, 20)

    elif title == "Vento (km/h)":
        valor_rpm = read_rpm()
        kmh = calcular_kmh(valor_rpm)
        oled.text(f"{kmh} km/h", 0, 20)

    oled.show()

# Lê direção horizontal do joystick
def read_joystick_direction():
    x = adc_x.read_u16()
    if x > 50000:
        return 'right'
    elif x < 10000:
        return 'left'
    else:
        return 'center'

# ========== Loop Principal ==========

while True:
    air_val = read_air_quality()
    air_quality_status(air_val)

    # Navegação com joystick
    direction = read_joystick_direction()
    now = time.ticks_ms()

    if direction == 'right' and time.ticks_diff(now, last_move) > 500:
        menu_index = (menu_index + 1) % len(menu_items)
        last_move = now
    elif direction == 'left' and time.ticks_diff(now, last_move) > 500:
        menu_index = (menu_index - 1) % len(menu_items)
        last_move = now

    # Botão A alterna LED RGB
    button_a_state = button_a.value()
    if button_a_state == 0 and last_button_a == 1:
        rgb_on = not rgb_on
        air_quality_status(air_val)
    last_button_a = button_a_state

    draw_menu()
    time.sleep(0.1)
