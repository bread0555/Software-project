from p2p import CodeBlock
import os

path = "test_files"

for filename in os.listdir(path):
    try:
        with open(os.path.join(path, filename), "r") as f:
            i_p = f.readlines()
        i_p = [line.strip("\n") for line in i_p]
        c = CodeBlock(i_p)
        c.analyse()
        print(c.o_p)
        print(filename + " passed successfully")
    except Exception as e:
        print("Error in file: " + filename)
        print("Error details: ", e)