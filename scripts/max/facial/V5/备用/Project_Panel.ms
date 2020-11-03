

fn ImportInfoDataFn ConstomStr=
(
    --local tempPath = getThisScriptFilename()
	local tempPath = ConstomStr
    local tokens = filterString tempPath "\\"
	
    local prth = substituteString tempPath  tokens[tokens.count] "InfoData\ProjectInfoData.ms" 
    filein prth
	local prth = substituteString tempPath  tokens[tokens.count] "CommondFn\KeysFn.ms" 
    filein prth
	local prth = substituteString tempPath  tokens[tokens.count] "CommondFn\MorpherFn.ms" 
    filein prth
	local prth = substituteString tempPath  tokens[tokens.count] "CommondFn\UIControlFn.ms" 
    filein prth
	local prth = substituteString tempPath  tokens[tokens.count] "CommondFn\ProjectFn.ms" 
    filein prth
)
ImportInfoDataFn (getThisScriptFilename())

	
CheckToolsRoull = newRolloutFloater "FacialAnimationMakingDetailsTool" 973 676
ImportUIPanelFn (getThisScriptFilename()) "Project_Panel"
ImportUIPanelFn (getThisScriptFilename()) "EyePart_Panel"
ImportUIPanelFn (getThisScriptFilename()) "MouthPart_Panel"	
ImportUIPanelFn (getThisScriptFilename()) "EffectPart_Panel"	



addRollout ProjectPanelRollout CheckToolsRoull
addRollout EyebrowPartRollout CheckToolsRoull 
addRollout MouthPartRollout CheckToolsRoull 
addRollout EffectPartRollout CheckToolsRoull 


/*dfsfdfd
sdfds

dsfsdffsad
asdf

dsf

dsaf
dsaf
sdf
ggdsaf