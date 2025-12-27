# import os
# from dotenv import load_dotenv
# from groq import Groq

# load_dotenv()  # MUST come before reading env vars

# print("DEBUG KEY:", os.getenv("GROQ_API_KEY"))  # should NOT be None

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# response = client.chat.completions.create(
#     model="meta-llama/llama-4-scout-17b-16e-instruct",
#     messages=[{"role": "user", "content": "Hello"}]
# )

# print(response.choices[0].message.content)

from pathlib import Path

print("Testing input and file creation...")

# Create data directory
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)
print(f"✓ Directory created: {data_dir.absolute()}")

# Test input
print("\nEnter some text (type DONE and press Enter):")
lines = []
while True:
    line = input()
    if line.strip().upper() == 'DONE':
        break
    lines.append(line)

description = "\n".join(lines).strip()
print(f"\n✓ You entered: {description}")

# Save to file
file_path = data_dir / "test_description.txt"
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(description)

print(f"✓ File saved to: {file_path.absolute()}")

# Verify file exists
if file_path.exists():
    print("✅ SUCCESS! File was created.")
    with open(file_path, 'r') as f:
        print(f"Content: {f.read()}")
else:
    print("❌ FAILED! File was NOT created.")