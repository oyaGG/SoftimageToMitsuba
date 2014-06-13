# MaSsCameraPropertyPlugin
# Initial code generated by Softimage SDK Wizard
# Executed Sat Mar 15 18:16:42 UTC+0600 2014 by Philipp
# 
# 
# Tip: The wizard only exposes a small subset of the possible controls
# and layout that can be achieved on a Property Page.  To find out more
# please refer to the Object Model reference documentation for PPGLayout, PPG
# and CustomProperty
# 
# Tip: Don't be concerned about achieving the exact ordering of the parameters
# because they can easily be reordered in the second phase.
# Tip: To add a command to this plug-in, right-click in the 
# script editor and choose Tools > Add Command.
import win32com.client
from win32com.client import constants as c
lm = Application.LogMessage

null = None
false = 0
true = 1

def XSILoadPlugin( in_reg ):
	in_reg.Author = "Angel 07"
	in_reg.Name = "MaSsPropertyPlugin"
	in_reg.Major = 1
	in_reg.Minor = 0

	in_reg.RegisterProperty("MaSsObjectProperty")
	in_reg.RegisterProperty("MaSsCameraProperty")
	in_reg.RegisterProperty("MaSsSpherePrimitiveProperty")
	in_reg.RegisterProperty("MaSsCubePrimitiveProperty")
	in_reg.RegisterProperty("MaSsCylinderPrimitiveProperty")
	in_reg.RegisterProperty("MaSsRectanglePrimitiveProperty")
	in_reg.RegisterProperty("MaSsDiskPrimitiveProperty")
	in_reg.RegisterCommand("MaSsCameraApply","MaSsCameraApply")
	in_reg.RegisterCommand("MaSsObjectApply","MaSsObjectApply")
	in_reg.RegisterCommand("MaSsSpherePrimitiveApply","MaSsSpherePrimitiveApply")
	in_reg.RegisterCommand("MaSsCubePrimitiveApply","MaSsCubePrimitiveApply")
	in_reg.RegisterCommand("MaSsCylinderPrimitiveApply","MaSsCylinderPrimitiveApply")
	in_reg.RegisterCommand("MaSsRectanglePrimitiveApply","MaSsRectanglePrimitiveApply")
	in_reg.RegisterCommand("MaSsDiskPrimitiveApply","MaSsDiskPrimitiveApply")
	
	in_reg.RegisterCommand("MaSsCreatePointLight", "MaSsCreatePointLight")
	in_reg.RegisterCommand("MaSsCreateSpotLight", "MaSsCreateSpotLight")
	in_reg.RegisterCommand("MaSsCreateDirectionalLight", "MaSsCreateDirectionalLight")
	in_reg.RegisterCommand("MaSsCreateAreaSphereLight", "MaSsCreateAreaSphereLight")
	in_reg.RegisterCommand("MaSsCreateAreaCubeLight", "MaSsCreateAreaCubeLight")
	in_reg.RegisterCommand("MaSsCreateAreaCylinderLight", "MaSsCreateAreaCylinderLight")
	in_reg.RegisterCommand("MaSsCreateAreaRectangleLight", "MaSsCreateAreaRectangleLight")
	in_reg.RegisterCommand("MaSsCreateAreaDiskLight", "MaSsCreateAreaDiskLight")
	in_reg.RegisterCommand("MaSsCreateConstantLight", "MaSsCreateConstantLight")
	in_reg.RegisterCommand("MaSsCreateEnvironmentLight", "MaSsCreateEnvironmentLight")
	in_reg.RegisterCommand("MaSsCreateSunSkyLight", "MaSsCreateSunSkyLight")
	in_reg.RegisterCommand("MaSsCreateSunLight", "MaSsCreateSunLight")
	in_reg.RegisterCommand("MaSsCreateSkyLight", "MaSsCreateSkyLight")

	in_reg.RegisterMenu(c.siMenuMainTopLevelID, "MaSs menu", False, False)
	
	
	#RegistrationInsertionPoint - do not remove this line

	return true
	

