# Calculating the expectation value of a UK lottery ticket

The UK lotto is a game played every Wednesday and Saturday in which each player pays a £2 entry fee and selects 6 numbers from 1-59. Then, 6 main balls and 1 bonus ball are drawn randomly, without replacement from a pot of balls numbered 1-59 inclusive. Cash prizes are won by ticket-holders who match 2 or more of the selected balls.
More information available at https://www.national-lottery.co.uk/games/lotto/about-lotto

This code scrapes national-lottery webpages to find the current jackpot amount and the number of rollovers, combines the relevant prizes with the probability of winning each level of prize and returns the expectation value of a lottery ticket purchased for the upcoming draw.

The probability of matching n numbers can be calculated using equation 1, except in the case of n = 5 because if 5 main numbers are correctly guessed the prize depends upon whether the bonus ball was also correctly guessed. The probability for 5 correct balls and no bonus ball can be found using equation 2. The probability for 5 correct balls and correct bonus ball can be found using equation 3.

Equation 1: $\frac{\binom{6}{n}\binom{53}{6-n}}{\binom{59}{6}}$   

Equation 2: $\frac{\binom{6}{5}\binom{52}{1}}{\binom{59}{6}}$ 

Equation 3: $\frac{\binom{6}{5}\binom{52}{0}}{\binom{59}{6}}$

More information on lottery mathematics available at https://en.wikipedia.org/wiki/Lottery_mathematics

The prizes for each draw are dependant upon whether this draw is 'Rolldown' draw. A 'Rolldown' draw occurs if there have been 5 consecutive draws in which the jackpot hasn't been won. After each of these unsuccessful draws, a rollover is declared and the remaining jackpot is added to the current jackpot for the upcoming draw. <br/>

In the case of a non-rolldown draw, the prizes are as follows: <br/>
2 main numbers: Free lucky dip (£2 face value) <br/>
3 main numbers: £30 <br/>
4 main numbers: £140 <br/>
5 main numbers: £1750 <br/>
5 main numbers and bonus ball: £1,000,000 <br/>
6 main numbers: Jackpot 

In the case of a rolldown draw, the prizes are as follows: <br/>
2 main numbers: Free lucky dip (£2 face value) + £5 cash  if jackpot isn't won<br/>
3 main numbers: £30 + a share of 85% of the remaining jackpot after £5 cash has been paid to each player matching 2 main numbers if jackpot isn't won <br/>
4 main numbers: £140 + a share of 7% of the remaining jackpot after £5 cash has been paid to each player matching 2 main numbers if jackpot isn't won <br/>
5 main numbers: £1750 + a share of 5% of the remaining jackpot after £5 cash has been paid to each player matching 2 main numbers if jackpot isn't won <br/>
5 main numbers and bonus ball: £1,000,000 + a share of 3% of the remaining jackpot after £5 cash has been paid to each player matching 2 main numbers if jackpot isn't won <br/>
6 main numbers: Jackpot 

In order to estimate the prizes in the case of a rolldown draw, it was necessary to estimate the number of £5 cash payments that are expected to be made for the current draw. A prediction for the number of tickets sold for the upcoming draw was therefore necessary, as this information is not published until after the event.
This prediction was achieved using a linear regression model, which takes the current jackpot as an input and predicts the number of tickets sold (the rationale being that people are more likely to buy a ticket when there is a large jackpot). The 2021 ticket sales and jackpot data used to train the linear regression model was sourced from http://lottery.merseyworld.com/cgi-bin/lottery?sales=1&year=2021&display=NoTables .

Finally, this information was combined to give a current expectation value of a ticket purchased for the UK national lottery.
