# BattleshipGame
Developed for MIDS Project1 in Fall 2018 by Steve Dille


Background:
I completed the game of Battleship in an old looking 1970s/80s looking line editor format.  Long ago, you may have heard, there was a 
famous star trek program written in Basic that was included on UNIX mini computers everywhere.  I used to waste a lot of time playing that
in the computer lab in the middle of the night.  This game is a throwback to that with the matrix printed out, shooting at locations and 
with the continual print out nature of it all (like the old PDP-writers) that we used to use.  I even put time delays in to slow it down a 
bit to give it that feel. I think I found the source code in Basic online (for Star Trek) and I’m going to consider rewriting it in Python 
if I ever get time.  Have fun..

Instructions:
You really want to run this game in Terminal and I am giving you the .py file.  The experience is awful in Jupyter as you have this little 
window so you can’t see the whole progression of the game very well and the matrices all at once.  

Observations and Improvements:
The first question my 14 year old asked me was will the computer try and shoot around the ship when you first get a hit? Fortunately, I had
just coded that and it was one of the challenges.  I called it the shot optimizer and I made it miss the first shot which would always be 
adjacent to the hit (just like a human guessing) so the computer would not have an unfair advantage of needing fewer shots to sink the ship.

As I have played more, I found I can beat the computer most of the time, so the game is still tilted towards the human who has a field of 
view of where the most productive shots might be placed vs. picking random shots. An opportunity for extension would be improving the shot 
optimizer to optimize the computer’s random shot making into areas that cover the most possibilities just like I do when I play.  That is 
probably why I have an advantage still and find ships faster. Chris suggested I use machine learning to evaluate the player tendancies and 
that is a great idea. This game could have levels of easy to hard depending on which shot optimizer is used.

