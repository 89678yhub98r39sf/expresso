from test_expressions import *
from expr_tree import *

"""
tests method on lone sample q
"""
def ExprTree__find_inner_chunk_test():

    q = "((A & (B | C)) & (F | E)"
    et = ExprTree(q)

    index = et.find_inner_chunk()
    assert q[index[0]:index[1] + 1] == "(B | C)"

    ## MOVE THIS
    """
    oo = re.compile(OPERATOR_OR_OPERAND)
    x = oo.search(" (!A & B)")
    print("SEARCH RESULT:\t", x)
    """

def ExprTree__find_outer_chunk_test():

    start,end = ExprTree.find_outer_chunk(sample1)
    assert sample1[start:end+1] == "(A & B)"

    start,end = ExprTree.find_outer_chunk(sample2)
    assert sample2[start:end+1] == "(A & (B | C))"

    start,end = ExprTree.find_outer_chunk(sample4)
    assert sample4[start:end+1] == "(((A & B) & (C & D)) | 5)"

    start,end = ExprTree.find_outer_chunk(sample5)
    assert sample5[start:end+1] == "(A & (B | C))"

def ExprTree_parse_test():

    et = ExprTree(sample4)
    x = et.parse()
    y = ExprTree.inorder_traversal_display(x)
    assert y == " A  &  B  &  C  &  D  |  5 "
    ##print("SIZE 4:\t", et.size)

    et = ExprTree(sample5)
    x = et.parse()
    y = ExprTree.inorder_traversal_display(x)
    assert y == " A  &  B  |  C  &  F  |  E "
    ##print("SIZE 5:\t", et.size)


"""
performs further testing of NOT operand
"""
def ExprTree_parse__notop_test():

    et = ExprTree(sample6)
    x = et.parse()
    y = ExprTree.inorder_traversal_display(x)
    assert y == " A  &  B  !  |  C  |  D  &  E "

    et = ExprTree(sample7)
    x = et.parse()
    y = ExprTree.inorder_traversal_display(x)
    assert y == " A  !  &  B "

    et = ExprTree(sample8)
    x = et.parse()
    y = ExprTree.inorder_traversal_display(x)
    assert y == " A  &  B  ! "

    et = ExprTree(sample9)
    x = et.parse()
    y = ExprTree.inorder_traversal_display(x)
    assert y == " A  &  B  !  &  C  ! "

####---------------------------------------------------------------------------------

# TODO: add assertions to this method
def ExprTree__random_decision_printtest():

    et = ExprTree(sample5)
    x = et.parse()

    print("** target tree:\t", ExprTree.inorder_traversal_display(x))
    rd = et.random_decision()
    print("** random decision:\t", rd)

def ExprTree__inorder_traversal_finder_test():

    et = ExprTree(sample12)
    et.process()
    assert len(et.possibleDecisions) == 2, "invalid {}, want {}".format(len(et.possibleDecisions), 4)

    et = ExprTree(sample6)
    et.process()
    assert len(et.possibleDecisions) == 3, "invalid {}, want {}".format(len(et.possibleDecisions), 3)

    answers = {"!(A & B)", "C", "D & E"}

    q = [ExprTree.traversal_display(x, "partial") for x in et.possibleDecisions.values()]

    for q_ in q: assert q_ in answers


def ExprTree__evaluate_decision_absolute_truth():

    # parse sample
    et = ExprTree(sample6)
    x = et.parse()

    # get possible decisions
    et.inorder_decision_finder()

    # iterate through decisions and
    for k, x in et.possibleDecisions.items():
        y = ExprTree.inorder_traversal_display(x)
        result = et.evaluate_decision_absolute_truth(x, sample6__truthtable1)
        assert result == sample6__truthtable1_output[y], "truth table {}: wrong for {}".format("1", y)

def ExprTree__evaluate_decision_absolute_truth_test2():

    def evaluate_etree(e, truthTable):
        results = []
        for k, x in e.possibleDecisions.items():
            y = ExprTree.inorder_traversal_display(x)
            result = et.evaluate_decision_absolute_truth(x, truthtable1)
            results.append(result)
        return results

    et = ExprTree("A & !B & C")
    et.process()
    q = evaluate_etree(et, truthtable1)
    assert q == [True]
    ###
    et = ExprTree("!A & B & C")
    et.process()
    q = evaluate_etree(et, truthtable1)
    assert q == [False]

    et = ExprTree("!(A & B) & C")
    et.process()
    q = evaluate_etree(et, truthtable1)
    assert q == [True]

