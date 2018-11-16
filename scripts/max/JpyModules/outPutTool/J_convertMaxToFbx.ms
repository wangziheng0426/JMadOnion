fn J_outPutGeoAndBone =
(
    outFileName=inputPath
    --outFileName="d:/aa.fbx"
	select_bone=#()
	select_geo=#()
	for item in geometry do
	(
		if (classof item == Biped_Object or classof item == BoneGeometry) do
			(	
				append select_bone item
			)
		if classof item == PolyMeshObject or classof item == Editable_Poly or classof item == Editable_mesh do
			(	
				append select_geo item
                select item
                $.material= none
			)
	)
	try select select_bone catch()
	try selectMore select_geo catch()
	try selectMore $head_front catch()

	FbxExporterSetParam "Animation" False
	FbxExporterSetParam "UpAxis" "Y"
    FbxExporterSetParam "EmbedTextures" False
	exportFile outFileName #noPrompt selectedOnly:true

)
J_outPutGeoAndBone()
--quitMax #noPrompt