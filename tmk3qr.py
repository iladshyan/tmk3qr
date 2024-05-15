import qrcode
from PIL import Image
import subprocess


def multiply_colors(color1, color2):
    """Multiply two colors (R, G, B) element-wise."""
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    # Perform element-wise multiplication
    r_result = r1 * r2
    g_result = g1 * g2
    b_result = b1 * b2

    return (r_result, g_result, b_result)

def add_colors(c1,c2,c3):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    r3, g3, b3 = c3
    
    return(r1 + r2 + r3, g1 + g2 + g3, b1 + b2 + b3)

def makeqr(data,ver):
    # Generate QR code
    qr = qrcode.QRCode(
        version=ver,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to RGB mode
    img = img.convert("RGB")

    # Get pixel data as a 2D array of colors
    pixels = list(img.getdata())
    width, height = img.size
    pixel_array = [pixels[i * width:(i + 1) * width] for i in range(height)]
    return pixel_array

def make3channelqr(rc,gc,bc,ver):
    qrrc = makeqr(rc,ver)
    conv_qrrc = [[None]*len(qrrc) for _ in range(len(qrrc))]
    for i in range(len(qrrc)):
        for j in range(len(qrrc)):
            conv_qrrc[i][j] = multiply_colors((1,0,0), qrrc[i][j])
    qrgc = makeqr(gc,ver)
    conv_qrgc = [[None]*len(qrgc) for _ in range(len(qrgc))]
    for i in range(len(qrgc)):
        for j in range(len(qrgc)):
            conv_qrgc[i][j] = multiply_colors((0,1,0), qrgc[i][j])          
    qrbc = makeqr(bc,ver)
    conv_qrbc = [[None]*len(qrbc) for _ in range(len(qrbc))]
    for i in range(len(qrbc)):
        for j in range(len(qrbc)):
            conv_qrbc[i][j] = multiply_colors((0,0,1), qrbc[i][j])

    final_qr = [[None]*len(qrrc) for _ in range(len(qrrc))]
    for i in range(len(final_qr)):
        for j in range(len(final_qr)):
            final_qr[i][j] = add_colors(conv_qrrc[i][j],conv_qrgc[i][j],conv_qrbc[i][j])
    return (final_qr)

def create_image_from_array(pixel_array, filename):
    """Create an image from a 2D array of pixel colors and save it as a PNG file."""
    # Determine image dimensions
    height = len(pixel_array)
    width = len(pixel_array[0])

    # Create a new image with RGB mode
    img = Image.new("RGB", (width, height))

    # Put pixel data into the image
    pixels = [color for row in pixel_array for color in row]  # Flatten the 2D array
    img.putdata(pixels)

    # Save the image
    img.save(filename)
    print("Image saved as", filename)

def image_to_2d_arrays(image_path):
    """Convert an image to 2D arrays for each channel (R, G, B) in grayscale."""
    # Open the image
    img = Image.open(image_path)

    # Convert the image to RGB mode (in case it's in a different mode)
    img = img.convert("RGB")

    # Get the width and height of the image
    width, height = img.size

    # Initialize 2D arrays for each channel
    red_array = [[0] * width for _ in range(height)]
    green_array = [[0] * width for _ in range(height)]
    blue_array = [[0] * width for _ in range(height)]

    # Iterate over each pixel and extract RGB values
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            # Convert RGB values to grayscale
            red_array[y][x] = r
            green_array[y][x] = g
            blue_array[y][x] = b

    return red_array, green_array, blue_array

def create_bw_image_from_array(pixel_array, filename):
    """Convert a 2D array of grayscale pixel intensities to a grayscale image."""
    # Determine image dimensions
    height = len(pixel_array)
    width = len(pixel_array[0])

    # Create a new image with L mode (grayscale)
    img = Image.new("L", (width, height))

    # Put pixel data into the image
    pixels = [value for row in pixel_array for value in row]  # Flatten the 2D array
    img.putdata(pixels)

    # Save the image
    img.save(filename)
    print("Image saved as", filename)

def read_qr(file):
    # Run the command in the command prompt
    result = subprocess.run(f'C:\Windows\System32\cmd.exe /c "zbarimg -q {file}"', shell=True, capture_output=True)
    output = result.stdout.strip()
    return output[8:].decode('utf-8')
        
        
def dec(img):
    cr , cg , cb = image_to_2d_arrays(img)

    create_bw_image_from_array(cr,'cr.png')
    create_bw_image_from_array(cg,'cg.png')
    create_bw_image_from_array(cb,'cb.png')

    dcrqr = read_qr('cr.png')
    dcgqr = read_qr('cg.png')
    dcbqr = read_qr('cb.png')
    
    return (dcrqr,dcgqr,dcbqr)

def enc(a,b,c,file,ver):
    create_image_from_array(make3channelqr(a,b,c,ver), file)

def main():
    enc('a','a','a', 'out.png',ver=4)
    a = dec('out.png')
    print(type(a),f'>{a}')
    
if __name__ == "__main__":
    main()