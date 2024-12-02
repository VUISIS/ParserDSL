model_text = "model tm of TarParser at \"Tar.4ml\" {\n\
inputData is InputData(\"tarfile\", \"data\", 1024).\n\
initState is State(inputData, INIT, 0, 0).\n"

for pos in range(1024):
    line = "Byte(inputData,%s,%s)." % (1, pos)
    model_text += line + "\n"

model_text += "}"

output_file = "tm.4ml"
with open(output_file, "w") as file:
        file.write(model_text + "\n")