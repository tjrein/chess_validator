For my coverage tool, I used Coverage.py

Once installed, useing Coverage.py is a two-fold process.

You first have to run "coverage run --branch test_chess.py"
Next, to generate the report, you have to run "coverage report -m"

I achieved a final code coverage of 93%. The code that is missing is mostly in my main function, which primarily exists to call other functions, all of which are tested. 

Part of my input function is also missing coverage. I tried to cover as much as I could, but ultimately, I wasn't quite sure if it was possible to stub out a call to "raw_input", since that requires user input.

In using coverage.py, I restructered much of my code so it could be adequetly tested. For instance, my function "format_moves" used to be "output_moves". Rather than using that function to print, I had it instead return a formatted string, that way I could more easily write tests for it. 

Coverage.py only allows for statement and branch coverage, which doesn't seem ideal in light of our recent lectures, but it is the best I could do.
