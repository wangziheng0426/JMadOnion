fn ImportScriptFn scriptFilePath  constomStrA constomStrB=
(
	local tempPath = scriptFilePath
	local tokens = filterString tempPath "\\"
	local FilePath = substituteString  tempPath constomStrA (constomStrB +".ms")
	filein FilePath
)



rollout FaicalToolsMainRollout "表情动画工具架" width:441 height:49
(
	button 'btn38' "排版功能" pos:[115,13] width:100 height:23 align:#left
	button 'btn39' "morpher制作" pos:[9,13] width:100 height:23 align:#left
	button 'btn40' "表情动画制作" pos:[332,13] width:100 height:23 align:#left
	button 'btn41' "morpher拾取" pos:[223,13] width:100 height:23 align:#left
	on btn38 pressed  do
	(
		messagebox "开发中"
	)
	on btn39 pressed  do
	(
		messagebox "开发中"
	)
	on btn40 pressed  do
	(
		local tokens = filterString (getThisScriptFilename())  "\\"
		local tempRR = tokens[tokens.count]
		ImportScriptFn (getThisScriptFilename()) tempRR "Control\FacailAnimationTools"

	)
	on btn41 pressed  do
	(
		local tokens = filterString (getThisScriptFilename())  "\\"
		local tempRR = tokens[tokens.count]
		ImportScriptFn (getThisScriptFilename()) tempRR "Control\SetMorpherChannelRollout"
	)
)

createdialog FaicalToolsMainRollout




/*
df
dsa
fa
dsf
d
sa
f
das
f
das
f
sdaf
ads
f
adsd
f
asd


substituteString  "dsfadssfdsafhaoshanhufsdafad"  "haoshanhu"   "qusiba"