def MaSsmenu_Init(ctxt):
	menu = ctxt.source
	bgColor = [130, 197, 85]
	sectionMenu = menu.AddItem( "Primitives", c.siMenuItemSection )
	sectionMenu.SetBackgroundColor( *bgColor )
	menu.AddCommandItem("mCube primitive", "MaSsCubePrimitiveApply")
	menu.AddCommandItem("mSphere primitive", "MaSsSpherePrimitiveApply")
	menu.AddCommandItem("mCylinder primitive", "MaSsCylinderPrimitiveApply")
	menu.AddCommandItem("mRectangle primitive", "MaSsRectanglePrimitiveApply")
	menu.AddCommandItem("mDisk primitive", "MaSsDiskPrimitiveApply")

	sectionMenu = menu.AddItem( "Lights", c.siMenuItemSection )
	sectionMenu.SetBackgroundColor( *bgColor )
	menu.AddCommandItem("mPoint light", "MaSsCreatePointLight")
	menu.AddCommandItem("mSpot light", "MaSsCreateSpotLight")
	menu.AddCommandItem("mDirectional light", "MaSsCreateDirectionalLight")
	menu.AddCommandItem("mSpherical light", "MaSsCreateAreaSphereLight")
	menu.AddCommandItem("mCube light", "MaSsCreateAreaCubeLight")
	menu.AddCommandItem("mCylinder light", "MaSsCreateAreaCylinderLight")
	menu.AddCommandItem("mRectanfle light", "MaSsCreateAreaRectangleLight")
	menu.AddCommandItem("mDisk light", "MaSsCreateAreaDiskLight")
	menu.AddCommandItem("mConstant light", "MaSsCreateConstantLight")
	menu.AddCommandItem("mEnvironment light", "MaSsCreateEnvironmentLight")
	menu.AddCommandItem("mSunSky light", "MaSsCreateSunSkyLight")
	menu.AddCommandItem("mSun light", "MaSsCreateSunLight")
	menu.AddCommandItem("mSky light", "MaSsCreateSkyLight")


	sectionMenu = menu.AddItem( "Properties", c.siMenuItemSection )
	sectionMenu.SetBackgroundColor( *bgColor )
	menu.AddCommandItem("mCamera property", "MaSsCameraApply")
	menu.AddCommandItem("mObject property", "MaSsObjectApply")


	sectionMenu = menu.AddItem( "Main menu", c.siMenuItemSection )
	sectionMenu.SetBackgroundColor( *bgColor )
	menu.AddCommandItem("MaSs window", "MaSsOpen")


def XSIUnloadPlugin( in_reg ):
	strPluginName = in_reg.Name
	Application.LogMessage(str(strPluginName) + str(" has been unloaded."), c.siVerbose)
	return true

def MaSsObjectApply_Init( in_ctxt ):
	oCmd = in_ctxt.Source
	oCmd.Description = ""
	oCmd.Tooltip = ""
	oCmd.SetFlag(c.siSupportsKeyAssignment, False)
	oCmd.SetFlag(c.siCannotBeUsedInBatch, True)

	return true
	
def MaSsCameraApply_Init( in_ctxt ):
	oCmd = in_ctxt.Source
	oCmd.Description = ""
	oCmd.Tooltip = ""
	oCmd.SetFlag(c.siSupportsKeyAssignment, False)
	oCmd.SetFlag(c.siCannotBeUsedInBatch, True)

	return true

def MaSsCameraProperty_Define( in_ctxt ):
	oProp = in_ctxt.Source
	oProp.AddParameter3("Type", c.siString, "perspective", "", "", False, False)
	oProp.AddParameter2("apertureRadius", c.siFloat, 0.1, 0, 1000, 0, 1)
	oProp.AddParameter3("focusDistance", c.siFloat, 1, 0, 1000, False, False)
	oProp.AddParameter3("kc", c.siFloat, 0, 0, 1000, False, False)
	return true

def MaSsObjectProperty_Define( in_ctxt ):
	oProp = in_ctxt.Source
	oProp.AddParameter3("isSolid", c.siBool, 0, "", "", False, False)
	oProp.AddParameter3("isSubdivide", c.siBool, 0, "", "", False, False)
	oProp.AddParameter3("subLevel", c.siInt2, 1, 1, 10, False, False)
	return true

# Tip: Use the "Refresh" option on the Property Page context menu to 
# reload your script changes and re-execute the DefineLayout callback.
def MaSsCameraProperty_DefineLayout( in_ctxt ):
	return True

def MaSsObjectProperty_DefineLayout( in_ctxt ):
	return True

def MaSsSpherePrimitiveProperty_DefineLayout( in_ctxt ):
	return True

def MaSsCubePrimitiveProperty_DefineLayout( in_ctxt ):
	return True

def MaSsCylinderPrimitiveProperty_DefineLayout( in_ctxt ):
	return True

def MaSsRectanglePrimitiveProperty_DefineLayout( in_ctxt ):
	return True

def MaSsDiskPrimitiveProperty_DefineLayout( in_ctxt ):
	return True

def OPbuildUI():
	oProp = PPG.Inspected(0)
	oLayout = PPG.PPGLayout
	oLayout.Clear()
	
	oLayout.AddRow()
	oLayout.AddSpacer(10, 10)
	oItem = oLayout.AddItem("isSolid", "Is solid")
	oItem.SetAttribute(c.siUILabelMinPixels, 75)
	oItem.SetAttribute(c.siUILabelPercentage, 15)
	oLayout.AddSpacer(10, 10)
	oLayout.EndRow()
	
	oLayout.AddRow()
	oLayout.AddSpacer(10, 10)
	oItem = oLayout.AddItem("isSubdivide", "Is subdivide")
	oItem.SetAttribute(c.siUILabelMinPixels, 75)
	oItem.SetAttribute(c.siUILabelPercentage, 15)
	oLayout.AddSpacer(10, 10)
	oLayout.EndRow()
	
	strType = str(oProp.Parameters("isSubdivide").Value)
	
	if strType == "True":
		oLayout.AddRow()
		oLayout.AddSpacer(10, 10)
		oItem = oLayout.AddItem("subLevel", "Subdivision level")
		oItem.SetAttribute(c.siUILabelMinPixels, 75)
		oItem.SetAttribute(c.siUILabelPercentage, 15)
		oLayout.AddSpacer(10, 10)
		oLayout.EndRow()
	
	PPG.Refresh()

