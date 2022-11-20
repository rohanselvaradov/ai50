# Experimentation process
## Different numbers of convolutional and pooling layers
When I tried with just one convolutional layer and one pooling layer, the accuracy was very low (below 10% on testing 
and training). However, when I introduced a second convolutional layer before the pooling layer, the accuracy was
hugely improved, and I reached over 95% accuracy on both training and testing. When I tried two pairs of convolutional
and pooling layers, the accuracy was still very high, but it was slightly lower than when only one pooling layer was
used. However, the model took around half the time to train, so this may be a worthwhile compromise, depending on the
application.
## Different numbers and sizes of filters for convolutional layers
At first, I used 32 filters and a (3, 3) kernel. Using 64 filters did not improve accuracy (in fact, it fell to 89%),
and also increased the training time by around 50%. I also experimented with a (5, 5) kernel, which resulted in lower
accuracy, again of around 90%.
## Different pool sizes for pooling layers
Initially I used a (2,2) pool size for both pools. When I tried the second pool with either a (3,3) or (4,4) pool size,
the accuracy was much worse, at around 85% and 75% respectively, and this was the same when both pools were modified to
the larger size.
## Different numbers and sizes of hidden layers
My first model had a single hidden layer with 128 nodes. When I tried adding a second hidden layer of the same size,
the accuracy fell to 90%. Three hidden layers led the accuracy to fall even further (to 40%). I think this may be
because not enough training epochs were used, and the model was not able to learn the data well enough. This could be
due to an effect known as the "vanishing gradient phenomenon", a problem that occurs when the architecture is too deep.
Using a single hidden layer with only 64 units resulted in very poor accuracy, of only 5%. On the other hand, using 
256 nodes did not increase accuracy noticeably.
## Dropout
At first, I was confused as to why the testing accuracy was greater than the training accuracy of the final epoch.
However, I then realised that this was because of my use of 0.5 dropout in the model. Dropout is a technique used to
prevent overfitting, and it works by randomly setting some of the weights in the model to zero, essentially removing
those units from the network -- but crucially, all the units are used once the model is trained. This means that the
accuracy of the model could feasibly be expected to be higher on the testing data than on the training data. When I
removed the dropout, the final training accuracy was higher, at 98% but this fell to 93% on the testing data, suggesting
that there had indeed been overfitting. Increasing the dropout to 0.75 led to very low accuracy, perhaps because the 
network was too sparse to learn the data; reducing it to 0.25 didn't have a noticeable effect.