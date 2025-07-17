# restore_from_text.py
import base64

# Replace this with your pasted base64 text file
input_file = 'example_encoded.txt'
output_file = 'example_restored.bin'

with open(input_file, 'r') as f:
    encoded = f.read()

# Decode base64 back to binary
binary_data = base64.b64decode(encoded)

with open(output_file, 'wb') as f:
    f.write(binary_data)

print(f"Binary content restored to {output_file}")
