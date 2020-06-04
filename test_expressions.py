from collections import defaultdict

#### test expressions
sample1 = "(A & B) & (F | E)"
sample2 = "(A & (B | C)) & (F | E)"
sample3 = "FAKE"
sample4 = "(((A & B) & (C & D)) | 5)"
sample5 = "(A & (B | C)) & (F | E)"

sample6 = "!(A & B) | (C | (D & E))"

sample7 = "!A & B"
sample8 = "!(A & B)"
sample9 = "!(A & B) & !C"

sample10 = "!(A & B) | !(C & D)"

#### below variables are used to test sample 6 truth output for ExprTree
sample6__truthtable1 = defaultdict(list)
sample6__truthtable1["B"] = False
sample6__truthtable1["C"] = False
sample6__truthtable1["D"] = True
sample6__truthtable1["E"] = True

sample6__truthtable1_output = {}
sample6__truthtable1_output[" A  &  B  ! "] = [] # undet
sample6__truthtable1_output[" C "] = False
sample6__truthtable1_output[" D  &  E "] = True

##### decisions: satisfiability
sample_sat1 = "!(A & !B) & C & !D & !(E & F & G) & !H"
sample_sat2 = "!(A & B & !C) & !(D & E) & (G & !H)"


#### implications to trees
i1 = "A -> B & C"
i2 = "B & D -> A"
implicationSet1 = [i1, i2]

i3 = "A -> B"
i4 = "B -> C & D"
i5 = "C & D -> A"
implicationSet2 = [i3,i4,i5]

i6 = "A & !B & C -> D | E"
i7 = "A & C -> D | E"
i8 = "A | B | !(A & B) -> D | E"
implicationSet3 = [i6,i7,i8]

implicationSet3__truthtable1 = defaultdict(list)
implicationSet3__truthtable1["A"] = True
implicationSet3__truthtable1["B"] = False
implicationSet3__truthtable1["C"] = True

i9 = "A & (B | C) -> (D & !E) | (E & !F)"
i10 = "A & B -> (D & S)"
i11 = "A & C -> (D & E)"
i12 = "A & B | D -> F & T & N"
i13 = "C | D -> T & !R | Q"
implicationSet4 = [i9,i10,i11,i12,i13]

i14 = "A & (B | C) -> (D & !E) | (E & F & !G) | (!A & B)"
i15 = "B & D & (E | F) -> (C & D & A) | (!A & !D & !C)"
implicationSet5 = [i14,i15]