def MaSsObjectProperty_isSubdivide_OnChanged():
	OPbuildUI()

	return

def CPbuildUI():
	oProp = PPG.Inspected(0)
	oLayout = PPG.PPGLayout
	oLayout.Clear()

	oLayout.AddRow()
	oLayout.AddSpacer(10, 10)
	oItem = oLayout.AddEnumControl("Type", ["Perspective", "perspective", "Perspective with a thin lens", "thinlens", "Orthographic", "orthographic", "Telecentric lens", "telecentric", "Spherical", "spherical", "Radiance meter", "radiancemeter", "Fluence meter", "fluencemeter", "Perspective pinhole with radial distortion", "perspective_rdist"])
	oItem.SetAttribute(c.siUILabelMinPixels, 75)
	oItem.SetAttribute(c.siUILabelPercentage, 15)
	oLayout.AddSpacer(10, 10)
	oLayout.EndRow()

	strType = oProp.Parameters("Type").Value
	if strType == "perspective":
		pass
	elif strType == "thinlens":
		oLayout.AddGroup("Additional parameters")
		oLayout.AddRow()
		oLayout.AddSpacer(10, 10)
		oItem = oLayout.AddItem("apertureRadius", "Aperture Radius")
		oItem.SetAttribute(c.siUILabelMinPixels, 75)
		oItem.SetAttribute(c.siUILabelPercentage, 15)
		oLayout.AddSpacer(10, 10)
		oLayout.EndRow()
		
		oLayout.AddRow()
		oLayout.AddSpacer(10, 10)
		oItem = oLayout.AddItem("focusDistance", "Focus Distance")
		oItem.SetAttribute(c.siUILabelMinPixels, 75)
		oItem.SetAttribute(c.siUILabelPercentage, 15)
		oLayout.AddSpacer(10, 10)
		oLayout.EndRow()
		

		oLayout.AddSpacer(10, 10)
		oItem = oLayout.AddButton("CalculateDistance", "Get distance to interest point")
		oItem.SetAttribute(c.siUICY, 30)	
		oLayout.AddSpacer(10, 10)
		oLayout.EndGroup()
	elif strType == "orthographic":
		pass
	elif strType == "telecentric":
		oLayout.AddGroup("Additional parameters")
		oLayout.AddRow()
		oLayout.AddSpacer(10, 10)
		oItem = oLayout.AddItem("apertureRadius", "Aperture Radius")
		oItem.SetAttribute(c.siUILabelMinPixels, 75)
		oItem.SetAttribute(c.siUILabelPercentage, 15)
		oLayout.AddSpacer(10, 10)
		oLayout.EndRow()
		
		oLayout.AddRow()
		oLayout.AddSpacer(10, 10)
		oItem = oLayout.AddItem("focusDistance", "Focus Distance")
		oItem.SetAttribute(c.siUILabelMinPixels, 75)
		oItem.SetAttribute(c.siUILabelPercentage, 15)
		oLayout.AddSpacer(10, 10)
		oLayout.EndRow()
		
		oLayout.AddSpacer(10, 10)
		oItem = oLayout.AddButton("CalculateDistance", "Get distance to interest point")
		#oItem.SetAttribute(c.siUICX, 380)
		oItem.SetAttribute(c.siUICY, 30)	
		oLayout.AddSpacer(10, 10)
		
		oLayout.EndGroup()
	elif strType == "spherical":
		pass
	elif strType == "irradiancemeter":
		pass
	elif strType == "radiancemeter":
		pass
	elif strType == "fluencemeter":
		pass
	elif strType == "perspective_rdist":
		oLayout.AddGroup("Additional parameters")
		oLayout.AddRow()
		oLayout.AddSpacer(10, 10)
		oItem = oLayout.AddItem("kc", "kc")
		oItem.SetAttribute(c.siUILabelMinPixels, 75)
		oItem.SetAttribute(c.siUILabelPercentage, 15)
		oLayout.AddSpacer(10, 10)
		oLayout.EndRow()
		oLayout.EndGroup()
	
	PPG.Refresh()

def MaSsSpherePrimitiveProperty_Define( in_ctxt ):
	oProp = in_ctxt.Source
	oProp.AddParameter2("radius", c.siFloat, 1, 0, 1000, 0, 10, c.siClassifUnknown, c.siAnimatable)
	return true

def SpherePbuildUI():
	oProp = PPG.Inspected(0)
	oLayout = PPG.PPGLayout
	oLayout.Clear()

	oLayout.AddGroup("Parameters")
	#oLayout.AddRow()
	#oLayout.AddSpacer(10, 10)
	oItem = oLayout.AddItem("radius", "Radius")
	oItem.SetAttribute(c.siUILabelMinPixels, 75)
	oItem.SetAttribute(c.siUILabelPercentage, 15)
	#oLayout.AddSpacer(10, 10)
	#oLayout.EndRow()
	oLayout.EndGroup()
	
	PPG.Refresh()

