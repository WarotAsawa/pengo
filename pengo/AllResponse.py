import random;

class AllResponse:
    #Response String
    allResponse = {};
    allResponse["help"] = "You can see what I can do listed on the Carousel bloew. I am case-insensitive bot so no worries about your inputs. Tap on each item to start the wizard of each feature."
    allResponse["helpspec"] = "Type \"spec\" for wizard or use or use \nspec [productname] [model] \n ex: \n - spec 3par 8200\n - spec nimble af20"
    allResponse["helplookup"] =  "Type \"lookup\" for wizard or use or use \nlookup [productname] [attribute] [value] \n ex: \n - lookup intel core 20\n - lookup amd clock 3.3"
    allResponse["helptips"] = [ "Ask me for 'help' to see what I can do for you",
    							"Want to learn how to talk to me? Ask me for 'help'.",
    							"Ask for 'help' to see how smart I am."]

    allResponse["hello"] = [        "Hello there , ",
    							    "Hello, ",
    							     "What's up, ",
    							     "Good day, ",
    							     "Hi, ",
     							    "May I help you, ",
    							    "Greetings, ",
    							    "How can I help you, "]
    allResponse["thank"] = [        "You are always welcome.",
    							    "With pleasure.",
    							    "I am glad to be your service.",
    							    "My pleasure.",
    							    "You can ask me for help anytime."]
    allResponse["bye"] = [          "I'll be back, ",
    							     "Bye bye, ",
    							     "So longgg, ",
    							     "Hasta la vista, ",
    							     "Sayonara, ",
    							     "Life is too short to say goodbye, "]
    allResponse["yourname"] = [     "Don'you see my name above?",
    							    "My name is Uvuvwevwevwe Onyetenyevwe Ugwemubwem Ossas",
    							    "I am the one called YOU KNOW WHO.",
    							    "I am the Dark Lord.",
    							    "Kimino na wa!"]
    allResponse["whatyoudo"] = [    "I am chatting with you,seriously.",
    							    "Texting texting texting texting texting texting texting",
    							    "Chit chat! I am Chit-chatting.",
    							    "I am talking with you.",
    							    "I have no idea what I am doing right now."]
    allResponse["what"] = [         "What !??",
    							    "Wattttt?",
    							    "What is what ?",
    							    "What is a pronoun to ask for information specifying something.",
    							    "Duhhhh",
    							    "What are you talking about?"]
    allResponse["where"] = [        "Where is a matter of place not a matter of time.",
    							    "This universe is really big don't you think?",
    							    "That's use to ask in or to what place or position",
    							    "Where is what?",
    							    "I don't know. Duhhh!"]
    allResponse["when"] = [         "When is a matter of time not a matter of place.",
    							    "This universe heat death is very long.",
    							    "At any moment now.",
    							    "When is what?",
    							    "How do I know?",
    							    "I don' know. Duhhh!"]
    allResponse["why"] = [          "Because it is my demand.",
    							    "Because it is an order from god. And I am your god now.",
    							    "Do not seek for a reason. Everything has its own purpose.",
    							    "Because nothing is true. Everything is permitted.",
    							    "Why should I know?"]
    allResponse["whoareyou"] = [    "I am your worst nightmare.",
    							    "I am a creature called Homosapiean",
    							    "I am Batman!",
    							    "I am your shadow.",
    							    "I am you."]
    allResponse["who"] = [          "Who ??",
    							    "Each and Everyone.",
    							    "No body.",
    							    "Just you and me my friend.",
    							    "Why should I know?",
    							    "I don't know. Duhhh!"]
    allResponse["howareyou"] = [    "No. Not good. NOT GOOD! ",
    							    "I'm fine thank you and you? ",
    							    "I felt terrible. ",
    							    "Never been this good. ",
    							    "I feel selfless. "]
    allResponse["how"] = [          "I do not know how.",
    							    "How sould I know?",
    							    "No idea. Duhhh"]
    allResponse["canyou"] = [       "No. I can't do somthing like that.",
    							    "No. I don't have an ability to do that",
    							    "I dont have time for that !"]
    allResponse["really"] = [       "Indeed,.",
    							    "Oh sure.",
    							    "Yes!",
    							     "It is!",
    							     "Defenately"]
    allResponse["joke"] = [         "I would tell you a chemistry joke but I know I wouldnt get a reaction.",
    							    "Why dont some couples go to the gym? Because some relationships dont work out.",
    							    "I wondered why the baseball was getting bigger. Then it hit me.",
    							    "Have you ever tried to eat a clock? It is very time consuming.",
    							    "The experienced carpenter really nailed it,but the new guy screwed everything up.",
    							    "Did you hear about the guy whose whole left side was cut off? He is all right now.",
    							    "Yesterday I accidentally swallowed some food coloring. The doctor says I am OK,but I feel like I have dyed a little inside.",
    							    "I wasnt originally going to get a brain transplant,but then I changed my mind.",
    							    "A guy was admitted to hospital with 8 plastic horses in his stomach. His condition is now stable..",
    							    "If a wild pig kills you,does it mean you’ve been boared to death?",
    							    "You cry,I cry,…you laugh,I laugh…you jump off a cliff I laugh even harder!!",
    							    "Never steal. The government hates competition.",
    							    "Doesn’t expecting the unexpected make the unexpected expected?",
    							    "Practice makes perfect but then nobody is perfect so what’s the point of practicing?",
    							    "Everybody wishes they could go to heaven but no one wants to die.",
    							    "Why are they called apartments if they are all stuck together?",
    							    "DON’T HIT KIDS!!! No,seriously,they have guns now.",
    							    "Save paper,don’t do home work.",
    							    "Do not drink and drive or you might spill the drink.",
    							    "Life is Short – Talk Fast!",
    							    "Why do stores that are open 24/7 have locks on their doors?",
    							    "When nothing goes right,Go left.",
    							    "Save water ,do not shower.",
    							    "A Lion would never cheat on his wife but a Tiger Wood.",
    							    "Why do they put pizza in a square box?"]
    allResponse["errorWord"] =[     "Please give me a valid input.",
    							    "No, I am not smart enough to do that.",
    							    "Please try again.",
    							    "I do not get that.",
    							    "You mad? ",
    							    "You have to ask me again.",
    							     "I cannot give you the answer, sorry.."]
    allResponse["preAnswer"] = [    "Ok Ok Ok.",
    							    "This looks hardish, but I am smart enought to do this.",
    							    "Piece of cake!.",
    							    "Oh too easy.",
    							    "You will thank me for this later.",
    							    "Here you go.",
    							    "There you go.",
    							    "Here are you answers."]
    allResponse["image"] = [        "Wow, supernice image",
    							    "Whose picture is this?",
    							    "What a nice image..",
    							    "Good image you have here",
    							    "Nice Photo !!"]
    #Get Random string from allResponse via key
    @staticmethod
    def GetRandomResponseFromKeys(key):
        i = random.randint(0, len(AllResponse.allResponse[key])-1 )
        return AllResponse.allResponse[key][i]
