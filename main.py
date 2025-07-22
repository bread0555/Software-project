lines = []
with open("demo/if_else.txt") as f:
  for line in f:
    lines.append(line.strip("\n"))



class CodeBlock:
  def __init__(self, input, indent_level = 0):
    self.input = input
    self.output = output
    self.indent_level = indent_level

  def analyse(self)):
    if self.input[0].startswith(" " + " " * self.indent_level):
      
    else:
      self.name = self.input[0].strip(" ")
      return
      
    # analyse the line given, storesthe first word in a variable

  def to_python(self):

    # need something to check how long the indent goes for, and send in the input into the recursive input
    if self.block_type == "IF":
      pass
    if self.block_type == "ELSE":
      pass
    if self.variable_name == "while":
      CodeBlock(self.input) # recurrsively create new classes to solve the problem of code idented far inside


c = CodeBlock(lines)
      