def MaSsCubePrimitiveProperty_Define( in_ctxt ):
	oProp = in_ctxt.Source
	oProp.AddParameter2("lengthX", c.siFloat, 1, 0, 1000, 0, 10, c.siClassifUnknown, c.siAnimatable)
	oProp.AddParameter2("lengthY", c.siFloat, 1, 0, 1000, 0, 10, c.siClassifUnknown, c.siAnimatable)
	oProp.AddParameter2("lengthZ", c.siFloat, 1, 0, 1000, 0, 10, c.siClassifUnknown, c.siAnimatable)
	return true

def CubePbuildUI():
	oProp = PPG.Inspected(0)
	oLayout = PPG.PPGLayout
	oLayout.Clear()
	oLayout.AddGroup("Parameters")
	#oLayout.AddRow()
	#oLayout.AddSpacer(10, 10)
	oItem = oLayout.AddItem("lengthX", "Length X")
	oItem.SetAttribute(c.siUILabelMinPixels, 75)
	oItem.SetAttribute(c.siUILabelPercentage, 15)
	#oLayout.AddSpacer(10, 10)
	#oLayout.EndRow()
	
	#oLayout.AddRow()
	#oLayout.AddSpacer(10, 10)
	oItem = oLayout.AddItem("lengthY", "Length Y")
	oItem.SetAttribute(c.siUILabelMinPixels, 75)
	oItem.SetAttribute(c.siUILabelPercentage, 15)
	#oLayout.AddSpacer(10, 10)
	#oLayout.EndRow()
	
	#oLayout.AddRow()
	#oLayout.AddSpacer(10, 10)
	oItem = oLayout.AddItem("lengthZ", "Length Z")
	#oItem.SetAttribute(c.siUILabelMinPixels, 75)
	#oItem.SetAttribute(c.siUILabelPercentage, 15)
	#oLayout.AddSpacer(10, 10)
	#oLayout.EndRow()
	oLayout.EndGroup()
	PPG.Refresh()

def MaSsCylinderPrimitiveProperty_Define( in_ctxt ):
	oProp = in_ctxt.Source
	oProp.AddParameter2("length", c.siFloat, 1, 0, 1000, 0, 10, c.siClassifUnknown, c.siAnimatable)
	oProp.AddParameter2("radius", c.siFloat, 1, 0, 1000, 0, 10, c.siClassifUnknown, c.siAnimatable)
	return true

def CylinderPbuildUI():
	oProp = PPG.Inspected(0)
	oLayout = PPG.PPGLayout
	oLayout.Clear()
	oLayout.AddGroup("Parameters")
	#oLayout.AddRow()
	#oLayout.AddSpacer(10, 10)
	oItem = oLayout.AddItem("length", "Length")
	oItem.SetAttribute(c.siUILabelMinPixels, 75)
	oItem.SetAttribute(c.siUILabelPercentage, 15)
	#oLayout.AddSpacer(10, 10)
	#oLayout.EndRow()
	
	#oLayout.AddRow()
	#oLayout.AddSpacer(10, 10)
	oItem = oLayout.AddItem("radius", "Radius")
	oItem.SetAttribute(c.siUILabelMinPixels, 75)
	oItem.SetAttribute(c.siUILabelPercentage, 15)
	#oLayout.AddSpacer(10, 10)
	#oLayout.EndRow()
	oLayout.EndGroup()
	PPG.Refresh()

def MaSsDiskPrimitiveProperty_Define( in_ctxt ):
	oProp = in_ctxt.Source
	oProp.AddParameter2("radius", c.siFloat, 1, 0, 1000, 0, 10, c.siClassifUnknown, c.siAnimatable)
	return true

def DiskPbuildUI():
	oProp = PPG.Inspected(0)
	oLayout = PPG.PPGLayout
	oLayout.Clear()
	oLayout.AddGroup("Parameters")
	#oLayout.AddRow()
	#oLayout.AddSpacer(10, 10)
	oItem = oLayout.AddItem("radius", "Radius")
	oItem.SetAttribute(c.siUILabelMinPixels, 75)
	oItem.SetAttribute(c.siUILabelPercentage, 15)
	#oLayout.AddSpacer(10, 10)
	#oLayout.EndRow()
	oLayout.EndGroup()
	PPG.Refresh()

def MaSsRectanglePrimitiveProperty_Define( in_ctxt ):
	oProp = in_ctxt.Source
	oProp.AddParameter2("lengthX", c.siFloat, 1, 0, 1000, 0, 10, c.siClassifUnknown, c.siAnimatable)
	oProp.AddParameter2("lengthY", c.siFloat, 1, 0, 1000, 0, 10, c.siClassifUnknown, c.siAnimatable)
	return true

