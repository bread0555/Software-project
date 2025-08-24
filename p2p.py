class CodeBlock:

    def __init__(self, i_p):
        self.i_p = i_p # i_p in this class represents the input (in pseudocode)
        self.o_p = [] # o_p in this class represents the output (in python)
        self.indent = "    "
        self.indent_lvl = 0

    def tab_to_spaces(self):
        for i in range(len(self.i_p)):
            if "\t" in self.i_p[i]:
                self.i_p[i] = self.i_p[i].replace("\t", "    ")

    def check_indents(self):
        if not self.i_p:
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
        keywords = ["IF", "WHILE", "FOR", "TRY", "CASE", "REPEAT", "FUNCTION", "CASEWHERE"]
        i = 0
        self.i_p[:] = [line for line in self.i_p if line.strip()]
        while i < len(self.i_p):
            if (self.i_p[i].startswith(self.indent * self.indent_lvl)
                    and not self.i_p[i].startswith(self.indent *
                                                   (self.indent_lvl + 1))
                    and self.i_p[i].upper().split()[0] not in keywords):
                action = self.i_p[i].upper().split()[0]
                self.o_p.append(self.process_sequential_line(action, self.i_p[i]))
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
                self.o_p += self.process_control_block(constructor, self.i_p[start:end + 1])
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
                    if line[j] == "NOT":
                        line[j] = "not"
                    if line[j] == "=":
                        line[j] = "=="
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
                                   line[0] + " in " + line[1] + ":")
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

    def process_sequential_line(self, action, i_p):
        if action == "PRINT":
            return self.translate_print(i_p)
        elif action == "INPUT":
            return self.translate_input(i_p)
        elif action == "SET":
            return self.translate_set(i_p)
        elif action == "CALL":
            return self.translate_call(i_p)
        elif action == "APPEND":
            return self.translate_append(i_p)
        elif action in ["BREAK", "CONTINUE", "PASS", "RETURN"]:
            return self.translate_control(i_p, action)
        else:
            return i_p

    def translate_print(self, i_p):
        operand = " ".join(i_p.split()[1:])
        o_p = self.indent * self.indent_lvl + "print(" + operand + ")"
        return o_p

    def translate_input(self, i_p):
        pseudo_python_eqv = {
            "INTEGER": "int",
            "FLOAT": "float",
            "STRING": "str",
            "BOOLEAN": "bool",
        }
        variable = i_p.split()[-1]
        operand = " ".join(i_p.split()[1:-1])
        if "'" in operand:
            operand = operand.split("'")
        elif '"' in operand:
            operand = operand.split('"')
        else:
            operand = [operand]
        operand = [seq.strip() for seq in operand if seq.strip()]
        if len(operand) == 0:
            o_p = self.indent * self.indent_lvl + variable + " = input()"
        elif len(operand) == 1:
            if "AS" in operand[0]:
                data_type = operand[0].split("AS")[1].strip()
                o_p = self.indent * self.indent_lvl + variable + " = " + pseudo_python_eqv[data_type] + "(input())"
            else:
                o_p = self.indent * self.indent_lvl + variable + " = input('" + operand[0] + "')"
        elif len(operand) == 2:
            data_type = operand[1].split("AS")[1].strip()
            o_p = self.indent * self.indent_lvl + variable + " = " + pseudo_python_eqv[data_type] + "(input('" + operand[0] + "'))"
        return o_p

    def translate_set(self, i_p):
        operand = " ".join(i_p.split()[1:])
        o_p = self.indent * self.indent_lvl + operand
        return o_p

    def translate_call(self, i_p):
        operand = " ".join(i_p.split()[1:])
        o_p = self.indent * self.indent_lvl + operand
        return o_p

    def translate_append(self, i_p):
        operand = " ".join(i_p.split()[1:])
        operand = operand.split("TO")
        operand = [seq.strip() for seq in operand]
        print(operand)
        o_p = self.indent * self.indent_lvl + operand[1] + ".append(" + operand[0] + ")"
        return o_p

    def translate_control(self, i_p, action):
        if action == "BREAK":
            o_p = self.indent * self.indent_lvl + "break"
        elif action == "CONTINUE":
            o_p = self.indent * self.indent_lvl + "continue"
        elif action == "PASS":
            o_p = self.indent * self.indent_lvl + "pass"
        elif action == "RETURN":
            if len(i_p.split()) > 1:
                operand = " ".join(i_p.split()[1:])
                o_p = self.indent * self.indent_lvl + "return " + operand
            else:
                o_p = self.indent * self.indent_lvl + "return"
        return o_p