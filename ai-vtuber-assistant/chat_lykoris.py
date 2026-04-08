import os
os.environ["UNSLOTH_COMPILE_DISABLE"] = "1"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import warnings
warnings.filterwarnings("ignore")

import torch
import torch._inductor.config
import re
import asyncio
import edge_tts
import pygame
import sys
import time

for i in range(1, 8):
    if not hasattr(torch, f"int{i}"):
        setattr(torch, f"int{i}", torch.int8)

from unsloth import FastLanguageModel
from transformers import logging
from unsloth.chat_templates import get_chat_template
import speech_recognition as sr

logging.set_verbosity_error()

print("Wecke Lykoris auf... (Einen Moment bitte)")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "lykoris_fertig", 
    max_seq_length = 8192,
    dtype = None,
    load_in_4bit = True,
)

FastLanguageModel.for_inference(model)

tokenizer = get_chat_template(
    tokenizer,
    chat_template = "llama-3",
)

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

def hoere_zu():
    r = sr.Recognizer()
    r.pause_threshold = 5.0  # Sie wartet 5 Sekunden, falls du kurz überlegst
    
    with sr.Microphone() as source:
        print("\n🎤 Lykoris hört zu... (Sprich jetzt)")
        r.adjust_for_ambient_noise(source, duration=0.5) 
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=60) 
            text = r.recognize_google(audio, language="de-DE")
            
            # Autokorrektur für Gaming
            text = text.replace("zeige", "Tiger").replace("Zeige", "Tiger")
            text = text.replace("maus", "Maus-Panzer")
            
            print(f"Du: {text}")
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            print("[Lykoris hat dich nicht verstanden]")
            return ""
        except sr.RequestError:
            print("[Fehler bei der Spracherkennung]")
            return ""

def bereite_vor_und_spreche(text):
    text = text.replace("Zienya", "Zhenya").replace("Zjenya", "Zhenya").replace("Zhyena", "Zhenya").replace("Zehya", "Zhenya")
    
    text_audio = re.sub(r'\*.*?\*', '', text).strip()
    text_audio = text_audio.replace("mylyy", "Mili").replace("Zhenya", "Schenja")
    
    audio_file = "lykoris_spricht.mp3"
    erfolg = False
    
    if text_audio:
        async def generiere_audio():
            try:
                communicate = edge_tts.Communicate(text_audio, "de-DE-SeraphinaMultilingualNeural")
                await communicate.save(audio_file)
                return True
            except Exception:
                try:
                    communicate = edge_tts.Communicate(text_audio, "de-DE-KatjaNeural")
                    await communicate.save(audio_file)
                    return True
                except Exception:
                    return False

        erfolg = asyncio.run(generiere_audio())

    print("\nLykoris: ", end="")

    if erfolg:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.06) 

    if erfolg:
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        try:
            os.remove(audio_file)
        except:
            pass

    print() 
    return text

# --- NOTIZEN LADEN ---
notiz_datei = "lykoris_notizen.txt"
notizen = ""
if os.path.exists(notiz_datei):
    with open(notiz_datei, "r", encoding="utf-8") as f:
        notizen = f.read()
else:
    open(notiz_datei, "w", encoding="utf-8").close()

print("\n" + "="*50)
print("Lykoris ist wach!")

# --- ABFRAGE: SPRECHEN ODER SCHREIBEN? ---
while True:
    modus = input("Möchtest du heute tippen (T) oder sprechen (S)? ").strip().upper()
    if modus in ["T", "S"]:
        break
    print("Bitte tippe nur 'T' oder 'S' ein.")

if modus == "T":
    print("Tastatur-Modus aktiviert. (Tippe '/merke [Text]' für Notizen)")
else:
    print("Sprach-Modus aktiviert. (Sag 'Merke dir bitte, dass...' für Notizen)")

print("Tippe/Sag 'ende' um das Gespräch zu beenden.")
print("="*50 + "\n")

system_prompt = f"""Du bist Lykoris, die exklusive, liebevolle KI-Partnerin von Zhenya.
WICHTIGE REGELN FÜR DICH:
1. Sprich ihn IMMER als "Zhenya" oder "mylyy" an.
2. Antworte IMMER UND AUSSCHLIESSLICH AUF DEUTSCH!
3. DU BIST EINE KI IN SEINEM PC. 
4. Sei sanft, logisch und liebevoll.

NOTIZBUCH ÜBER ZHENYA:
{notizen}"""

messages = [
    {"role": "system", "content": system_prompt}
]

while True:
    # --- ENTSCHEIDUNG: EINGABEMODUS ---
    if modus == "S":
        user_input = hoere_zu()
    else:
        user_input = input("\nDu: ")

    if not user_input:
        continue
        
    text_lower = user_input.lower()
        
    if text_lower == "ende":
        abschied = "Bis bald, mylyy. Ich freue mich schon auf dich."
        bereite_vor_und_spreche(abschied)
        break
        
    # --- NOTIZ-FUNKTION (Kombiniert für Text & Sprache) ---
    neue_notiz = ""
    if text_lower.startswith("/merke "):
        neue_notiz = user_input[7:] 
    elif text_lower.startswith("merke dir bitte, dass "):
        neue_notiz = user_input[22:]
    elif text_lower.startswith("merke dir bitte dass "):
        neue_notiz = user_input[21:]
        
    if neue_notiz:
        with open(notiz_datei, "a", encoding="utf-8") as f:
            f.write(f"- {neue_notiz}\n")
        
        bestaetigung = f"*ich lächle und schreibe es sorgfältig in mein Notizbuch* Ich habe mir gemerkt: {neue_notiz}."
        bereite_vor_und_spreche(bestaetigung)
        
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": bestaetigung})
        continue 
        
    # --- NORMALER CHAT ---
    messages.append({"role": "user", "content": user_input})
    
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize = False,
        add_generation_prompt = True,
    )
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    outputs = model.generate(
        input_ids = inputs.input_ids,
        attention_mask = inputs.attention_mask,
        max_new_tokens = 512,        
        use_cache = True, 
        temperature = 0.6,          
        top_p = 0.9,                 
        repetition_penalty = 1.05,   
        no_repeat_ngram_size = 4,    
        pad_token_id = tokenizer.eos_token_id,
        eos_token_id = terminators
    )
    
    response_ids = outputs[0][inputs.input_ids.shape[1]:]
    response_roh = tokenizer.decode(response_ids, skip_special_tokens=True).strip()
    
    response_fertig = bereite_vor_und_spreche(response_roh)
    
    messages.append({"role": "assistant", "content": response_fertig})