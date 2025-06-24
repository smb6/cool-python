import qrcode
from PIL import Image, ImageDraw, ImageFont


def create_qr():
    # WiFi configuration details
    security = "WPA"  # This can be WPA, WEP, or leave empty for no password

    # WiFi credentials
    ssid = "YourSSID"
    password = "YourPassword"
    # security = "WPA"  # WPA, WEP, or "" for open networks

    # Generate QR code
    wifi_data = f"WIFI:T:{security};S:{ssid};P:{password};;"
    qr = qrcode.make(wifi_data).convert("RGB")

    # Load Helvetica (macOS)
    try:
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", size=20)
    except:
        font = ImageFont.load_default()

    # Text lines
    lines = [f"Network: {ssid}", f"\n", f"Password: {password}"]  # Empty line for spacing

    # Measure sizes
    temp_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(temp_img)
    line_sizes = [draw.textbbox((0, 0), line, font=font) for line in lines]
    line_heights = [bbox[3] - bbox[1] for bbox in line_sizes]
    max_text_width = max(bbox[2] - bbox[0] for bbox in line_sizes)
    total_text_height = sum(line_heights) + (len(lines) - 1) * 5

    # Layout
    padding_top = 20
    padding_left = 20
    text_block_width = max_text_width + padding_left * 2
    img_width = max(qr.width, text_block_width)
    img_height = qr.height + total_text_height + padding_top + 20

    # Create final image
    final_img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(final_img)

    # Draw text (left-aligned)
    current_y = padding_top
    for i, line in enumerate(lines):
        draw.text((padding_left, current_y), line, fill="black", font=font)
        current_y += line_heights[i] + 5

    # Paste QR code
    qr_x = (img_width - qr.width) // 2
    qr_y = current_y + 10
    final_img.paste(qr, (qr_x, qr_y))

    # Save and show
    final_img.save("wifi_qr_with_line_spacing.png")
    final_img.show()


print("QR code generated and saved as wifi_qr.png")

if __name__ == '__main__':
    create_qr()