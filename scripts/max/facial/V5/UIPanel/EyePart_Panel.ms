rollout EyebrowPartRollout "眼部调整" width:973 height:260
(
	--GroupBox 'grp1' "眉毛" pos:[4,2] width:474 height:180 align:#left
	GroupBox 'grp2' "眉毛样式" pos:[4,2] width:461 height:120 align:#left
	button 'ButtEyebrowStyle01' "Button" pos:[20,22] width:82 height:20 align:#left
	button 'ButtEyebrowStyle02' "Button" pos:[109,21] width:82 height:20 align:#left
	button 'ButtEyebrowStyle03' "Button" pos:[198,21] width:82 height:20 align:#left
	button 'ButtEyebrowStyle04' "Button" pos:[288,20] width:82 height:20 align:#left
	--button 'ButtEyebrowStyle05' "Button" pos:[384,97] width:82 height:20 align:#left
	GroupBox 'grp5' "瞳孔方向" pos:[488,7] width:461 height:105 align:#left
	GroupBox 'grp6' "细调" pos:[493,114] width:460 height:130 align:#left
	slider 'SldPupilDirWeight' "位置权重" pos:[618,128] width:100 height:44 range:[0,100,0] align:#left
	dropdownList 'DDPupilDirs' "瞳孔位置" pos:[497,127] width:118 height:41 align:#left
	
	button 'BtnPupilDir' "正常" pos:[749,55] width:82 height:20 align:#left
	button 'BtnPupilDir01' "上" pos:[751,29] width:82 height:20 align:#left
	button 'BtnPupilDir02' "下" pos:[747,83] width:82 height:20 align:#left
	button 'BtnPupilDir03' "左" pos:[660,55] width:82 height:20 align:#left
	button 'BtnPupilDir04' "右" pos:[843,55] width:82 height:20 align:#left
	button 'BtnPupilDir05' "左上" pos:[659,29] width:82 height:20 align:#left
	button 'BtnPupilDir06' "右上" pos:[843,29] width:82 height:20 align:#left
	button 'BtnPupilDir07' "左下" pos:[660,82] width:82 height:20 align:#left
	button 'BtnPupilDir08' "右下" pos:[843,81] width:82 height:20 align:#left
	
	
	radiobuttons 'RdoPupilSync' "眼睛同步" pos:[501,32] width:51 height:46 labels:#("开启", "关闭") default:1 columns:1 align:#left
	radiobuttons 'RdoPupilRandL' "眼睛方向" pos:[568,31] width:51 height:46 labels:#("左眼", "右眼") default:1 columns:1 align:#left
	dropdownList 'DDButtEyebrowStyles' "眉毛方位" pos:[114,74] width:118 height:41 align:#left
	spinner 'SpnPupilDirWeight' "权重值" pos:[509,87] width:98 height:16 align:#left

	GroupBox 'grp26' "眼皮样式" pos:[4,124] width:461 height:122 align:#left
	button 'ButtEyeStyle01' "Button" pos:[18,146] width:82 height:20 align:#left
	button 'ButtEyeStyle02' "Button" pos:[107,145] width:82 height:20 align:#left
	button 'ButtEyeStyle03' "Button" pos:[196,145] width:82 height:20 align:#left
	button 'ButtEyeStyle04' "Button" pos:[286,144] width:82 height:20 align:#left
	button 'ButtEyeStyle05' "Button" pos:[375,144] width:82 height:20 align:#left
	dropdownList 'DDButtEyeStyles' "眼皮" pos:[23,198] width:102 height:41 align:#left
	slider 'DDButtEyeStylesWeight' "眼皮权重值" pos:[127,193] width:115 height:44 range:[0,100,0] align:#left
	--radiobuttons 'RDOPupilLinkEye' "瞳孔眼皮关联" pos:[21,288] width:106 height:30 labels:#("同步", "异步") columns:2 align:#left
	dropdownList 'DDPupilStyles' "瞳孔造型" pos:[498,179] width:118 height:41 align:#left
	slider 'SldPupilStyleWeight' "位置权重" pos:[619,180] width:100 height:44 range:[0,100,0] align:#left
	
	slider 'DDButtEyebrowStylesWeight' "眉毛方位权重" pos:[236,70] width:118 height:44 range:[0,100,0] align:#left
	dropdownList 'DDEyeEffectControlWay' "特殊眼皮" pos:[722,127] width:102 height:41 align:#left
	slider 'DDEyeEffectControlWeight' "特殊眼皮权重" pos:[828,127] width:111 height:44 range:[0,100,0] align:#left
	dropdownList 'DDPupilEffectControl' "瞳孔特效" pos:[721,182] width:105 height:41 align:#left
	slider 'DDPupilEffectControlWeight' "位置权重" pos:[830,180] width:109 height:44 range:[0,100,0] align:#left
	
	
	button 'ButtResetEyebrowStyle02' "Button" pos:[109,48] width:82 height:20 align:#left
	button 'ButtResetEyebrowStyle03' "Button" pos:[199,48] width:82 height:20 align:#left
	button 'ButtResetEyebrowStyle04' "Button" pos:[288,48] width:82 height:20 align:#left
	button 'ButtResetEyeStyle02' "Button" pos:[107,172] width:82 height:20 align:#left
	button 'ButtResetEyeStyle03' "Button" pos:[196,172] width:82 height:20 align:#left
	button 'ButtResetEyeStyle04' "Button" pos:[285,170] width:82 height:20 align:#left
	button 'ButtResetEyeStyle05' "Button" pos:[375,171] width:82 height:20 align:#left
	
	
	local tempEyebrowUIControlsArray = #()
	local tempEyeUIControlsArray =#()
	local tempPupilUIControlsArray =#()
	local tempMouthUIControlsArray =#()
	
	local isEyeDouble =true
	local isEyeRight = false
	--左右眼的逻辑
	fn SetEyeMorpherValueByUICaptionFn  UICaption  constomValue=
	(
		if isEyeDouble then
		(
			select $Pupil_Part
			local morpherName = GetMorpherNameByUICaptionFn PupilMorpherNameStrArray UICaption
			local morpherChannelId = GetMorpherIDByStringFn $ MorpherName
			if morpherChannelId != undefined do
			(	
				WM3_MC_SetValue $.modifiers[1] morpherChannelId constomValue
			)
			local morpherName = GetMorpherNameByUICaptionFn PupilMorpherNameStrArray UICaption
			morpherName = substituteString morpherName "Right" "Left"
			local morpherChannelId = GetMorpherIDByStringFn $ MorpherName
			if morpherChannelId != undefined do
			(	
				WM3_MC_SetValue $.modifiers[1] morpherChannelId constomValue
			)
		)
		else
		(
			if isEyeRight then
			(
				select $Pupil_Part
				local morpherName = GetMorpherNameByUICaptionFn PupilMorpherNameStrArray UICaption
				local morpherChannelId = GetMorpherIDByStringFn $ MorpherName
				if morpherChannelId != undefined do
				(	
					WM3_MC_SetValue $.modifiers[1] morpherChannelId constomValue
				)
			)
			else
			(
				select $Pupil_Part
				local morpherName = GetMorpherNameByUICaptionFn PupilMorpherNameStrArray UICaption
				morpherName = substituteString morpherName "Right" "Left"
				local morpherChannelId = GetMorpherIDByStringFn $ MorpherName
				if morpherChannelId != undefined do
				(	
					WM3_MC_SetValue $.modifiers[1] morpherChannelId constomValue
				)
			)
		)		
			
		
	)
	
	
		
	fn CollectUIControlsFN = 
	(
		for b in EyebrowPartRollout.controls do
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
		--口型列表
		--local tempMouthArray  =  MouthSayMorpherNameStrArray  + MouthStyleMorpherNameStrArray
		--PartMorpherMatchUIDDlistFN		DDMouthStyles				tempMouthArray			1		tempMouthArray.count
-------------------------------------------------------------		
		--PartMorpherMatchUIDDlistFN		DDButtEffectStyles		EffectMorpherNameStrArray			1		EffectMorpherNameStrArray.count
		
		
		--PartMorpherMatchUIDDlistFN      DDFacialStyles          FacialMorpherNameStrArray    1        FacialMorpherNameStrArray.count
	)
	
	
	
	
	
	--button 'BtnRefurbishEyePart' "眼部权重刷新" pos:[13,88] width:82 height:20 align:#left
	on EyebrowPartRollout open do
	(
		ToolOpenMatchUINameFn()
	)
	on EyebrowPartRollout close do
	(
	
	)
	on ButtEyebrowStyle01 pressed do
	(
		select $Eyebrow_Part
		MorpherResetFN()
	)
	on ButtEyebrowStyle02 pressed do
	(
		select $Eyebrow_Part
		SetMorpherValueByUICaptionFn $ ButtEyebrowStyle02.caption EyebrowMorpherNameStrArray 100.0
		--print ButtEyebrowStyle02.caption
		--print EyebrowMorpherNameStrArray
	)
	on ButtEyebrowStyle03 pressed do
	(
		select $Eyebrow_Part
		SetMorpherValueByUICaptionFn $ ButtEyebrowStyle03.caption EyebrowMorpherNameStrArray 100.0
	)
	on ButtEyebrowStyle04 pressed do
	(
		select $Eyebrow_Part
		SetMorpherValueByUICaptionFn $ ButtEyebrowStyle04.caption EyebrowMorpherNameStrArray 100.0
	)
	on SldPupilDirWeight changed val do
	(
		SetEyeMorpherValueByUICaptionFn  DDPupilDirs.items[DDPupilDirs.selection]  SldPupilDirWeight.value
	)
	on DDPupilDirs selected sel do
	(
		--print (DDPupilDirs.items[sel])
	)
	on BtnPupilDir pressed do
	(
		select $Pupil_Part
		MorpherResetFN()
	)
	on BtnPupilDir01 pressed do
	(
		select $Pupil_Part
		local tempMorpherValue = GetMorpherValueByUICaptionFn $ PupilMorpherNameStrArray BtnPupilDir01.caption
		tempMorpherValue = tempMorpherValue + SpnPupilDirWeight.value
		if tempMorpherValue >100.0 do
		(
			tempMorpherValue = 100.0
		)
		SetEyeMorpherValueByUICaptionFn  BtnPupilDir01.caption  tempMorpherValue
	)
	on BtnPupilDir02 pressed do
	(
		select $Pupil_Part
		local tempMorpherValue = GetMorpherValueByUICaptionFn $ PupilMorpherNameStrArray BtnPupilDir02.caption
		tempMorpherValue = tempMorpherValue + SpnPupilDirWeight.value
		if tempMorpherValue >100.0 do
		(
			tempMorpherValue = 100.0
		)
		SetEyeMorpherValueByUICaptionFn  BtnPupilDir02.caption  tempMorpherValue
	)
	on BtnPupilDir03 pressed do
	(
		select $Pupil_Part
		local tempMorpherValue = GetMorpherValueByUICaptionFn $ PupilMorpherNameStrArray BtnPupilDir03.caption
		tempMorpherValue = tempMorpherValue + SpnPupilDirWeight.value
		if tempMorpherValue >100.0 do
		(
			tempMorpherValue = 100.0
		)
		SetEyeMorpherValueByUICaptionFn  BtnPupilDir03.caption  tempMorpherValue
	)
	on BtnPupilDir04 pressed do
	(
		select $Pupil_Part
		local tempMorpherValue = GetMorpherValueByUICaptionFn $ PupilMorpherNameStrArray BtnPupilDir04.caption
		tempMorpherValue = tempMorpherValue + SpnPupilDirWeight.value
		if tempMorpherValue >100.0 do
		(
			tempMorpherValue = 100.0
		)
		SetEyeMorpherValueByUICaptionFn  BtnPupilDir04.caption  tempMorpherValue
	)
	on BtnPupilDir05 pressed do
	(
		local tempStr = BtnPupilDir05.caption
		for i in 1 to 2 do
		(
			select $Pupil_Part
			local tempMorpherValue = GetMorpherValueByUICaptionFn $ PupilMorpherNameStrArray tempStr[i]
			tempMorpherValue = tempMorpherValue + SpnPupilDirWeight.value
			if tempMorpherValue >100.0 do
			(
				tempMorpherValue = 100.0
			)
			SetEyeMorpherValueByUICaptionFn  tempStr[i]  tempMorpherValue
		)
	)
	on BtnPupilDir06 pressed do
	(
		local tempStr = BtnPupilDir06.caption
		for i in 1 to 2 do
		(
			select $Pupil_Part
			local tempMorpherValue = GetMorpherValueByUICaptionFn $ PupilMorpherNameStrArray tempStr[i]
			tempMorpherValue = tempMorpherValue + SpnPupilDirWeight.value
			if tempMorpherValue >100.0 do
			(
				tempMorpherValue = 100.0
			)
			SetEyeMorpherValueByUICaptionFn  tempStr[i]  tempMorpherValue
		)
	)
	on BtnPupilDir07 pressed do
	(
		local tempStr = BtnPupilDir07.caption
		for i in 1 to 2 do
		(
			select $Pupil_Part
			local tempMorpherValue = GetMorpherValueByUICaptionFn $ PupilMorpherNameStrArray tempStr[i]
			tempMorpherValue = tempMorpherValue + SpnPupilDirWeight.value
			if tempMorpherValue >100.0 do
			(
				tempMorpherValue = 100.0
			)
			SetEyeMorpherValueByUICaptionFn  tempStr[i]  tempMorpherValue
		)	
	)
	on BtnPupilDir08 pressed do
	(
		local tempStr = BtnPupilDir08.caption
		for i in 1 to 2 do
		(
			select $Pupil_Part
			local tempMorpherValue = GetMorpherValueByUICaptionFn $ PupilMorpherNameStrArray tempStr[i]
			tempMorpherValue = tempMorpherValue + SpnPupilDirWeight.value
			if tempMorpherValue >100.0 do
			(
				tempMorpherValue = 100.0
			)
			SetEyeMorpherValueByUICaptionFn  tempStr[i]  tempMorpherValue
		)
	)
	on RdoPupilSync changed stat do
	(
		if  RdoPupilSync.state == 1 then
		(
			isEyeDouble  = true
		)
		else
		(
			isEyeDouble  = false
		)
		--isEyeDouble 
	)
	on RdoPupilRandL changed stat do
	(
		if  RdoPupilRandL.state == 1 then
		(
			isEyeRight  = true
		)
		else
		(
			isEyeRight  = false
		)
	)
	on ButtEyeStyle01 pressed do
	(
		select $Eye_Part
		MorpherResetFN()
	)
	on ButtEyeStyle02 pressed do
	(
		select $Eye_Part
		SetMorpherValueByUICaptionFn $ ButtEyeStyle02.caption EyeMorpherNameStrArray 100.0
	)
	on ButtEyeStyle03 pressed do
	(
		select $Eye_Part
		SetMorpherValueByUICaptionFn $ ButtEyeStyle03.caption EyeMorpherNameStrArray 100.0
	)
	on ButtEyeStyle04 pressed do
	(
		select $Eye_Part
		SetMorpherValueByUICaptionFn $ ButtEyeStyle04.caption EyeMorpherNameStrArray 100.0
	)
	on ButtEyeStyle05 pressed do
	(
		select $Eye_Part
		SetMorpherValueByUICaptionFn $ ButtEyeStyle05.caption EyeMorpherNameStrArray 100.0
	)
	on DDButtEyeStyles selected sel do
	(
		DDButtEyeStylesWeight.value = GetMorpherValueByUICaptionFn $Eye_Part EyeMorpherNameStrArray DDButtEyeStyles.items[sel]
	)
	on DDButtEyeStylesWeight changed val do
	(
		select $Eye_Part
		SetMorpherValueByUICaptionFn $ DDButtEyeStyles.items[DDButtEyeStyles.selection] EyeMorpherNameStrArray DDButtEyeStylesWeight.value
	)
	on DDPupilStyles selected sel do
	(
		if $Eye_Effect_Part != undefined do
		(
			SldPupilStyleWeight.value =  GetMorpherValueByUICaptionFn $Eye_Effect_Part EyeEffectMorpherNameStrArray DDEyeEffectControlWay.items[sel]
		)	
	)
	on SldPupilStyleWeight changed val do
	(
		SetEyeMorpherValueByUICaptionFn  DDPupilStyles.items[DDPupilStyles.selection]  SldPupilStyleWeight.value
		if $Pupil_Part != undefined do
		(
			select $Pupil_Part
			SetMorpherValueByUICaptionFn $  DDPupilStyles.items[DDPupilStyles.selection] PupilMorpherNameStrArray SldPupilStyleWeight.value
		)
	)
	on DDButtEyebrowStyles selected sel do
	(
		print(DDButtEyebrowStyles.items[sel])
		DDButtEyebrowStylesWeight.value = GetMorpherValueByUICaptionFn $Eyebrow_Part EyebrowMorpherNameStrArray DDButtEyebrowStyles.items[sel]
		
	)
	on DDButtEyebrowStylesWeight changed val do
	(
		select $Eyebrow_Part
		SetMorpherValueByUICaptionFn $ DDButtEyebrowStyles.items[DDButtEyebrowStyles.selection] EyebrowMorpherNameStrArray DDButtEyebrowStylesWeight.value
	)
	on DDEyeEffectControlWay selected sel do
	(
		if $Eye_Effect_Part != undefined do
		(
			DDEyeEffectControlWeight.value = GetMorpherValueByUICaptionFn $Eye_Effect_Part EyeEffectMorpherNameStrArray DDEyeEffectControlWay.items[sel]	
		)	
	)
	on DDEyeEffectControlWeight changed val do
	(
		if $Eye_Effect_Part != undefined do
		(
			select $Eye_Effect_Part
			SetMorpherValueByUICaptionFn $ DDEyeEffectControlWay.items[DDEyeEffectControlWay.selection] EyeEffectMorpherNameStrArray DDEyeEffectControlWeight.value
		)	
	)
	on DDPupilEffectControl selected sel do
	(
		if $Pupil_Effect_Part != undefined do
		(
			DDPupilEffectControlWeight.value = GetMorpherValueByUICaptionFn $Pupil_Effect_Part PupilEffectMorpherNameStrArray DDPupilEffectControl.items[sel]	
		)
	)
	on DDPupilEffectControlWeight changed val do
	(
		if $Pupil_Effect_Part != undefined do
		(
			select $Pupil_Effect_Part
			SetMorpherValueByUICaptionFn $ DDPupilEffectControl.items[DDPupilEffectControl.selection] PupilEffectMorpherNameStrArray DDPupilEffectControlWeight.value
		)	
	)
	on ButtResetEyebrowStyle02 pressed do
	(
		select $Eyebrow_Part
		SetMorpherValueByUICaptionFn $ ButtEyebrowStyle02.caption EyebrowMorpherNameStrArray 0.0
	)
	on ButtResetEyebrowStyle03 pressed do
	(
		select $Eyebrow_Part
		SetMorpherValueByUICaptionFn $ ButtEyebrowStyle03.caption EyebrowMorpherNameStrArray 0.0
	)
	on ButtResetEyebrowStyle04 pressed do
	(
		select $Eyebrow_Part
		SetMorpherValueByUICaptionFn $ ButtEyebrowStyle04.caption EyebrowMorpherNameStrArray 0.0
	)
	on ButtResetEyeStyle02 pressed do
	(
		select $Eye_Part
		SetMorpherValueByUICaptionFn $ ButtEyeStyle02.caption EyeMorpherNameStrArray 0.0
	)
	on ButtResetEyeStyle03 pressed do
	(
		select $Eye_Part
		SetMorpherValueByUICaptionFn $ ButtEyeStyle03.caption EyeMorpherNameStrArray 0.0
	)
	on ButtResetEyeStyle04 pressed do
	(
		select $Eye_Part
		SetMorpherValueByUICaptionFn $ ButtEyeStyle04.caption EyeMorpherNameStrArray 0.0
	)
	on ButtResetEyeStyle05 pressed do
	(
		select $Eye_Part
		SetMorpherValueByUICaptionFn $ ButtEyeStyle05.caption EyeMorpherNameStrArray 0.0
	)
	/*
	on BtnRefurbishEyePart pressed do
	(
		clearSelection()
		select $*Body_H_001
		if selection.count == 1 do
		(	
			--眼睛列表
			local morpherNameStr = GetMorpherNameByUICaptionFn EyeMorpherNameStrArray DDButtEyeStyles.items[DDButtEyeStyles.selection]
			local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
			if morpherChannelID != undefined do
			(
				DDButtEyeStylesWeight.value =  WM3_MC_GetValue $.modifiers[#Morpher]  morpherChannelID
				print DDButtEyeStylesWeight.value
			)
				
		)
		clearSelection()
		select $*Eye_Effect_001
		if selection.count == 1 do
		(
			--spnEyeEffectTexID.value = $.baseObject.EyeTextureTrans.texIndex
			local morpherNameStr = GetMorpherNameByUICaptionFn EyeEffectMorpherNameStrArray DDEyeEffectControlWay.items[DDEyeEffectControlWay.selection]
			local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
			if morpherChannelID != undefined do
			(
				DDEyeEffectControlWeight.value = WM3_MC_GetValue $.modifiers[#Morpher]  morpherChannelID
			)	
		)
		clearSelection()
		select $*Pupil_Effect_001
		if selection.count == 1 do
		(
			--SPNPupilEffectTexID.value = $.baseObject.EyeTextureTrans.texIndex
			local morpherNameStr = GetMorpherNameByUICaptionFn PupilEffectMorpherNameStrArray DDPupilEffectControl.items[DDPupilEffectControl.selection]
			local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
			if morpherChannelID != undefined do
			(
				DDPupilEffectControlWeight.value = WM3_MC_GetValue $.modifiers[#Morpher] morpherChannelID	
			)	
		)
		clearSelection()
		select $Eye_Part
		if selection.count == 1 do
		(
			
			local morpherNameStr = GetMorpherNameByUICaptionFn PupilMorpherNameStrArray DDPupilDirs.items[DDPupilDirs.selection]
			local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
			--print morpherNameStr
			if morpherChannelID != undefined do
			(	
				print morpherChannelID
				SldPupilDirWeight.value =WM3_MC_GetValue $.modifiers[#Morpher] morpherChannelID
			)
				
		)
	)
	*/
)
--createdialog EyebrowPartRollout

/*
dsfdsaf

dfds
f
saf
dsf
sda
fasd
f
asd
f
sdaf
asd
f
sda
f
asdd
f
asd
