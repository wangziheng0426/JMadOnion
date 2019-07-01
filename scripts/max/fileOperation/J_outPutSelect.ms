fn J_outPutSelect = 
(
    unhide objects
    --outFileName=inputPath
    outFileName=maxFilePath+maxFileName
	outFileName=replace outFileName  (outFileName.count  - 3) 4 ".fbx"
	outFileName=maxFilePath+$.name+".fbx"
	
    FbxExporterSetParam "Animation" False
    FbxExporterSetParam "UpAxis" "Y"
    FbxExporterSetParam "EmbedTextures" False
    FbxExporterSetParam "FileVersion" "FBX201200"
    exportFile outFileName #noPrompt selectedOnly:true

)

 J_outPutSelect()