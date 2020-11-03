
fn ImportInfoDataFn ConstomStr=
(
	--local tempPath = getThisScriptFilename()
	local tempPath = ConstomStr
	local tokens = filterString tempPath "\\"
	local strTemp = (tokens[tokens.count-1] + "\\" +tokens[tokens.count])
	local prth = substituteString tempPath  strTemp "InfoData\ProjectInfoData.ms" 
	filein prth
	local prth = substituteString tempPath  strTemp "CommondFn\KeysFn.ms" 
	filein prth
	local prth = substituteString tempPath  strTemp "CommondFn\MorpherFn.ms" 
	filein prth
	local prth = substituteString tempPath  strTemp "CommondFn\UIControlFn.ms" 
	filein prth
	local prth = substituteString tempPath strTemp "CommondFn\ProjectFn.ms" 
	filein prth
)

tokens = filterString (getThisScriptFilename())  "\\"
tempRR = (tokens[tokens.count-1] + "\\" +tokens[tokens.count])

ImportInfoDataFn (getThisScriptFilename()) 




	
CheckToolsRoull = newRolloutFloater  "FacialAnimationMakingDetailsTool" 973 676
ImportScriptFn (getThisScriptFilename()) tempRR "UIPanel\Project_Panel"
ImportScriptFn (getThisScriptFilename()) tempRR	"UIPanel\EyePart_Panel"
ImportScriptFn (getThisScriptFilename()) tempRR "UIPanel\MouthPart_Panel"	
ImportScriptFn (getThisScriptFilename()) tempRR "UIPanel\EffectPart_Panel"	



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



getThisScriptFilename()