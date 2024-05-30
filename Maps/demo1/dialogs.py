def initDialog(actor, action, gameTimeSinceLastFrame):
	print("initDialog")
	MGE.TextDialog.get().runDialog("stepDialog", 1)
	return True

MGE.GUIConsole.get().addScript("dialog", "start dialog", "initDialogCmd")
def initDialogCmd(cmd, argsStr):
	MGE.TextDialog.get().runDialog("stepDialog", 1)
	return True


def stepDialog(step):
	print("stepDialog:", step)
	
	if step == 1:
		MGE.TextDialog.get().setImage("LoadingDemoMap.png", "General")
		#MGE.TextDialog.get().showText("BBB BBB BBB", "test1.ogg", 3000, "stepDialog", 2)
		MGE.TextDialog.get().showText("BBB BBB BBB", "", 3000, "stepDialog", 2)
	elif step == 2:
		MGE.TextDialog.get().showText("123456789 abcdefghi 123456789 jklmnoprs 123456789 twuqxyzv0 aaaaaaa aaaaaa aaaaa [colour='FFFFFF00'] 123456789 [colour='990000FF']abcdefghi 123456789 jklmnoprs 123456789 twuqxyzv0 bbbbbbbbbbbb bbbbbbbbbb [font='DejaVuMono-bold']123456789 abcdefghi 123456789 jklmnoprs 123456789 twuqxyzv0", "", 10000, "stepDialog", 3)
	elif step == 3:
		MGE.TextDialog.get().unsetImage(True)
		MGE.TextDialog.get().addAnswer("AA [font='DejaVuMono-bold']QQQ[colour='FFFF0000']QQ[;]Q", 1)
		MGE.TextDialog.get().addAnswer("BB QQQQQQ Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce fringilla magna quam, velx tristique velit tempus id. Duis accumsan", 2)
		MGE.TextDialog.get().addAnswer("BB QQQQQQ Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n Fusce fringilla magna quam, vel tristique velit tempus id.\n Duis accumsan laoreet fermentum. Integer vestibulum mattis ante", 3)
		for i in range(4, 10):
			MGE.TextDialog.get().addAnswer("BB QQQQQQ" + str (i), i)
		MGE.TextDialog.get().showAnswers("dialogQuestionA01")
	return False

def dialogQuestionA01(answerID):
	if answerID == 1:
		MGE.TextDialog.get().showText("111 qqq www eeee", "", 2000)
	elif answerID == 2:
		MGE.TextDialog.get().showText("222 qqq www 2222", "fire_alarm.ogg", 2000)
