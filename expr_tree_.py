from copy import deepcopy
import re
import random
from collections import OrderedDict

# TODO : not operator not implemented

# no NOT provided
LOGIC_OPERATORS = {"&", "|", "!"}

FIRST_PARENTHESIS_EXP = r"\(.*\)" ##r"\(.*\)(?=(.*\())"
##FIRST_PARENTHESIS_EXP = r"\(.*\)(?=(.*\())"

FIRST_PARENTHESIS_EXP2 = r"(?<=(\())(\(.*\))(?=(.*\())"

##OPERATOR_OR_OPERAND = r"(\w+|[|&])"
##OPERATOR_OR_OPERAND = r"(!?\w+|[|&])"
OPERATOR_OR_OPERAND = r"(\w+|[!|&])"


class ExprTreeNode:

    """
    TODO : index variable not used.
    """
    def __init__(self, val, index = None):
        self.val = val
        self.truth = None
        self.index = index
        self.left, self.right, self.parent = None, None, None

    """
    description:
    - attaches node and returns the root

    arguments:
    - etn := ExprTreeNode, to add to self
    - relativePlacement := (c for child)|(p for parent)

    """
    def attach_node_as(self, etn, relativePlacement):
        assert relativePlacement in {"c", "p"}, "invalid relativePlacement {}".format(relativePlacement)

        if relativePlacement == "c":
            if self.left == None:
                self.left = etn
            elif self.right == None:
                self.right =etn
            else:
                raise ValueError("all children are occupied")
            etn.parent = self

            if etn.val == "!":
                return self.left if self.left == etn else self.right
            return self
        else:
            # special case : !, have to attach to first previous that is either & or |
            q = None
            if self.val == "!":
                while True:
                    q = self.parent
                    if q == None:
                        q = self
                        break
                    if q.val == "&" or q.val == "|":
                        break
            else:
                q = self

            if etn.left == None:
                etn.left = q
            elif etn.right == None:
                etn.right = q
            else:
                raise ValueError("parent's children are occupied")
            self.parent = etn
            return etn

    """
    description:
    ~
    """
    def is_operator(self):
        return True if ExprTree.is_operator(self.val) else False

    def __str__(self):
        return self.val

