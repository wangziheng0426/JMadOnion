tokens = filterString (getThisScriptFilename())  "\\"
tempRR = (tokens[tokens.count-1] + "\\" +tokens[tokens.count])
ImportScriptFn (getThisScriptFilename()) tempRR "InfoData\ProjectInfoData"
ImportScriptFn (getThisScriptFilename()) tempRR "CommondFn\MorpherFn"





rollout SetMorpherChannelRollout "Morpher拾取工具" width:238 height:52
(
	button 'BTNShiQu' "拾取morpher" pos:[9,13] width:102 height:25 align:#left
	
	
	--local facialMorpherNameStrArray = #()
	--local pupilMorpherNameStrArray = #()
	--local pupilEffectMorpherNameStrArray = #()
	--local eyeEffectMorpherNameStrArray = #()
	
	
	
	
	
	
	button 'BtnMorpherNum' "morpher计数" pos:[120,13] width:102 height:25 toolTip:"" align:#left
	
	

	on BTNShiQu pressed do
	(
	
		if selection.count >0 then
		(	
			for each in selection do
			(
				if matchPattern each.name  pattern:("*_Body_H_001") do
				(
                    --合并数据列表，所有表情和眼睛
					local tempArray =  MouthSayMorpherNameStrArray + MouthStyleMorpherNameStrArray + EyeMorpherNameStrArray + EyebrowMorpherNameStrArray + FacialMorpherNameStrArray
                    --morpherfn.ms  74
					SetMorpherChnnelByNameArrayFn each tempArray
				)
				if matchPattern  each.name  pattern:("*_Eye_001") do
				(
					SetMorpherChnnelByNameArrayFn each PupilMorpherNameStrArray
				)
				if matchPattern  each.name  pattern:("*_Pupil_Effect_001") do
				(
					SetMorpherChnnelByNameArrayFn each PupilEffectMorpherNameStrArray
				)
				if matchPattern  each.name  pattern:("*_Eye_Effect_001") do
				(
					SetMorpherChnnelByNameArrayFn each EyeEffectMorpherNameStrArray
				)
				if matchPattern  each.name  pattern:("*_EffectPart_001") do
				(
					SetMorpherChnnelByNameArrayFn each EffectMorpherNameStrArray
				)
			)
		)
		else
		(
			messagebox "没有选中物体"
		)
	
	
	)
	on BtnMorpherNum pressed do
	(
		if selection.count == 1 then
		(	
			local tempMorpherNum = GetMorpherNumFn selection[1]
			messagebox (selection[1].name +"物体的morpher通道个数为：" + tempMorpherNum as string)
		)
		else
		(
			messagebox "必须选择一个物体"
		)
		
	)
)
createdialog SetMorpherChannelRollout	

