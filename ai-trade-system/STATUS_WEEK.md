# STATUS_WEEK_1

## Maandag
* Tim Schelpe: Gitlab opzetten en stock data pullen onderwerp onderzoeken
* Laurien Cools: Gitlab opzetten, stock data pullen en onderwerp onderzoeken
* Elias Malomgré: Gitlab opzetten en onderwerp onderzoeken

## Dinsdag
* Tim Schelpe: Python Mongo databank opzetten en diagram architectuur opstellen
* Laurien Cools: Onderzoek naar Policy gradient methodes
* Elias Malomgré: Architectuur van project opzetten en hiervoor diagram opstellen

## Woensdag
* Tim Schelpe: Stock data pullen en Mongo databank in architectuur verwerkt
* Laurien Cools: Onderzoek naar Policy gradient methodes
* Elias Malomgré: Buy en sell transacties aangemaakt

## Donderdag
* Tim Schelpe: Onderzoek hoe python werkt
* Laurien Cools: Onderzoek naar Policy gradient methodes en demo project opzetten
* Elias Malomgré: Onderzoek naar Policy gradient methodes, demo project opzetten en buy en sell transacties afgewerkt

## Globale stand
De basis van het project is klaar. Stock gegevens kunnen voor een bepaalde periode opgevraagd worden en opgeslagen worden in de databank. Er kunnen op bepaalde momenten in de stockhistoriek transacties aangemaakt worden. Er is een demo project voor een Policy gradient methode gemaakt. We denken ~16% klaar te zijn.


# STATUS_WEEK_2

## Maandag
* Tim Schelpe: Zoeken naar framework om candlesticks chart
* Laurien Cools: Onderzoek naar policy gradient in documenten
* Elias Malomgré: Onderzoek naar policy gradient in documenten

## Dinsdag
* Tim Schelpe: Vue project en mongo repository aangemaakt 
* Laurien Cools: Policy gradient proberen omzetten naar praktijk
* Elias Malomgré: Policy gradient proberen omzetten naar praktijk

## Woensdag
* Tim Schelpe: Verder uitwerken vue project
* Laurien Cools: Mountain car project oplossen met policy gradient
* Elias Malomgré: Mountain car project oplossen met policy gradient

## Donderdag
* Tim Schelpe: Annotations op chart (Grote bug oplossen)
* Laurien Cools: Voorbeeld code proper gemaakt en deze naar echt project verplaatst. Environment klasse en simulator uitgewerkt
* Elias Malomgré: Voorbeeld code proper gemaakt en deze naar echt project verplaatst. Environment klasse en simulator uitgewerkt

## Globale stand
Position, transactions en historical data ophalen en weergeven in een front end project. Goede architectuur van ai component aangemaakt. Werkende A2C policy gradient methode toegevoegd. Agent klasse uitgewerkt. Link tussen project en ai component via environment zo goed als afgemaakt. We denken 35% klaar te zijn.

# STATUS_WEEK_3

## Maandag
* Tim Schelpe: Stop loss proberen tonen op candlestick chart met lijn
* Laurien Cools: 4 policy gradient methodes toegevoegd en aanpassingen agent
* Elias Malomgré: 4 policy gradient methodes toegevoegd en aanpassingen agent

## Dinsdag
* Tim Schelpe: Stop loss tonen op candlestick chart met puntjes en data parsing aangepast
* Laurien Cools: Code aangepast voor toelating van meerdere bars in een state
* Elias Malomgré: Code aangepast voor toelating van meerdere bars in een state

## Woensdag
* Tim Schelpe: Herstructurering webapplicatie
* Laurien Cools: Ai training zonder gebruik te maken van databank
* Elias Malomgré: Ai training zonder gebruik te maken van databank

## Donderdag
* Tim Schelpe: Herstructurering webapplicatie en maken testdata
* Laurien Cools: Opgeslagen weights 
* Elias Malomgré: Bugs uit code halen en onderzoeken policy gradient met meerdere outputs

## Globale stand
Ai kan transacties uitvoeren en kan meerdere waardes generen met enkele niet opgeloste bugs. Er kunnen meerdere bars gebruikt worden in een state. Er zijn 4 policy gradient methodes toegevoegd en de settings van deze metodes kunnen in de Properties klasse aangepast worden. De webapplicatie is volledig functioneel. We denken aan dat we ongeveer 60% klaar zijn.


# STATUS_WEEK_4

## Maandag
* Tim Schelpe: Video's reinforcement learning bekeken en begonnen aan frozenlake
* Laurien Cools: Ai meerdere waarden laten outputten
* Elias Malomgré: Ai meerdere waarden laten outputten

## Dinsdag
* Tim Schelpe: Frozenlake uitgewerkt
* Laurien Cools: Opslaan van positions
* Elias Malomgré: Opslaan van positions

## Woensdag
* Tim Schelpe: Deepqlearning bekeken
* Laurien Cools: Stocksimulator proper gemaakt en andere manier om acties te bepalen uitgewerkt
* Elias Malomgré: Stocksimulator proper gemaakt en andere manier om acties te bepalen uitgewerkt 

## Donderdag
* Tim Schelpe: Front-end up to date gebracht
* Laurien Cools: Weights van actor model opslaan, Rewards proberen finetunen en agent summary laten tonen
* Elias Malomgré: Weights van actor model opslaan, Rewards proberen finetunen en agent summary laten tonen

## Globale stand
Webapplicatie is functioneel uitgewerkt. Ai kan meerdere waarden outputten en kan aan de hand van deze outputs alle transacties uitvoeren. Bij foutieve acties wordt de ai afgestraft. De weights van alle models kunnen opgeslagen worden. We denken 75% klaar te zijn.

# STATUS_WEEK_5

## Maandag
* Tim Schelpe: Deep q learning bestudeerd
* Laurien Cools: Transaction testen weer werkende krijgen
* Elias Malomgré: Transaction testen weer werkende krijgen

## Dinsdag
* Tim Schelpe: Deep q learning bestudeerd
* Laurien Cools: Bugs oplossen en grafiek van rewards history
* Elias Malomgré: Bugs oplossen en grafiek van rewards history

## Woensdag
* Tim Schelpe: Verbinding front en back end
* Laurien Cools: Bugs oplossen
* Elias Malomgré: Bugs oplossen

## Donderdag
* Tim Schelpe: Verbinding front en back end
* Laurien Cools: AI laten werken met enkel kopen en verkopen
* Elias Malomgré: AI laten werken met enkel kopen en verkopen

## Globale stand
De webapplicatie is performanter geworden, heeft eenlaadschermen en een infoscherm. De functionaliteit van de simulator is zo goed als klaar. De AI kan ook trainen met enkel kopen en verkopen. De AI lijkt wel nog niet bij te leren. We denken 90%.
