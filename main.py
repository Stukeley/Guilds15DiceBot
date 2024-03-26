import cv2
from enum import Enum
import pygetwindow as gw
import pyautogui
import time
import keyboard
import pydirectinput


class Resolution(Enum):
    P1080 = 1080,
    P1440 = 1440


def process_image(path, resolution=Resolution.P1080):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    sub_images = []

    if resolution == Resolution.P1080:
        cropped_image = image[200:400, 775:975]

        for y_start in [0, 120]:
            for x_start in [0, 135]:
                # Pierwsze wycięcie, wycięcie kości wraz z obszarem wokół
                sub_image = cropped_image[y_start:y_start+75, x_start:x_start+75]
                sub_image = cv2.resize(sub_image, (100, 100))
                # Drugie wycięcie, wycięcie samej kości
                sub_image = sub_image[20:80, 20:80]
                sub_images.append(sub_image)
    elif resolution == Resolution.P1440:
        # Pozycje kości w 1440p:
        # 1050:1110, 290:345
        # 1050:1110, 447:504
        # 1228:1292, 290:345
        # 1228:1292, 447:504
        for y_start in [290, 448]:
            for x_start in [1050, 1230]:
                sub_image = image[y_start:y_start+57, x_start:x_start+62]
                sub_image = cv2.resize(sub_image, (100, 100))
                sub_images.append(sub_image)

    return sub_images


def threshold_image(gray):
    threshed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return threshed


def count_dots(threshed, image):
    cnts = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 500:
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opening = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, kernel, iterations=3)

    # Znalezienie konturów
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        # Sprawdzenie, czy kontur jest odpowiedniej wielkości
        area = cv2.contourArea(c)
        if area > 20 and area < 50:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)

    return len(cnts)


def get_window(name):
    try:
        window = gw.getWindowsWithTitle(name)[0]
        window.activate()
        return window
    except IndexError:
        print(f"Okno o nazwie {name} nie zostało znalezione")
        return None


def take_screenshot(window):
    if window is None:
        return None
    window.activate()
    time.sleep(0.1)
    screenshot = pyautogui.screenshot()
    return screenshot


def spam_dialogue(window, dialoguenumber, exitsdialogue):
    if window is None:
        return

    window.activate()
    time.sleep(0.5)

    # Wejście do dialogu
    pyautogui.keyDown('ctrlleft')
    pyautogui.keyUp('ctrlleft')
    time.sleep(1)

    # Strzałka w dół (dialogueNumber - 1) razy
    for i in range(dialoguenumber - 1):
        pydirectinput.press('down')
        time.sleep(0.1)

    # Enter (kości)
    pyautogui.press('enter')
    time.sleep(0.1)

    # Skip dialogów
    for i in range(4):
        pyautogui.press('esc')
        time.sleep(0.1)

    time.sleep(0.2)

    # Enter x2
    # Stawka
    # Wyrzucenie kości
    pyautogui.press('enter')
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(0.1)
    
    time.sleep(0.2)

    # Skip dialogów
    for i in range(3):
        pyautogui.press('esc')
        print(f"{i} Dialog skipnięty")
        time.sleep(0.1)
        
    time.sleep(0.2)
    
    # Enter
    # Rzuć pierwszy
    pyautogui.press('enter')
    print("Rzuć pierwszy")
    time.sleep(0.2)
    
    # Skip dialogów
    for i in range(3):
        pyautogui.press('esc')
        print(f"{i} Dialog skipnięty w drugiej turze")
        time.sleep(0.1)

    # Enter
    # Moja kolej
    pyautogui.press('enter')
    print("Moja kolej")
    time.sleep(0.2)
    
    # Teraz na ekranie będą już wszystkie kości
    # Ale musimy dać więcej escape'ów, bo nie działa xdd
    for i in range(3):
        pyautogui.press('esc')
        print(f"{i} Dialog skipnięty w trzeciej turze")
        time.sleep(0.1)
        
    # Jeżeli NPC wychodzi z dialogu, to nie robimy nic więcej
    # Inaczej klikamy opcje, by wyjść z dialogu
    if not exitsdialogue:
        pyautogui.press('2')    #! Potencjalny config, ale powinno zawsze być 2
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.1)
        
    time.sleep(0.2)


