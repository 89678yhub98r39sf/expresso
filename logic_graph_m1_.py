from expr_tree_ import *
from collections import defaultdict

class RestrictionMap:

    def __init__(self, name = None):
        self.name = None
        self.restrictions = defaultdict(set)

    """
    description:
    - adds a restriction.

    arguments:
    - s := int, source
    - t := int, target
    """
    def add_restriction(self, s, t):
        self.restrictions[s].add(t)

    def remove_restriction(self, s, t):
        self.restrictions[s].remove(t)

    def is_restricted(self, s, t):
        return True if t in self.restrictions[s] else False

"""
description:
- A SimpleLogicMap
"""
class SimpleLogicMap:

    medianFinder = re.compile("->")

    def __init__(self):
        # key is integer, value is list of integers;
        # integers correspond to hashed identifiers for expression
        self.contents = defaultdict(list)
        self.indexia = 0
        # key is integer,
        # value is (string representation of expression, ExprTreeNode)
        self.hash = defaultdict(None)

    """
    description:
    -
    """
    def reverse_lookup_expression(self, expString):
        for k, v in self.hash.items():
            if v[0] == expString: return k
        return -1

    def fetch_hash(self, indexia):
        return self.hash[indexia]

    """
    description:
    -
    """
    @staticmethod
    def parse_implication(implication):
        ##print("IMPLICATION:\t", implication)
        searched = SimpleLogicMap.medianFinder.search(implication)
        assert searched != None, "implication must contain ?Arrows"

        start, end = searched.span()
        left, right = implication[:start], implication[end+1:]
        return left, right

    def expression_exists(self, expression):
        for k, v in self.hash.items():
            if v[0] == expression:
                return k
        return -1

    def log_implication(self, lickt, royt):

        def process_it(trianco):
            indices = []
            for v in trianco.possibleDecisions.values():
                v_ = ExprTree.traversal_display(v, "partial")
                exists = self.expression_exists(v_)

                if exists == -1:
                    self.hash[self.indexia] = (v_, v)
                    indices.append(self.indexia)
                    self.indexia += 1
                else:
                    indices.append(exists)

            return indices

        iLeft = process_it(lickt)
        iRight = process_it(royt)

        for x in iLeft:
            self.contents[x].extend(iRight)

    def add_implication(self, implication):
        # parse implication and log its left and right data
        ##print("PROCESSING: {}".format(implication))
        left, right = SimpleLogicMap.parse_implication(implication)
        lickt, royt = ExprTree(left), ExprTree(right)

        lickt.process()
        royt.process()

        self.log_implication(lickt, royt)

    def add_implication_set(self, impSet):
        for x in impSet:
            self.add_implication(x)

    """
    arguments:
    - truthMap := defaultdict(list)
    """
    def get_qualifying_sources(self, truthMap):
        sources = []
        for k, v in self.hash.items():
            eval = self.evaluate_decision_absolute_truth(v[1], truthMap)
            if eval:
                sources.append(k)
        return sources

    @staticmethod
    def compare_required_truth_with_option(requiredTruth, option, toConsider = set()):
        considerAll = True if len(toConsider) == 0 else False
        contr = []

        def compare(k, v):
            q = requiredTruth[k]
            if q == []:
                return

            if q != v:
                contr.append(k)

        for k, v in option.items():

            if considerAll:
                compare(k, v)
            else:
                if k in toConsider:
                    compare(k, v)

        return contr

    # TODO: code case in which |typeTarget[1]| > 0
    """
    description:
    - given an expression, finds a valid implication for it based on `truthMap`,
        `prohibitedImplications`, and `typeTarget`.

    arguments:
    - sourceHash := int, hash identifier for expression.
    - truthMap := dict(str->bool)
    - prohibitedImplications := set(int), expressions that are prohibited from being implied
    - typeTarget := [0] lc(least contradiction)|nc(no contradiction)
                    [1] set(operands): operands to consider, if set is empty,
                                       then will consider alll operands
    """
    def choose_best_implication(self, sourceHash, truthMap, prohibitedImplications, typeTarget = ("lc", set())):

        q = self.contents[sourceHash]
        q = set(q) - prohibitedImplications

        """
        description:
        - given a generator of options, considers the one that results in the best
          score (if)
        """
        def consider_best_option(genOpt):
            bestOption = None
            bestScore = float("inf")

            for opt in genOpt:
                d = ExprTree.option_tree_to_dict(opt)
                cont = SimpleLogicMap.compare_required_truth_with_option(truthMap, d, toConsider = set())

                if typeTarget[0] == "lc":
                    if len(cont) < bestScore:
                        bestScore = len(cont)
                        bestOption = d

                else:
                    # random choice
                    if len(cont) == 0:
                        if bestOption == None: bestOption = d
                        else:
                            prefer = True if random.random() > 0.5 else False
                            if prefer:
                                bestOption = d

            return bestOption, bestScore

        # iterate through each implication
        bo, bs = None, float("inf")
        for q_ in q:
            if q_ in prohibitedImplications: continue

            impl = self.hash[q_]
            nodo = impl[1]

            # convert the decision to a choice
            choice = ExprTree.decision_to_choice(nodo)
            options = ExprTree.choice_tree_to_options(choice, output = "gen")
            bo_, bs_ = consider_best_option(options)

            if typeTarget[0] == "nc":
                if bo_ == None: continue
                return bo_
            else:
                if bo_ == None: continue
                if bs_ < bs:
                    bo, bs = bo_, bs_

        return bo

    # TODO
    """
    description:
    - conducts choice based on criteria `typeChoice`

    arguments:
    - choice :=
    - truthMap :=
    - truthChoice := lc(least contradiction)|nc(no contradiction)

    return:
    - dict(key-> > 0 contradictions), ExprTreeNode (choice)
    """
    def make_choice(self, choice, truthMap, typeChoice = "lc"):
        return -1

    def __str__(self):
        s = ""
        for k, v in self.contents.items():
            s += "* SOURCE:\t{}".format(self.hash[k][0])
            s += "\n* TARGETS:\n"
            for v_ in v:
                s += "\t{}\n".format(self.hash[v_][0])
            s += "\n\n"
            s += "--------------------------\n"
        return s


