import cv2
from DetectDiceState import DetectDiceState
import pygetwindow as gw
import pyautogui
import pydirectinput
import time
import keyboard


# Funkcja zwraca okno o podanej nazwie
def GetWindow(name):
    try:
        window = gw.getWindowsWithTitle(name)[0]
        return window
    except IndexError:
        print("Nie znaleziono okna o takiej nazwie")
        return None


# Funkcja zwraca zrzut ekranu uzyskanego okna
def TakeScreenshot(window):
    if window is None:
        return None
    window.activate()
    time.sleep(0.1)
    screenshot = pyautogui.screenshot()
    return screenshot


# Funkcja przeklikująca dialogi w kości
# Wywoływana po sekwencji akcji w PerformInputActions
# Parametrem jest numer dialogu w kolejności
def SpamDialogue(window, dialogueNumber, exitsDialogue):
    if window is None:
        return

    window.activate()
    time.sleep(0.5)

    # Wejście do dialogu
    pyautogui.keyDown('ctrlleft')
    pyautogui.keyUp('ctrlleft')
    time.sleep(1)

    # Strzałka w dół (dialogueNumber - 1) razy
    for i in range(dialogueNumber - 1):
        pydirectinput.press('down')
        time.sleep(0.1)

    # Enter (kości)
    pyautogui.press('enter')
    time.sleep(0.1)

    # Skip dialogów
    for i in range(4):
        pyautogui.press('esc')
        time.sleep(0.1)

    # Enter x2
    # Stawka
    # Wyrzucenie kości
    pyautogui.press('enter')
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(0.1)

    # Skip dialogów
    for i in range(6):
        pyautogui.press('esc')
        time.sleep(0.1)

    # Enter
    # Moja kolej
    pyautogui.press('enter')
    time.sleep(0.1)

    # Skip dialogów
    for i in range(4):
        pyautogui.press('esc')
        time.sleep(0.1)

    # Jeżeli NPC wychodzi z dialogu, to nie robimy nic więcej
    # Inaczej klikamy opcje, by wyjść z dialogu
    if not exitsDialogue:
        pydirectinput.press('up')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.1)


# Funkcja wykonująca sekwencję akcji w zależności od tego, czy gracz wygrał czy przegrał w kości
# Inne zachowanie w przypadku, gdy NPC wychodzi z dialogu
def PerformInputActions(window, outcome):
    if window is None:
        return

    window.activate()
    time.sleep(0.1)

    if outcome == 1:
        # Wygrana:
        # Zapisz grę
        # Odczekaj
        # Kliknij ponownie
        pyautogui.keyDown('f10')
        pyautogui.keyUp('f10')
        time.sleep(6)

    else:
        # Przegrana:
        # Wczytaj grę
        # Odczekaj
        # Kliknij ponownie
        pyautogui.keyDown('f12')
        pyautogui.keyUp('f12')
        time.sleep(6)


def MainLoop(gothic_window, dialogue_number, exits_dialogue):

    # Przeklikanie kości
    SpamDialogue(gothic_window, dialogue_number, exits_dialogue)

    # Czekamy 0.5 sekundy, po czym wykonujemy zrzut ekranu
    time.sleep(0.5)
    screenshot = TakeScreenshot(gothic_window)

    # Zapis zrzutu ekranu i wczytanie za pomocą cv2
    screenshot.save("data/screenshot.png")
    screenshot = cv2.imread("data/screenshot.png")

    # Wykrywamy stan kości
    dice_state = DetectDiceState(screenshot)

    # W zależności od stanu kości wykonujemy akcje
    PerformInputActions(gothic_window, dice_state)


def main():

    gothic_name = "Gothic II - 2.6 (fix)"    # Do zmiany
    dialogue_number = 3        # Do zmiany
    exits_dialogue = False     # Do zmiany
    loop_active = False

    gothic_window = GetWindow(gothic_name)

    if gothic_window is None:
        print("Nie znaleziono okna Gothic 2")
        return

    def toggle_loop():
        nonlocal loop_active
        loop_active = not loop_active
        print("Działanie skryptu: " + str(loop_active))

    # Rejestrujemy hotkey do włączania/wyłączania skryptu
    print("On/Off shift+q")
    keyboard.add_hotkey("shift+q", toggle_loop)

    # TODO: strzałki nie działają

    try:
        while True:
            if loop_active:
                # Wykonujemy główną pętlę
                MainLoop(gothic_window, dialogue_number, exits_dialogue)

            # Czekamy przed następną iteracją
            time.sleep(2)

    except KeyboardInterrupt:
        print("Przerwano działanie skryptu")
    finally:
        keyboard.unhook_all()


if __name__ == "__main__":
    main()
