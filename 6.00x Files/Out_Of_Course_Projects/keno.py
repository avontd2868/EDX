#FINDS THE BEST NUMBER CHOICE (OUT OF 12) FOR MAXIMUM PROFIT PLAYING KENO
import pylab
import random

class simpleKeno(object):
    """
    Defines a class simpleKeno without take into account
    the profits.
    """
    #profits per game category
    PROFITS_TABLE = {(1,1):2.5, (1,2):1, (2,2):5, (2,3):2.5, (3,3):25,
                     (2,4):1, (3,4):4, (4,4):100, (3,5):2, (4,5):20,
                     (5,5):450, (3,6):1, (4,6):7, (5,6):50, (6,6):1600,
                     (3,7):1, (4,7):3, (5,7):20, (6,7):100, (7,7):5000,
                     (4,8):2, (5,8):10, (6,8):50, (7,8):1000, (8,8):15000,
                     (4,9):1, (5,9):5, (6,9):25, (7,9):200, (8,9):4000,
                     (9,9):40000, (0,10):2, (5,10):2, (6,10):20, (7,10):80,
                     (8,10):500, (9,10):10000, (10,10):100000, (0,11):2,
                     (5,11):1, (6,11):10, (7,11):50, (8,11):250, (9,11):1500,
                     (10,11):15000, (11,11):500000, (0,12):4, (6,12):5,
                     (7,12):25, (8,12):150, (9,12):1000, (10,12):2500,
                     (11,12):25000, (12,12):1000000}
    
    def __init__(self, categoryGame, eightyNumbers=80, twentyNumbers=20):
        """
        Initializes the instance with 3 parameters.
        categoryGame: How many numbers the user will play (1 to 12)
        maxNum: Represents all the possible numbers. Usually is equal to 80
        twentyNumbers: The amount of lucky numbers, usually 20
        """
        self.categoryGame = categoryGame
        self.eightyNumbers = range(1, eightyNumbers+1)
        self.twentyNumbers = twentyNumbers

    ##START---Getter Methods
    def getCategoryGame(self):
        return self.categoryGame

    def getEightyNumbers(self):
        return self.eightyNumbers

    def getTwentyNumbers(self):
        return self.twentyNumbers
    ###END---Getter Methods

    def fillerList(self, categoryGame):
        """
        Fills a list with a specific amount of numbers
        from 1 to 80 (NOT duplicated)

        numbersChoice: integer, amount of different numbers
    
        returns: a list filled with categoryGame numbers
        """
        lista = []
        while len(lista) < categoryGame:
            tempNumber = random.choice( self.getEightyNumbers() )
            if tempNumber not in lista:
                lista.append(tempNumber)
        return lista


    def preparePlayer(self):
        """
        Prepares the player. That is, stochastically fills
        user's numbers, myNumbers, which varies in size
        (1 to 12) in range [1,80].
        
        returns: myNumbers (list in list)
        """
        myNumbers = []
        for i in range(1, self.getCategoryGame()+1):
            myNumbers.append(self.fillerList(i))

        return myNumbers

    def prepareBoard(self):
        """
        Prepares the board. That is, stochastically fills
        the lucky 20 numbers in range [1,80]
        
        returns: a list with the 20 lucky numbers out of 80
        """
        return self.fillerList(self.getTwentyNumbers())


    def correctMatch(self, luckyNumbers, myNumbers):
        """
        Checks bingo for each of the played numbers. That is,
        if player has played 5 numbers, checks how many of these
        numbers match the kenoNumbers, etc.

        returns: a list with integers, represent successfull hits
        """
        self.correctHits = [0]*len(myNumbers)
    
        for i in range(len(myNumbers)):
            for num in myNumbers[i]:
                if num in luckyNumbers:
                    self.correctHits[i] += 1
        return self.correctHits #list of size 12


    def profit(self, correctHits, columnCost=0.5):
        """
        Computes the profit of the player analogous to the
        game category.

        correctHits: a list of 12 integer elements, showing matches
        columnCost: a float, usually 0.50 Euros, the cost to participate

        returns: a list of 12 float elements, showing the profit for each game
        """
        profitsList = [0.0]*len(self.correctHits)
        
        for i in range(len(self.correctHits)):
            profitsList[i] += simpleKeno.PROFITS_TABLE.get( (self.correctHits[i], i+1), 0)

        return profitsList
        

def playKeno(numTrials):
    """
    Checks how many sucessfull hits the player did
    over numTrials trials

    returns: avgHits, a list with the average results
    """
    correctHits = ( pylab.array(12) )*0
    profitsList = ( pylab.array(12) )*0
    
    #myNumbers = [[1], [2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 1, 2, 3, 4], [5, 6, 7, 8, 9, 10, 11, 12], [1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
    
    for i in range(numTrials):
        player = simpleKeno(12)
        myNumbers = player.preparePlayer()
        luckyNumbers = player.prepareBoard()
        #luckyNumbers = range(1,21)
        correctHits += player.correctMatch(luckyNumbers, myNumbers)
        profitsList += player.profit(correctHits)
        
    avgHits = correctHits/float(numTrials)
    avgProfit = profitsList/float(numTrials)
    
    return avgHits, avgProfit


def plotKenoResults(numTrials):
    avgHits, avgProfit = playKeno(numTrials)
    print avgHits, '\n', avgProfit
    #Set the x-axis
    xAxis = pylab.array(range(1,13))
    #First plot design
    pylab.subplot(2,1,1)
    pylab.bar(xAxis, avgHits, align='center', edgecolor='black')
    pylab.xlim(0,13)
    ymin, ymax = pylab.ylim()
    pylab.title('***KENO GAME***\n Results of successful hits and profits over 100,000 trials')
    pylab.xlabel('Category game')
    pylab.ylabel('Number of successful hits')
    pylab.text(0.5, ymax-(ymax-ymin)/8, 'Max hits=' + str(int(avgHits.max())) + ' in category ' + str(list(avgHits).index(avgHits.max())+1),  )
    pylab.grid(True)
    #Second plot design
    pylab.subplot(2,1,2)
    pylab.bar(xAxis, avgProfit, align='center', edgecolor='black')
    pylab.xlim(0,13)
    #pylab.hist(avgProfit, bins=len(avgProfit), cumulative=True)
    pylab.xlabel('Category game')
    pylab.ylabel('Profit Earned (euros)')
    pylab.grid(True)
    pylab.show()
