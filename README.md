# GrillMeister
Eine einfache open-source Web-Applikation auf Flask-Basis zur Abstimmung von gemeinsamen Grillveranstaltungen und Frühstücken.

Die Applikation wurde über einen halben Nachmittag in einer kleinen Weiterbildungsmaßnahme nach internem Bedarf aufgesetzt und soll nun als open source Projekt weiterentwickelt werden.

Prinzipiell sind PR sehr willkommen und wir werden und beizeiten mit einer Richtlinie auseinandersetzen, aber vorerst werden wir PRs in Einzefällen reviewen und behandeln. Nach GitHub inbound=outbound Konvention lizensiert ihr durch das Beitragen von Code eure Beiträge ebenfalls unter der MIT Lizenz.

## Ausführen
Bevor du das Projekt starten kannst solltest die in einer lokalen, virtuellen Umgebung die Abhängigkeiten installieren. Dann führe im GrillMeister Ordner folgende Commands aus (selbstverständlich solltest du dir einen Geheimschlüssel generieren und an der entsprechenden Stelle einfügen):

´´´bash
export GRILLMEISTER_SECRET="your_grillmeister_secret"
FLASK_APP=grillen.py python3 -m flask run
´´´

Jetzt solltet ihr unter http://localhost:5000/grillen Bestellungen eintragen und unter http://localhost:5000/summary die Bestellungen in etwas unschönem stringified JSON als Übersicht sehen können.
Vorübergehend ist es unter http://localhost:5000/delete möglich **alle Bestellungen zu löschen**. Dies ist ein Platzhalter, damit man über das Webinteface auch resetten kann. **ES WIRD NICHT UM BESTÄTIGUNG GEFRAGT, EINFACH GELÖSCHT!**

## Geplante Features
Es gibt einige geplante Features, die wir zeitnah formalisieren wollen. Erstmal kurzfristige Ziele, hier grob als Liste:
* Flexible Auswahl für Bestellungen
* Neue Events erstellen
* Eigene Bestellungen überarbeiten, Kosten einsehen
* Templates ausbauen und Navigation erleichtern
* Summary-Seite mit Template und zusammengerechneten Bestellungszahlen und Beiträgen
* Standardisierung auf eine Sprache auf Code-Seite (nicht auf Lokalisierung bezogen)

## Disclaimer
Die Joomo GmbH bietet keinerlei Gewährleistung für diese Software (s. Lizenz). Dies ist ein open source 'Bastelprojekt'. Die Software ist nicht in einem Zustand, der sich für den produktiven Betrieb eignet.
