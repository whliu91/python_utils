# save_as_text.py
import base64

# Replace this with your binary file path
input_file = 'pnpm-win-x64.exe'
output_file = 'pnpm.exe.txt'

with open(input_file, 'rb') as f:
    binary_data = f.read()

# Encode to base64
encoded = base64.b64encode(binary_data).decode('utf-8')

# Write the base64 string to a .txt file
with open(output_file, 'w') as f:
    f.write(encoded)

print(f"Base64-encoded content written to {output_file}")
