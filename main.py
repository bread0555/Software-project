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

    def if_constructor(self, i_p):
        o_p = []
        i = 0
        while i < len(i_p):
            constructor = i_p[i].upper().split()[0]
            if constructor == "IF" or constructor == "ELIF":
                line = i_p[i].split()
                for j in range(len(line)):
                    if line[j] == "AND":
                        line[j] = "and"
                    if line[j] == "OR":
                        line[j] = "or"
            if constructor == "END":
                break
            elif constructor == "IF":
                o_p.append(self.indent * self.indent_lvl + "if " + " ".join(line[1:-1]) + ":")
            elif constructor == "ELIF":
                o_p.append(self.indent * self.indent_lvl + "elif " + " ".join(line[1:-1]) + ":")
            elif constructor == "ELSE":
                o_p.append(self.indent * self.indent_lvl + "else:")
            else:
                start = i
                while i < len(i_p):
                    if (
                        i_p[i].startswith(self.indent * self.indent_lvl)
                        and not i_p[i].startswith(self.indent * (self.indent_lvl + 1))
                    ):
                        end = i
                        break
                    i += 1
                c = CodeBlock(i_p[start:end+1])
                c.analyse()
                o_p += c.o_p
            i += 1
        return o_p

a = [
    "IF mode == 'admin' THEN",
    "    PRINT 'Admin access granted.'",
    "    enable_admin_panel()",
    "END IF",

    "IF user_age < 18 THEN",
    "    PRINT 'Access to restricted content denied.'",
    "END IF",

    "IF is_logged_in == FALSE THEN",
    "    PRINT 'Please log in to continue.'",
    "END IF",

    "PRINT 'Initial checks complete.'"
]

c = CodeBlock(a)
c.analyse()
print(c.o_p)