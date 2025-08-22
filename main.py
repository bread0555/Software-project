class CodeBlock:
    def __init__(self, i_p):
        self.i_p = i_p
        self.o_p = []
        self.keywords = ["IF", "WHILE", "FOR", "TRY", "CASE", "REPEAT"]

    def tab_to_spaces(self):
        for i in range(len(self.i_p)):
            if "\t" in self.i_p[i]:
                self.i_p[i] = self.i_p[i].replace("\t", "    ")

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
        self.indent_lvl = (len(self.i_p[0]) - len(self.i_p[0].lstrip(" "))) // self.indent
        self.indent = " " * self.indent

    def analyse(self):
        self.tab_to_spaces()
        self.check_indents()
        i = 0
        self.i_p[:] = [line for line in self.i_p if line.strip()]
        while i < len(self.i_p):
            if (
                self.i_p[i].startswith(self.indent * self.indent_lvl)
                and not self.i_p[i].startswith(self.indent * (self.indent_lvl + 1))
                and self.i_p[i].upper().split()[0] not in self.keywords
            ):
                self.o_p.append(self.i_p[i])
                i += 1
            else:
                start = i
                constructor = self.i_p[i].upper().split()[0]
                while i < len(self.i_p):
                    if (
                        self.i_p[i].startswith(self.indent * self.indent_lvl)
                        and not self.i_p[i].startswith(self.indent * (self.indent_lvl + 1))
                        and (self.i_p[i].upper().split() == ["END", constructor]
                             or self.i_p[i].upper().split()[0] == "UNTIL")
                    ):
                        end = i
                        break
                    i += 1
                self.o_p += self.translator(constructor, self.i_p[start:end + 1])
                i += 1
            

    def translator(self, constructor, i_p):
        if constructor == "IF":
            return self.if_constructor(i_p)
        if constructor == "TRY":
            return self.try_constructor(i_p)
        if constructor == "WHILE":
            return self.while_constructor(i_p)
        if constructor == "FOR":
            return self.for_constructor(i_p)
        if constructor == "CASE":
            return self.case_constructor(i_p)
        if constructor == "REPEAT":
            return self.repeat_constructor(i_p)

    def if_constructor(self, i_p):
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
                    o_p.append(self.indent * self.indent_lvl + "if " + " ".join(line[1:]))
                elif constructor == "ELSE" and len(line) > 1:
                    o_p.append(self.indent * self.indent_lvl + "elif " + " ".join(line[2:]))
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
                    if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                        end = i
                        break
                    i += 1
                c = CodeBlock(i_p[start:end])
                c.analyse()
                o_p += c.o_p
        return o_p


    def try_constructor(self, i_p):
        o_p = []
        i = 0
        while i < len(i_p):
            if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                constructor = i_p[i].upper().split()[0]
                line = i_p[i].split()
                if constructor == "TRY":
                    o_p.append(self.indent * self.indent_lvl + "try:")
                elif constructor == "EXCEPT":
                    o_p.append(self.indent * self.indent_lvl + "except " + " ".join(line[1:]) + ":")
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
                    if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                        end = i
                        break
                    i += 1
                c = CodeBlock(i_p[start:end])
                c.analyse()
                o_p += c.o_p
        return o_p


    def while_constructor(self, i_p):
        o_p = []
        i = 0
        while i < len(i_p):
            if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                constructor = i_p[i].upper().split()[0]
                line = i_p[i].split()
                if constructor == "WHILE":
                    o_p.append(self.indent * self.indent_lvl + "while " + " ".join(line[1:]) + ":")
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

    def for_constructor(self, i_p):
        # needs to distinguish between "min, max, step" (will use TO and STEP))
        # if iterating through list, will use "in"
        o_p = []
        i = 0
        while i < len(i_p):
            if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
                constructor = i_p[i].upper().split()[0]
                line = i_p[i].split()
                if constructor == "FOR":
                    # more logic needed here to build the for loop
                    o_p.append(self.indent * self.indent_lvl + "for " + " ".join(line[1:]) + ":")
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

    def case_constructor(self, i_p):
        pass

    def repeat_constructor(self, i_p):
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


a = [
    'REPEAT',
    '    PRINT "Enter your password:"',
    '    INPUT password',
    '    PRINT "Checking password..."',
    '    IF password == "hint" THEN',
    '        PRINT "That was a hint, not the actual password."',
    '    END IF',
    'UNTIL password == "secret"'
]


c = CodeBlock(a)
c.analyse()
print(c.o_p)


# use to put back in the indented code into the thingy
# start = i
# while i < len(i_p):
#     if not i_p[i].startswith(self.indent * (self.indent_lvl + 1)):
#         end = i
#         break
#     i += 1
# c = CodeBlock(i_p[start:end])
# c.analyse()
# o_p += c.o_p