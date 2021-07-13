
from NimbleSizer import NimbleSizer;

from linebot.models import (
    TextSendMessage
)
from PrimeraSizer import PrimeraSizer
from SimplivitySizer import SimplivitySizer
from Help import Help

class Sizer:

    #List Supported Product
    products = ["Primera", "Nimble", "SimpliVity"]

    @staticmethod
    def GenerateSizerResponse(words):
        if len(words) == 1:
            return Help.GenerateCarousel(type='size product', list=Sizer.products)
        elif len(words) > 1:
            selectedProduct = str(words[1]).lower().strip()
            #Check if valid product
            unMatch = True
            for product in Sizer.products:
                if selectedProduct == product.lower().strip(): unMatch = False
            if unMatch: return [TextSendMessage(text="Please Select supported Products"),Sizer.GetSizerMenu()]
            if selectedProduct == "primera":
                return PrimeraSizer.GeneratePrimeraSizer(words)
            elif selectedProduct == "nimble":
                return NimbleSizer.GenerateNimbleSizer(words)
            elif selectedProduct == "simplivity":
                return SimplivitySizer.GenerateSimplivitySizer(words)