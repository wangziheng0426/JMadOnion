tokens = filterString (getThisScriptFilename())  "\\"
tempRR = (tokens[tokens.count-1] + "\\" +tokens[tokens.count])
ImportScriptFn (getThisScriptFilename()) tempRR "InfoData\ProjectInfoData"
ImportScriptFn (getThisScriptFilename()) tempRR "CommondFn\MorpherFn"





rollout SetMorpherChannelRollout "Morpherʰȡ����" width:238 height:52
(
	button 'BTNShiQu' "ʰȡmorpher" pos:[9,13] width:102 height:25 align:#left
	
	
	--local facialMorpherNameStrArray = #()
	--local pupilMorpherNameStrArray = #()
	--local pupilEffectMorpherNameStrArray = #()
	--local eyeEffectMorpherNameStrArray = #()
	
	
	
	
	
	
	button 'BtnMorpherNum' "morpher����" pos:[120,13] width:102 height:25 toolTip:"" align:#left
	
	

	on BTNShiQu pressed do
	(
	
		if selection.count >0 then
		(	
			for each in selection do
			(
				if matchPattern each.name  pattern:("*_Body_H_001") do
				(
                    --�ϲ������б������б�����۾�
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
			messagebox "û��ѡ������"
		)
	
	
	)
	on BtnMorpherNum pressed do
	(
		if selection.count == 1 then
		(	
			local tempMorpherNum = GetMorpherNumFn selection[1]
			messagebox (selection[1].name +"�����morpherͨ������Ϊ��" + tempMorpherNum as string)
		)
		else
		(
			messagebox "����ѡ��һ������"
		)
		
	)
)
createdialog SetMorpherChannelRollout	
