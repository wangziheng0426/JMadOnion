rollout MouthPartRollout "嘴部调整" width:945 height:146
(
	GroupBox 'grp20' "口型样式" pos:[4,4] width:461 height:136 align:#left
	button 'BtnMouthStyle01' "Button" pos:[48,27] width:53 height:20 align:#left
	button 'BtnMouthStyle02' "Button" pos:[115,26] width:53 height:20 align:#left
	button 'BtnMouthStyle03' "Button" pos:[178,25] width:53 height:20 align:#left
	button 'BtnMouthStyle04' "Button" pos:[242,25] width:53 height:20 align:#left
	button 'BtnMouthStyle05' "Button" pos:[309,25] width:53 height:20 align:#left
	button 'BtnMouthStyle06' "Button" pos:[375,25] width:53 height:20 align:#left
	button 'BtnMouthStyle07' "Button" pos:[116,85] width:53 height:20 align:#left
	button 'BtnMouthStyle08' "Button" pos:[179,85] width:53 height:20 align:#left
	button 'BtnMouthStyle09' "Button" pos:[243,84] width:53 height:20 align:#left
	button 'BtnMouthStyle10' "Button" pos:[310,83] width:53 height:20 align:#left
	button 'BtnResetMouthStyle07' "Button" pos:[117,114] width:53 height:20 align:#left
	button 'BtnResetMouthStyle08' "Button" pos:[180,114] width:53 height:20 align:#left
	button 'BtnResetMouthStyle09' "Button" pos:[245,113] width:53 height:20 align:#left
	button 'BtnResetMouthStyle10' "Button" pos:[311,112] width:53 height:20 align:#left
	button 'BtnResetMouthStyle02' "Button" pos:[115,56] width:53 height:20 align:#left
	button 'BtnResetMouthStyle03' "Button" pos:[177,55] width:53 height:20 align:#left
	button 'BtnResetMouthStyle04' "Button" pos:[242,55] width:53 height:20 align:#left
	button 'BtnResetMouthStyle05' "Button" pos:[309,55] width:53 height:20 align:#left
	button 'BtnResetMouthStyle06' "Button" pos:[375,55] width:53 height:20 align:#left
	--特殊需求按钮
	button 'BtnSpecial_001' "嘴角向下" pos:[374,84] width:52 height:19 align:#left
	button 'ButtResetBtnSpecial_001' "Button" pos:[376,112] width:53 height:20 align:#left
	GroupBox 'grp21' "细调" pos:[477,4] width:461 height:136 align:#left
	--slider 'DDMouthAddStylesWeight' "叠加权重调整" pos:[636,220] width:119 height:44 range:[0,100,0] align:#left
	--dropdownList 'DDMouthAddStyles' "情绪叠加" pos:[510,221] width:118 height:41 align:#left
	
	dropdownList 'DDMouthStyles' "口型" pos:[491,25] width:99 height:41 align:#left
	slider 'DDMouthStylesWeight' "口型调整" pos:[596,24] width:95 height:44 range:[0,100,0] align:#left
	slider 'SldMouthAddUp' "上撇" pos:[491,77] width:102 height:44 align:#left
	slider 'SldMouthAddDown' "下撇" pos:[597,78] width:102 height:44 range:[0,100,0] align:#left
	slider 'SldMouthAddScaleMin' "缩嘴" pos:[704,78] width:102 height:44 range:[0,100,0] align:#left
	slider 'SldMouthAddScaleMax' "伸长" pos:[811,77] width:102 height:44 range:[0,100,0] align:#left
	dropdownList 'DDFacialStyles' "脸" pos:[705,26] width:99 height:41 align:#left
	slider 'DDFacialStylesWeight' "脸调整" pos:[812,25] width:95 height:44 range:[0,100,0] align:#left
	
	local tempMouthUIControlsArray =#()
	
	fn CollectUIControlsFN = 
	(
		for b in MouthPartRollout.controls do
		(
			a = (findString b.name "ButtEyebrowStyle") as string
			if  a == "1"  do
			(	
				append tempEyebrowUIControlsArray b
			)
			c = (findString b.name "ButtEyeStyle") as string
			if  c == "1"  do
			(	
				append tempEyeUIControlsArray b
			)
			d = (findString b.name "BtnPupilDir") as string
			if  d == "1"  do
			(	
				append tempPupilUIControlsArray b
			)
			g = (findString b.name "BtnMouthStyle") as string
			if  g == "1"  do
			(	
				append tempMouthUIControlsArray b
			)
		)
	)
	fn ToolOpenMatchUINameFn =
	(
		CollectUIControlsFN()
		/*
		--按钮UI
		PartMorpherMatchUIControlsFN 	tempEyebrowUIControlsArray 	EyebrowMorpherNameStrArray  	(EyebrowMorpherNameStrArray.count-2) 	EyebrowMorpherNameStrArray.count
		PartMorpherMatchUIControlsFN 	tempEyeUIControlsArray 		EyeMorpherNameStrArray  		6 		EyeMorpherNameStrArray.count
		--PartMorpherMatchUIControlsFN 	tempMouthUIControlsArray	MouthSayMorpherNameStrArray  	1										MouthSayMorpherNameStrArray.count
		--眉毛列表
		PartMorpherMatchUIDDlistFN		DDButtEyebrowStyles	EyebrowMorpherNameStrArray		1	EyebrowMorpherNameStrArray.count
		--眼睛列表
		PartMorpherMatchUIDDlistFN		DDButtEyeStyles	EyeMorpherNameStrArray		1	EyeMorpherNameStrArray.count
		--眼睛特效列表
		PartMorpherMatchUIDDlistFN		DDEyeEffectControlWay	EyeEffectMorpherNameStrArray		1	EyeEffectMorpherNameStrArray.count
		--瞳孔特效列表
		PartMorpherMatchUIDDlistFN		DDPupilEffectControl	PupilEffectMorpherNameStrArray		(PupilEffectMorpherNameStrArray.count-1)	PupilEffectMorpherNameStrArray.count
		--瞳孔方位列表
		PartMorpherMatchUIDDlistFN		DDPupilDirs				PupilMorpherNameStrArray			1		6
		--情绪叠加列表
		--PartMorpherMatchUIDDlistFN		DDMouthAddStyles		MouthStyleMorpherNameStrArray		(MouthStyleMorpherNameStrArray.count-12)	 (MouthStyleMorpherNameStrArray.count-4)
		
		--瞳孔styles列表
		PartMorpherMatchUIDDlistFN       DDPupilStyles         PupilMorpherNameStrArray      13       PupilMorpherNameStrArray.count
		*/
		--口型btn
		PartMorpherMatchUIControlsFN 	tempMouthUIControlsArray	MouthSayMorpherNameStrArray  	1										MouthSayMorpherNameStrArray.count
		--口型列表
		local tempMouthArray  =  MouthSayMorpherNameStrArray  + MouthStyleMorpherNameStrArray
		PartMorpherMatchUIDDlistFN		DDMouthStyles				tempMouthArray			1		tempMouthArray.count
-------------------------------------------------------------		
		--PartMorpherMatchUIDDlistFN		DDButtEffectStyles		EffectMorpherNameStrArray			1		EffectMorpherNameStrArray.count
		
		
		PartMorpherMatchUIDDlistFN      DDFacialStyles          FacialMorpherNameStrArray    1        FacialMorpherNameStrArray.count
	)
	
	
	
	
	on MouthPartRollout open do
	(
		ToolOpenMatchUINameFn()
	)
	on MouthPartRollout close do
		(
	
	)
	on BtnMouthStyle01 pressed do
	(
		select $Mouth_Part
		MorpherResetFN()
	)
	on BtnMouthStyle02 pressed do
	(
		select $Mouth_Part
		MorpherResetFN()
		SetMorpherValueByUICaptionFn $ BtnMouthStyle02.caption MouthSayMorpherNameStrArray 100.0
	)
	on BtnMouthStyle03 pressed do
	(
		select $Mouth_Part
		MorpherResetFN()
		SetMorpherValueByUICaptionFn $ BtnMouthStyle03.caption MouthSayMorpherNameStrArray 100.0
	)
	on BtnMouthStyle04 pressed do
	(
		select $Mouth_Part
		MorpherResetFN()
		SetMorpherValueByUICaptionFn $ BtnMouthStyle04.caption MouthSayMorpherNameStrArray 100.0
	)
	on BtnMouthStyle05 pressed do
	(	
		select $Mouth_Part
		MorpherResetFN()
		SetMorpherValueByUICaptionFn $ BtnMouthStyle05.caption MouthSayMorpherNameStrArray 100.0				
	)
	on BtnMouthStyle06 pressed do
	(
		select $Mouth_Part
		MorpherResetFN()
		SetMorpherValueByUICaptionFn $ BtnMouthStyle06.caption MouthSayMorpherNameStrArray 100.0
	)
	on BtnMouthStyle07 pressed do
	(
		select $Mouth_Part
		MorpherResetFN()
		SetMorpherValueByUICaptionFn $ BtnMouthStyle07.caption MouthSayMorpherNameStrArray 100.0
	)
	on BtnMouthStyle08 pressed do
	(
		select $Mouth_Part
		MorpherResetFN()
		SetMorpherValueByUICaptionFn $ BtnMouthStyle08.caption MouthSayMorpherNameStrArray 100.0
	)
	on BtnMouthStyle09 pressed do
	(
		select $Mouth_Part
		MorpherResetFN()
		SetMorpherValueByUICaptionFn $ BtnMouthStyle09.caption MouthSayMorpherNameStrArray 100.0
	)
	on BtnMouthStyle10 pressed do
	(	
		select $Mouth_Part
		MorpherResetFN()
		SetMorpherValueByUICaptionFn $ BtnMouthStyle10.caption MouthSayMorpherNameStrArray 100.0				
	)
	on BtnResetMouthStyle07 pressed do
	(
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ BtnMouthStyle07.caption MouthSayMorpherNameStrArray 0.0
	)
	on BtnResetMouthStyle08 pressed do
	(
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ BtnMouthStyle08.caption MouthSayMorpherNameStrArray 0.0
	)
	on BtnResetMouthStyle09 pressed do
	(
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ BtnMouthStyle09.caption MouthSayMorpherNameStrArray 0.0
	)
	on BtnResetMouthStyle10 pressed do
	(	
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ BtnMouthStyle10.caption MouthSayMorpherNameStrArray 0.0				
	)
	on BtnResetMouthStyle02 pressed do
	(
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ BtnMouthStyle02.caption MouthSayMorpherNameStrArray 0.0
	)
	on BtnResetMouthStyle03 pressed do
	(
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ BtnMouthStyle03.caption MouthSayMorpherNameStrArray 0.0
	)
	on BtnResetMouthStyle04 pressed do
	(
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ BtnMouthStyle04.caption MouthSayMorpherNameStrArray 0.0
	)
	on BtnResetMouthStyle05 pressed do
	(	
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ BtnMouthStyle05.caption MouthSayMorpherNameStrArray 0.0				
	)
	on BtnResetMouthStyle06 pressed do
	(
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ BtnMouthStyle06.caption MouthSayMorpherNameStrArray 0.0
	)
	on BtnSpecial_001 pressed do
	(	
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ BtnSpecial_001.caption MouthStyleMorpherNameStrArray 100.0				
	)
	on ButtResetBtnSpecial_001 pressed do
	(	
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ BtnSpecial_001.caption MouthStyleMorpherNameStrArray 0.0				
	)
	on DDMouthStyles selected sel do
	(
		--print(DDMouthStyles.items[sel])
		local tempMorpherArray = MouthStyleMorpherNameStrArray + MouthSayMorpherNameStrArray
		DDMouthStylesWeight.value = GetMorpherValueByUICaptionFn $Mouth_Part tempMorpherArray DDMouthStyles.items[sel]
	)
	on DDMouthStylesWeight changed val do
	(
		/*
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ DDMouthStyles.items[DDMouthStyles.selection] MouthStyleMorpherNameStrArray DDMouthStylesWeight.value
		*/
		local tempMorpherArray = MouthStyleMorpherNameStrArray + MouthSayMorpherNameStrArray
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ DDMouthStyles.items[DDMouthStyles.selection] tempMorpherArray DDMouthStylesWeight.value
	)
	on SldMouthAddUp changed val do
	(	
		local tempMorpherArray = MouthStyleMorpherNameStrArray + MouthSayMorpherNameStrArray
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ SldMouthAddUp.caption tempMorpherArray SldMouthAddUp.value
	)
	on SldMouthAddDown changed val do
	(
		local tempMorpherArray = MouthStyleMorpherNameStrArray + MouthSayMorpherNameStrArray
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ SldMouthAddDown.caption tempMorpherArray SldMouthAddDown.value
		
	)
	on SldMouthAddScaleMin changed val do
	(
		local tempMorpherArray = MouthStyleMorpherNameStrArray + MouthSayMorpherNameStrArray
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ SldMouthAddScaleMin.caption tempMorpherArray SldMouthAddScaleMin.value
	)
	on SldMouthAddScaleMax changed val do
	(
		local tempMorpherArray = MouthStyleMorpherNameStrArray + MouthSayMorpherNameStrArray
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ SldMouthAddScaleMax.caption tempMorpherArray SldMouthAddScaleMax.value
	)
	on DDFacialStyles selected sel do
	(
		DDFacialStylesWeight.value = GetMorpherValueByUICaptionFn $Facial_Part FacialMorpherNameStrArray DDFacialStyles.items[sel]
	)
	on DDFacialStylesWeight changed val do
	(
		select $Facial_Part
		SetMorpherValueByUICaptionFn $ DDFacialStyles.items[DDFacialStyles.selection] FacialMorpherNameStrArray DDFacialStylesWeight.value
	)
)
--createdialog MouthPartRollout 



/*
sdfds
sdfd
fdgfds
g
dfgd
afsd
g
dasg
fd
g
fds
ag
fad
g
a
g
fa
gf
