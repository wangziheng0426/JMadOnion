fn J_outPutGeoAndBone = 
(
    unhide objects
    --outFileName=inputPath
    outFileName=maxFilePath+maxFileName
	outFileName=replace outFileName  (outFileName.count  - 3) 4 ".fbx"
	logFileName=replace outFileName  (outFileName.count  - 3) 4 ".log"
	logString="\n"
	logFile = openfile (logFileName) mode:"w"
    bodyParts=#("Hair_001","Body_001","Body_002","Body_003","Mech_001",
                    "Mech_002","Mech_101","Mech_102","Gem_001","Gem_002","Glass_001")
    bodyParts1=#("Body_001_P","Body_002_P","Body_003_P","Mech_001_P",
                    "Mech_002_P","Mech_101_P","Mech_102_P","Gem_001_P","Gem_002_P","Glass_001_P")
	if (matchPattern  MaxFileName pattern:("*001_P.max") or matchPattern  MaxFileName pattern:("*001_P_3K.max") )do
        (bodyParts=bodyParts1)	
	if (matchPattern  MaxFileName pattern:("*Nude_001.max"))do
		(bodyParts=#("Nude_Body_001","Nude_Hair_001"))	
	if (matchPattern  MaxFileName pattern:("*Swimwear_001.max") or matchPattern  MaxFileName pattern:("*Swimwear_001_3K.max"))do
		(bodyParts=#("Swimwear_Body_001","Swimwear_Hair_001","Swimwear_Body_002","Swimwear_Body_003","Swimwear_Mech_001",
			"Swimwear_Mech_002","Swimwear_Mech_101","Swimwear_Mech_102","Swimwear_Gem_001","Swimwear_Gem_002","Swimwear_Glass_001"))				
    select_bone=#()
    select_geo=#()
    clearSelection()
	boneCount=0
	is_Pfile=matchPattern  MaxFileName pattern:("*_001_P.max")
	is_P3Kfile= matchPattern  MaxFileName pattern:("*_001_P_3K.max")
	is_Nudefile= matchPattern  MaxFileName pattern:("*_Nude*") 
	is_Swimwearfile=matchPattern  MaxFileName pattern:("*_Swimwear*")
	if (matchPattern  MaxFileName pattern:("*_Skin*")) do
		(
			is_Nudefile=false
			is_Swimwearfile=false
		)
    for item in geometry do
    (
		
        if (classof item == Biped_Object or classof item == BoneGeometry) do
            (
                append select_bone item
				boneCount=boneCount+1
            )
        if classof item == PolyMeshObject or classof item == Editable_Poly or classof item == Editable_mesh do
            (   
            for part in bodyParts do
                (
					
                if (matchPattern  item.name pattern:("*"+part) and (item.modifiers[#Skin] != undefined and length(item.pivot)<1)) do
                    (
						print item
						print part
						append select_geo item
						logString=logString+item.name+"\n"
					if (item.parent!=undefined) then
						(logString=logString+"    parentNode: "+item.parent.name+"\n")
					else
						(logString=logString+"    parentNode: NotExists"+ "\n")
					if (item.modifiers[#Skin]!=undefined) then
						(logString=logString+"    skinNode: "+"Exists"+"\n")
					else
						(logString=logString+"    skinNode: "+"NotExists"+"\n")						
					)
                )
            )
		
        if not (is_Pfile or is_P3Kfile or is_Nudefile or is_Swimwearfile ) do
            (
            if (matchPattern item.name pattern:("*Eye_001") or matchPattern item.name pattern:("*Body_H_001") )  do
                (
					append select_geo item
					logString=logString+item.name+"\n"
					if (item.parent!=undefined) then
						(logString=logString+"    parentNode: "+item.parent.name+"\n")
					else
						(logString=logString+"    parentNode: NotExists"+ "\n")
					if (item.modifiers[#Skin]!=undefined) then
						(logString=logString+"    skinNode: "+"Exists"+"\n")
					else
						(logString=logString+"    skinNode: "+"NotExists"+"\n")
				)
			if (matchPattern item.name pattern:("*Eye_Effect_001") or matchPattern item.name pattern:("*Pupil_Effect_001") )  do
                (
					append select_geo item
					logString=logString+item.name+"\n"
					if (item.parent!=undefined) then
						(logString=logString+"    parentNode: "+item.parent.name+"\n")
					else
						(logString=logString+"    parentNode: NotExists"+ "\n")
					if (item.modifiers[#Skin]!=undefined) then
						(logString=logString+"    skinNode: "+"Exists"+"\n")
					else
						(logString=logString+"    skinNode: "+"NotExists"+"\n")
				)
            )
    )	
    try select select_bone catch()
    try selectMore select_geo catch()
    try selectMore $head_front catch()
    FbxExporterSetParam "Animation" False
    FbxExporterSetParam "UpAxis" "Y"
    FbxExporterSetParam "EmbedTextures" False
    FbxExporterSetParam "FileVersion" "FBX201200"
    exportFile outFileName #noPrompt selectedOnly:true
	logString=logString+"\nBoneCount "+(boneCount as string )+"\n"
	print logString to:logFile
	close logFile
)
J_outPutGeoAndBone()