def ExprTree__traversal_display_test():
    # test sample 6,7,8,9
    et = ExprTree(sample6)
    et.process()
    q = ExprTree.traversal_display(et.parsedEas, "partial")
    assert q == sample6, "want {}, got {}".format(sample6, q)
    ##print("TD s6:\t_" + q + "_")

    et = ExprTree(sample7)
    et.process()
    q = ExprTree.traversal_display(et.parsedEas, "partial")
    assert q == sample7, "want {}, got {}".format(sample7, q)
    ##print("TD s7:\t_" + q + "_")

    et = ExprTree(sample8)
    et.process()
    q = ExprTree.traversal_display(et.parsedEas, "partial")
    assert q == sample8, "want {}, got {}".format(sample8, q)
    ##print("TD s8:\t_" + q + "_")

    et = ExprTree(sample9)
    et.process()
    q = ExprTree.traversal_display(et.parsedEas, "partial")
    assert q == sample9, "want {}, got {}".format(sample9, q)
    ##print("TD s9:\t_" + q + "_")

def ExprTree__get_binary_permutations_test():
    sequenceSize = 5
    sequenceElements = ["l", "r"]

    allSequences = ExprTree.get_binary_permutations(sequenceSize, sequenceElements)

    q = list(allSequences)
    assert len(q) == 2 ** 5, "number of sequences {} does not match {}".format(len(q), 2**5)

# TODO: this method needs further testing.
"""
this method does not have assertions. Requires human manual check.
"""
def ExprTree__decision_to_choice_printtest(verbose = False):

    e = ExprTree(sample_sat1)
    e.process()
    x = e.parsedEas
    q = ExprTree.decision_to_choice(x)
    if verbose:
        print("SAMPLE1")
        print(ExprTree.traversal_display(q))

    e = ExprTree(sample_sat2)
    e.process()
    x = e.parsedEas
    q = ExprTree.decision_to_choice(x)
    if verbose:
        print("SAMPLE2")
        print(ExprTree.traversal_display(q))

    return

def ExprTree__choice_tree_to_options():

    # create the choice tree
    e = ExprTree(sample_sat2)
    e.process()
    x = e.parsedEas

    q = ExprTree.decision_to_choice(x)
    q2 = ExprTree.choice_tree_to_options(q)
    assert len(q2) == 6, "invalid number of options, want {}, got {}".format(6, len(q2))

def ExprTree__make_copy_at_or_test():

    e = ExprTree(sample6)
    e.process()
    q1, q2 = ExprTree.make_copy_at_or(e.parsedEas)
    q1_ = ExprTree.traversal_display(q1, "partial")
    q2_ = ExprTree.traversal_display(q2, "partial")
    assert q1_ == "!(A & B)"
    assert q2_ == "C | (D & E)"

    e = ExprTree(sample1)
    e.process()
    q = e.find_all_matching_nodes("|", 1)
    n = e.locate_node_by_index(q[0])
    q1, q2 = ExprTree.make_copy_at_or(n)
    q1 = ExprTree.rewind_to_root_(q1)
    q2 = ExprTree.rewind_to_root_(q2)
    q1_ = ExprTree.traversal_display(q1, "partial")
    q2_ = ExprTree.traversal_display(q2, "partial")
    assert q1_ == "(A & B) & F"
    assert q2_ == "(A & B) & E"

def ExprTree___is_syntactical_test():
    e = ExprTree(syntact1)
    e.process()
    assert e.parsedEas != False

    e = ExprTree(nonsyntact2)
    e.process()
    assert e.parsedEas == False

    e = ExprTree("&")
    e.process()
    assert e.parsedEas == False    

if __name__ == "__main__":

    print("* Find inner chunk test")
    ExprTree__find_inner_chunk_test()
    print()

    print("* Find outer chunk test")
    ExprTree__find_outer_chunk_test()
    print()


    print("* Parse test")
    ExprTree_parse_test()
    print()

    print("* Not operator test")
    ExprTree_parse__notop_test()
    print()

    print("* Random decision print-test")
    ExprTree__random_decision_printtest()
    print()

    print("* Inorder traversal finder")
    ExprTree__inorder_traversal_finder_test()
    print()

    print("* Decision finder")
    ExprTree__inorder_traversal_finder_test()
    print()

    print("* Evaluate decision absolute truth ")
    ExprTree__evaluate_decision_absolute_truth()
    print()

    print("* Evaluate decision absolute truth 2")
    ExprTree__evaluate_decision_absolute_truth_test2()
    print()

    print("* Traversal display test")
    ExprTree__traversal_display_test()
    print()

    print("* Get binary permutations test")
    ExprTree__get_binary_permutations_test()
    print()

    print("* Decision to choice print-test")
    ExprTree__decision_to_choice_printtest(verbose = True)
    print()

    print("* Choice tree to options")
    ExprTree__choice_tree_to_options()
    print()

    print("* Make copy at or test")
    ExprTree__make_copy_at_or_test()
    print()

    print("** Is Syntactical")
    ExprTree___is_syntactical_test()
    print()
