When the game Clicker Heroes 2 got an update changing the game's progression balance and adding a new system of buying artifacts many of us were quick notice issues with the games progression. Because of this several us more dedicated fans decided to dig a bit deeper and find out why we were now getting completely stuck much ealier than expected.

We were quickly able to deduce that many of the previous number's hadn't changed, but the overall scaling of each world had, going from x^1.16 to x^1.218, a 5% increase in difficultly per world traversed. This combined with the find that forge cores(the currency used to interact with the new artifact system) were scale at a rate of x^1.05 per world gave us a clear idea in what was going wrong: artifacts were not providing a x^1.05 growth they should, causing us to slow down and become stuck.

This motivated me write out some python code to simulate playing the game and buying and upgrading artifacts whenever possible. Using a text dump of artifact data someone else had created by parsing game code, I was able to load in the data, create logic to optimally buy artifacts, and then print out the resulting multiplitive increase for every system(a set of 30 worlds). The findings were surprising: the overall multiplier per world was in fact 1.05, but a majority of the systems were averaging well under that per world, with many sitting around 1.02.

Further investigation allowed us to realize that most of the scaling of artifacts was in the intial purchase, with upgrades not contributing much towards their power. This explained why most systems were below 1.05, buying a new artifact was a rather rare event, with you spending most of your forge cores on upgrades. This knowledge eventually went on to help create a balance mod, which is recomended for play to this day.

Included files:

Artifact-Thing.txt - The text dump of all artifact information
worldMults.txt - An output file the code created for easy sharing
SolveArtifacts.py - The code used to calculate the multiplier per world from artifacts
