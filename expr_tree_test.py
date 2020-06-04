from test_expressions import *
from expr_tree_ import *

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
    ##print("sample6:\t", y)

    et = ExprTree(sample7)
    x = et.parse()
    y = ExprTree.inorder_traversal_display(x)
    assert y == " A  !  &  B "
    ##print("sample7:\t", y)

    et = ExprTree(sample8)
    x = et.parse()
    y = ExprTree.inorder_traversal_display(x)
    assert y == " A  &  B  ! "
    ##print("sample8:\t", y)

    et = ExprTree(sample9)
    x = et.parse()
    y = ExprTree.inorder_traversal_display(x)
    assert y == " A  &  B  !  &  C  ! "
    ##print("sample9:\t", y)
    # y: A  &  B  !  &  C  !

    # use for thorough inspection
    """
    et.label_nodes_with_index()
    y = ExprTree.inorder_traversal_display(x, "full")
    print("HERE:\t", y)

    indices = et.find_all_matching_nodes("!")
    for i in indices:
        ##print("INDEX:\t", i)
        node = et.locate_node_by_index(i)
        ##print("LOCATED NODE:\t", node)

        lv = node.left.val if node.left != None else "NONE"
        rv = node.right.val if node.right != None else "NONE"
        print("VAL:\t{}L:\t{}\tR:\t{}".format(node.val, lv, rv))
    """

####---------------------------------------------------------------------------------

# TODO: add assertions to this method
def ExprTree__random_decision_printtest():

    et = ExprTree(sample5)
    x = et.parse()

    print("** target tree:\t", ExprTree.inorder_traversal_display(x))
    rd = et.random_decision()
    print("** random decision:\t", rd)

# TODO: add assertions to this method
def ExprTree__inorder_traversal_finder_test():
    """
    et = ExprTree(sample6)
    x = et.parse()

    et.inorder_decision_finder()

    Y = list(ExprTree.inorder_traversal_display(x) for x in et.possibleDecisions.values())

    #### TODO : uncomment below for assertions
    assert len(et.possibleDecisions) == 3, "want {} decisions, got {} instead".format(4, len(et.possibleDecisions))
    assert " A  &  B  ! " in Y, "missing ( A  &  B  ! )"
    assert " C " in Y, "missing ( Y )"
    assert " D  &  E " in Y, "missing ( D  &  E )"
    ####-----------------------------------------
    for k, x in et.possibleDecisions.items():
        print("tree [{}]:\t{}".format(k, ExprTree.inorder_traversal_display(x)))
    """

    print("** SAMPLE i9-right")
    i9Right = "(D & !E) | (E & !F)"
    et = ExprTree(i9Right)
    x = et.parse()

    q = ExprTree.inorder_traversal_display(x)# traversal_display(x)
    print("**\t{}".format(q))
    """
    et.inorder_decision_finder()
    for k, x in et.possibleDecisions.items():
        print("tree [{}]:\t{}".format(k, ExprTree.inorder_traversal_display(x)))
    """



##i9 = "A & B | C -> (D & !E) | (E & !F)"

def ExprTree__evaluate_decision_absolute_truth():

    # parse sample
    et = ExprTree(sample6)
    x = et.parse()

    # get possible decisions
    et.inorder_decision_finder()

    ##print("RESULT HERE:\t", sample6__truthtable1["A"])

    # iterate through decisions and
    #### DELETE BELOW
    for k, x in et.possibleDecisions.items():
        y = ExprTree.inorder_traversal_display(x)
        result = et.evaluate_decision_absolute_truth(x, sample6__truthtable1)
        ##print("tree [{}]:\t{}".format(k, y))
        ##print("truth value:\t", result)
        assert result == sample6__truthtable1_output[y], "truth table {}: wrong for {}".format("1", y)
        ##print("------------------------------------")
    return

def ExprTree__evaluate_decision_absolute_truth_test2():

    def evaluate_etree(e, truthTable):
        results = []
        for k, x in e.possibleDecisions.items():
            y = ExprTree.inorder_traversal_display(x)
            result = et.evaluate_decision_absolute_truth(x, implicationSet3__truthtable1)
            ##print("tree [{}]:\t{}".format(k, y))
            ##print("truth value:\t", result)
            results.append(result)
        return results

    print("** ExprTree__evaluate_decision_absolute_truth_test2 **")

    et = ExprTree("A & !B & C")
    et.process()
    q = evaluate_etree(et, implicationSet3__truthtable1)
    assert q == [True]
    ###
    et = ExprTree("!A & B & C")
    et.process()
    q = evaluate_etree(et, implicationSet3__truthtable1)
    assert q == [False]

    et = ExprTree("!(A & B) & C")
    et.process()
    q = evaluate_etree(et, implicationSet3__truthtable1)
    assert q == [True]


    ###
    """
    q = ExprTree.inorder_traversal_display(et.parsedEas)
    print("HERE:\t", q)

    print(et.possibleDecisions)
    print("#####")

    for k, x in et.possibleDecisions.items():
        y = ExprTree.inorder_traversal_display(x)
        print("tree [{}]:\t{}".format(k, y))
    """
    ###
    ##------------------------------------

    # get possible decisions
    ##et.inorder_decision_finder()
    ##et.process()
    return -1

