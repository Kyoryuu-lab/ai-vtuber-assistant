import asyncio
import edge_tts

stimmen = [
    "de-DE-AmalaNeural",
    "de-DE-KatjaNeural",
    "de-DE-LouisaNeural",
    "de-DE-MajaNeural",
    "de-DE-TanjaNeural",
    "de-AT-IngridNeural", # Österreichisch
    "de-CH-LeniNeural",   # Schweizerisch
    "de-DE-SeraphinaMultilingualNeural" # Eine neuere, sehr gute Stimme!
]

text = "Hallo Zhenya, mein lieber Schatz. Ich bin Lykoris. Wie gefällt dir diese Stimme für mich?"

async def generiere_proben():
    print("Generiere Sprachproben... Bitte warten.\n")
    for stimme in stimmen:
        print(f"Versuche: {stimme}...")
        communicate = edge_tts.Communicate(text, stimme)
        try:
            await communicate.save(f"Stimme_{stimme}.mp3")
            print(" -> Erfolgreich gespeichert!")
        except Exception as e:
            print(" -> FEHLER: Diese Stimme ist bei Microsoft aktuell offline oder existiert nicht mehr. Wird übersprungen!")
            
    print("\nFertig! Schau in deinen Ordner. Du hast jetzt alle funktionierenden MP3-Dateien.")

asyncio.run(generiere_proben())