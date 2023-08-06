The bet between Pip and Anna concerns which ludo position is optimal for a two player game in which the two players bases are adjacent to each other: Pip believes the player further clockwise has the better position, while Anna believes the player further counter-clockwise has the better position. 

E.g., if an observer is in front of a board in which the two players start on the top left (position 0, which will be referred to as player0) and top right (position 1, which will be referred to as player1), Pip would declare position 1 superior, and Anna would declare position 0 superior. (See: https://github.com/jaib1/ludoSim/blob/master/StandardLudoBoard.jpeg) 

To determine if one position is superior, we run this simulation N times, with the null hypothesis that neither position is superior. After the simulation is run, if the number of times player1 wins has a probability of < 0.05 given the null hypothesis (that the null distribution is a binomial distribution with n=N and p=0.5), Pip wins the bet. Similarly, if the number of times player0 wins has a probability of < 0.05 given the same null hypothesis, Anna wins. Else, no one wins the bet. 

E.g., if N = 10000, s.d. = 50, so if player1 wins >=5100 times Pip wins, and if player0 wins >=5100 times Anna wins. Else, no one wins the bet.

Player moves are chosen randomly amongst the set of possible moves each turn, with two exceptions:

1) a move in which a player can hit another player's piece has highest order priority.
2) a move in which a player can avoid moving their piece within six spaces of another player's piece has second highest order priority.
