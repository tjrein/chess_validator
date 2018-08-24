For my static analysis tool I used Pytlint.

To exectute pylint, provided you have it installed, run "pylint chess.py --reports=y"

In this directory are two generated reports from using pylint.
One report was from early on in the development process, and the other is the final report.

Pylint assisted me in several in writing cleaner code.
For instance, as detailed in my original report, I had many whitespace errors, many of my lines were too long, unused variables, etc.

I corrected those issues, added docstrings to all my functions, removed unused variables, and reduced the number of arguments in my function calls.
Pylint also complained about my usage of single character variables.
Since my implementation of the validator utilizes a 2d array, I was using letters to represent indices. To rectify this, I implemented a helper function, which made my code a lot a cleaner. 

Pylint did not catch that many logical errors, how ever it did catch one or two.
In the report it threw the warning: "Unnecessary "else" after "return" (no-else-return)"
Basically, as it sounds, I had an else after a return which was never going to be hit, so I removed it. 

Mostly Pylint was valuable in helping me restructure my code. Although some warnings felt slightly pedantic, I was pleased with the outcome. In my final generated report my code passed Pylint without any warnings.
