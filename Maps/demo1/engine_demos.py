import CEGUI
import Ogre

class EngineDemos:
	@staticmethod
	def addDemoAction2SelectedActors():
		for actor in MGE.getSelectedActors().selection:
			print("name =", actor.getName())
			actions = actor.getProperty("PosibleActions", MGE.StringList())
			[ print("  (pre)->", a) for a in actions ]
			for na in ["getActors", "getLine", "getArea", "getAreaAndActors", "isFreePath", "initDialog", "loopTest"]:
				actions.push_back(na)
			[ print("  (post)->", a) for a in actions ]
			actions = actor.addProperty("PosibleActions", actions, True)
		
	objIdx = 255
	mode   = 255
	sceneNode = None
	
	@classmethod
	def testMarkers(cls):
		cls.objIdx += 1
		if cls.objIdx > 4:
			cls.objIdx = 1
		cls.mode += 1;
		if cls.mode > 5:
			cls.mode = 0
		
		vmm = MGE.VisualMarkersManager.get()
		ohm = MGE.ObjectHighlightManager.get()
		
		vmm.hideMarker(cls.sceneNode)
		ohm.disable(cls.sceneNode)
		
		cls.sceneNode = MGE.getSceneNode("house{:02d}".format(cls.objIdx))
		
		print("mark mode={} on house{:02d}".format(cls.mode, cls.objIdx))
		if   cls.mode == 0:
			ohm.enable(cls.sceneNode, Ogre.ColourValue(2.0, 1.0, 0.0, 1.0))
		elif cls.mode == 1:
			vmm.showMarker(cls.sceneNode, None, MGE.VisualMarker.OUTLINE, MGE.OgreUtils.getColorDatablock(Ogre.ColourValue(1.0, 0.0, 0.0, 1)), 0.03)
		elif cls.mode == 2:
			vmm.showMarker(cls.sceneNode, None, MGE.VisualMarker.OBBOX | MGE.VisualMarker.CORNER_BOX | MGE.VisualMarker.ABSOLUTE_THICKNESS, MGE.OgreUtils.getColorDatablock(Ogre.ColourValue(0.3, 1, 0, 1)), 0.1)
		elif cls.mode == 3:
			vmm.showMarker(cls.sceneNode, None, MGE.VisualMarker.OBBOX | MGE.VisualMarker.FULL_BOX | MGE.VisualMarker.NO_THICKNESS, MGE.OgreUtils.getColorDatablock(Ogre.ColourValue(0.7, 1, 0, 1)), 0)
		elif cls.mode == 4:
			vmm.showMarker(cls.sceneNode, None, MGE.VisualMarker.PLANE, "SelectionMarkerRed", 1.1)
		elif cls.mode == 5:
			vmm.showMarker(cls.sceneNode, None, MGE.VisualMarker.DECAL, "DecalMarker", 1.1) # this TEXTURE must be set as decal in <SceneManager> → <Decals> → <Texture>
	
	@staticmethod
	def goToWeb():
		wb = MGE.WebBrowser.get("BilboardScreen02")
		wb.loadURL("rpath://resources/SampleMod/Media/WebPages/test.html")
	
	@staticmethod
	def HTTPcallback(browser, args):
		print("Run HTTPcallback: ", args)
		browser.loadURL("http://www.opcode.eu.org")
	
	@staticmethod
	def testParticle():
		sceneNode = MGE.getSceneNode("house01").createChildSceneNode()
		sceneNode.setPosition(Ogre.Vector3(0, 5, -3))
		
		MGE.createParticle("SFX/Fire", "particleTest1", sceneNode)
			# also OK: "Examples/Smoke", "Examples/Fireworks"
	
	@classmethod
	def gui3DProgressBar(cls):
		cls.guiProgressBar = MGE.ProgressBar3D(
			MGE.getSceneNode("house02"),
			"house02",
			Ogre.Vector3(0, 6, 0)
		)
		cls.guiProgressBar.setProgress(0.66, 0xffeedd00);
	
	@classmethod
	def guiOnTexture(cls):
		cls.guiOnTexture = MGE.GUIOnTexture("BilboardScreen01", 600, 600, MGE.LoadingSystem.get().getGameSceneManager(), True, True)
		
		cls.guiOnTextureRootWin = CEGUI.WindowManager.getSingleton().loadLayoutFromFile("Console.layout")
		cls.guiOnTextureRootWin.setName("test")
		cls.guiOnTextureRootWin.setText("test test test")
		cls.guiOnTexture.getRootWindow().addChild(cls.guiOnTextureRootWin);
		
		print(cls.guiOnTextureRootWin.getText())
	
	class MessageDemo():
		class TestEvent(MGE.EventMsg):
			def __init__(self):
				MGE.EventMsg.__init__(self, "wiadomość typu B")
			ii = 15
		
		@staticmethod
		def TestRec(evt, rid):
			try:
				print("odebrano wiadomość:", type(evt), "typu:", evt.getType(), "z wartością:", evt.ii, "reciverID:", rid)
			except:
				print("odebrano wiadomość:", type(evt), "typu:", evt.getType(), "reciverID:", rid)
		
		@classmethod
		def run(cls):
			MGE.Engine.get().getMessagesSystem().sendMessage( MGE.EventMsg("wiadomość typu A") )
			for actor in MGE.getSelectedActors().selection:
				MGE.Engine.get().getMessagesSystem().registerReceiver("wiadomość typu A", "EngineDemos.MessageDemo.TestRec", 0, actor)
			MGE.Engine.get().getMessagesSystem().registerReceiver("wiadomość typu B", "EngineDemos.MessageDemo.TestRec", 0, None)
			MGE.Engine.get().getMessagesSystem().sendMessage( cls.TestEvent() )
	
	animTexCtrl  = None
	animTexSpeed = 1.0
	animTexMode  = 0
	
	@classmethod
	def testTextureAnimation(cls, name = "BilboardScreen01"):
		if not cls.animTexCtrl:
			cls.animTexCtrl = MGE.VideoSystem.setAnimatedTexture( MGE.getMovable(name, name), cls.animTexSpeed, True )
			
		if cls.animTexMode == 4:
			if cls.animTexSpeed == 1.0:
				cls.animTexSpeed = 0.4
			elif cls.animTexSpeed == 0.4:
				cls.animTexSpeed = 2.3
			else:
				cls.animTexSpeed = 1.0
			print ("speed =", cls.animTexSpeed)
			cls.animTexCtrl.configure(cls.animTexSpeed, True)
			cls.animTexMode = 0
			return
		
		cls.animTexCtrl.scrollAnimation(0, 0)
		cls.animTexCtrl.tiledAnimation(0, 0)
		cls.animTexCtrl.rotationAnimation(0)
		cls.animTexCtrl.scaleAnimation(0, 0)
		cls.animTexCtrl.reset(0)
		
		if cls.animTexMode == 0:
			print("scrollAnimation")
			cls.animTexCtrl.scrollAnimation(1, 1)
		elif cls.animTexMode == 1:
			print("tiledAnimation")
			cls.animTexCtrl.tiledAnimation(4, 4)
		elif cls.animTexMode == 2:
			print("rotationAnimation")
			cls.animTexCtrl.rotationAnimation(1)
		elif cls.animTexMode == 3:
			print("scaleAnimation")
			cls.animTexCtrl.scaleAnimation(1, 0)
		
		cls.animTexMode += 1
	
	videoClip  = None
	
	@classmethod
	def testVideo(cls):
		if not cls.videoClip:
			cls.videoClip = MGE.VideoSystem.setVideoTexture("bunny.ogv", "ScreenDefault1", MGE.getSceneNode("BilboardScreen04"))
		else:
			if MGE.InputSystem.get().isModifierDown(0x0000001):
				MGE.VideoSystem.destroyVideoTexture("ScreenDefault1")
				cls.videoClip = None
			else:
				print(cls.videoClip.isPaused())
				if cls.videoClip.isPaused():
					cls.videoClip.play()
				else:
					cls.videoClip.pause()
	
	@staticmethod
	def testHlms(targetName = "crane02"):
		MGE.HlmsSimpleShader.getOrCreateDatablock("crane02test1", "SimpleColor", Ogre.ColourValue(1,1,0,1), 3)
		MGE.VisualMarkersManager.get().showMarker(
			MGE.getSceneNode(targetName),
			None, MGE.VisualMarker.OBBOX | MGE.VisualMarker.FULL_BOX, "crane02test1", 0
		)
	
	@staticmethod
	def testMovePhysicsObjects():
		for n in ["house01", "house02", "house03"]:
			node = MGE.getSceneNode(n)
			if MGE.InputSystem.get().isModifierDown(0x0000001):
				node.yaw(Ogre.Radian(0.01))
			else:
				node.setPosition(node.getPosition() + Ogre.Vector3(0, 0, 3))
	
	@classmethod
	def showInfoWin(cls):
		if MGE.GUISystem.get().getMainWindow().isChildRecursive("DemoInfoWin"):
			CEGUI.WindowManager.getSingleton().destroyWindow(
				MGE.GUISystem.get().getMainWindow().getChild("DemoInfoWin")
			)
		
		cls.infoWin = CEGUI.WindowManager.getSingleton().loadLayoutFromString("""
		<Window type="FrameWindow" name="DemoInfoWin">
			<Property name="Size"     value="{{0, 640}, {0,  170}}" />
			<Property name="Position" value="{{0.06,0},  {-0.06,0}}" />
			<Property name="VerticalAlignment" value="Bottom" />
			<Property name="CloseButtonEnabled" value="True" />
			<Property name="TitlebarFont" value="DejaVuSans" />
			<Property name="Text" value="Demo Info" />
			<Window type="MultiLineEditbox" name="Info">
				<Property name="ReadOnly" value="True" />
				<Property name="Position" value="{{0,3},{0,3}}" />
				<Property name="Size" value="{{1,-6},{1,-6}}" />
				<Property name="Font" value="DejaVuMono" />
				<Property name="Text">Keyboard actions:
=================
A - add demo actions to selected actor(s)
B - demonstrate markers (next press switch mode)
C - navigate texture web browser client to homepage
D - show particle
E - show 3D GUI progress bar
F - demo GUI on texture
G - message system test
H - move object (for checking moving physics, F12 to switch physic debug show)
I - test HlmsSimpleShader
J - demonstrate texture animation (next press switch mode)
K - show video on texture (next press pause/unpause video, with Shift destroy video)

See also console commands after run console via ScrollLock key and run cmdlist commands.

When you close this windows, after save and restore game it will not be shown (this
demonstrate usage of ScriptsStoredData dict for saving and restoring scripts data).</Property>
			</Window>
		</Window>""")
		MGE.GUISystem.get().getMainWindow().addChild(cls.infoWin)
		
		class Callback(CEGUI.PySubscriber):
			def run(self, n):
				EngineDemos.infoWin.hide()
				ScriptsStoredData["infoWinHide"] = True
				return True; # must return bool
		cls.handleHideInfoWin = Callback() # can't be temporary object !!!
		CEGUI.toFrameWindow(cls.infoWin).getCloseButton().subscribeEvent( CEGUI.PushButton.EventClicked.c_str(), cls.handleHideInfoWin )
		
		cls.infoWin.show()
		
	@classmethod
	def keyPressed(cls, key):
		if   key == 30: # A
			cls.addDemoAction2SelectedActors()
		elif key == 48: # B
			cls.testMarkers()
		elif key == 46: # C
			cls.goToWeb()
		elif key == 32: # D
			cls.testParticle()
		elif key == 18: # E
			cls.gui3DProgressBar()
		elif key == 33: # F
			cls.guiOnTexture()
		elif key == 34: # G
			cls.MessageDemo.run()
		elif key == 35: # H
			cls.testMovePhysicsObjects()
		elif key == 23: # I
			cls.testHlms()
		elif key == 36: # J
			cls.testTextureAnimation()
		elif key == 37: # K
			cls.testVideo()
		elif key == 38: # L
			print(len(MGE.ActorFactory.get().allActors))
			for f in MGE.ActorFactory.allActors:
				print(f[0], f[1].getName())
			pass
		elif key == 50: # M
			pass
		elif key == 49: # N
			pass
		elif key == 24: # O
			pass
		elif key == 25: # P
			# used in engine_debug.py for visual raycasting
			pass
	
	inputListener = MGE.InputListener("EngineDemos.keyPressed", "", "", "", "", "")
	MGE.InputSystem.get().registerListener(inputListener, -1, -1, -1, -1, 44, -1)


