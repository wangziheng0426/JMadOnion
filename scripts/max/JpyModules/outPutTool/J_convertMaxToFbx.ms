fn J_outPutGeoAndBone outFileName=
(
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
			)
		
		
	)
	select select_bone 
	selectMore select_geo
	selectMore $head_front

	FbxExporterSetParam "Animation" false
	FbxExporterSetParam "UpAxis" "Y"

	exportFile outFileName #noPrompt selectedOnly:true

)
J_outPutGeoAndBone "c:/pb.fbx"