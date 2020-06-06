# Expresso

This is a small program that performs parsing and solves operations on boolean expressions. Boolean expressions *are not confined to 3-CNF* format. The following capabilities have been programmed into the `ExprTree` class:

1. Determine if a boolean expression string is valid.
2. Parse a boolean expression string.
3. Determine the possible decisions of a boolean expression string.
   A possible decision is an *exclude-OR* boolean expression string.
   Examples include:
   * SADFLSJDFLSDAJ & SADFLSJDFDAJ & SDFSADF  
   * AFSD & JYTHR & !AFSD
   * ITYUER & MNVXC & YKUTHRSG

   For the worst-case `3-CNF` expression, defined below as
   ```
   <B | B a boolean expression with L clauses, each clause has 3 unique variables>
   ```
   there are 3^L possible decisions.
    aka Infinitus Maximus  

4. Determine the possible choices of a decision. A choice is a one `ExprTree`
   that gives possible truth values to the operands of a decision so that it outputs True.
   Examples include:
   * Akyujt == TRUE | Bjytehrs == FALSE & Ctujynhgdbf == TRUE

   For the best-case decision, defined below as
   ```
   <B | B a decision with no NOT-clauses>
   ```
   there is only one choice.

## Usage

1. git clone <THIS_REPO>
2. cd into REPO
3. run `python interface.py`


The parsing in this program is not perfect. Start with some simple examples,
like
* SDLKFJSALDKJFSDLFKJSFLKASJDFLKDAJJ & 387426Y59842HNGANGAIE

And go from there! Take your time and you'll make it! Never give up!

## Limitations
Any sizably large boolean expression will probably fail. Contribute if you want more!
