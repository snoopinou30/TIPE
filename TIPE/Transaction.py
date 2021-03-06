from hashlib import sha256
from pathlib import Path

class Transaction:
    

    def __init__(self, personId, maladieId, newDate, clientId, privateKey = - 1):
        self.personId = personId    # id de la personne liée à la transaction
        self.maladieId = maladieId  # id de la maladie liée à la transaction
        self.newDate = newDate      # date à ajouter à la personne (que ce soit attrapée ou perdue)
        self.clientId = clientId    # nom de la personne qui a envoyée la transaction
        
        if privateKey != -1:
            s = ""
            s += str(self.personId) + "|"
            s += str(self.maladieId) + "|"
            s += str(self.newDate) + "|"
            s += str(self.clientId) 
            
            hash = int.from_bytes(sha256(bytes(s, 'utf-8')).digest(), byteorder='big')
        
            hashSignature = pow(hash, privateKey[1], privateKey[0])

            self.signature = hashSignature  # Signature de la transaction
                                            # Ici par l'hopital et donc fait avec la clé privée
        
    
    def __eq__(self, other):
        return self.personId == other.personId and self.maladieId == other.maladieId and self.newDate == other.newDate and self.clientId == other.clientId and self.signature == other.signature


    def transToString(self): # Séparateurs entre infos d'une transaction sont |
        s = ""
        s += str(self.personId) + "|"
        s += str(self.maladieId) + "|"
        s += str(self.newDate) + "|"
        s += str(self.signature) + "|"
        s += str(self.clientId) 
        return s

    @staticmethod
    def stringToTrans (string) :
        aux = string.split("|")
        personId = int(aux[0])
        maladieId = int(aux[1])
        newDate = aux[2]
        signature = int(aux[3])
        clientId = int(aux[4])
        
        transaction = Transaction(personId, maladieId, newDate, clientId)
        transaction.signature = signature
        
        return transaction 
    
    def isValidTrans(self) :
        s = ""
        s += str(self.personId) + "|"
        s += str(self.maladieId) + "|"
        s += str(self.newDate) + "|"
        s += str(self.clientId) 

        p = Path('.')
        hopitalFile = None

        f = open("listeHopital8000.txt", "r") # TODO : essayer de trouver un fichier pour sûr
        g = f.readlines()
        h = g[self.clientId].split("%")

        hash = int.from_bytes(sha256(bytes(s, 'utf-8')).digest(), byteorder='big')
        hashFromSignature = pow(self.signature, int(h[1]),int(h[0]))

        f.close()

        if hashFromSignature == hash :
            return True
        return False
