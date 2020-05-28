import pyautogui
import time

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()

print(screenWidth, screenHeight)


def openTerminal():
	pyautogui.hotkey('command', 'space')
	pyautogui.write('terminal')
	pyautogui.press('enter')

def spotlightSearch(query):
	pyautogui.hotkey('command', 'space')
	pyautogui.write(query)
	pyautogui.press('enter')


# spotlightSearch('brave')
# pyautogui.alert("Hello Woorld")
