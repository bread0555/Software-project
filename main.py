lines = []
with open("demo/if_else.txt") as f:
  for line in f:
    lines.append(line.strip("\n"))



class CodeBlock:
  def __init__(self, input, indent_level = 0):
    self.input = input
    self.output = []
    self.indent_level = indent_level
    self.avoid_keywords = ["elif", "else", "except"]

  def analyse(self):
    line = 0
    block = []
    start = None
    while line < len(self.input):
      if self.input[line].startswith(" " * self.indent_level) and not self.input[line].startswith(" " * (self.indent_level + 1)):
        # add code that deals with sequential statements
        # a bunch of if statements
        # add to output
        line += 1
        start = line
      else:
        # deals with control structures
        while line > len(self.input) and not self.input[line].startswith(" " * self.indent_level) and  self.input[line].split(" ")[0] not in self.avoid_keywords:
          line += 1
        end = line
        block = self.input[start:end]
        codeblock = CodeBlock(block, self.indent_level + 1)
        codeblock.analyse()
        self.output += codeblock.output


  def to_python(self):
    # Different block types: FUNCTION, IF, WHILE, FOR, TRY, assignment, function call, comment
    
  

    # need something to check how long the indent goes for, and send in the input into the recursive input
    if self.block_type == "IF":
      pass
    if self.block_type == "ELSE":
      pass
    if self.variable_name == "while":
      CodeBlock(self.input) # recurrsively create new classes to solve the problem of code idented far inside


  # Control structures that will call the class again
  # Find a way to determine where the block ends, and pass it through into the class
  # Add multiway selection and post-test iteration
  def function_struc(self):
    pass

  def if_struc(self):
    pass
    # find out way to seperate if, elif, and else statements

  def while_struc(self):
    pass

  def for_struc(self):
    pass
    # manage the two different for loop structures

  def try_struc(self):
    pass

  # Sequential statements
  def assignment(self):
    pass

  def function_call(self):
    pass

  def comment(self):
    pass

  # Function to 


c = CodeBlock(lines)
      