"""
description:

This class provides a representation of Logic.
This representation of Logic does not consider the | operator.
It does consider the & and ! operators as nodes.

If an AND expression is NOT'ed, then its operand nodes will be connected
by a NOT node.

If the AND expression is not NOT'ed, then its operand nodes will instead be
connected by an AND node.
"""
class LogicGraphM1:

    def __init__(self):
        self.slm = SimpleLogicMap()
        self.rm = RestrictionMap()

    def load_implication_set(self, impSet):
        self.slm.add_implication_set(impSet)

    def get_next_in_chain(self, source):
        return -1

    """
    description:
    - adds an element identified by `contentIndex`
    """
    def add_to_chain(self, hashIndex, truthMap, addType="nocon"):
        assert addType in {"nocon", "confee"}, "invalid addType {}".format(addType)

        if addType == "confee":
            raise ValueError("confee mode not yet implemented.")

        # check if qualifies
        hash = self.slm.fetch_hash(contentIndex)
        if hash == None:
            return
        else:
            stringRepr, tree = hash

        involvedNodes = ExprTree.get_involved_nodes(tree)

    """
    description:

    """
    def add_involved_nodes_to_chain_data(self, involvedNodes, truthMap, addType = "nocon"):

        for s in involvedNodes:
            return -1

        return -1

    def get_source(self, sourceMap, typeSource = ""):
        return -1

    def analyze_target_from_source(self, sourceHash):
        return -1

    """

    chain does not allow for contradiction.
    """
    def get_random_implication_chain(self, source, excluded, chain, chainType = "full"):

        includedNodes = set()
        activatedNodes = {}

        def initialize_chain():
            possibleSources = self.slm.get_qualifying_sources(source)

            if len(sources) == 0:
                return -1

            q = random.choice(possibleSources)
            return q

        if len(chain) == 0:
            q = initialize_chain()
            if q == -1:
                return chain
            chain.append(q)
            activatedNodes = deepcopy(source)
        else:
            return -1
        return -1

    def initialize_chain():
        return -1 

    def get_one_implication_chain(self, source, restrictions):
        return -1

    def get_all_implication_chains(self, source):

        return -1
