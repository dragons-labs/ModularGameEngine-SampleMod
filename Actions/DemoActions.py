#
# sample "debug" actor actions:
#

def getTargetActors(actor, action, gameTimeSinceLastFrame):
	print("Run action: getTargetActors")
	printTargetInfo(actor, action, gameTimeSinceLastFrame)
	return True

def getStandardActors(actor, action, gameTimeSinceLastFrame):
	print("Run action: getStandardActors")
	printTargetInfo(actor, action, gameTimeSinceLastFrame)
	return True

def getLine(actor, action, gameTimeSinceLastFrame):
	print("Run action: getLine")
	printTargetInfo(actor, action, gameTimeSinceLastFrame)
	return True

def getArea(actor, action, gameTimeSinceLastFrame):
	print("Run action: getArea")
	printTargetInfo(actor, action, gameTimeSinceLastFrame)
	return True

def getAreaAndActors(actor, action, gameTimeSinceLastFrame):
	print("Run action: getAreaAndActors")
	printTargetInfo(actor, action, gameTimeSinceLastFrame)
	return True

def isFreePath(actor, action, gameTimeSinceLastFrame):
	print("Run action: isFreePath for ", actor.getName())
	w3do = MGE.World3DObject.getFromActor(actor)
	res = MGE.isFreePath(w3do.getOgreSceneNode(), w3do.getWorldPosition(), action.targetPoints[0], (1<<13))
	print("isFreePath: ", res)
	return True

def printTargetInfo(actor, action, gameTimeSinceLastFrame):
	print("Run action type =", action.getType())
	
	num = len(action.targetPoints)
	print("NUMBER OF TARGET POINTS:", num)
	if num > 0:
		print("FIRST POINT: x=", action.targetPoints[0].x, " y=", action.targetPoints[0].y, " z=", action.targetPoints[0].z)
		print("LAST POINT: x=", action.targetPoints[-1].x, " y=", action.targetPoints[-1].y, " z=", action.targetPoints[-1].z)
		num = 1
		for point in action.targetPoints:
			print("POINT ", num, ": x=", point.x, " y=", point.y, " z=", point.z)
			num = num + 1
	
	print("NUMBER OF TARGET OBJECTS:", len(action.targetObjects))
	for a in action.targetObjects:
		print("OBJECT: name =", a.getName())



loopTestActorStatus = {}
loopTestSelectionReciverUsageCount = 0

def loopTestSelectionReciver(evt, rid):
	print("Message:", evt.getType())
	
	for actor in MGE.getSelectedActors():
		actorID = actor.getID()
		if actorID in loopTestActorStatus:
			if loopTestActorStatus[actorID] == 0:
				loopTestActorStatus[actorID] = 2
	
	for actor in loopTestActorStatus:
		if loopTestActorStatus[actor] == 1:
			loopTestActorStatus[actor] = 0
			print(actor, "is now NOT selected")
		elif loopTestActorStatus[actor] == 2:
			loopTestActorStatus[actor] = 1
			print(actor, "is now selected")

def loopTestStart(actor, action):
	actorID  = actor.getID()
	actionID = action.getID()
	print( "Init action: loopTest", hex(actorID), hex(actionID) )
	
	global loopTestSelectionReciverUsageCount
	if loopTestSelectionReciverUsageCount == 0:
		print("register message receiver")
		MGE.Engine.get().getMessagesSystem().registerReceiver("SelectionChange", "loopTestSelectionReciver", 0, None)
	loopTestSelectionReciverUsageCount += 1
	
	# set initial value of selection
	loopTestActorStatus[actorID] = 0;
	for tmp in MGE.getSelectedActors():
		if tmp.getID() == actorID:
			loopTestActorStatus[actorID] = 1;
			break
	
	print(" size of loopTestActorStatus:", len(loopTestActorStatus))
	return MGE.ActionInitState.INIT_DONE_OK

def loopTest(actor, action, gameTimeSinceLastFrame):
	# never ending action
	return False

def loopTestEnd(actor, action):
	print( "Finish action: loopTest", hex(action.getID()) )
	
	global loopTestSelectionReciverUsageCount
	loopTestSelectionReciverUsageCount -= 1
	if loopTestSelectionReciverUsageCount == 0:
		print("unregister message receiver")
		MGE.MessagesSystem.get().unregisterReceiver("SelectionChange", "loopTestSelectionReciver", 0, None)
	
	del loopTestActorStatus[ actor.getID() ]
	
	print(" size of loopTestActorStatus:", len(loopTestActorStatus))
