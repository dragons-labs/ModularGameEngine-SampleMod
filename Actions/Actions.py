def lightControl(actor, action, gameTimeSinceLastFrame):
	grpID = action.mode
	lc = MGE.Light.getFromActor(actor)
	print(actor)
	print(lc)
	if lc:
		if grpID == 0:
			print("switch all light OFF")
			lc.setAllOff()
		elif grpID == 1:
			print("switch all light ON")
			lc.setAllOn()
		elif grpID > 99:
			grpID = grpID - 100
			print("switch light group", grpID)
			if lc.isGroupOn(grpID):
				print("light group", grpID, "is ON, set OFF")
				lc.setGroupOff(grpID)
			else:
				print("light group", grpID, "is OFF, set ON")
				lc.setGroupOn(grpID)
	return True

def soundControl(actor, action, gameTimeSinceLastFrame):
	sc = MGE.Sound.getFromActor(actor)
	if sc:
		if action.mode == 0:
			print("switch sound OFF")
			sc.playOnMoving("s1", False)
			sc.stop("s1")
		elif action.mode == 1:
			print("switch sound ON")
			sc.playOnMoving("s1", False)
			sc.play("s1")
		elif action.mode == 2:
			print("switch sound AUTO")
			sc.playOnMoving("s1", True)
	return True
