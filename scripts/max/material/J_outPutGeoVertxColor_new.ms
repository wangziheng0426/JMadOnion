'fn CheckVertexColorFn objEach=\n'+\
'(\n'+\
'	geoVertsCount = getNumVerts objEach\n'+\
'	currentGemData=\"{\\"part\\":\\"\"+objEach.name+\"\\",\\"rgba\\":\"\n'+\
'	--editableMesh\n'+\
'	if classof objEach.baseobject == Editable_mesh then\n'+\
'	(\n'+\
'		if (meshop.getMapSupport objEach 0 == false) do\n'+\
'		(\n'+\
'			append currentGemData (\"\\"None\\"\")\n'+\
'		)\n'+\
'		if meshop.getMapSupport objEach -2 then\n'+\
'		(\n'+\
'			append currentGemData \"[\"\n'+\
'			for vertexID in 1 to geoVertsCount do \n'+\
'			(\n'+\
'				vertAlpha = (meshop.getMapVert objEach -2 vertexID).x\n'+\
'				vertColor= (meshop.getMapVert objEach 0 vertexID)\n'+\
'				\n'+\
'				append currentGemData \"[\"\n'+\
'				\n'+\
'				append currentGemData (\"\\"\"+vertColor[1] as string + \"\\",\"+\"\\"\"+vertColor[2] as string + \"\\",\"+\"\\"\"+vertColor[2] as string + \"\\",\"+\"\\"\"+vertAlpha as string + \"\\"\")\n'+\
'\n'+\
'				append currentGemData \"]\"\n'+\
'\n'+\
'				if vertexID!=geoVertsCount do\n'+\
'					(append currentGemData \",\")\n'+\
'			)\n'+\
'			append currentGemData \"]\"			\n'+\
'		)	\n'+\
'		\n'+\
'	)\n'+\
'		\n'+\
'	--editablePoly\n'+\
'	if classof objEach.baseobject == Editable_Poly then\n'+\
'	(\n'+\
'		if (polyop.getMapSupport objEach 0 == false) do\n'+\
'		(\n'+\
'			append currentGemData (\"\\"None\\"\")\n'+\
'		)\n'+\
'		if polyop.getMapSupport objEach -2 then\n'+\
'		(\n'+\
'			append currentGemData \"[\"\n'+\
'			for vertexID in 1 to geoVertsCount do \n'+\
'			(\n'+\
'			vertAlpha = (polyop.getMapVert objEach -2 vertexID).x\n'+\
'			vertColor= (polyop.getMapVert objEach 0 vertexID)\n'+\
'				\n'+\
'			append currentGemData \"[\"\n'+\
'			\n'+\
'			append currentGemData (\"\\"\"+vertColor[1] as string + \"\\",\"+\"\\"\"+vertColor[2] as string + \"\\",\"+\"\\"\"+vertColor[2] as string + \"\\",\"+\"\\"\"+vertAlpha as string + \"\\"\")\n'+\
'\n'+\
'			append currentGemData \"]\"\n'+\
'\n'+\
'			if vertexID!=geoVertsCount do\n'+\
'				(append currentGemData \",\")\n'+\
'			)\n'+\
'			\n'+\
'		)		\n'+\
'		append currentGemData \"]\"\n'+\
'	)\n'+\
'	\n'+\
'	append currentGemData \"}\"\n'+\
'	gc()\n'+\
'	return currentGemData\n'+\
')\n'+\
'\n'+\
'\n'+\
'fn J_outPutGeoVertxColor =\n'+\
'(\n'+\
'	outFileName=maxfilepath +maxfilename\n'+\
'	logFileName=replace outFileName  (outFileName.count  - 3) 4 \"_vertexColor.log\"\n'+\
'	logFile = openfile (logFileName) mode:\"w\"\n'+\
'	outString=\"{\\"\"+\"GeoVertexColorDataFromJson\"+\"\\":[\"\n'+\
'	bodyParts=#(\"Hair_001\",\"Body_001\",\"Body_H_001\",\"Eye_001\",\"Body_002\",\"Body_003\",\"Mech_001\",\"Mech_002\",\"Mech_101\",\"Mech_102\",\"Gem_001\",\"Gem_002\",\"Glass_001\",\n'+\
'		\"Body_001_P\",\"Body_002_P\",\"Body_003_P\",\"Mech_001_P\",\"Mech_002_P\",\"Mech_101_P\",\"Mech_102_P\",\"Gem_001_P\",\"Gem_002_P\",\"Glass_001_P\",\n'+\
'		\"Nude_Body_001\",\"Nude_Hair_001\",\n'+\
'		\"Swimwear_Body_001\",\"Swimwear_Hair_001\",\"Swimwear_Body_002\",\"Swimwear_Body_003\",\"Swimwear_Mech_001\",\n'+\
'		\"Swimwear_Mech_002\",\"Swimwear_Mech_101\",\"Swimwear_Mech_102\",\"Swimwear_Gem_001\",\"Swimwear_Gem_002\",\"Swimwear_Glass_001\"\n'+\
'		)\n'+\
'		\n'+\
'	outGeo=#()\n'+\
'	for item in geometry do\n'+\
'	(\n'+\
'		for part in bodyParts do\n'+\
'		(\n'+\
'			if (matchPattern  item.name pattern:(\"*\"+part)) do\n'+\
'			(\n'+\
'				append outGeo item\n'+\
'			)\n'+\
'		)\n'+\
'	)\n'+\
'	for i in 1 to outGeo.count do\n'+\
'	(\n'+\
'		if classof outGeo[i] == PolyMeshObject or classof outGeo[i]  == Editable_Poly or classof outGeo[i]  == Editable_mesh do\n'+\
'		(\n'+\
'			append outString (CheckVertexColorFn(outGeo[i]))\n'+\
'			if i!=outGeo.count do (append outString \",\")	\n'+\
'		)		\n'+\
'	)\n'+\
'	append outString \"]}\"\n'+\
'	format outString to:logFile\n'+\
'	close logFile\n'+\
')\n'+\
'--¼ì²é¶¥µãÉ«\n'+\
'\n'+\
'J_outPutGeoVertxColor()\n'+\
'--CheckVertexColorFn($)\n'+\
'\n'+\
