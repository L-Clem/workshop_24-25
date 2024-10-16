from pynput import keyboard
import time
import re
import threading
# import gui
import model as ml



texte_capture = ""
score_total = 0
dernier_reset = time.time()
SEUIL_ALERTE = 0.7  # Seuil pour le sentiment négatif
SEUIL_POPUP = 2.1  # Seuil pour déclencher le pop-up (3 * SEUIL_ALERTE)
DUREE_RESET = 300  # 5 minutes en secondes


def run():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def detecter_humour(texte):
    texte_lower = texte.lower()
    return any(re.search(r'\b' + re.escape(exp) + r'\b', texte_lower) for exp in expressions_humoristiques)

def analyser_texte(texte):
    global score_total, dernier_reset
    
    contexte_humoristique = detecter_humour(texte)
    sentiment_scores = ml.analyser_sentiment(texte)
    sentiment_negatif = sentiment_scores[0]  # Indice 0 pour le sentiment négatif
    
    print(f"\nPhrase analysée : '{texte}'")
    print(f"Score de sentiment négatif : {sentiment_negatif:.2f}")
    
    if contexte_humoristique:
        print("Contexte humoristique détecté, score ajusté.")
        sentiment_negatif *= 0.5  # Réduire le score négatif de moitié si contexte humoristique
    
    if sentiment_negatif > SEUIL_ALERTE:
        temps_actuel = time.time()
        if temps_actuel - dernier_reset > DUREE_RESET:
            score_total = 0
            dernier_reset = temps_actuel
        
        score_total += sentiment_negatif
        print(f"Score total de négativité : {score_total:.2f}")
        
        if score_total >= SEUIL_POPUP:
            print("\n!!! ALERTE : Niveau de négativité critique atteint !!!")
            print("Une intervention peut être nécessaire.")
            # threading.Thread(target=gui.afficher_alert_popup).start()
        
        return True
    return False

def on_press(key):
    global texte_capture
    try:
        if key == keyboard.Key.enter:
            if analyser_texte(texte_capture):
                print("Attention : Ce message pourrait être considéré comme négatif ou offensant.")
            else:
                print(f"\nTexte analysé (aucun contenu négatif significatif détecté)")
            texte_capture = ""
        elif key == keyboard.Key.space:
            texte_capture += " "
        else:
            texte_capture += key.char
    except AttributeError:
        if key == keyboard.Key.backspace:
            texte_capture = texte_capture[:-1]

def on_release(key):
    if key == keyboard.Key.esc:
        return False
