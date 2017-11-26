intro = ["Welcome to the Starlight Casino bar! Tonight we have the best Elvis impersonator in Las Vegas. Please enjoy the show.",
         "As the show starts--BANG!--a loud gun shot is heard. The curtain comes up, and Elvis falls over. The casino's bar doors slam shut.]",
         "Everyone here is now a suspect to the murder of the Elvis impersonator. Please talk to everyone, and help me find out who the murderer is.",
         "After 15 minutes, I will ask who you think is the murderer. If you want help, please type @Botfather help language",
         "Try to find out 1) WHO is the murderer, 2) WHY did she/he commit the murder, and 3) HOW did they commit the murder."]

lang_tips = ["Try asking who has been to the casino before: 'Have you been to the casino before?'",
             "Try to find out who is married: 'Are you married?'",
             "Find out who has a gun: 'Do you have guns?'"]

tips = ["Very few of us are what we seem. -Agatha Christie",
        "When you have eliminated the impossible, whatever remains, however improbable, must be the truth. -Sherlock Holmes",
        "Good advice is always certain to be ignored, but that's no reason not to give it. -Agatha Christie",
        "Just when I thought I was out, they pull me back in.",
        "I'm going to make him an offer he can't refuse.",
        "Revenge is a dish best served cold."]

roles = ["reporter","tutor","gunnut","escort","gladiator"]  # shuffle

private_msg = {
    "reporter": ["You are the reporter, a bad boy with a reputation for using dirty tricks to get the latest news.",
                 "Your methods are not always legal..but that only matters if you get caught, right?",
                 "You have never been to the casino before.",
                 "Clue: You have been following Elvis for a story and you know that he was in a relationship with someone who was married."],
    "tutor": ["tutors gotta tute"],
    "gunnut": ["You own several guns, as a true American.",
               "You and your wife are big Elvis fans.",
               "But you saw this this Elvis impersonator before, and think he is terrible.",
               "You have been to several of his other shows and heckle him on and off stage.",
               "You are NOT the murderer.",
               "Clue: You lost your gun at the casino bar last week."],
    "escort": ["You are an escort hired by many of the Starlight Casino's most famous guests.",
               "You are proud to be high-class, and would never mix with street prostitutes.",
               "Clue: Elvis once brought the Escort to a wedding, and she tried to fool around with him afterwards but he was not interested."],
    "gladiator" : ["You are a recently-fired gladiator, and used to be best friends with Elvis.",
                   "You were previously employed by the casino to entertain the gamblers.",
                   "Elvis revealed to the owner that you were drinking on the job.",
                   "One night, very drunk, you told the dancer that planned to stab Elvis in the back (like Brutus stabbed Caesar)."]
}
