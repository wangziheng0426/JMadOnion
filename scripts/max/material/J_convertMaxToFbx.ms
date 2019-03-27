fn J_outPutGeoAndBone = 
(
    unhide objects
    --outFileName=inputPath
    outFileName=maxFilePath+maxFileName
	outFileName=replace outFileName  (outFileName.count  - 3) 4 ".fbx"
    bodyParts=#("Hair_001","Body_001","Body_002","Body_003","Mech_001",
                    "Mech_002","Mech_101","Mech_102","Gem_001","Gem_002","Glass_001")
    bodyParts1=#("Body_001_P","Body_002_P","Body_003_P","Mech_001_P",
                    "Mech_002_P","Mech_101_P","Mech_102_P","Gem_001_P","Gem_002_P","Glass_001_P")
    if (matchPattern  MaxFileName pattern:("*001_P.max") or matchPattern  MaxFileName pattern:("*001_P_3K.max") )do
        (bodyParts=bodyParts1)
    select_bone=#()
    select_geo=#()
    clearSelection()
    for item in geometry do
    (
        if (classof item == Biped_Object or classof item == BoneGeometry) do
            (
                append select_bone item
            )
        if classof item == PolyMeshObject or classof item == Editable_Poly or classof item == Editable_mesh do
            (   
            for part in bodyParts do
                (
                if (matchPattern  item.name pattern:("*"+part) and (item.modifiers[#Skin] != undefined and length(item.pivot)<1)) do
                    (append select_geo item)
                )
            )
        if not ((matchPattern  MaxFileName pattern:("*001_P.max") or matchPattern  MaxFileName pattern:("*001_P_3K.max") )) do
            (
            if (matchPattern item.name pattern:("*Eye_001") or matchPattern item.name pattern:("*Body_H_001") )  do
                (append select_geo item)
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
)
J_outPutGeoAndBone()