def perform_input_actions(window, outcome):
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
        time.sleep(4)

    else:
        # Przegrana:
        # Wczytaj grę
        # Odczekaj
        # Kliknij ponownie
        pyautogui.keyDown('f12')
        pyautogui.keyUp('f12')
        time.sleep(4)


def controls_loop(gothic_window, dialoguenumber, exitsdialogue, resolution=Resolution.P1080):
    try:
        spam_dialogue(gothic_window, dialoguenumber, exitsdialogue)

        # Czekamy 0.2 sekundy, po czym wykonujemy zrzut ekranu
        time.sleep(0.2)
        screenshot = take_screenshot(gothic_window)

        screenshot.save("data/screenshot.png")

        dices = process_image("data/screenshot.png", resolution)
        enemy_dices = 0
        player_dices = 0

        for i in range(2):
            thresh = threshold_image(dices[i])
            cv2.imwrite(f"out/thresh{i}.png", thresh)
            white_dots = count_dots(thresh, dices[i])
            enemy_dices += white_dots

        for i in range(2, 4):
            thresh = threshold_image(dices[i])
            cv2.imwrite(f"out/thresh{i}.png", thresh)
            white_dots = count_dots(thresh, dices[i])
            player_dices += white_dots

        print("Przeciwnik:", enemy_dices)
        print("Gracz:", player_dices)

        outcome = 0

        if player_dices > enemy_dices:
            outcome = 1

        perform_input_actions(gothic_window, outcome)

        return True
    except Exception as e:
        print(e)
        return False


def take_user_input():
    # CONFIG
    windowname, dialoguenumber, exitsdialogue, resolution = "Gothic II - 2.6 (fix)", 3, False, Resolution.P1080
    
    # User input
    print("Podaj nazwę okna gry gotyckiej 2 (pozostaw puste - domyślne: 'Gothic II - 2.6 (fix)'):", end="")
    user_input = input()

    if user_input != "":
        windowname = user_input

    print("Podaj numer dialogu (pozostaw puste - domyślnie: 3):", end="")
    user_input = input()

    if user_input != "":
        try:
            dialoguenumber = int(user_input)
        except ValueError:
            print("Nieprawidłowy numer dialogu")
            return

    print("Czy NPC wychodzi z dialogu? (t/n, pozostaw puste - domyślnie: nie):", end="")
    user_input = input()

    if user_input == "t":
        exitsdialogue = True
        
    print("Podaj rozdzielczość (1080/1440, pozostaw puste - domyślnie: 1080):", end="")
    user_input = input()
    
    if user_input == "1440":
        resolution = Resolution.P1440
        
    return windowname, dialoguenumber, exitsdialogue, resolution


def print_config(windowname, dialoguenumber, exitsdialogue, resolution):
    print("Konfiguracja:")
    print(f"Okno gry: {windowname}")
    print(f"Numer dialogu: {dialoguenumber}")
    print(f"NPC wychodzi z dialogu: {exitsdialogue}")
    print(f"Rozdzielczość: {resolution}")
    

def main():
    loop_active = False
    
    # User input - CONFIG
    windowname, dialoguenumber, exitsdialogue, resolution = take_user_input()
    
    print_config(windowname, dialoguenumber, exitsdialogue, resolution)

    gothic_window = get_window(windowname)

    if gothic_window is None:
        print("Nie znaleziono gry gotyckiej 2")
        return

    def toggle_loop():
        nonlocal loop_active
        loop_active = not loop_active
        print("Działanie skryptu: ", str(loop_active))

    print("On/Off Shift+Q")
    keyboard.add_hotkey('shift+q', toggle_loop)

    try:
        while True:
            if loop_active:
                result = controls_loop(gothic_window, dialoguenumber, exitsdialogue, resolution)

                if result:
                    print("Tura zakończona pomyślnie")
                else:
                    print("Tura zakończona niepomyślnie")
    except KeyboardInterrupt:
        print("Koniec")
    finally:
        keyboard.unhook_all()


if __name__ == '__main__':
    main()
