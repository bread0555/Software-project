class CodeBlock:
    def __init__(self, i_p):
        self.i_p = i_p
        self.o_p = []
        self.keywords = ["IF", "WHILE", "FOR", "TRY"]

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
                        and self.i_p[i].upper().split() == ["END", constructor]
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


blended_demo = [
    "TRY",
    "    OPEN file 'data.txt'",
    "    READ contents",
    "    IF score >= 90 THEN",
    "        PRINT 'Grade: A'",
    "    ELSE IF score >= 80 THEN",
    "        PRINT 'Grade: B'",
    "    ELSE",
    "        PRINT 'Grade: C'",
    "    END IF",
    "EXCEPT FileNotFoundError",
    "    PRINT 'File not found.'",
    "EXCEPT PermissionError",
    "    PRINT 'Permission denied.'",
    "ELSE",
    "    PRINT 'File read successfully.'",
    "FINALLY",
    "    CLOSE file",
    "END TRY"
]





c = CodeBlock(blended_demo)
c.analyse()
print(c.o_p)