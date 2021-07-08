import math

class Converter:

    @staticmethod
    def TBToUnitMultipler(unit = "tb"):
        unit = str(unit).strip().lower()
        multiplier = 1.0
        if unit == "tb":
            multiplier = 1.0
        elif unit == "pb":
            multiplier = 1000.0
        elif unit == "gb":
            multiplier = math.pow(0.001,1)
        elif unit == "mb":
            multiplier = math.pow(0.001,2)
        elif unit == "kb":
            multiplier = math.pow(0.001,3)
        elif unit == "pib":
            multiplier = 1000 * math.pow(1.024,5)
        elif unit == "tib":
            multiplier = math.pow(1.024,4)
        elif unit == "gb":
            multiplier = math.pow(0.001,1) * math.pow(1.024,3)
        elif unit == "mb":
            multiplier = math.pow(0.001,2) * math.pow(1.024,2)
        elif unit == "kb":
            multiplier = math.pow(0.001,3) * math.pow(1.024,1)
        return multiplier
    