def RectanglePbuildUI():
	oProp = PPG.Inspected(0)
	oLayout = PPG.PPGLayout
	oLayout.Clear()
	oLayout.AddGroup("Parameters")
	#oLayout.AddRow()
	#oLayout.AddSpacer(10, 10)
	oItem = oLayout.AddItem("lengthX", "Length X")
	oItem.SetAttribute(c.siUILabelMinPixels, 75)
	oItem.SetAttribute(c.siUILabelPercentage, 15)
	#oLayout.AddSpacer(10, 10)
	#oLayout.EndRow()
	
	#oLayout.AddRow()
	#oLayout.AddSpacer(10, 10)
	oItem = oLayout.AddItem("lengthY", "Length Y")
	oItem.SetAttribute(c.siUILabelMinPixels, 75)
	oItem.SetAttribute(c.siUILabelPercentage, 15)
	#oLayout.AddSpacer(10, 10)
	#oLayout.EndRow()
	oLayout.EndGroup()
	PPG.Refresh()

def MaSsCameraProperty_Type_OnChanged():
	CPbuildUI()

	return
	



def MaSsCameraApply_Execute(  ):
	Application.LogMessage("MaSsCameraApply_Execute called", c.siVerbose)

	#we should add the property to selected object (if it is the camera)
	oSel = Application.Selection(0)
	if oSel != None and oSel.Type == "camera":
		if oSel.GetPropertyFromName2("MaSsCameraProperty"):
			prop = oSel.GetPropertyFromName2("MaSsCameraProperty")
		else:
			prop = oSel.AddProperty("MaSsCameraProperty")

		Application.InspectObj(prop)
	else:
		lm("This property can be allpied only to camera object")
	
	return True

def MaSsObjectApply_Execute(  ):
	Application.LogMessage("MaSsObjectApply_Execute called", c.siVerbose)

	#we should add the property to selected object (if it is the polymesh)
	oSel = Application.Selection(0)
	if oSel != None and oSel.Type == "polymsh":
		if oSel.GetPropertyFromName2("MaSsObjectProperty"):
			prop = oSel.GetPropertyFromName2("MaSsObjectProperty")
		else:
			prop = oSel.AddProperty("MaSsObjectProperty")

		Application.InspectObj(prop)
	else:
		lm("This property can be allpied only to polymesh object")
	
	return True


def MaSsCreatePointLight_Execute():
	Application.LogMessage("MaSsCreatePointLight_Execute called", c.siVerbose)
	lm("Create point light")
	root = Application.ActiveProject.ActiveScene.Root
	pLight = root.AddLight("Point", False, "mPointLight")
	#delete all shaders
	for sh in pLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, pLight)
	#add point shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mPoint.1.0", pLight, "mPoint")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(pLight) + ".LightShader", False)
	Application.InspectObj(newShader)
	Application.SelectObj(pLight)
	
	return True


def MaSsCreateSpotLight_Execute():
	Application.LogMessage("MaSsCreateSpotLight_Execute called", c.siVerbose)
	lm("Create spot light")
	root = Application.ActiveProject.ActiveScene.Root
	lRoot = root.AddNull("mSpotRoot")
	Application.SIHideObjects(lRoot)
	sLight = lRoot.AddLight("Spot", True, "mSpotLight")
	#delete all shaders
	for sh in sLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, sLight)
	#add spot shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mSpot.1.0", sLight, "mSpot")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(sLight) + ".LightShader", False)
	Application.InspectObj(newShader)
	Application.SelectObj(sLight)
	return True
	


def MaSsCreateDirectionalLight_Execute():
	Application.LogMessage("MaSsCreateDirectionalLight_Execute called", c.siVerbose)
	lm("Create directional light")
	root = Application.ActiveProject.ActiveScene.Root
	dLight = root.AddLight("Infinite", False, "mDirectionalLight")
	#delete all shaders
	for sh in dLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, dLight)
	#add directional shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mDirectional.1.0", dLight, "mDirectional")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(dLight) + ".LightShader", False)
	#tip = dLight.AddNull("tip")
	#Application.SIHideObjects(tip)
	#Application.Translate(tip, 0, 0, -9)
	Application.InspectObj(newShader)
	Application.SelectObj(dLight)
	
	return True


def MaSsCreateAreaSphereLight_Execute():
	Application.LogMessage("MaSsCreateAreaSphereLight_Execute called", c.siVerbose)
	lm("Create spherical area light")
	root = Application.ActiveProject.ActiveScene.Root
	asLight = root.AddLight("Point", False, "mAreaSphereLight")
	#delete all shaders
	for sh in asLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, asLight)
	#add shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mAreaSphere.1.0", asLight, "mAreaSphere")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(asLight) + ".LightShader", False)
	Application.SetValue(str(asLight) + ".light.LightArea", True, "")
	Application.SetValue(str(asLight) + ".light.LightAreaGeom", 3, "")
	#Application.CopyPaste(str(asLight) + ".light.mAreaSphere.radius", "", str(asLight) + ".light.LightAreaXformSX", 1)
	asLight.Parameters("LightAreaXformSX").AddExpression(str(asLight) + ".light.mAreaSphere.radius")
	Application.InspectObj(newShader)
	Application.SelectObj(asLight)
	return True



