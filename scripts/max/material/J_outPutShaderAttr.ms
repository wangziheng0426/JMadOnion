fn J_outPutGeoMaterial =
(
	python.init()
	outFileName=inputPath
	outFileName=maxFilePath+maxFileName
	outFileName=replace outFileName  (outFileName.count  - 3) 4 ".txt"
	bu=python.Import("__builtin__")
	json=python.Import("json")
	outStr=bu.dict()
	for i in sceneMaterials do
	(
		if classof i ==DirectX_9_Shader do
		(
			outStr[i.name]=bu.dict()
			for j in 1 to i.numsubs do
			(
				outStr[i.name][i[j].name]=(i[j].value as string)
			)
		)

    )
	file =bu.open outFileName "w"
	file.write (json.dumps outStr)
	file.close()
)



J_outPutGeoMaterial()