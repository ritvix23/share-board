import pyperclip
import sys


def copy(text):
		pyperclip.copy(text)
		pyperclip.paste()
		return


if __name__=="__main__":
	copy(sys.argv[1])