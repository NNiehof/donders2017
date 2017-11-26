intro = ["Benvenuti allo Starlight Casinò! Stasera abbiamo con noi il miglior sosia di Elvis di Las Vegas. Godetevi lo spettacolo.",
             "Appena lo spettacolo inizia, si sente un forte sparo. Il sipario di alza, ed Elvis cade. La porta del casinò sbatte.",
             "Tutti i presenti sono ora sospettati dell'omicidio del sosia di Elvis. Parlate tra di voi, e aiutatemi a capire chi è l'assassino.",
             "Dopo 15 minuti, vi chiederò chi pensate sia l'assassino. Se hai bisogno di aiuto, scrivi @botfather help",
             "Cerca di capire 1) CHI è l'assassino/a, 2) PERCHE' ha ucciso e 3) COME ha commesso l'omicidio."]

lang_tips = ["Try asking who has been to the casino before: 'Sei stato al casinò prima d'ora?'",
             "Try to find out who is married: 'Sei sposato?'",
             "Find out who has a gun: 'Hai pistole?'"]

tips = ["Solo pochi tra noi sono quello che sembrano. -Agatha Christie",
        "Una volta che hai eliminato l'impossibile, quel che rimane, per quanto improbabile, dev'essere la verità. -Sherlock Holmes",
        "Un buon consiglio sarà quasi certamente ignorato, ma non c'è motivo di non darlo. -Agatha Christie",
        "Proprio quando pensavo di esserne fuori, mi tirano di nuovo in mezzo.",
        "Gli farò una proposta che non può rifiutare.",
        "La vendetta è un piatto da servire freddo."]

roles = ["reporter","tutor","gunnut","escort","gladiator"]  # shuffle

private_msg = {
    "reporter": ["You are the reporter, a bad boy with a reputation for using dirty tricks to get the latest news.",
                 "Your methods are not always legal..but that only matters if you get caught, right?",
                 "You have never been to the casino before.",
                 "Clue: You have been following Elvis for a story and you know that he was in a relationship with someone who was married."],
    "tutor": ["tutors gotta tute"],
    "gunnut": ["Possiedi diverse pistole.",
               "Tu e tua moglie siete grandi fan di Elvis.",
               "Ma tu hai visto questo sosia di Elvis e pensi che sia pessimo.",
               "Hai assistito ad altri suoi spettacoli e hai manifestato l'hai fischiato mentre era sul palco e a spettacolo finito.",
               "NON sei l'assassino.",
               "Indizio: Hai perso la tua pistola al casinò la scorsa settimana."],
    "escort": ["Intrattieni alcuni tra i più stimati ospiti del Starlight Casino.",
               "Sei orgogliosa di essere una di alto bordo, e non ti mischieresti mai alle battone.",
               "Indizio: una volta Elvis ha portato la Escort a un matrimonio, e lei dopo ci aveva provato con lui, ma lui non era interessato."],
    "gladiator" : ["You are a recently-fired gladiator, and used to be best friends with Elvis.",
                   "You were previously employed by the casino to entertain the gamblers.",
                   "Elvis revealed to the owner that you were drinking on the job.",
                   "One night, very drunk, you told the dancer that planned to stab Elvis in the back (like Brutus stabbed Caesar)."]
}
