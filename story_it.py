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

roles = ["tutor","gunnut","escort","gladiator","reporter"]  # shuffle

private_msg = {
    "reporter": ["Tu sei il giornalista, un cattivo ragazzo con la reputazione di usare trucchi sporchi per ottenere le ultime notizie.",
                 "I tuoi metodi non sono sempre legali ... ma questo è importante solo se vieni catturato, giusto?",
                 "Non sei mai stato al casinò prima d'ora.",
                 "Indizio: Hai seguito Elvis per una storia e sai che era in una relazione con qualcuno che era sposato."],
    "tutor": ["Sei l'assassino. Gli altri avranno indizi che potrebbero portare a te.",
              "Devi dire agli altri che:",
              "- Sei un maestro di canto che lavorava con Elvis sulla sua voce.",
              "- Spesso gli hai dato lezioni private al casinò per stare con lui.",
              "- Hai una moglie (che non è al casinò questa sera).",
              "I fatti che seguono sono segreti, ma se qualcuno di fa domande NON puoi mentire:",
              "- Avevi una relazione sessuale con Elvis.",
              "- Avevi promesso a Elvis che avresti lasciato tua moglie per lui, ma non hai mai pensato di farlo davvero.",
              "- Elvis aveva capito che non avresti mai lasciato tua moglie per lui e aveva minacciato di rendere pubblica la vostra relazione.",
              "- Hai preso la pistola del matto (l'aveva dimenticata al casinò una notte) e hai sparato a Elvis quando il sipario si è alzato.",
              "- Te la sei svignata mischiandoti alla folla e al caos."],
    "gunnut": ["Possiedi diverse pistole.",
               "Tu e tua moglie siete grandi fan di Elvis.",
               "Ma tu hai visto questo sosia di Elvis e pensi che sia pessimo.",
               "Hai assistito ad altri suoi spettacoli e hai manifestato l'hai fischiato mentre era sul palco e a spettacolo finito.",
               "NON sei l'assassino.",
               "Indizio: Hai perso la tua pistola al casinò la scorsa settimana."],
    "escort": ["Intrattieni alcuni tra i più stimati ospiti del Starlight Casino.",
               "Sei orgogliosa di essere una di alto bordo, e non ti mischieresti mai alle battone.",
               "Indizio: una volta Elvis ha portato la Escort a un matrimonio, e lei dopo ci aveva provato con lui, ma lui non era interessato."],
    "gladiator" : ["Tu ed Elvis eravate migliori amici.",
                   "In passato hai lavorato per il casinò, intrattenevi i giocatori d'azzardo.",
                   "Elvis ha rivelato al padrone che tu bevevi sul lavoro.",
                   "Una notte, molto ubriaco, hai detto alla ballerina che avevi intenzione di pugnalare Elvis alla schiena (come Bruto fece con Cesare)."]
}
