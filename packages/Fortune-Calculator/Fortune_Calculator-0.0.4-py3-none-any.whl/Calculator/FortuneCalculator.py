from random import SystemRandom

class Ore:
    """
    Attributes
    ----------
    Coal = 1
    Diamond = 1
    Emerald = 1
    Iron = 1
    Copper = "Copper" (2~3)
    Gold = 1
    NetherGold = "NetherGold" (2~6)
    NetherQuartz = 1
    Lapis = "Lapis" (4~9)
    AmyestCluster = 4
    """
    Coal = 1
    Diamond = 1
    Emerald = 1
    Iron = 1
    Copper = "Copper"  # (2~3)
    Gold = 1
    NetherGold = "NetherGold"  # (2~6)
    NetherQuartz = 1
    Lapis = "Lapis"  # (4~9)
    AmyestCluster = 4

class Calculator:
    def __init__(self, fortunelevel:int or float, ore:Ore):
        self.fortune = fortunelevel
        self.ore = ore

    def calculatingfortune(self, simulatingamount:int=1000000, noprint:bool=True):
        ore = self.ore
        fortune = self.fortune
        fortunelist = []
        if noprint is False:
            print("Start Calculating")
        for i in range(simulatingamount):
            amount = 1
            if type(ore) is int or type(ore) is float:
                amount = SystemRandom().uniform(ore, ore * (143 / 100))
            elif type(ore) is str:
                if ore == "Copper":
                    amount = SystemRandom().randint(2, 3)
                elif ore == "NetherGold":
                    amount = SystemRandom().randint(2, 6)
                elif ore == "Lapis":
                    amount = SystemRandom().randint(4, 9)
            if noprint is False:
                print(i)
            fortunecalculating = 1 / (fortune + 2) + (fortune + 1) / 2
            if noprint is False:
                print(i)
            fortunelist.append(fortunecalculating * amount)
        result = sum(fortunelist) / len(fortunelist)
        if noprint is False:
            print(result)
        return result

    @property
    def self(self):
        return self

    @property
    def ore1(self):
        return self.ore

    @property
    def fortune1(self):
        return self.fortune