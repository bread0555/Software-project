lines = []
with open("demo/if_else.txt") as f:
    for line in f:
        lines.append(line.strip("\n"))

class CodeBlock:
    def __init__(self, i_p):
        self.i_p = i_p
        self.o_p = []

    def tab_to_spaces(self):
        for i in range(len(self.i_p)):
            if "\t" in lines[i]:
                lines[i] = lines[i].replace("\t", "    ")

    def check_indents(self):
        if not self.i_p:
            self.indent = 0
        indents = []
        for line in self.i_p:
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
        self.indent = hcf
        self.indent_lvl = (len(self.i_p[0]) - len(self.i_p[0].lstrip(" "))) / self.indent
        self.indent = " " * self.indent

    def analyse(self):
        self.tab_to_spaces()
        self.check_indents()
        i = 0
        while i < len(self.i_p):
            if (self.i_p[i].startswith(self.indent * self.indent_lvl) 
                and not self.i_p[i].startswith(self.indent * (self.indent_lvl + 1))
               ):
                
                i += 1
            else:
                start = i - 1
                ctrl_type = self.i_p[i - 1].strip().split(" ")[0].upper()
                while i < len(self.i_p):
                    if self.i_p[i].split(" ")[0].strip().upper() == f"{self.indent * self.indent_lvl}END {ctrl_type}":
                        break
                    i += 1
                end = i
                code_block = self.i_p[start:end]
 
            
                # mark the line that the first control structure starts (i - 1)
                # find when the control structure block ends
                # depending on the first word of the line, pass the block into the appropriate method
                
            


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
            