def MaSsCreateAreaCubeLight_Execute():
	Application.LogMessage("MaSsCreateAreaCubeLight_Execute called", c.siVerbose)
	lm("Create cube area light")
	root = Application.ActiveProject.ActiveScene.Root
	acLight = root.AddLight("Point", False, "mAreaCubeLight")
	#delete all shaders
	for sh in acLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, acLight)
	#add point shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mAreaCube.1.0", acLight, "mAreaCube")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(acLight) + ".LightShader", False)
	icon = acLight.AddNull("Icon")
	Application.SetValue(str(icon) + ".null.primary_icon", 0, "")
	Application.SetValue(str(icon) + ".null.shadow_icon", 4, "")
	Application.MakeLocal(str(icon) + ".display", "siNodePropagation")
	Application.SetValue(str(icon) + ".display.wirecolorr", 0.878, "")
	Application.SetValue(str(icon) + ".display.wirecolorg", 0.251, "")
	Application.SetValue(str(icon) + ".display.wirecolorb", 0, "")
	icon.Parameters("shadow_scaleX").AddExpression(str(acLight) + ".light.mAreaCube.lengthX")
	icon.Parameters("shadow_scaleY").AddExpression(str(acLight) + ".light.mAreaCube.lengthY")
	icon.Parameters("shadow_scaleZ").AddExpression(str(acLight) + ".light.mAreaCube.lengthZ")
	Application.ApplyCns("Pose", icon, acLight, "")
	Application.InspectObj(newShader)
	Application.SelectObj(acLight)
	return True
	


def MaSsCreateAreaCylinderLight_Execute():
	Application.LogMessage("MaSsCreateAreaCylinderLight_Execute called", c.siVerbose)
	lm("Create cylinder area light")
	root = Application.ActiveProject.ActiveScene.Root
	acLight = root.AddLight("Point", False, "mAreaCylinderLight")
	#delete all shaders
	for sh in acLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, acLight)
	#add shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mAreaCylinder.1.0", acLight, "mAreaCylinder")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(acLight) + ".LightShader", False)
	Application.SetValue(str(acLight) + ".light.LightArea", True, "")
	Application.SetValue(str(acLight) + ".light.LightAreaGeom", 4, "")
	acLight.Parameters("LightAreaXformSX").AddExpression(str(acLight) + ".light.mAreaCylinder.radius")
	acLight.Parameters("LightAreaXformSZ").AddExpression(str(acLight) + ".light.mAreaCylinder.length")
	#add expression for scale Z transform
	Application.SetExpr(str(acLight) + ".kine.local.sclz", str(acLight) + ".light.mAreaCylinder.length", "")
	#start = acLight.AddNull("startPoint")
	#Application.SIHideObjects(start)
	#end = acLight.AddNull("endPoint")
	#Application.SIHideObjects(end)
	#Application.SetExpr(str(start) + ".kine.local.posz", str(acLight) + ".light.mAreaCylinder.length * -1", "")
	#Application.SetExpr(str(end) + ".kine.local.posz", str(acLight) + ".light.mAreaCylinder.length", "")
	Application.InspectObj(newShader)
	Application.SelectObj(acLight)
	return True
	


def MaSsCreateAreaRectangleLight_Execute():
	Application.LogMessage("MaSsCreateAreaRectangleLight_Execute called", c.siVerbose)
	lm("Create rectangle area light")
	root = Application.ActiveProject.ActiveScene.Root
	arLight = root.AddLight("Point", False, "mAreaRectangleLight")
	#delete all shaders
	for sh in arLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, arLight)
	#add shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mAreaRectangle.1.0", arLight, "mAreaRectangle")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(arLight) + ".LightShader", False)
	Application.SetValue(str(arLight) + ".light.LightArea", True, "")
	Application.SetValue(str(arLight) + ".light.LightAreaGeom", 1, "")
	arLight.Parameters("LightAreaXformSX").AddExpression(str(arLight) + ".light.mAreaRectangle.lengthX")
	arLight.Parameters("LightAreaXformSY").AddExpression(str(arLight) + ".light.mAreaRectangle.lengthY")
	Application.InspectObj(newShader)
	Application.SelectObj(arLight)
	return True
	


def MaSsCreateAreaDiskLight_Execute():
	Application.LogMessage("MaSsCreateAreaDiskLight_Execute called", c.siVerbose)
	lm("Create disk area light")
	root = Application.ActiveProject.ActiveScene.Root
	adLight = root.AddLight("Point", False, "mAreaDiskLight")
	#delete all shaders
	for sh in adLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, adLight)
	#add shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mAreaDisk.1.0", adLight, "mAreaDisk")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(adLight) + ".LightShader", False)
	Application.SetValue(str(adLight) + ".light.LightArea", True, "")
	Application.SetValue(str(adLight) + ".light.LightAreaGeom", 2, "")
	adLight.Parameters("LightAreaXformSX").AddExpression(str(adLight) + ".light.mAreaDisk.radius")
	Application.InspectObj(newShader)
	Application.SelectObj(adLight)
	return True



