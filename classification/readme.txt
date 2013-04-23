lsc568, lyeechong@gmail.com
ksa435, kendall.ahrendsen@utexas.edu

Question 1:
Followed the equations in the text.
Iterates through each k in kgrid
resets the conditional probabilty table each time for each k, storing the previous one just before it does
trains the tables on the data from training, counting each time a pixel is on for that label
then it adds k to each of the counts
after validation, it selects the conditional probability table with the best validation results

Question 2:
followed the equation in the text

Question 3:
More or less the same as naive bayes for training, but on incorrect labels, we followed the
equation in the text to update the weights accordingly.

Question 4:
followed the equation in the text, more or less the same as the one from naive bayes
except we subtracted instead of divided

Question 5:
followed the equations in the text, using methods from the Counter class in util

Question 6:
the feature we added was finding if the digit had more than one contiguous regioin of "off" pixels
we did this by using a flood fill method
the algorithm obtains 84% exactly

Mini Contest:
copied and pasted our naive bayes. it doesn't really work for some reason
and gets around 10%, which is not much better than random picking.

Both Kendall and Lyee slaved away in the computer lab on all the problems.
