Took me a lot of time.
I fairly quickly figured out that we had to have Ripple Carry Adder (see Lomig's excellent post).
I also settled on a non-programming solution, but manually checking. Just used python to make that easier.


Then driving to XMAS dinner (or was it an X-MAS dinner?), I realized that I should rename all the wires
from the random names, to more meaningful names with numbers (like we have x01, y02, z03, etc.).

So:
1. Sort the inputs based on some elements in there.
2. That way I could split into:
   - Wires that are directly determined by the inputs (those are used to calculate the digit and the carry, based on just the inputs)
   - Wires that are intermediary calculations
3. Using the first category, I renamed all those wires into c01, d01, ... and used those new names also
   in the second categroy
4. That started to look nicer. In the second category I identified two main blocks of gates: ANDs and ORs
5. So rename all of those too.
6. Print out everything in a nice manner.
7. Spot 3x2 swapped wires rather easily based on anomaly in the gate used within the sorted outputs.
8. That left a last one to find.
9. Swap the 3x2 wires in the input already, to make it easier to spot the 4th pair.
10. In part 1, add some printouts of x, y, x+y and z in binary. Also print the XOR to figure out the different bits.
11. Copied the output of the xor into VS Code, to see that it was around the 24th digit.
12. Check the printed out gates, and notice that on 24 there is a different combination: c.. AND a.. instead of c.. and d..
    That's number 4.
