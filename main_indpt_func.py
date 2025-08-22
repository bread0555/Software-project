indent_lvl = 1
indent = "    "
keywords = ["IF", "WHILE", "FOR", "TRY"]


def analyse(i_p):
    i = 0
    i_p[:] = [line for line in i_p if line.strip()]
    while i < len(i_p):
        if (i_p[i].startswith(indent * indent_lvl)
                and not i_p[i].startswith(indent * (indent_lvl + 1))
                and i_p[i].upper().split()[0] not in keywords):
            i += 1
        else:
            start = i
            ctrl_struc = i_p[i].upper().split()[0]
            while i < len(i_p):
                if (i_p[i].startswith(indent * (indent_lvl))
                        and i_p[i].upper().split() == ["END", ctrl_struc]):
                    end = i + 1
                    break
                i += 1
            translator(ctrl_struc, i_p[start:end])
            i += 1
