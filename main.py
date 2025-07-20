print("Hello World")

class CodeBlock:
  def __init__(self, block_type):
    self.block_type = block_type

  def to_python(self):
    if self.block_type == "IF":
      pass
    if self.block_type == "ELSE":
      pass