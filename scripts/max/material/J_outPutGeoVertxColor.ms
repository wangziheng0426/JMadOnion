fn CheckVertexColorFn objEach=
(
	geoVertsCount = getNumVerts objEach
	currentGemData="{\"part\":\""+objEach.name+"\",\"rgba\":"
	--editableMesh
	if classof objEach.baseobject == Editable_mesh then
	(
		if (meshop.getMapSupport objEach 0 == false) do
		(
			append currentGemData ("\"None\"")
		)
		if meshop.getMapSupport objEach -2 then
		(
			append currentGemData "["
			for vertexID in 1 to geoVertsCount do 
			(
				vertAlpha = (meshop.getMapVert objEach -2 vertexID).x
				vertColor= (meshop.getMapVert objEach 0 vertexID)
				
				append currentGemData "["
				
				append currentGemData ("\""+vertColor[1] as string + "\","+"\""+vertColor[2] as string + "\","+"\""+vertColor[2] as string + "\","+"\""+vertAlpha as string + "\"")

				append currentGemData "]"

				if vertexID!=geoVertsCount do
					(append currentGemData ",")
			)
			append currentGemData "]"			
		)	
		
	)
		
	--editablePoly
	if classof objEach.baseobject == Editable_Poly then
	(
		if (polyop.getMapSupport objEach 0 == false) do
		(
			append currentGemData ("\"None\"")
		)
		if polyop.getMapSupport objEach -2 then
		(
			append currentGemData "["
			for vertexID in 1 to geoVertsCount do 
			(
			vertAlpha = (polyop.getMapVert objEach -2 vertexID).x
			vertColor= (polyop.getMapVert objEach 0 vertexID)
				
			append currentGemData "["
			
			append currentGemData ("\""+vertColor[1] as string + "\","+"\""+vertColor[2] as string + "\","+"\""+vertColor[2] as string + "\","+"\""+vertAlpha as string + "\"")

			append currentGemData "]"

			if vertexID!=geoVertsCount do
				(append currentGemData ",")
			)
			
		)		
		append currentGemData "]"
	)
	
	append currentGemData "}"
	gc()
	return currentGemData
)


fn J_outPutGeoVertxColor =
(
	outFileName=maxfilepath +maxfilename
	logFileName=replace outFileName  (outFileName.count  - 3) 4 "_vertexColor.log"
	logFile = openfile (logFileName) mode:"w"
	outString="{\""+"GeoVertexColorDataFromJson"+"\":["
	bodyParts=#("Hair_001","Body_001","Body_H_001","Eye_001","Body_002","Body_003","Mech_001","Mech_002","Mech_101","Mech_102","Gem_001","Gem_002","Glass_001",
		"Body_001_P","Body_002_P","Body_003_P","Mech_001_P","Mech_002_P","Mech_101_P","Mech_102_P","Gem_001_P","Gem_002_P","Glass_001_P",
		"Nude_Body_001","Nude_Hair_001",
		"Swimwear_Body_001","Swimwear_Hair_001","Swimwear_Body_002","Swimwear_Body_003","Swimwear_Mech_001",
		"Swimwear_Mech_002","Swimwear_Mech_101","Swimwear_Mech_102","Swimwear_Gem_001","Swimwear_Gem_002","Swimwear_Glass_001"
		)
		
	outGeo=#()
	for item in geometry do
	(
		for part in bodyParts do
		(
			if (matchPattern  item.name pattern:("*"+part)) do
			(
				append outGeo item
			)
		)
	)
	for i in 1 to outGeo.count do
	(
		if classof outGeo[i] == PolyMeshObject or classof outGeo[i]  == Editable_Poly or classof outGeo[i]  == Editable_mesh do
		(
			append outString (CheckVertexColorFn(outGeo[i]))
			if i!=outGeo.count do (append outString ",")	
		)		
	)
	append outString "]}"
	format outString to:logFile
	close logFile
)
--¼ì²é¶¥µãÉ«

J_outPutGeoVertxColor()
--CheckVertexColorFn($)