"""
tree construction is from left-to-right
"""
class ExprTree:

    fpe = re.compile(FIRST_PARENTHESIS_EXP)
    ope = re.compile(OPERATOR_OR_OPERAND)

    nt = None

    def __init__(self, expAsString, dataStorage = "sparse"):
        self.eas = expAsString
        self.chunk = None # current chunk to look at
        self.targetChunk = None
        self.chunkIndices = None

        self.parsedEas = None
        self.extraNode = None

        self.size = 0
        ##self.root = None
        ##self.subtree = None
        ##self.mergeSymbol = None
        ##self.prevSearch = None # operand|operator|block
        self.subtreeAsString = None
        self.possibleDecisions = OrderedDict()
        self.randomDecision = None

        self.loc = None
        self.occupiedIndices = set()

    """
    ATTENTION: this method is used to fix a bug during parsing of string.
            The bug is that the parent variable of some nodes do not get
            properly assigned.
    """
    def assign_parents(self, node):

        def assign(n):
            if n == None: return

            if n.left != None:
                n.left.parent = n
            if n.right != None:
                n.right.parent = n

            assign(n.left)
            assign(n.right)

        assign(node)

    @staticmethod
    def assign_parents(node):

        def assign(n):
            if n == None: return

            if n.left != None:
                n.left.parent = n
            if n.right != None:
                n.right.parent = n

            assign(n.left)
            assign(n.right)

        assign(node)

    """
    description:
    - has the same functionality as itertools.product on 2 elements.

    return:
    - generator, each element is a list of size `sequenceSize`
    """
    @staticmethod
    def get_binary_permutations(sequenceSize, sequenceElements):

        assert len(sequenceElements) == 2, "sequenceElements must be size 2"

        def add_one(sequence):
            if len(sequence) == sequenceSize: yield sequence

            else:
                for x in add_one(sequence + [sequenceElements[0]]):
                    yield x
                for x in add_one(sequence + [sequenceElements[1]]):
                    yield x

        return add_one([])

    # TODO: delete this method.
    def find_inner_chunk(self):
        start, end = -1, -1
        for i, x in enumerate(self.eas):
            if x == "(": start = i
            elif x == ")":
                end = i
                break
        return start, end

    """
    description:
    - finds the indices of the outermost parenthetical chunk that is closest to the beginning
      of the substring.

    arguments:
    - substring := str, string to observe

    return:
    - (int::(start index), int::(end index))
    """
    @staticmethod
    def find_outer_chunk(substring):
        start, end = -1, -1
        inc, inc2 = 0, 0

        for i, x in enumerate(substring):
            if x == "(":
                inc += 1
                if start == -1: start = i

            elif x == ")":
                inc2 += 1

                if inc == inc2:
                    end = i
                    break
        return start, end

    @staticmethod
    def find_all_operands(subtree):
        operands = set()

        def find(node):
            if node == None: return

            if not ExprTree.is_operator(node.val):
                operands.add(node.val)

            find(node.left)
            find(node.right)

        find(subtree)
        return operands

    """
    description:
    ~
    """
    @staticmethod
    def is_operator(s):
        return True if s in LOGIC_OPERATORS else False

    """
    description:
    - finds the next variable in `substring`, outputting the results in a dictionary.

    return:
    - dict := next variable data, with keys `info` and `type`
            `info` is the string variable
            `type` is one of `op` (operator|operand) or `chunk` (parentheses)

    - string := remaining substring
    """
    @staticmethod
    def fetch_next_var(substring):
        firstOp = ExprTree.ope.search(substring)
        if firstOp == None:
            return False, False # indicates finish

        outerIndices = ExprTree.find_outer_chunk(substring)
        firstOpIndex = firstOp.span()[0]

        varData = {}

        # operand/operator comes first
        if firstOpIndex < outerIndices[0] or outerIndices[0] == -1:
            varData["info"] = firstOp.group()
            varData["type"] = "op"
            substring = substring[firstOp.span()[1]:]
        else:
            varData["info"] = substring[outerIndices[0]: outerIndices[1] + 1]
            varData["type"] = "chunk"
            substring = substring[outerIndices[1]:]

        return varData, substring

    """
    description:
    - parses `substring` into an ExprTreeNode
    """
    def parse_into_tree(self, substring, node):

        varData, substring = ExprTree.fetch_next_var(substring)

        # finished parsing
        if varData == False: return node
        firstOp = ExprTree.ope.search(substring)

        if varData["type"] == "op":
            isOperator = ExprTree.is_operator(varData["info"])

            # check if current root is operand
            if node != None:
                isOperand = not ExprTree.is_operator(node.val)
                assert (isOperator and isOperand) or not (isOperator and isOperand), "invalid substring"

            # if operator, make parent else child
            newNode = ExprTreeNode(varData["info"])

            if node == None: node = newNode
            else:
                ##node = node.attach_node_as(newNode, "p" if isOperator and newNode.val != "! else "c")
                if newNode.val == "!":
                    node = node.attach_node_as(newNode, "c")
                    #if node.parent != None:
                    #    node = node.parent
                else:
                    node = node.attach_node_as(newNode, "p" if isOperator else "c")

            self.size += 1

            x = deepcopy(node)
            x = ExprTree.rewind_to_root_(x)
            ##print("CURRENT TREE:\t", ExprTree.traversal_display(x))
            ##print("current val:\t", node.val)

            return self.parse_into_tree(substring, node)
        else:
            info = varData["info"]
            info = info[1:-1]
            x = self.parse_into_tree(info, None)

            x = ExprTree.rewind_to_root_(x)
            if node == None: node = x
            else:
                node = node.attach_node_as(x, "c")

            x = deepcopy(node)
            x = ExprTree.rewind_to_root_(x)
            ##print("CURRENT TREE:\t", ExprTree.traversal_display(x))
            ##print("current val:\t", node.val)
            return self.parse_into_tree(substring, node)

    """
    description:
    - primary method to perform parsing on target string `parsedEas`

    return:
    - ExprTreeNode
    """
    def parse(self):
        self.parsedEas = self.parse_into_tree(self.eas, None)
        self.parsedEas = ExprTree.rewind_to_root_(self.parsedEas)
        self.assign_parents(self.parsedEas)
        return self.parsedEas

    """
    description:
    - constructs a string out of subtree by in-order traversal

    arguments:
    - subtree := ExprTreeNode
    - displayType := partial|full

    return:
    - str, string representation of `subtree`
    """
    @staticmethod
    def inorder_traversal_display(subtree, displayType = "partial"):
        if subtree == None:
            return ""

        if displayType == "partial":
            return ExprTree.inorder_traversal_display(subtree.left, displayType) + " " + subtree.val + " " +\
                ExprTree.inorder_traversal_display(subtree.right, displayType)
        else:
            return ExprTree.inorder_traversal_display(subtree.left, displayType) + " " + subtree.val + ":{}".format(subtree.index) + " " +\
                ExprTree.inorder_traversal_display(subtree.right, displayType)

    """
    arguments:
    - displayType := truth|partial|full
    """
    @staticmethod
    def traversal_display(subtree, displayType = "truth"):
        if subtree == None: return ""

        isOp = ExprTree.is_operator(subtree.val)
        if displayType == "partial":
            val = subtree.val
        elif displayType == "full":
            val = subtree.val + ":[" + str(subtree.index) + "]"
        else:
            if not isOp:
                val = subtree.val + ":[" + str(subtree.truth) + "]"
            else:
                val = subtree.val

        if not isOp: return val

        if subtree.val in {"&", "|"}:
            openLeft, closeLeft = "", " "
            openRight, closeRight = " ", ""

            if subtree.left != None:
                if subtree.left.val in {"&", "|"}:
                    openLeft, closeLeft = "(", ") "

            if subtree.right != None:
                if subtree.right.val in {"&", "|"}:
                    openRight, closeRight = " (", ")"

            return openLeft + ExprTree.traversal_display(subtree.left, displayType) + closeLeft + val +\
                openRight + ExprTree.traversal_display(subtree.right, displayType) + closeRight
        else:
            open, close = "", ""
            if subtree.left != None:
                if subtree.left.val in {"&", "|"}:
                    open, close = "(", ")"
            elif subtree.right != None:
                if subtree.right.val in {"&", "|"}:
                    open, close = "(", ")"

            q = ExprTree.traversal_display(subtree.left if subtree.left != None else subtree.right, displayType)
            return val + open + q + close

    @staticmethod
    def test_display(node):

        def d(node):
            if node == None: return

            print("NODE:\t", node)
            print("NODE PARENT:\t", node.parent)

            d(node.left)
            d(node.right)

        d(node)



    # TODO : delete or incorporate this method
    # iterates through parsed results and outputs a random subexpression
    # that would output True
    """
    description:
    - makes a random decision given `self.parsedEas`
    """
    def random_decision(self):

        def decide_at_point(node):
            if node == None: return ""

            # choose random path
            if node.val == "|":
                if node.left and node.right:
                    direction = "l" if random.random() > 0.5 else "r"

                elif node.left:
                    direction = "l"
                elif node.right:
                    direction = "r"
                else:
                    return ""

                if direction == "l":
                    return decide_at_point(node.left)
                else:
                    return decide_at_point(node.right)

            elif node.val == "&":
                return "(" + decide_at_point(node.left) + ")" + node.val + "(" + decide_at_point(node.right) + ")"
            else:
                return node.val

        if self.parsedEas == None: return
        return decide_at_point(self.parsedEas)

    """
    description:
    - recursively iterates through `easParsed` and labels each node with a
      unique key.
    """
    def label_nodes_with_index(self):

        def label_one(node, maxRange):
            if node == None: return

            label_one(node.left, maxRange)
            label_one(node.right, maxRange)

            while True:
                q = random.randrange(maxRange)
                if q not in self.occupiedIndices:
                    node.index = q
                    break

        maxRange = self.size * 100
        label_one(self.parsedEas, maxRange)

    """
    description:
    - requires that index value for each node is set.
    """
    def is_right_child(self, p, c):
        if p.right == None: return False
        return True if p.right.index == c.index else False

    # recursively iterates through easParsed and for each OR, creates a
    """
    description:
    - traverses through tree by inorder algorithm and finds a possible decision.
    - outputs the decision and a dictionary of key=nodeIdentifier value=choice
        in which each nodeIdentifier belongs to an OR node
    """
    def inorder_decision_finder(self):

        def choose_child(node, direction):
            assert node != None, "node cannot be None!"
            return node.left if direction == "l" else node.right

        """
        have to initialize ExprTree decision at `decisionIndex` before calling
        """
        def construct_new_tree(refNode, refNodeIndex, orKey):

            if refNode == None: return

            if refNode.val == "|":
                # get left or right child
                decision = orKey[refNode.index]
                x = refNode.left if decision == "l" else refNode.right

                # connect child to refNode parent
                p = refNode.parent

                # case : refNode is root
                if p == None:
                    x.parent = None
                    self.possibleDecisions[refNodeIndex] = x
                    refNode = x
                else: # refNode is not root, connect parent to child
                    isRightChild = self.is_right_child(p, refNode)
                    if isRightChild:
                        p.right = x
                    else:
                        p.left = x
                    x.parent = p
                    refNode = x
                construct_new_tree(refNode, refNodeIndex, orKey)
            elif refNode.val == "&":
                construct_new_tree(refNode.left, refNodeIndex, orKey)
                construct_new_tree(refNode.right, refNodeIndex, orKey)

        # label the nodes
        self.label_nodes_with_index()

        # find all nodes with OR keys
        orIndices = self.find_all_matching_nodes("|")
        self.possibleDecisions = OrderedDict()

        # set initial path
        orKey = OrderedDict()
        for x in orIndices:
            orKey[x] = "l"

        # get possible paths
        length = len(orKey)

        if length == 0:
            self.possibleDecisions[0] = deepcopy(self.parsedEas)
            return

        permIterable = ExprTree.get_binary_permutations(length, ["l", "r"])

        # construct a tree for each possible path
        c = 0
        uniqueDecisions = set()
        for x in permIterable:
            # construct the path

            for i, k in enumerate(orKey.keys()):
                orKey[k] = x[i]

            # construct the tree using path info
            refNode = deepcopy(self.parsedEas)
            self.possibleDecisions[c] = refNode
            construct_new_tree(refNode, c, orKey)
            dec = ExprTree.inorder_traversal_display(self.possibleDecisions[c])

            # TODO: possible bug in ascertaining uniqueness of subtree expression.
            if dec in uniqueDecisions:
                del self.possibleDecisions[c]
            else:
                uniqueDecisions.add(dec)
                c += 1


    @staticmethod
    def rewind_to_root_(node):
        if node == None: return None

        while True:
            if node.parent != None:
                node = node.parent
            else:
                break
        return node

    # TODO : below fix
    def rewind_to_root(self, index):
        if self.possibleDecisions[index] == None: return

        while True:
            x = self.possibleDecisions[index].parent
            if x != None:
                self.possibleDecisions[index] = self.possibleDecisions[index].parent
            else:
                break

    """
    description:
    - finds all nodes that have value `nodeVal`
    - NOTE: nodes have to be assigned index values beforehand.

    arguments:
    - nodeVal :=

    return:
    -
    """
    def find_all_matching_nodes(self, nodeVal, limitNumber = -1):

        indices = []
        def find_all_matching_nodes_(node):
            if node == None: return

            if limitNumber != -1 and len(indices) >= limitNumber:
                return

            if node.val == nodeVal: indices.append(node.index)

            find_all_matching_nodes_(node.left)
            find_all_matching_nodes_(node.right)

        find_all_matching_nodes_(self.parsedEas)
        return indices

    def locate_node_by_index(self, index):
        self.loc = None

        def locate(node):
            if node == None:
                return None
            """
            if self.loc != None:
                return
            """

            if node.index == index:
                self.loc = node
                return node

            x = locate(node.left)
            x2 = locate(node.right)
            return x if x != None else x2


        return locate(self.parsedEas)
        #return self.loc

    """
    description:
    - evaluates `decision` based on `truthMap`, and returns either True or False

    arguments:
    - decision := ExprTreeNode, contains decision expression
    - truthMap := dict, preferably a defaultdict in case there are missing keys.
                    Each key is an operand and value a truth value.
                    Undetermined values will usually be empty list [].
    - undet := value, signifies undetermined value
    - undetEval := bool|random, value to assign expression if there exist an
                        undetermined operand in it.

    return:
    - bool
    """
    # TODO : undetEval == random not yet implemented
    def evaluate_decision_absolute_truth(self, decision, truthMap, undet = []):

        def evaluate(node):
            assert node != "|", "node cannot be a |"

            if not ExprTree.is_operator(node.val):
                return truthMap[node.val]
            else:
                if node.val == "&":
                    leftEval = evaluate(node.left)
                    rightEval = evaluate(node.right)
                    if leftEval == undet or rightEval == undet:
                        ##print("jsdflasjdlfsjadlfsajd;lfsjdlfsajkldf")
                        ##return undetEval
                        return undet
                    return leftEval and rightEval
                elif node.val == "!":
                    rest = evaluate(node.left if node.left != None\
                        else node.right)
                    if rest == undet:
                        ##print("LSDJFSLADFJLSADFJLAFJSLADFJSD;LJAFJLSAFLJ;KSDA")
                        ##return undetEval
                        return undet
                    return not rest

        return evaluate(decision)

    # TODO: this
    """
    description:
    - outputs the nodes present in the subtree.

    arguments:
    - outputType := basic|neg
                    basic outputs set<Node>
                    neg outputs dict<Node:Set<Sign=1|-1>>
    """
    @staticmethod
    def get_involved_nodes(subtree, outputType = "basic"):

        involved = set()
        def get_involved(node):
            if node == None:
                return

            if not ExprTree.is_operator(node.val):
                involved.add(node.val)

            get_involved(node.left)
            get_involved(node.right)

        get_involved(subtree)
        return involved

    """
    description:
    -
    """
    @staticmethod
    def get_violation(notSubtree):
        return -1

    def pop_not_subtree():
        return -1

    def split_tree_at_node(self, node):

        q = node.parent

        if q == None:
            return node, None

        isRight = True if q.right == node else False

        if isRight:
            q.right = None
        else:
            q.left = None

        #node.parent = None
        q = ExprTree.rewind_to_root_(q)
        return node, q

    """
    description:
    - given a node with value |, makes a copy of it into two subtrees,
      for the left and right subtrees.
    """
    @staticmethod
    def make_copy_at_or(node):
        assert node.val == "|", "node has improper value {}".format(node)

        nc = deepcopy(node)

        if node.parent != None:
            isRight = True if node.parent.right == node else False
            if isRight:
                node.parent.right = node.left
                node.left.parent = node.parent

                nc.parent.right = nc.right
                nc.right.parent = nc.parent
                return node.parent.right, nc.parent.right

            else:
                node.parent.left = node.left
                node.left.parent = node.parent

                nc.parent.left = nc.right
                nc.right.parent = nc.parent
                return node.parent.left, nc.parent.left

        else:
            node.left.parent = None
            node = node.left

            nc.right.parent = None
            nc = nc.right
            return node, nc

    """
    description:
    - converts a choice, defined as a ExprTreeNode representing an expression
      with | operators that denote possible truth assignments to operands that
      satisfy the expression, into
      a list of ExprTreeNode, each representing an expression with only & operators
      in it.

    arguments:
    - choice := ExprTreeNode
    - output := list|gen
    """
    @staticmethod
    def choice_tree_to_options(choice, output = "list"):
        assert output in {"list", "gen"}
        options = []
        options.append(deepcopy(choice))

        def process_one_choice(node, index):
            # locate |
            e = ExprTree("")
            e.parsedEas = node

            q = e.find_all_matching_nodes("|", 1)
            if len(q) == 0:
                return False
            else:
                node = e.locate_node_by_index(q[0])

                # make copy
                node, nc = ExprTree.make_copy_at_or(node)
                node = ExprTree.rewind_to_root_(node)
                nc = ExprTree.rewind_to_root_(nc)

                options[index] = node
                options.append(nc)
                return True

        c = 0
        while True:
            q_ = False
            for (i,q) in enumerate(options):
                result = process_one_choice(q, i)
                # still active
                if result:
                    q_ = True
                    break
                c += 1

            if q_ == False:
                break

        if output == "list":
            return options
        else:
            for o in options: yield o

    @staticmethod
    def option_tree_to_dict(optionTree):
        d = {}
        def convert(n):
            if n == None: return

            if not ExprTree.is_operator(n.val):
                assert n.val not in d, "operand {} is present more than twice, not an option!"
                d[n.val] = n.truth
            else:
                assert n.val not in {"|", "!"}, "argument is not an option!"

            convert(n.left)
            convert(n.right)
            
        convert(optionTree)
        return d

    """
    description:
    - given a decision in the form of an ExprTreeNode, converts it into a choice,
      defined as a tree with operands allocated truth values that would satisfy
      the decision.
    """
    @staticmethod
    def decision_to_choice(decision):

        decisionCopy = deepcopy(decision)

        def convert(node, wantedTruth, numberOfNots):
            # remove the NOT
            if node.val == "!":
                wantedTruth = not wantedTruth

                q = node.parent
                if q != None:
                    isRight = True if q.right == node else False
                    if isRight:
                        q.right = node.left if node.left != None else node.right
                        convert(q.right, wantedTruth, numberOfNots + 1)
                    else:
                        q.left = node.left if node.left != None else node.right
                        convert(q.left, wantedTruth, numberOfNots + 1)
                else:
                    decisionCopy = node.left if node.left != None else node.right
                    convert(decisionCopy, wantedTruth, numberOfNots + 1)

            elif node.val == "&":
                if numberOfNots % 2 == 1:
                    node.val = "|"

                convert(node.left, wantedTruth, numberOfNots)
                convert(node.right, wantedTruth, numberOfNots)

            elif node.val == "|":
                raise ValueError("decision cannot have an | operator in it.")

            else: # operand
                node.truth = wantedTruth

        convert(decisionCopy, True, 0)
        ExprTree.assign_parents(decisionCopy)
        return decisionCopy

    def process(self):
        self.parse()
        self.inorder_decision_finder()

    # TODO:
    """
    matching variables vs variable values.
    """
    ################################ TODO: below 2 methods needs to be designed and
    ################################       implemented tonight.
    """
    """
    def get_truth_score(self, truthMap):
        return -1

    """
    occurrenceMap := dict, key is expression, value is probability
    """
    def get_occurrence_score(self, occurrenceMap):
        return -1
