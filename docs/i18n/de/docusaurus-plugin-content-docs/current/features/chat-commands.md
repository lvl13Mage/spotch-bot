---
sidebar_position: 1
---

# Chat-Befehle

Spotch Bot bietet eine Vielzahl von Chat-Befehlen, um nahtlos mit Twitch und Spotify zu interagieren. Diese Befehle ermöglichen es Streamern und ihren Moderatoren, Songanfragen zu verwalten, die Song-Warteschlange zu steuern und in Echtzeit mit Zuschauern zu interagieren.

## Verfügbare Befehle

### `!songqueue` (Aliase: `!sq`)
**Beschreibung**: Zeigt die aktuelle Song-Warteschlange an.

- **Verwendung**: `!songqueue`
- **Antwort**: Listet die Songs in der aktuellen Warteschlange auf.
- **Beispiel**:
  ```
  1️⃣ Künstler 1 - Song 1 2️⃣ Künstler 2 - Song 2
  ```

---

### `!lastsongs` (Aliase: `!ls`)
**Beschreibung**: Zeigt die zuletzt gespielten Songs an.

- **Verwendung**: `!lastsongs`
- **Antwort**: Listet die zuletzt gespielten Songs auf.
- **Beispiel**:
  ```
  1️⃣ Künstler 1 - Song 1 2️⃣ Künstler 2 - Song 2
  ```

---

### `!currentsong` (Aliase: `!cs`)
**Beschreibung**: Zeigt den aktuell gespielten Song an.

- **Verwendung**: `!currentsong`
- **Antwort**: Zeigt den Künstler und den Titel des aktuell gespielten Songs an.
- **Beispiel**:
  ```
  🎵 Jetzt spielt: Künstler - Songtitel
  ```

---

### `!findsong` (Aliase: `!searchsong`, `!fs`)
**Beschreibung**: Sucht nach einem Song auf Spotify. 
:::warning
**(Noch nicht implementiert)**
:::

- **Verwendung**: `!findsong <Songname>`
- **Antwort**: Sucht auf Spotify nach dem angegebenen Song und zeigt das Ergebnis an.
- **Beispiel**:
  ```
  🔍 Gefunden: Künstler - Songtitel
  ```

---

### `!skip`
**Beschreibung**: Überspringt den aktuell gespielten Song.  
**Berechtigung**: Nur Moderatoren.

- **Verwendung**: `!skip`
- **Antwort**: Überspringt den aktuellen Song und wechselt zum nächsten in der Warteschlange.
- **Beispiel**:
  ```
  ⏭ Song übersprungen.
  ```