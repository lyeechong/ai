lsc568, lyeechong@gmail.com
ksa???, kendallemailhere

Lyee Chong and Kendall Ahrendsen's submission for the
CS378H: Reinforcement Learning Assignment

The value iteration agent just followed the value iteration algorithm
which was given in the book. We tested it by running it and checking
the result was the same for 5 iterations in the gridworld.

For question 2 (BridgeGrid), we just set the noise to zero. This way
it would never fall off and think that by heading right, it would finish
in a -100 terminal state.

With question 3, for each part of it, we thought a bit about it before
changing the parameters and running the simulation over and over until it worked.
I've listed a bit of our reasoning below.
For a:
  The discount should be low, but not very low. This way it would
  prefer the closer terminal state but not the further one. Noise
  was set to zero otherwise it may not risk the cliff.
For b:
  Noise was turned up for b since it was to avoid the cliff. By
  increasing the noise, it sometimes fell off the cliff and marked
  that going away from the near-cliff locations was the only sure
  way that it would not fall off the cliff. Again, the discount was
  relatively low.
For c:
  We turned up the discount for this one so that the reward would
  help guide it to the distant terminal state instead of the closer
  one. Noise was set to zero so it would risk the cliff.
For d:
  Noise was set to a higher value and discount high also.
For e:
  Discount was set to 1 and livingReward also so that the agent's policy
  would be to just stay where it is and not move.

Question 4, we followed the instructions of the comments and the update
algorithm which was given in the AI textbook. We were scared by the
warning given about argMax and avoided it completely in all of our programming.

After watching it fail miserably over and over again, we concluded that
for the Q-learner to learn cross the bridge, it must cross the bridge
at least more than one time, and to do so, it had to avoid falling off
at any point in time. Given that each spot on the bridge has four sucessors,
and that two of those were off-the-bridge -100 terminal states, one was
in the wrong direction, and only one was right, using a bit of math and the
given that there are 5 spots it has to go across successfully, it's not possible
within 50 episodes of learning for it to cross with greater than 99% chance.

The crawler was fun to watch and see it learn strange ways of crawling.

The same with Pacman. We were surprised to see how well it performed and
it easily won around 90-100% of its matches after the 1000 episode mark.

We followed the approximate Q-learning algorithm from the book since we
got a bit confused with the given one in the assignment page. Most of the code
was the same from the previous Q-learning agent.

Who did what: we all worked on everything, especially watching the agent fall
off the bridge many, many times.