def MaSsCreateConstantLight_Execute():
	Application.LogMessage("MaSsCreateConstantLight_Execute called", c.siVerbose)
	lm("Create constant light")
	root = Application.ActiveProject.ActiveScene.Root
	cLight = root.AddLight("Point", False, "mConstantLight")
	#delete all shaders
	for sh in cLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, cLight)
	#add shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mConstant.1.0", cLight, "mConstant")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(cLight) + ".LightShader", False)
	
	Application.InspectObj(newShader)
	Application.SelectObj(cLight)
	return True



def MaSsCreateEnvironmentLight_Execute():
	Application.LogMessage("MaSsCreateEnvironmentLight_Execute called", c.siVerbose)
	lm("Create Environment light")
	root = Application.ActiveProject.ActiveScene.Root
	sLight = root.AddLight("Point", False, "mEnvironmentLight")
	#delete all shaders
	for sh in sLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, sLight)
	#add shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mEnvironment.1.0", sLight, "mEnvironment")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(sLight) + ".LightShader", False)
	
	Application.InspectObj(newShader)
	Application.SelectObj(sLight)
	return True



def MaSsCreateSunSkyLight_Execute():
	Application.LogMessage("MaSsCreateSunSkyLight_Execute called", c.siVerbose)
	lm("Create SunSky light")
	root = Application.ActiveProject.ActiveScene.Root
	sLight = root.AddLight("Point", False, "mSunSkyLight")
	#delete all shaders
	for sh in sLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, sLight)
	#add shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mSunSky.1.0", sLight, "mSunSky")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(sLight) + ".LightShader", False)
	
	Application.InspectObj(newShader)
	Application.SelectObj(sLight)
	return True



def MaSsCreateSunLight_Execute():
	Application.LogMessage("MaSsCreateSunLight_Execute called", c.siVerbose)
	lm("Create Sun light")
	root = Application.ActiveProject.ActiveScene.Root
	sLight = root.AddLight("Point", False, "mSunLight")
	#delete all shaders
	for sh in sLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, sLight)
	#add shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mSun.1.0", sLight, "mSun")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(sLight) + ".LightShader", False)
	
	Application.InspectObj(newShader)
	Application.SelectObj(sLight)
	return True


def MaSsCreateSkyLight_Execute():
	Application.LogMessage("MaSsCreateSkyLight_Execute called", c.siVerbose)
	lm("Create Sky light")
	root = Application.ActiveProject.ActiveScene.Root
	sLight = root.AddLight("Point", False, "mSkyLight")
	#delete all shaders
	for sh in sLight.Shaders:
		Application.DisconnectAndDeleteOrUnnestShaders(sh, sLight)
	#add shader
	newShader = Application.CreateShaderFromProgID("MaSsShaders.mSky.1.0", sLight, "mSky")
	Application.SIConnectShaderToCnxPoint(str(newShader) + ".out", str(sLight) + ".LightShader", False)
	
	Application.InspectObj(newShader)
	Application.SelectObj(sLight)
	return True



def MaSsSpherePrimitiveApply_Execute(  ):
	Application.LogMessage("MaSsSpherePrimitiveApply_Execute called", c.siVerbose)
	lm("Create mSphere primitive")
	mSphere = Application.CreatePrim("Sphere", "NurbsSurface", "mSphere", "")
	Application.SetValue(mSphere.Name + ".sphere.radius", 1, "")
	#mSphere = Application.GetPrim("EmptyPolygonMesh", "mSphere", "", "")
	#icon = mSphere.AddNull("mSphereIcon")
	#Application.SetValue(str(icon) + ".null.primary_icon", 0, "")
	#Application.SetValue(str(icon) + ".null.shadow_icon", 2, "")
	#Application.ApplyCns("Pose", icon, mSphere, "")
	Application.FreezeObj(mSphere, "", "")
	prop = mSphere.AddProperty("MaSsSpherePrimitiveProperty")
	#icon.Parameters("size").AddExpression(str(mSphere) + ".MaSsSpherePrimitiveProperty.radius")
	mSphere.Parameters("sclX").AddExpression(mSphere.Name + ".MaSsSpherePrimitiveProperty.radius")
	mSphere.Parameters("sclY").AddExpression(mSphere.Name + ".MaSsSpherePrimitiveProperty.radius")
	mSphere.Parameters("sclZ").AddExpression(mSphere.Name + ".MaSsSpherePrimitiveProperty.radius")
	Application.InspectObj(prop)
	
	return True



