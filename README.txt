==== CHESS VALIDATOR ====

    Author: Tom Rein
    Email: tr557@drexel.edu

==== DEPENDENCIES ====

    Pip
    Python 2.7.x
    Coverage.py
    PyUnit
    Pylint

==== USAGE INSTRUCTIONS ====

    NOTE: Python 3 is untested and may not work
          Use Python 2.7.x if possible

    1: To run the program, type "python chess.py"
    2: The program will prompt the user for input regarding the board configuration
        2a: The first prompt will first ask for white pieces
        2b: The second prompt will be for black pieces
        2c: The final prompt will ask for a piece to compute the legal moves for
   3: The program will output all the legal moves for a given piece

==== INPUT CONSIDERATIONS ====

    This program typically expects the user to enter values seperated by spaces.
        ex: "Kg1 Bf3 Qc6".

    However, the program will sanitize various inputs that don't match this format.

    It is also capable of handling values separated by commas and values seperated by commas and spaces.
        ex: "Kg1,Bf3,Qc6", "Kg1, Bf3, Qc6" 

    Values where the first letter isn't capitalized and/or the second letter isn't lowercase will also be sanitized. 
        ex: "kG1 bf3 QC6"

    If a user enters an invalid value somewhere in the string, the program will reprompt for input.

    Conditions that will trigger a re-prompt:
        1) Non-sensical values ex: "Vf2", "Bl", "Qc10"
        2) Repeated values when entering pieces for white or black
        3) Entering more than one value to compute moves for 
        4) Blank input

==== SYSTEM STATUS ==== 

Overall, the system functions as expected. However, I did encounter two situations where the code does not work as expected.
Both issues were found late in the development process, so I was unable to fix them and I did not want to radically restructure my code near the deadline since many of my functions are recursive. 

Both issues are related to a King being in check.

The first issue is when calculating the moves for a piece that is not a king, the system does not take into consideration whether that move would put a king in check. 
So, when computing the moves for a piece, those moves are considered valid, even though moving there would put the King in check which is invalid. 

The second issue was more difficult to diagnose, but my funtion for determining check for a king does not calculate every move correctly. My function is designed to scan all the squares of a potential move for a piece that would induce check. 
So, if it encounters a Queen in an open diagonal square, that move is invalid, and that part works fine.
However, the logic is not fully flushed out. 
If it doesn't encounter a piece, it considers that move valid, but that is not always the case for check, and as a result, it records false positives

==== UNIT TESTS ====

Units for this program are located in the file "test_chess.py"
It utilizes PyUnit.

To run the tests, type: "python test_chess.py -b"
NOTE: The "-b" flag is optional, I just use it to squelch error messages from being printed

There are 19 total tests, but most attempt to accomplish one of two objectives:
    1) Testing movement of pieces
    2) Testing inputs

The rationale is this the most meaningful usage that the program will undergo.
In structuring tests this way, I was able to achieve a total branch coverage of 93%.
More information regarding coverage can be found in the associtive directory.

A primary goal of mine was to make succsive tests easy to write, so I wrote several helper functions to assist in that end.
For instance, my chessboard in "chess.py" is a 2d list, and as such, many functions use list indices as arugments. 
However mentally calculating which indices correspond to which positions is somewhat taxing, and this was complicating how my tests were written.  
To solve this I wrote a function that translates positions into indices, which made it much easier to write tests moving forward.
So, when testing a piece's movement, I only had to supply the expected positions and not the corresponding indices

==== STATIC ANALYSIS AND CODE COVERAGE ====

Information regarding static analysis and code coverage can be found in there associative directories.
Both contain generated reports from running the tools as well as writeups regarding implementation and usage details
