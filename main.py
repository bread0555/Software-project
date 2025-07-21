print("Hello World")

lines = []
with open("demo/if_else.txt") as f:
  for line in f:
    lines.append(line.strip("\n"))

print(lines)

for line in lines:
  

class CodeBlock:
  def __init__(self, block_type):
    self.block_type = block_type

  def to_python(self):
    if self.block_type == "IF":
      pass
    if self.block_type == "ELSE":
      pass