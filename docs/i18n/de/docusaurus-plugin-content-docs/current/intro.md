---
sidebar_position: 1
---

# Tutorial

Lass uns Spotch Bot zusammen einrichten!

## Installation

Lade die neueste Version von Spotch Bot von den Releases herunter:  
[Releases](https://github.com/lvl13Mage/spotch-bot/tags)

Wir unterstützen Linux und Windows.

Entpacke den ZIP-Inhalt in ein Verzeichnis deiner Wahl.

## Bot starten

Führe die Datei im Verzeichnis aus, um den Spotch Bot zu starten.

Es wird ein Terminalfenster und dein Browser mit einem neuen Tab geöffnet.

:::note
In zukünftigen Versionen könnten wir das Terminalfenster entfernen.
:::
![img alt](/img/tutorial/spotchbot-firstpage.png)

## Konfiguration

Damit Spotch Bot funktioniert, musst du eine Spotify Developer App und eine Twitch Developer App einrichten.

### Spotify Developer App einrichten

1. Navigiere zu den Spotify-Einstellungen in Spotch Bot.  
![img alt](/img/tutorial/spotch-spotify-setup.png)

2. Besuche die Spotify Developer Website und melde dich an:  
[https://developer.spotify.com/](https://developer.spotify.com/)

3. Gehe nach dem Anmelden zum Dashboard:  
[https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)

4. Klicke auf "App erstellen"  
![img alt](/img/tutorial/spotify-dev-creation1.png)

5. Fülle die Informationen aus  
⚠️ Stelle sicher, dass du die "Redirect URI" aus Schritt 1 einfügst  
![img alt](/img/tutorial/spotify-dev-creation2.png)

6. Kopiere die Client-ID und das Client-Geheimnis in die Spotch Bot App  
![img alt](/img/tutorial/spotify-dev-creation3.png)  
![img alt](/img/tutorial/spotify-dev-creation4.png)

7. Klicke auf Speichern und authentifiziere dich dann in der Spotch App  
Ein neuer Tab sollte sich öffnen und um Erlaubnis bitten.  
Nach der Annahme solltest du dies sehen:  
```{"Token erhalten":true}```

Deine Spotify-App ist jetzt authentifiziert!

### Twitch Developer App einrichten

1. Navigiere zu den Twitch-Einstellungen in Spotch Bot.  
![img alt](/img/tutorial/spotch-twitch-setup.png)

2. Besuche die Twitch Developer Website und melde dich an:  
[https://dev.twitch.tv/](https://dev.twitch.tv/)

3. Gehe nach dem Anmelden zur Konsole -> Anwendungsbereich:  
[https://dev.twitch.tv/console/apps](https://dev.twitch.tv/console/apps)

4. Klicke auf "+ Deine Anwendung registrieren"  
![img alt](/img/tutorial/twitch-dev-create.png)

5. Fülle die Informationen aus  
⚠️ Stelle sicher, dass du die "Redirect URI" aus Schritt 1 einfügst  
![img alt](/img/tutorial/twitch-dev-create2.png)

6. Wenn die App erstellt wurde, klicke auf "Verwalten"  
![img alt](/img/tutorial/twitch-dev-create3.png)

7. Kopiere die Client-ID und das Client-Geheimnis in die Spotch App  
⚠️ Drücke auf "Neues Geheimnis", um das Geheimnis sichtbar zu machen  
![img alt](/img/tutorial/twitch-dev-create4.png)  
![img alt](/img/tutorial/twitch-dev-create5.png)

8. Klicke auf Speichern und authentifiziere dich in der Spotch App  
Ein neuer Tab sollte sich öffnen und um Erlaubnis bitten.  
Nach der Annahme solltest du dies sehen:  
```{"message":"Zugriffstoken erhalten und Anwendung erfolgreich neu gestartet!"}```

Deine Twitch-App ist jetzt authentifiziert!

### Kanalpunkt-Belohnungen

![img alt](/img/tutorial/spotchbot-rewards-list.png)
