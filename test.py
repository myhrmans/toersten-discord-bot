import re

def addTodo(itemToAdd):
    outputstring = ""
    try:
        File = open("./README.md", "r+", encoding="UTF-8")
        FileInfo = File.read()
        regexBeforeTodo = r"(.*)(?=## Todo)"
        regexTodo = r"(?=## Todo)(.*)(?=## Commands)"
        regexAfterTodo = r"(?=## Commands)(.*)"
        matchesBeforeTodo = re.search(regexBeforeTodo, FileInfo, re.DOTALL)
        matchesTodo = re.search(regexTodo, FileInfo, re.DOTALL)
        matchesAfterTodo = re.search(regexAfterTodo, FileInfo, re.DOTALL)

        if matchesBeforeTodo or matchesTodo or matchesAfterTodo:
            output = matchesTodo.group().split("\n")
            if not (itemToAdd[0] == " " or itemToAdd[0] == "-"):
                del output[len(output)-2]
                output.insert(len(output)-1, "- " + itemToAdd)
        
            for row in output:
                outputstring = outputstring + row + "\n"
            
        File.seek(0)
        File.write((matchesBeforeTodo.group() + outputstring + matchesAfterTodo.group()))
        File.close()

    except Exception as e:
        #await ctx.channel.send(f"Error: Cant find README.md, contact admins!")
        print(e)


def main():
    addTodo("Test")
    addTodo("TestTest")
    addTodo("TestTestTest")
    addTodo("TestTestTestTest")
    addTodo("TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest")





if __name__ == "__main__":
    main()