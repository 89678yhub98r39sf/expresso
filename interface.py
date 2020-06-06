from expr_tree import *

def whilus_loopus():

    while True:

        q = input("Input your boolean string:\t")
        e = ExprTree(q)
        e.process()
        if e.parsedEas == False:
            print("Invalid string")
            continue

        while True:
            c = input("Want Possible decisions? pd\t")

            if c.lower() != "pd":
                print("you want no decide then. bye.\n" * 100)
                print("\n\n")
                break

            for k, v in e.possibleDecisions.items():
                print("number {}\n{}\n".format(k, ExprTree.traversal_display(v, "partial")))

            q = None
            while True:
                try:
                    q = int(input("* select the decision by number\n* of your interest, and you will receive choices:\t"))
                    break
                except:
                    print("invalid number {}".format(q))

            q = e.possibleDecisions[q]
            q2 = ExprTree.decision_to_choice(q)
            print("* Choice is :\n{}\n".format(ExprTree.traversal_display(q2)))




def main():
    print("iqop program parses input boolean expression string")
    whilus_loopus()

if __name__ == "__main__":
    main()
