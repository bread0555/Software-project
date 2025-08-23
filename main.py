class CodeBlock:

    def __init__(self, i_p):
        self.i_p = i_p
        self.o_p = []

    def tab_to_spaces(self):
        for i in range(len(self.i_p)):
            if "\t" in self.i_p[i]:
                self.i_p[i] = self.i_p[i].replace("\t", "    ")

    def check_indents(self):
        if not self.i_p:
            self.indent = "    "
            self.indent_lvl = 0
            return

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

        if hcf == 0:
            self.indent_lvl = 0
            hcf = 4

        self.indent = hcf
        self.indent_lvl = (len(self.i_p[0]) - len(self.i_p[0].lstrip(" "))) // self.indent
        self.indent = " " * self.indent

    def analyse(self):
        self.tab_to_spaces()
        self.check_indents()
        i = 0
        self.i_p[:] = [line for line in self.i_p if line.strip()]
        while i < len(self.i_p):
            if (self.i_p[i].startswith(self.indent * self.indent_lvl)
                    and not self.i_p[i].startswith(self.indent *
                                                   (self.indent_lvl + 1))
                    and self.i_p[i].upper().split()[0] not in ["IF", "WHILE", "FOR", "TRY", "CASE", "REPEAT", "FUNCTION", "CASEWHERE"]):
                self.o_p += self.process_sequential_line(self.i_p[i])
                i += 1
            else:
                start = i
                constructor = self.i_p[i].upper().split()[0]
                while i < len(self.i_p):
                    if (self.i_p[i].startswith(self.indent * self.indent_lvl)
                            and
                            not self.i_p[i].startswith(self.indent *
                                                       (self.indent_lvl + 1))
                            and
                        (self.i_p[i].upper().split() == ["END", constructor]
                         or self.i_p[i].upper().split()[0] == "UNTIL")):
                        end = i
                        break
                    i += 1
                self.o_p += self.translator(constructor, self.i_p[start:end + 1])
                i += 1

    def process_control_block(self, constructor, i_p):
        if constructor == "IF":
            return self.transalte_if(i_p)
        elif constructor == "TRY":
            return self.translate_try(i_p)
        elif constructor == "WHILE":
            return self.translate_which(i_p)
        elif constructor == "FOR":
            return self.translate_for(i_p)
        elif constructor == "CASEWHERE":
            return self.translate_casewhere(i_p)
        elif constructor == "REPEAT":
            return self.translate_repeat(i_p)
        elif constructor == "FUNCTION":
            return self.translate_function(i_p)

    def transalte_if(self, i_p):
        o_p = []
        i = 0
        while i < len(i_p):
            if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                constructor = i_p[i].upper().split()[0]
                line = i_p[i].split()
                for j in range(len(line)):
                    if line[j] == "AND":
                        line[j] = "and"
                    if line[j] == "OR":
                        line[j] = "or"
                    if line[j] == "THEN":
                        line[j] = ":"
                if constructor == "IF":
                    o_p.append(self.indent * self.indent_lvl + "if " +
                               " ".join(line[1:]))
                elif constructor == "ELSE" and len(line) > 1:
                    o_p.append(self.indent * self.indent_lvl + "elif " +
                               " ".join(line[2:]))
                elif constructor == "ELSE":
                    o_p.append(self.indent * self.indent_lvl + "else:")
                elif constructor == "END":
                    pass
                else:
                    line = [" ".join(line)]
                    c = CodeBlock(line)
                    c.analyse()
                    o_p += c.o_p
                i += 1
            else:
                start = i
                while i < len(i_p):
                    if not i_p[i].startswith(self.indent *
                                             (self.indent_lvl + 1)):
                        end = i
                        break
                    i += 1
                c = CodeBlock(i_p[start:end])
                c.analyse()
                o_p += c.o_p
        return o_p

    def translate_try(self, i_p):
        o_p = []
        i = 0
        while i < len(i_p):
            if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                constructor = i_p[i].upper().split()[0]
                line = i_p[i].split()
                if constructor == "TRY":
                    o_p.append(self.indent * self.indent_lvl + "try:")
                elif constructor == "EXCEPT":
                    o_p.append(self.indent * self.indent_lvl + "except " +
                               " ".join(line[1:]) + ":")
                elif constructor == "ELSE":
                    o_p.append(self.indent * self.indent_lvl + "else:")
                elif constructor == "FINALLY":
                    o_p.append(self.indent * self.indent_lvl + "finally:")
                elif constructor == "END":
                    pass
                else:
                    line = [" ".join(line)]
                    c = CodeBlock(line)
                    c.analyse()
                    o_p += c.o_p
                i += 1
            else:
                start = i
                while i < len(i_p):
                    if not i_p[i].startswith(self.indent *
                                             (self.indent_lvl + 1)):
                        end = i
                        break
                    i += 1
                c = CodeBlock(i_p[start:end])
                c.analyse()
                o_p += c.o_p
        return o_p

    def translate_which(self, i_p):
        o_p = []
        i = 0
        while i < len(i_p):
            if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                constructor = i_p[i].upper().split()[0]
                line = i_p[i].split()
                if constructor == "WHILE":
                    o_p.append(self.indent * self.indent_lvl + "while " +
                               " ".join(line[1:]) + ":")
                elif constructor == "END":
                    pass
                else:
                    line = [" ".join(line)]
                    c = CodeBlock(line)
                    c.analyse()
                    o_p += c.o_p
                i += 1
            else:
                start = i
                while i < len(i_p):
                    if not i_p[i].startswith(self.indent *
                                             (self.indent_lvl + 1)):
                        end = i
                        break
                    i += 1
                c = CodeBlock(i_p[start:end])
                c.analyse()
                o_p += c.o_p
        return o_p

    def translate_for(self, i_p):
        o_p = []
        i = 0
        while i < len(i_p):
            if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                constructor = i_p[i].upper().split()[0]
                line = i_p[i].split()
                if constructor == "FOR":
                    line = " ".join(line[1:])
                    if "IN" in line:
                        line = line.split("IN")
                        line = [seq.strip() for seq in line]
                        o_p.append(self.indent * self.indent_lvl + "for " +
                                   line[0] + "in" + line[1] + ":")
                    elif "TO" in line:
                        line = line.split("TO")
                        line = [seq.strip() for seq in line]
                        line[0] = line[0].split("=")
                        line[0] = [seq.strip() for seq in line[0]]
                        if "STEP" in line[1]:
                            line[1] = line[1].split("STEP")
                            line[1] = [seq.strip() for seq in line[1]]
                            o_p.append(self.indent * self.indent_lvl + "for " +
                                       line[0][0] + " in range(" + line[0][1] +
                                       ", " + line[1][0] + ", " + line[1][1] +
                                       "):")
                        else:
                            o_p.append(self.indent * self.indent_lvl + "for " +
                                       line[0][0] + " in range(" + line[0][1] +
                                       ", " + line[1] + "):")
                elif constructor == "END":
                    pass
                else:
                    line = [" ".join(line)]
                    c = CodeBlock(line)
                    c.analyse()
                    o_p += c.o_p
                i += 1
            else:
                start = i
                while i < len(i_p):
                    if not i_p[i].startswith(self.indent *
                                             (self.indent_lvl + 1)):
                        end = i
                        break
                    i += 1
                c = CodeBlock(i_p[start:end])
                c.analyse()
                o_p += c.o_p
        return o_p

    def translate_casewhere(self, i_p):
        o_p = []
        i = 0
        comparative_ops = ["<", ">", "<=", ">=", "==", "!="]
        while i < len(i_p):
            if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                constructor = i_p[i].upper().split()[0]
                line = i_p[i].split()
                if constructor == "CASEWHERE":
                    variable = line[1]
                    selector = "if "
                elif constructor == "END":
                    pass
                i += 1
            elif ":" in i_p[i]:
                line = i_p[i].split(":")
                line = [seq.strip() for seq in line]
                if "TO" in line[0]:
                    line[0] = line[0].split("TO")
                    line[0] = [seq.strip() for seq in line[0]]
                    o_p.append(self.indent * self.indent_lvl + selector + line[0][0] + " <= " + variable + " <= " + line[0][1] + ":")
                elif any(operator in line[0] for operator in comparative_ops):
                    o_p.append(self.indent * self.indent_lvl + selector + variable + line[0] + ":")
                elif "OTHERWISE" in line[0]:
                    o_p.append(self.indent * self.indent_lvl + "else:")
                else:
                    o_p.append(self.indent * self.indent_lvl + selector + variable + " == " + line[0] + ":")
                c = CodeBlock(line[1:])
                c.analyse()
                o_p += [self.indent * (self.indent_lvl + 1) + line for line in c.o_p]
                selector = "elif "
                i += 1
            else:
                start = i
                while i < len(i_p):
                    if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                        end = i
                        break
                    i += 1
                c = CodeBlock(i_p[start:end])
                c.analyse()
                o_p += c.o_p
        return o_p

    def translate_repeat(self, i_p):
        o_p = []
        i = 0
        while i < len(i_p):
            if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                constructor = i_p[i].upper().split()[0]
                line = i_p[i].split()
                if constructor == "REPEAT":
                    o_p.append(self.indent * self.indent_lvl + "while True:")
                elif constructor == "UNTIL":
                    o_p.append(self.indent * (self.indent_lvl + 1) + "if " + " ".join(line[1:]) + ":")
                    o_p.append(self.indent * (self.indent_lvl + 2) + "break")
                else:
                    line = [" ".join(line)]
                    c = CodeBlock(line)
                    c.analyse()
                    o_p += c.o_p
                i += 1
            else:
                start = i
                while i < len(i_p):
                    if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                        end = i
                        break
                    i += 1
                c = CodeBlock(i_p[start:end])
                c.analyse()
                o_p += c.o_p
        return o_p

    def translate_function(self, i_p):
        o_p = []
        i = 0
        while i < len(i_p):
            if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                constructor = i_p[i].upper().split()[0]
                line = i_p[i].split()
                if constructor == "FUNCTION":
                    o_p.append(self.indent * self.indent_lvl + "def " + " ".join(line[1:]) + ":")
                elif constructor == "END":
                    pass
                else:
                    line = [" ".join(line)]
                    c = CodeBlock(line)
                    c.analyse()
                    o_p += c.o_p
                i += 1
            else:
                start = i
                while i < len(i_p):
                    if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                        end = i
                        break
                    i += 1
                c = CodeBlock(i_p[start:end])
                c.analyse()
                o_p += c.o_p
        return o_p

    def process_sequential_line(self, i_p):
        
        


c = CodeBlock(code)
c.analyse()
print(c.o_p)
