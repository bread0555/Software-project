from p2p import CodeBlock

files = ["test_files/assignment_arithmetic.txt", "test_files/edge.txt", "test_files/for.txt", "test_files/function.txt", "test_files/if_else.txt", "test_files/list.txt", "test_files/nested_if.txt", "test_files/operators.txt", "test_files/repeat_while.txt", "test_files/try_except.txt", "test_files/while.txt"]

for i in files:
    with open(i, "r") as f:
        i_p = f.readlines()
    i_p = [line.strip("\n") for line in i_p]
    c = CodeBlock(i_p)
    c.analyse()
    print(c.o_p)
print("success")