#
# sample trigger callback:
#

def testTrigger(actor):
	print("trigger uruchomiony przez:", actor.getName())


#
# create SubView on CEGUI window:
#

win = MGE.GUISystem.get().getMainWindow().getChild("WorldInfoWindow")
button = win.getChild("TabSwitching").getChild("Extra1")
button.setText("Ogre RTT")
button.show()
targetWin = CEGUI.WindowManager.getSingleton().loadLayoutFromString("""
	<Window type="InteractiveTexture"   			name="Extra1">
		<Property name="Position"               		value="{{0,5},{0,30}}" />
		<Property name="Size"                   		value="{{1,-10},{1,-35}}" />
		
		<Property name="Visible"                		value="False" />
		<Property name="FrameEnabled"           		value="False" />
	</Window>""")
win.addChild(targetWin)
MGE.LoadingSystem.get().loadDotSceneXML("""
	<scene>
		<SubView windowName="Extra1" putOnWindow="WorldInfoWindow/Extra1" resX="512" resY="512">
			<Camera>
				<Mode>
					<RotationAllowed>1</RotationAllowed>
					<MoveAllowed>1</MoveAllowed>
					<LookOutside>0</LookOutside>
				</Mode>
				<Place>
					<Position> <x>-11.5983</x> <y>0</y> <z>3.52944</z> </Position> 
					<Orientation> <w>1</w> <x>0</x> <y>0</y> <z>0</z> </Orientation>
					<Pitch> <rad>0.785</rad> </Pitch>
				</Place>
			</Camera>
		</SubView>
	</scene>""", None, None)


#
# display info about demos
#

# use ScriptsStoredData to restore saved value of visibility InfoWin ... we even don't create hidden window
#FIXME if not ("infoWinHide" in ScriptsStoredData and ScriptsStoredData["infoWinHide"]):
EngineDemos.showInfoWin()
