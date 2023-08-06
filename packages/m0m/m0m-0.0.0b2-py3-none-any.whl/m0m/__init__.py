import json
import os

def present(phrase):

    phrase = str(phrase).replace("?", "!")
    words = phrase.replace("'", " '")
    words = str(words).split(" ")

    file_path = str(os.path.realpath(__file__)).replace("__init__.py", "verbs.json")

    with open(file_path, "r") as file:
        data = json.load(file)
    
    try:
        parts = []
        for block in data:
            for phrase_word in words:
                if phrase_word in data[f"{block}"]:
                    parts = str(phrase).split(phrase_word)
                    part_num = len(parts)-1

                    print(f"Your mom {data[block][2]}{parts[part_num]}")

                    # if(str(block).endswith("uy")):
                    #     print(f"{str(block)}s")
                    # elif(str(block).endswith("y")):
                    #     print(str(block).replace("y", "ies"))
                    # elif(str(block).endswith("o")):
                    #     print(str(block).join("es"))
                    # else:
                    #     print(f"{str(block)}s")

    except KeyError:
        print("Verb is not in list.")
        