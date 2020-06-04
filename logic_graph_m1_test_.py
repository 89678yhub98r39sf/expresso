from logic_graph_m1_ import *
from test_expressions import *

def SimpleLogicMap__add_implication_set_test():

    slm = SimpleLogicMap()
    slm.add_implication_set(implicationSet4)

    print(slm)

    """
    print("------------------------------")
    print(slm.contents)
    print("------------------------------")
    for k, v in slm.hash.items():
        print("key {} : value {}".format(k, v[0]))
    print(slm.hash)
    """

# TODO : incomplete test. all arguments need to be accounted for. 
def SimpleLogicMap__choose_best_implication_test():

    truthMap1 = defaultdict(list)
    truthMap1["A"] = True
    truthMap1["B"] = True
    truthMap1["D"] = False
    truthMap1["E"] = True

    slm = SimpleLogicMap()
    slm.add_implication_set(implicationSet5)
    print(slm)

    q = slm.reverse_lookup_expression("A & B")
    print("INDEX:\t", q)
    res = slm.choose_best_implication(q, truthMap1, set())
    print("BEST IMP:\t", res)

    truthMap2 = defaultdict(list)
    res = slm.choose_best_implication(q, truthMap2, set())
    print("BEST IMP 2:\t", res)

    q2 = slm.reverse_lookup_expression("(E & F) & !G")
    res = slm.choose_best_implication(q, truthMap1, set([q2]))
    print("BEST IMP 3:\t", res)

    # TODO : make assertion here
    """
BEST IMP:	 {'E': True, 'F': True, 'G': False}
Q:	 2
HERE:	 ('D & !E', <expr_tree_.ExprTreeNode object at 0x7f88c3e57a50>)
Q:	 3
HERE:	 ('(E & F) & !G', <expr_tree_.ExprTreeNode object at 0x7f88c3e5b390>)
Q:	 4
HERE:	 ('!A & B', <expr_tree_.ExprTreeNode object at 0x7f88c3e5ba90>)
BEST IMP 2:	 {'D': True, 'E': False}
Q:	 2
HERE:	 ('D & !E', <expr_tree_.ExprTreeNode object at 0x7f88c3e57a50>)
Q:	 4
HERE:	 ('!A & B', <expr_tree_.ExprTreeNode object at 0x7f88c3e5ba90>)
BEST IMP 3:	 {'A': False, 'B': True}


    """

    return -1



#SimpleLogicMap__add_implication_set_test()
SimpleLogicMap__choose_best_implication_test()
