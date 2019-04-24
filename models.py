

class Bestellungen():
    def __init__(self, name, bestellungen):
        self.name = name
        self.bestellungen = bestellungen
        
    def getBestellungDict(self):
        return {self.name : self.bestellungen}
        
    def getName(self):
        return self.name
        
    def getBestellungen(self):
        return self.bestellungen      
  
    def __str__(self):
        return str(self.name) + str(self.bestellungen)
