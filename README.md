# QR Code Image Encoder and Decoder

 This Python script allows you to encode data into a QR code image and decode the QR code to retrieve the original data. It also provides functionality to merge three QR codes encoded with different colors into a single colored QR code image.

## Dependencies

- qrcode
- Pillow (PIL)
- subprocess

You can install the dependencies using pip: `pip install qrcode pillow`

## Usage

### Encoding Data into a QR Code Image

To encode data into a QR code image, use the `enc` function with the following parameters:

`enc(data_1, data_2, data_3, output_filename, version)`

- `data_1`, `data_2`, `data_3`: Data strings to be encoded into the three channels of the QR code.
- `output_filename`: Filename for the output QR code image.
- `version`: Version of the QR code (numeric value).

Example:

`enc('hello', 'world', '123', 'output.png', ver=4)`

### Decoding a QR Code Image

To decode a QR code image, use the `dec` function with the filename of the input image:

`dec(input_filename)`

This function returns a tuple containing the decoded data from the three channels of the QR code.

Example:

`decoded_data = dec('output.png') print(decoded_data)`

### main() Function

The `main` function demonstrates an example usage of encoding and decoding data.
