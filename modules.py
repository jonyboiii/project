
import random
import uuid
from faker import Faker
class Kiezer:
    def __init__(self, voornaam, achternaam, leeftijd):
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.leeftijd = leeftijd
        self.gestemd = False
        self.chipkaart = ""

    def stem(self, stemcomputer, kandidatenlijst):
        if not self.gestemd and self.chipkaart:
            stembiljet = stemcomputer.stem(self, kandidatenlijst)
            self.gestemd = True
            return stembiljet
        else:
            print(f"{self.voornaam} heeft al gestemd.")
            return None
        
class Lijst:
    def __init__(self, naam):
        self.naam = naam
        self.kandidaten = []

    def voegKandidaatToe(self, kiezer):
        self.kandidaten.append(kiezer)
class Stemcomputer:
    def __init__(self):
        self.usb_stick = None

    def InSteken(self, usb_stick):
        self.usb_stick = usb_stick
        return self

    def Stem(self, kiezer, kandidatenlijst):
        keuze = random.choice(kandidatenlijst.kandidaten)
        print(f"{kiezer.voornaam} stemt op {keuze.voornaam}")
        return Stembiljet(kiezer, keuze)
class Stembus:
    def __init__(self):
        self.stembiljetten = []

    def toevoegen(self, stembiljet):
        self.stembiljetten.append(stembiljet)

    def toon_uitslag(self):
        uitslag = {}
        for stembiljet in self.stembiljetten:
            keuze = stembiljet.keuze
            if keuze in uitslag:
                uitslag[keuze] += 1
            else:
                uitslag[keuze] = 1
        return uitslag
class USBStick:
    def __init__(self, opstartcode):
        self.opstartcode = opstartcode
class Stembiljet:
    def __init__(self, kiezer, keuze):
        self.kiezer = kiezer
        self.keuze = keuze
class Verloop:
    def __init__(self):
        self.kiezers = []
        self.lijsten = []
        self.stembus = Stembus()

    def Maak_kiezers(self, aantal):
        fake = Faker()
        for _ in range(aantal):
            voornaam = fake.first_name()
            achternaam = fake.last_name()
            leeftijd = random.randint(18, 90)
            kiezer = Kiezer(voornaam, achternaam, leeftijd)
            kiezer.chipkaart = uuid.uuid4()
            self.kiezers.append(kiezer)

    def maak_lijsten(self, aantal_lijsten, kandidaten_per_lijst):
        for i in range(aantal_lijsten):
            lijst = Lijst(f"partij {i + 1}")
            kandidaten = random.sample(self.kiezers, kandidaten_per_lijst)
            for i in kandidaten:
                lijst.voegKandidaatToe(i)
            self.lijsten.append(lijst)

    def StemComputer(self):
        opstartcode = uuid.uuid4()
        usb_stick = USBStick(opstartcode)
        stemcomputer = Stemcomputer()
        return stemcomputer.InSteken(usb_stick)

    def stemmen(self):
        for kiezer in self.kiezers:
            if not kiezer.gestemd:
                stemcomputer = self.StemComputer()
                kandidatenlijst = random.choice(self.lijsten)
                stembiljet = kiezer.stem(stemcomputer, kandidatenlijst)
                if stembiljet:
                    self.stembus.toevoegen(stembiljet)

    def toon_uitslag(self):
        uitslag = self.stembus.toon_uitslag()
        for kandidaat, stemmen in uitslag.items():
            print(f"{kandidaat}: {stemmen} stemmen")

