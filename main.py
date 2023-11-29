import cv2
from DetectDiceState import DetectDiceState


def main():
    # Find the Gothic 2 game window
    # Perform input actions
    # Take screenshots
    # Get the result
    # Based on the result, perform input actions
    # Repeat
    print("Guilds 1.5 Dice Bot")
    img = cv2.imread("data/ref_win.png")
    result = DetectDiceState(img)
    img = cv2.imread("data/ref_loss.png")
    result2 = DetectDiceState(img)

    print("1 - Wygrana" if result == 1 else "1 - Przegrana")
    print("2 - Wygrana" if result2 == 1 else "2 - Przegrana")


if __name__ == "__main__":
    main()