def MaSsCubePrimitiveApply_Execute(  ):
	Application.LogMessage("MaSsCubePrimitiveApply_Execute called", c.siVerbose)
	lm("Create mCube primitive")
	mCube = Application.CreatePrim("Cube", "NurbsSurface", "mCube", "")
	Application.SetValue(mCube.Name + ".cube.length", 1, "")
	Application.FreezeObj(mCube, "", "")
	prop = mCube.AddProperty("MaSsCubePrimitiveProperty")
	mCube.Parameters("sclX").AddExpression(mCube.Name + ".MaSsCubePrimitiveProperty.lengthX")
	mCube.Parameters("sclY").AddExpression(mCube.Name + ".MaSsCubePrimitiveProperty.lengthY")
	mCube.Parameters("sclZ").AddExpression(mCube.Name + ".MaSsCubePrimitiveProperty.lengthZ")
	Application.InspectObj(prop)
	return True


def MaSsCylinderPrimitiveApply_Execute(  ):
	Application.LogMessage("MaSsCylinderPrimitiveApply_Execute called", c.siVerbose)
	lm("Create mCylinder primitive")
	mCylinder = Application.CreatePrim("Cylinder", "NurbsSurface", "mCylinder", "")
	Application.SetValue(mCylinder.Name + ".cylinder.height", 1, "")
	Application.SetValue(mCylinder.Name + ".cylinder.radius", 1, "")
	Application.FreezeObj(mCylinder, "", "")
	prop = mCylinder.AddProperty("MaSsCylinderPrimitiveProperty")
	mCylinder.Parameters("sclX").AddExpression(mCylinder.Name + ".MaSsCylinderPrimitiveProperty.radius")
	mCylinder.Parameters("sclY").AddExpression(mCylinder.Name + ".MaSsCylinderPrimitiveProperty.length")
	mCylinder.Parameters("sclZ").AddExpression(mCylinder.Name + ".MaSsCylinderPrimitiveProperty.radius")
	
	Application.InspectObj(prop)
	return True


def MaSsRectanglePrimitiveApply_Execute(  ):
	Application.LogMessage("MaSsRectanglePrimitiveApply_Execute called", c.siVerbose)
	lm("Create mRectangle primitive")
	mRectangle = Application.CreatePrim("Grid", "NurbsSurface", "mRectangle", "")
	Application.SetValue(mRectangle.Name + ".surfmsh.geom.subdivu", 1, "")
	Application.SetValue(mRectangle.Name + ".surfmsh.geom.subdivv", 1, "")
	Application.SetValue(mRectangle.Name + ".grid.ulength", 1, "")
	Application.SetValue(mRectangle.Name + ".grid.vlength", 1, "")
	Application.FreezeObj(mRectangle, "", "")
	prop = mRectangle.AddProperty("MaSsRectanglePrimitiveProperty")
	mRectangle.Parameters("sclX").AddExpression(mRectangle.Name + ".MaSsRectanglePrimitiveProperty.lengthX")
	mRectangle.Parameters("sclZ").AddExpression(mRectangle.Name + ".MaSsRectanglePrimitiveProperty.lengthY")
	Application.InspectObj(prop)
	return True



def MaSsDiskPrimitiveApply_Execute(  ):
	Application.LogMessage("MaSsDiskPrimitiveApply_Execute called", c.siVerbose)
	lm("Create mDisk primitive")
	mDisk = Application.CreatePrim("Disc", "NurbsSurface", "mDiscs", "")
	Application.SetValue(mDisk.Name + ".disc.innerradius", 0.01, "")
	Application.SetValue(mDisk.Name + ".disc.outerradius", 1, "")
	Application.SetValue(mDisk.Name + ".surfmsh.geom.subdivv", 1, "")
	Application.FreezeObj(mDisk, "", "")
	prop = mDisk.AddProperty("MaSsDiskPrimitiveProperty")
	mDisk.Parameters("sclX").AddExpression(mDisk.Name + ".MaSsDiskPrimitiveProperty.radius")
	mDisk.Parameters("sclZ").AddExpression(mDisk.Name + ".MaSsDiskPrimitiveProperty.radius")
	Application.InspectObj(prop)
	return True


def MaSsCameraProperty_OnInit( ):
	CPbuildUI()
	return

def MaSsObjectProperty_OnInit( ):
	OPbuildUI()
	return

def MaSsSpherePrimitiveProperty_OnInit( ):
	SpherePbuildUI()
	return
	
def MaSsCubePrimitiveProperty_OnInit( ):
	CubePbuildUI()
	return

def MaSsCylinderPrimitiveProperty_OnInit( ):
	CylinderPbuildUI()
	return

def MaSsRectanglePrimitiveProperty_OnInit( ):
	RectanglePbuildUI()
	return

def MaSsDiskPrimitiveProperty_OnInit( ):
	DiskPbuildUI()
	return

def MaSsCameraProperty_CalculateDistance_OnClicked():
	oProp = PPG.Inspected(0)
	oCam = oProp.Parent
	oInterest = oCam.Interest
	toVector = XSIMath.CreateVector3(oCam.Kinematics.Global.PosX.Value - oInterest.Kinematics.Global.PosX.Value, oCam.Kinematics.Global.PosY.Value - oInterest.Kinematics.Global.PosY.Value, oCam.Kinematics.Global.PosZ.Value - oInterest.Kinematics.Global.PosZ.Value)
	oProp.Parameters("focusDistance").Value = toVector.Length()