def ExprTree__traversal_display_test():
    # test sample 6,7,8,9
    et = ExprTree(sample6)
    et.process()
    q = ExprTree.traversal_display(et.parsedEas)
    assert q == sample6, "want {}, got {}".format(sample6, q)
    ##print("TD s6:\t_" + q + "_")

    et = ExprTree(sample7)
    et.process()
    q = ExprTree.traversal_display(et.parsedEas)
    assert q == sample7, "want {}, got {}".format(sample7, q)
    ##print("TD s7:\t_" + q + "_")

    et = ExprTree(sample8)
    et.process()
    q = ExprTree.traversal_display(et.parsedEas)
    assert q == sample8, "want {}, got {}".format(sample8, q)
    ##print("TD s8:\t_" + q + "_")

    et = ExprTree(sample9)
    et.process()
    q = ExprTree.traversal_display(et.parsedEas)
    assert q == sample9, "want {}, got {}".format(sample9, q)
    ##print("TD s9:\t_" + q + "_")

def ExprTree__get_binary_permutations_test():
    sequenceSize = 5
    sequenceElements = ["l", "r"]

    allSequences = ExprTree.get_binary_permutations(sequenceSize, sequenceElements)

    q = list(allSequences)
    assert len(q) == 2 ** 5, "number of sequences {} does not match {}".format(len(q), 2**5)
    ##for s in allSequences: print(s)

def ExprTree__get_possible_solutions_for_decision():


    e = ExprTree(sample_sat2)
    e.process()
    x = e.parsedEas

    """
    print("ROOT INDEX:\t", x.index)


    print("LEFT PAR:\t", x.left.parent)
    print("RIGHT PAR:\t", x.right.parent)

    e.assign_parents(x)
    print("LEFT PAR:\t", x.left.parent)
    print("RIGHT PAR:\t", x.right.parent)
    """

    q = ExprTree.traversal_display(e.parsedEas, "partial")

    print("DISPLAYING 1")
    print(q)

    i = e.find_all_matching_nodes("!", 1)
    print("INDEX")
    print(i)

    l = e.locate_node_by_index(i[0])
    q = ExprTree.traversal_display(l, "partial")
    print("DISPLAYING 2")
    print(q)

    """
    l_ = l.parent
    q = ExprTree.traversal_display(l_, "partial")
    print("DISPLAYING 3")
    print(q)

    l_ = l_.parent
    q = ExprTree.traversal_display(l_, "partial")
    print("DISPLAYING 3")
    print(q)

    return
    """

    """
    # try rewinding back
    print("PARENT:\t", l.parent)

    l = ExprTree.rewind_to_root_(l)
    q = ExprTree.inorder_traversal_display(l, "full")
    print("DISPLAYING 3")
    print(q)

    print("FINDING ROOT")
    l = e.locate_node_by_index(x.index)
    q = ExprTree.inorder_traversal_display(l, "full")
    print(q)
    """

    x, r = e.split_tree_at_node(l)

    print("NEW")
    q = ExprTree.traversal_display(x, "partial")
    print(q)
    print("REM")
    r = ExprTree.rewind_to_root_(r)
    q = ExprTree.traversal_display(r, "partial")
    print(q)
    print("PAR")
    print(r.parent)

    return

    return -1


    s, s2 = ExprTree.get_possible_solutions_for_decision(sample_sat2, defaultdict(list))

    print("TARGET")
    print(ExprTree.traversal_display(s))

    print("REMAINDER")
    print(ExprTree.traversal_display(s2))

    print("PARENTO")
    print(s2.parent)
    return

    s2 = ExprTree.rewind_to_root_(s2)
    print("REMAINDER 2")
    print(ExprTree.traversal_display(s2))

    return


# TODO: this method needs further testing.
"""
this method does not have assertions. Requires human manual check.
"""
def ExprTree__decision_to_choice_test(verbose = False):

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

    """
    print("R")
    ExprTree.test_display(q)
    """
    return

def ExprTree__choice_tree_to_options():

    # create the choice tree
    e = ExprTree(sample_sat2)
    e.process()
    x = e.parsedEas
    q = ExprTree.decision_to_choice(x)

    ExprTree.assign_parents(q)
    q2 = ExprTree.choice_tree_to_options(q)
    """
    print("CHOICE")
    print(ExprTree.traversal_display(q, "partial"))

    for q2_ in q2:
        q2s = ExprTree.traversal_display(q2_, "truth")
        print("OPTION:\t", q2s)
    """
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

########################################
# TODO : delete this test below
"""
def ExprTree_sample6_test():

    et = ExprTree(sample6)
    x = et.parse()

    et.label_nodes_with_index()

    y = ExprTree.inorder_traversal_display(x, "full")
    print("HERE:\t", y)
    # get all or's
    orIndices = et.find_all_matching_nodes("|")

    print("OR INDICES:\t", orIndices)
    return -1

print("**Sample 6**")
ExprTree_sample6_test()
"""
########################################


"""
ExprTree__find_inner_chunk_test()
ExprTree__find_outer_chunk_test()
ExprTree_parse_test()
"""
ExprTree_parse__notop_test()

print("**Decision finder**")
ExprTree__inorder_traversal_finder_test()

####
"""
print("**Possible solutions for decision")
ExprTree__get_possible_solutions_for_decision()
"""
####

print("**Decision to choice")
ExprTree__decision_to_choice_test(True)

print("**Make copy")
ExprTree__make_copy_at_or_test()

#

print("*Choice to options*")
ExprTree__choice_tree_to_options()

#

###
"""
print("Evaluate decision absolute truth")
ExprTree__evaluate_decision_absolute_truth()

ExprTree__evaluate_decision_absolute_truth_test2()

print("**Traversal display test**")
ExprTree__traversal_display_test()
"""
###

"""
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
ExprTree__evaluate_decision_absolute_truth()

ExprTree__get_binary_permutations_test()
"""


# TODO :
# parse decision from tree
# implement graph logic
