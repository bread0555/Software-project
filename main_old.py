lines = []
with open("demo/if_else.txt") as f:
  for line in f:
    lines.append(line.strip("\n"))

class CodeBlock:
  def __init__(self, input):
    self.input = input
    self.output = []
    self.avoid_keywords = ["ELIF", "ELSE", "EXCEPT"]

  def check_indent_level(self):
    indents = []
    for line in self.input:
      indents.append(len(line) - len(line.lstrip(" ")))
    hcf = indents[0]
    for i in range(1, len(indents)):
      x = hcf
      y = indents[i]
      while y != 0:
        temp = y
        y = x % y
        x = temp
      hcf = x
    self.indent_level = hcf


  def analyse(self):
    line = 0
    start = None
    self.check_indent_level()
    while line < len(self.input):
      if (
        self.input[line].startswith(" " * self.indent_level) 
        and not self.input[line].startswith(" " * (self.indent_level + 1))
      ):
        # add code that deals with sequential statements
        # a bunch of if statements
        # add to output
        line += 1
      else:
        if not start:
          start = line
        control_type = self.input[line].split(" ")[0].upper()
        # deals with control structures
        while (
          line < len(self.input) 
          and not self.input[line].startswith(" " * self.indent_level) 
          and self.input[line].upper().split(" ")[0] not in self.avoid_keywords
        ):
          line += 1
        end = line
        code_block = self.input[start:end]
        self.output += self.pseudocode_to_python(code_block, control_type)
        line += 1

  def pseudocode_to_python(self, code_block, control_type):
    if control_type == "IF":
      line = self.if_control_struc(code_block)
      return line
    elif control_type == "WHILE":
      pass
    elif control_type == "FOR":
      pass
    elif control_type == "TRY":
      pass

    return []

  def if_control_struc(self, code_block):
    output = []
    line = 0
    print(self.indent_level)
    keywords = ["IF", "ELIF", "ELSE"]
    start = None
    while line < len(code_block):
      if code_block[line].upper().split(" ")[0] == keywords[0]:
        temp_line = code_block[line].split(" ")
        output.append(" " * self.indent_level + "if " + " ".join(temp_line[1:-1]) + ":")
        line += 1
      elif code_block[line].upper().split(" ")[0] == keywords[1]:
        temp_line = code_block[line].split(" ")
        output.append(" " * self.indent_level + "elif " + " ".join(temp_line[1:-1]) + ":")
        line += 1
      elif code_block[line].upper().split(" ")[0] == keywords[2]:
        output.append(" " * self.indent_level + "else:")
        line += 1
      else:
        if not start:
          start = line
        while (
          line < len(code_block) 
          and not code_block[line].startswith(" " * self.indent_level) 
          and code_block[line].upper().split(" ")[0] not in keywords
        ):
          line += 1
        end = line
        code_block = self.input[start:end]
        c = CodeBlock(code_block)
        c.analyse()
        output += c.output
    return output

  def try_control_struc(self, code_block):
    output = []
    line = 0
    keywords = ["TRY", "EXCEPT"]


c = CodeBlock(lines)
c.analyse()
print(c.output)