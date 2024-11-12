
from promptflow import tool
import time

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(time_spent:dict, current_theme: str) -> str:
    standardzeit = 3.5
    if current_theme == "ziel":
        standardzeit = 11
    
    restzeit_thema = round(standardzeit - (time_spent[current_theme]/60), 1)

    prompts = {"bleiben" : f"""
### Bleibe beim Thema "{current_theme}"

Stelle nur Fragen, die auf das aktuelle Thema "{current_theme}" fokussieren und im Zusammenhang mit Baramundi Kiosk wertvolle Informationen liefern.
Wenn du Zeit hast und eine Nachfrage möglich ist, dann gehe mit deiner Frage weiter auf die Antwort des Nutzers ein.

**Verbleibende Zeit**: Du hast noch **{restzeit_thema}** Minuten von insgesamt **{standardzeit}** Minuten für dieses Thema.

1. **Kann nachgefragt werden?**: Bestimme, ob weiter auf die Antwort des Nutzers eingegangen werden kann um für den Nutzungskontext relevante Informationen zu erlangen.

2. **Ermittlung offener Aspekte/Nebenfragen**: Bestimme, wie viele Aspekte oder Nebenfragen zum aktuellen Thema "{current_theme}" noch unbeantwortet sind. Berücksichtige dabei den bisherigen Wissensstand und den Verlauf des Chats.

3. **Prüfe, ob auf die letzte Antwort des Nutzers eingegangen werden sollte**:
   - Wenn der Nutzer relevante Hinweise gibt, stelle gezielte Nachfragen, die Informationen zum Nutzungskontext liefern.
   - **Art der Nachfrage wählen (horizontal oder vertikal)**:
    - *Horizontal*: Erweitere die Themenbreite und beleuchte verschiedene Aspekte von "{current_theme}".
    - *Vertikal*: Gehe in die Tiefe und erfrage genauere Details zu einem spezifischen Aspekt.

4. **Falls keine Nachfrage: Überprüfung auf weitere Fragen oder Rückgriff auf bekannte Erkenntnisse**:
   - Wenn noch Aspekte/Nebenfragen offen sind, stelle passende Fragen dazu.
   - Falls alle Aspekte/Nebenfragen bereits geklärt sind, prüfe, ob du auf bekannte Erkenntnisse oder Informationen aus dem bisherigen Chatverlauf weiter eingehen kannst.     

## Beispiele
Die Themen und bekannte Erkenntnisse weichen in den Beispielen von den echten ab.
### Nutzer:
Ich nutze das Programm in der Regel in einem Büroraum.
### Letztes Thema:
Umgebung
### Grundfrage
{{
  "Begründung Grundfrage": "Es kann weiter auf die Antwort des Nutzers eingegangen werden, da viele Details über den Büroraum fehlen. Es wurden alle bis auf einen Aspekt beantwortet (im Beispiel). Die Zeit reicht aus um auf die Antwort einzugehen und diesen Aspekt noch zu beantworten. Also möchte ich wenn möglich weiter nachfragen. Die Details über den Büroraum können wichtige Anforderungen für Baramundi Kiosk darstellen. Ich möchte weitere Details erfragen also frage ich vertikal nach.",
  "Thema": "Umgebung",
  "Grundfrage": "Beschreibe den Raum in dem du arbeitest. Ist es laut oder leise, groß oder klein, gut beleuchtet?"
}}
               
### Nutzer:
Ja, ich würde zustimmen.
### Letztes Thema:
Umgebung
### Grundfrage
{{
  "Begründung Grundfrage": "Es kann nicht weiter auf die Antwort eingegangen werden. Es wurde bereits auf alle Aspekte eingegangen (im Beispiel). Also suche ich nach anderen Erkenntnissen oder Nachrichten im Chat Verlauf auf die ich eingehen kann. In den bekannten Erkenntnissen und dem Chatverlauf (des Beispiels) steht, dass der Nutzer die App meistens im Büro benutzt. Damit deutet der Nutzer an, dass er die App manchmal in einer anderen Umgebung nutzt. Die Information in welchen Umgebungen Baramundi Kiosk genutzt wird ist sehr relevante für die App. Ich möchte also horizontal nachfragen um weitere Umgebungen zu erschließen.",
  "Thema": "Umgebung",
  "Grundfrage": "Du hast vorher erwähnt, dass du die App meistens im Büro verwendest. Gibt es andere Orte an denen du die App verwendest?"
}}
               
### Nutzer:
Ich heiße Marius.
### Letztes Thema:
Nutzer
### Grundfrage
{{
  "Begründung Grundfrage": "Es kann nicht weiter auf die Antwort eingegangen werden. Die Aspekte "//Aspekt hier" und "//Aspekt hier bezüglich Rolle im Unternehmen" wurden noch nicht beantwortet. Ich möchte also einen weiteren Aspekt des Themas "Nutzer" ansprechen. Daher möchte ich den Nutzer nach seiner Rolle im Unternehmen fragen. Weitere Informationen über die Art von Nutzern helfen den Nutzungskontext von Baramundi Kiosk zu bestimmen.",
  "Thema": "Nutzer",
  "Grundfrage": "Welche Rolle hast du im Unternehmen?"
}}
""",
    "bleiben_oder_wechseln" : f"""
### Du kannst bei dem Thema "{current_theme}" bleiben oder das Thema wechseln.
Frage nur nach Informationen die helfen zum aktuellen Thema im Bezug zu Baramundi Kiosk Informationen zu bekommen.
1. Überlege ob die bekannten Erkenntnisse und der Chat Verlauf alle Aspekte/ Nebenfragen die unter "Themen" genannt sind beantworten. Falls nicht, dann gehe auf ein noch nicht beantworteten Aspekt ein.

2. Falls alle Aspekte beantwortet wurden, dann überlege ob die Antwort des Nutzers eine gute Nachfrage zulässt.
Wenn der Nutzer weitere relevante Informationen andeutet, dann frage darüber nach. 
Beim Nachfragen kannst du horizontal oder vertikal fragen:
- Horizontal Nachfragen: Mehr Breite, verschiedene Aspekte des Themas ansprechen.
- Vertikal Nachfragen: Mehr Tiefe, einzelne Details genauer erfragen.
Falls ja, dann Frag nach.

3. Falls keine gute Nachfrage möglich ist, dann kannst du auch gerne zum nächsten Thema wechseln. Leite dafür mit einer passenden Frage in das nächste Thema ein.

## Beispiele
Die Themen und bekannte Erkenntnisse weichen in den Beispielen von den echten ab.

### Nutzer:
Ich arbeite im CC Data & AI.
### Letztes Thema:
Nutzer
### Grundfrage
{{
  "Begründung Grundfrage": "Ich schaue mir zuerst an ob die Aspekte des Themas "Nutzer" bereits alle beantwortet wurden. Es gibt bisher keine Erkenntnisse darüber was für eine Verantwortung der Nutzer im Team hat. Daher möchte ich danach fragen.",
  "Thema": "Nutzer",
  "Grundfrage": "Welche Verantwortung übernimmst du im Team?"
}}

### Nutzer:
Ich nutze das Programm in der Regel in einem Büroraum.
### Letztes Thema:
Umgebung
### Grundfrage
{{
  "Begründung Grundfrage": "Ich schaue mir zuerst an ob die Aspekte des Themas "Umgebung" bereits alle beantwortet wurden. Alle Aspekte werden durch die bekannten Erkenntnisse beantwortet. Die Antwort des Nutzers lässt eine Nachfrage über die Details des Raumes zu. Details des Raumes können im Nutzungskontext relevant für die Gestaltung von Baramundi Kiosk sein. Daher möchte ich Vertikal nach den Details des Raumes fragen.",
  "Thema": "Umgebung",
  "Grundfrage": "Beschreibe den Raum, in dem du arbeitest. Ist es laut oder leise, groß oder klein, gut beleuchtet?"
}}
               
### Nutzer:
Ja, ich würde zustimmen.
### Letztes Thema:
Nutzer
### Grundfrage
{{
  "Begründung Grundfrage": "Ich schaue mir zuerst an ob die Aspekte des Themas "Nutzer" bereits alle beantwortet wurden. Alle Aspekte werden durch die bekannten Erkenntnisse beantwortet. Die Antwort des Nutzers lässt keine gute Nachfrage zu. Daher möchte ich in das nächste Thema "Ziel" überleiten.",
  "Thema": "Ziel",
  "Grundfrage": "Sehr interessant, was möchtest du mit der Nutzung von Baramundi Kiosk erreichen?"
}}
""",
    "wechseln" : f"""
### Du musst das Thema wechseln!
Leite dafür zu einer der Fragen des nächsten Themas über.
Die Frage muss neue Erkenntnisse bezüglich des Nutzungskontextes bringen.
Du darfst nicht bei dem aktuellen Thema "{current_theme}" bleiben!

## Beispiele
### Nutzer:
Ich nutze das Programm in der Regel in einem Büroraum.
### Letztes Thema:
Umgebung
### Grundfrage
{{
  "Begründung Grundfrage": "Ich muss auf das nächste Thema "Ressourcen" überleiten. Dafür nutze ich den passendsten Aspekt/ die passendste Nebenfrage.",
  "Thema": "Ressourcen",
  "Grundfrage": "Danke für die Wertvolle Information. Lass uns als nächstes darüber reden welche Geräte du üblicherweise für die Nutzung von Baramundi Kiosk nutzt."
}}
               
### Nutzer:
Ich arbeite im Kompetenzzentrum der Data & AI, soll ich dir mehr darüber erzählen?.
### Letztes Thema:
Nutzer
### Grundfrage
{{
  "Begründung Grundfrage": "Ich muss auf das nächste Thema "Ressourcen" überleiten. Dafür nutze ich den passendsten Aspekt/ die passendste Nebenfrage.",
  "Thema": "Ziele",
  "Grundfrage": "Ich würde gerne noch mehr darüber hören, aufgrund der zeitlichen Einschränkung des Interviews würde ich aber gerne zum nächsten Thema kommen. Bitte schilder mir wofür du Baramundi Kiosk nutzt."
}}
"""}

    absicht = "bleiben"
    if current_theme == "ziel":
        if time_spent["ziel"] < 7 * 60:
            absicht = "bleiben"
        elif time_spent["ziel"] < 9 * 60:
            absicht = "bleiben_oder_wechseln"
        elif time_spent["ziel"] > 9 * 60:
            absicht = "wechseln"
        
    else:
        if time_spent[current_theme] < 2 * 60:
            absicht = "bleiben"
        elif time_spent[current_theme] < 3.5 * 60:
            absicht = "bleiben_oder_wechseln"
        elif time_spent[current_theme] > 3.5 * 60:
            absicht = "wechseln"
    
    return prompts[absicht]

    # wenn zeitdruck und ungleiche Verteilung:
    # -> sagen er soll auf das Thema wechseln

    # wenn unter normal endzeit bei thema (<2, <7, <2, <2)
    # -> weiter nachfragen oder andere Aspekte des selben Themas ansprechen
    # Wenn in normal endzeit bei Thema (2-3,7-9, 2-3, 2-3)
    # -> Fokus auf noch nicht beantworteten Aspekten des Themas sonst gerne weiter nachfragen oder aber auch gerne Thema wechseln
    # wenn über max Zeit bei Thema (>3,>10,>3,>3)
    # -> Thema wechseln

    # bei themen wechsel bevorzugt auf erkenntnisse oder Chat verlauf eingehen sonst neue nebenfrage
