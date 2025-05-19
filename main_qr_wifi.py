import qrcode

def create_qr():
    # WiFi configuration details
    ssid = "Oz_M"
    password = ""
    security = "WPA"  # This can be WPA, WEP, or leave empty for no password

    # Construct the WiFi QR code data string
    wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};;"

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(wifi_string)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save("wifi_qr.png")

print("QR code generated and saved as wifi_qr.png")

if __name__ == '__main__':
    create_qr()