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
	
	
rollout FacialAnimationMakingDetailsTool "动画调整工具" width:973 height:676
(
	button 'RefurbishBtn' "刷新" pos:[856,30] width:80 height:21 align:#left
	dropdownList 'FacialAnimateNameDDL' "表情动画名称" pos:[611,8] width:111 height:41 align:#left
	button 'ProjectPathBTN' "工程路径" pos:[7,8] width:63 height:18 align:#left
	edittext 'ProjectPathEDT' "" pos:[71,7] width:153 height:18 align:#left
	spinner 'WavOffsetSPN' "声音偏移" pos:[240,37] width:65 height:16 range:[0,10000,0] type:#integer align:#left
	edittext 'AnimateNameEDT' "动画名称" pos:[232,7] width:152 height:16 align:#left
	button 'ExportFacilAnimateBTN' "表情动画导出" pos:[735,31] width:97 height:22 align:#left
	dropdownList 'AnimateNameDDL' "动画名称" pos:[398,11] width:107 height:41 align:#left
	spinner 'MorpherUseableNumSPN' "Morpher数量" pos:[28,33] width:64 height:16 type:#integer align:#left
	button 'ImportMouthXafBTN' "语音口型导入" pos:[738,3] width:93 height:24 align:#left
	button 'StandBTN' "站立" pos:[513,1] width:83 height:22 align:#left
	button 'SailingBTN' "航行" pos:[514,29] width:83 height:22 align:#left
	button 'ResetAllAnimateBtn' "重置动画参数" pos:[854,5] width:87 height:19 align:#left
	--选择动画物体部分
	button 'EyeAnimatePartBtn' "眼皮" pos:[104,60] width:83 height:22 align:#left
	button 'PupilAnimatePartBtn' "瞳孔" pos:[286,60] width:83 height:22 align:#left
	button 'PupilEffectAnimatePartBtn' "瞳孔特效" pos:[382,61] width:83 height:22 align:#left
	button 'EyeEffectAnimatePartBtn' "眼部特效" pos:[477,60] width:83 height:22 align:#left
	button 'FlushAnimatePartBtn' "红晕" pos:[572,60] width:83 height:22 align:#left
	button 'EyebrowAnimatePartBtn' "眉毛" pos:[194,61] width:83 height:22 align:#left
	
	
	GroupBox 'grp1' "眉毛" pos:[5,88] width:474 height:180 align:#left
	GroupBox 'grp2' "眉毛样式" pos:[8,105] width:461 height:74 align:#left
	button 'ButtEyebrowStyle01' "Button" pos:[24,125] width:82 height:20 align:#left
	button 'ButtEyebrowStyle02' "Button" pos:[113,124] width:82 height:20 align:#left
	button 'ButtEyebrowStyle03' "Button" pos:[202,124] width:82 height:20 align:#left
	button 'ButtEyebrowStyle04' "Button" pos:[292,123] width:82 height:20 align:#left
	--button 'ButtEyebrowStyle05' "Button" pos:[384,97] width:82 height:20 align:#left
	GroupBox 'grp3' "细调" pos:[9,183] width:460 height:70 align:#left
	GroupBox 'grp4' "眼部" pos:[-1,288] width:474 height:381 align:#left
	GroupBox 'grp5' "瞳孔方向" pos:[8,437] width:461 height:113 align:#left
	GroupBox 'grp6' "细调" pos:[9,552] width:460 height:109 align:#left
	slider 'SldPupilDirWeight' "位置权重" pos:[139,568] width:100 height:44 range:[0,100,0] align:#left
	dropdownList 'DDPupilDirs' "瞳孔位置" pos:[18,570] width:118 height:41 align:#left
	
	button 'BtnPupilDir' "正常" pos:[272,488] width:82 height:20 align:#left
	button 'BtnPupilDir01' "上" pos:[271,464] width:82 height:20 align:#left
	button 'BtnPupilDir02' "下" pos:[271,515] width:82 height:20 align:#left
	button 'BtnPupilDir03' "左" pos:[179,489] width:82 height:20 align:#left
	button 'BtnPupilDir04' "右" pos:[362,489] width:82 height:20 align:#left
	button 'BtnPupilDir05' "左上" pos:[178,464] width:82 height:20 align:#left
	button 'BtnPupilDir06' "右上" pos:[362,463] width:82 height:20 align:#left
	button 'BtnPupilDir07' "左下" pos:[179,516] width:82 height:20 align:#left
	button 'BtnPupilDir08' "右下" pos:[362,515] width:82 height:20 align:#left
	
	
	radiobuttons 'RdoPupilSync' "眼睛同步" pos:[20,466] width:51 height:46 labels:#("开启", "关闭") default:1 columns:1 align:#left
	radiobuttons 'RdoPupilRandL' "眼睛方向" pos:[87,465] width:51 height:46 labels:#("左眼", "右眼") default:1 columns:1 align:#left
	GroupBox 'grp19' "口型" pos:[486,95] width:474 height:276 align:#left
	GroupBox 'grp20' "口型样式" pos:[494,111] width:461 height:136 align:#left
	button 'BtnMouthStyle01' "Button" pos:[538,133] width:53 height:20 align:#left
	button 'BtnMouthStyle02' "Button" pos:[605,132] width:53 height:20 align:#left
	button 'BtnMouthStyle03' "Button" pos:[668,131] width:53 height:20 align:#left
	button 'BtnMouthStyle04' "Button" pos:[732,131] width:53 height:20 align:#left
	button 'BtnMouthStyle05' "Button" pos:[799,131] width:53 height:20 align:#left
	button 'BtnMouthStyle06' "Button" pos:[865,131] width:53 height:20 align:#left
	button 'BtnMouthStyle07' "Button" pos:[606,191] width:53 height:20 align:#left
	button 'BtnMouthStyle08' "Button" pos:[669,191] width:53 height:20 align:#left
	button 'BtnMouthStyle09' "Button" pos:[733,190] width:53 height:20 align:#left
	button 'BtnMouthStyle10' "Button" pos:[800,189] width:53 height:20 align:#left
	
	--特殊需求按钮
	button 'BtnSpecial_001' "嘴角向下" pos:[864,190] width:52 height:19 align:#left
	button 'ButtResetBtnSpecial_001' "Button" pos:[866,218] width:53 height:20 align:#left
	GroupBox 'grp21' "细调" pos:[491,247] width:460 height:118 align:#left
	--slider 'DDMouthAddStylesWeight' "叠加权重调整" pos:[636,220] width:119 height:44 range:[0,100,0] align:#left
	--dropdownList 'DDMouthAddStyles' "情绪叠加" pos:[510,221] width:118 height:41 align:#left
	slider 'SldMouthAddUp' "上撇" pos:[497,310] width:102 height:44 align:#left
	slider 'SldMouthAddDown' "下撇" pos:[605,310] width:102 height:44 range:[0,100,0] align:#left
	slider 'SldMouthAddScale' "缩嘴" pos:[712,310] width:102 height:44 range:[0,100,0] align:#left
	
	
	
	
	dropdownList 'DDButtEyebrowStyles' "眉毛方位" pos:[18,205] width:118 height:41 align:#left
	spinner 'SpnPupilDirWeight' "权重值" pos:[32,521] width:98 height:16 align:#left
	dropdownList 'DDMouthStyles' "口型" pos:[498,265] width:99 height:41 align:#left
	slider 'DDMouthStylesWeight' "口型调整" pos:[602,261] width:95 height:44 range:[0,100,0] align:#left
	GroupBox 'grp26' "眼皮样式" pos:[6,306] width:461 height:78 align:#left
	button 'ButtEyeStyle01' "Button" pos:[21,328] width:82 height:20 align:#left
	button 'ButtEyeStyle02' "Button" pos:[110,327] width:82 height:20 align:#left
	button 'ButtEyeStyle03' "Button" pos:[199,327] width:82 height:20 align:#left
	button 'ButtEyeStyle04' "Button" pos:[289,326] width:82 height:20 align:#left
	button 'ButtEyeStyle05' "Button" pos:[378,326] width:82 height:20 align:#left
	dropdownList 'DDButtEyeStyles' "眼皮" pos:[11,389] width:102 height:41 align:#left
	slider 'DDButtEyeStylesWeight' "眼皮权重值" pos:[115,388] width:115 height:44 range:[0,100,0] align:#left
	--radiobuttons 'RDOPupilLinkEye' "瞳孔眼皮关联" pos:[21,288] width:106 height:30 labels:#("同步", "异步") columns:2 align:#left
	dropdownList 'DDPupilStyles' "瞳孔造型" pos:[18,615] width:118 height:41 align:#left
	slider 'SldPupilStyleWeight' "位置权重" pos:[139,614] width:100 height:44 range:[0,100,0] align:#left
	
	
	
	
	
	slider 'DDButtEyebrowStylesWeight' "眉毛方位权重" pos:[137,205] width:118 height:44 range:[0,100,0] align:#left
	dropdownList 'DDEyeEffectControlWay' "特殊眼皮" pos:[244,389] width:102 height:41 align:#left
	slider 'DDEyeEffectControlWeight' "特殊眼皮权重" pos:[348,388] width:111 height:44 range:[0,100,0] align:#left
	dropdownList 'DDPupilEffectControl' "瞳孔特效" pos:[236,570] width:118 height:41 align:#left
	slider 'DDPupilEffectControlWeight' "位置权重" pos:[355,566] width:109 height:44 range:[0,100,0] align:#left
	
	
	GroupBox 'grp22' "特殊效果" pos:[487,375] width:474 height:294 align:#left
	spinner 'SPNPupilEffectTexID' "瞳孔特效图片ID" pos:[497,395] width:42 height:16 type:#integer align:#left
	spinner 'spnEyeEffectTexID' "眼睛特效图片ID" pos:[496,414] width:41 height:16 range:[0,100,0] type:#integer align:#left
	slider 'SLDFlushRedIntensity' "红晕明显程度调整" pos:[497,502] width:99 height:44 align:#left
	slider 'SLDFlushBlackIntensity' "黑脸明显程度调整" pos:[499,549] width:100 height:44 range:[0,100,0] align:#left
	colorPicker 'CPFlushRedColor' "红晕颜色" pos:[496,600] width:95 height:22 color:(color 0 0 155) align:#left
	colorPicker 'CPFlushBlackColor' "黑脸颜色" pos:[496,626] width:95 height:22 color:(color 0 0 155) align:#left
	slider 'SLDFlushBlackRange' "红晕黑脸的范围" pos:[495,455] width:100 height:44 range:[0,100,0] align:#left
	checkbox 'CHKFlushState' "是否开启红晕" pos:[497,433] width:94 height:21 align:#left
	button 'RestFlushBtn' "重置红晕动画" pos:[750,388] width:90 height:20 align:#left
	
	button 'DelFlushAnimateBtn' "删除红晕动画" pos:[849,388] width:90 height:20 align:#left
	button 'RedFlushAnimateSetBtn' "脸红设置" pos:[749,416] width:90 height:20 align:#left
	button 'BlackFlushAnimateSetBtn' "脸黑设置" pos:[850,415] width:90 height:20 align:#left
	button 'MouthSayAnimatePartBtn' "口型嘴" pos:[12,59] width:83 height:22 align:#left
	--GroupBox 'XUQIU' "备份需求" pos:[11,620] width:955 height:60 align:#left
	colorPicker 'CPFlushBColor' "B通道颜色" pos:[602,597] width:100 height:22 color:(color 0 0 155) align:#left
	colorPicker 'CPFlushAColor' "A通道颜色" pos:[603,624] width:98 height:22 color:(color 0 0 155) align:#left
	slider 'SLDFlushBIntensity' "B通道强度调整" pos:[601,503] width:99 height:44 range:[0,100,0] align:#left
	slider 'SLDFlushAIntensity' "A通道强度调整" pos:[599,548] width:100 height:44 range:[0,100,0] align:#left
	spinner 'SPNFlushEffectTexID' "红晕图片ID" pos:[615,394] width:42 height:16 range:[0,100,0] type:#integer align:#left
	spinner 'SPNEyeTexID' "瞳孔贴图ID" pos:[616,415] width:41 height:16 range:[0,100,0] type:#integer align:#left
	dropdownList 'DDButtEffectStyles' "脸部特效" pos:[721,471] width:110 height:41 align:#left
	slider 'DDButtEffectStylesWeight' "特效强度调整" pos:[834,468] width:119 height:44 range:[0,100,0] align:#left
	
	dropdownList 'DDFacialStyles' "脸" pos:[708,265] width:99 height:41 align:#left
	slider 'DDFacialStylesWeight' "脸调整" pos:[812,260] width:95 height:44 range:[0,100,0] align:#left
	
	button 'ButtResetEyebrowStyle02' "Button" pos:[113,151] width:82 height:20 align:#left
	button 'ButtResetEyebrowStyle03' "Button" pos:[202,151] width:82 height:20 align:#left
	button 'ButtResetEyebrowStyle04' "Button" pos:[292,150] width:82 height:20 align:#left
	button 'BtnResetMouthStyle07' "Button" pos:[607,220] width:53 height:20 align:#left
	button 'BtnResetMouthStyle08' "Button" pos:[670,220] width:53 height:20 align:#left
	button 'BtnResetMouthStyle09' "Button" pos:[735,219] width:53 height:20 align:#left
	button 'BtnResetMouthStyle10' "Button" pos:[801,218] width:53 height:20 align:#left
	button 'BtnResetMouthStyle02' "Button" pos:[605,162] width:53 height:20 align:#left
	button 'BtnResetMouthStyle03' "Button" pos:[667,161] width:53 height:20 align:#left
	button 'BtnResetMouthStyle04' "Button" pos:[732,161] width:53 height:20 align:#left
	button 'BtnResetMouthStyle05' "Button" pos:[799,161] width:53 height:20 align:#left
	button 'BtnResetMouthStyle06' "Button" pos:[865,161] width:53 height:20 align:#left
	button 'ButtResetEyeStyle02' "Button" pos:[110,355] width:82 height:20 align:#left
	button 'ButtResetEyeStyle03' "Button" pos:[199,355] width:82 height:20 align:#left
	button 'ButtResetEyeStyle04' "Button" pos:[288,353] width:82 height:20 align:#left
	button 'ButtResetEyeStyle05' "Button" pos:[378,354] width:82 height:20 align:#left
	
	
	
	
	
	
	
	
	local isEyeEffectPart = false
	local isPupilEffectPart = false

	local isEyeDouble =true
	local isEyeRight = false
	
	
	
	
	local tempEyebrowUIControlsArray = #()
	local tempEyeUIControlsArray =#()
	local tempPupilUIControlsArray =#()
	local tempMouthUIControlsArray =#()

	
	fn PupilEffectInitValueFn =
	(
		if isPupilEffectPart do
		(
			--local tempMorpherNameArray = #("Effect_Pupil_appear_parallel","Effect_Pupil_appear_symmetry")
			local tempMorpherNameArray = #("Effect_Pupil_appear_parallel","Effect_Pupil_appear_symmetry")
			clearSelection()
			select $Pupil_Effect_Part
			if selection.count == 1 do
			(	
				for i in  tempMorpherNameArray do
				(
					local tempMorpherID =  GetMorpherIDByStringFn $  i
					if tempMorpherID != undefined do
					(
						WM3_MC_SetValue $.modifiers[1] tempMorpherID 100.0
					)	
				)
			)
		)	
	)
	
	fn CollectUIControlsFN = 
	(
		for b in FacialAnimationMakingDetailsTool.controls do
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
		
	

		
	
	fn aaa =
	(
		select  $*_Body_H_001
		if selection.count == 1 do
		(
			ff = copy $.Material 
			--ff.name = "material"
			$*_Body_H_001.material = ff
		)	
	)
	
	
	
	------逻辑函数
	fn ToolOpenMatchUINameFn =
	(
		CollectUIControlsFN()
		--按钮UI
		PartMorpherMatchUIControlsFN 	tempEyebrowUIControlsArray 	EyebrowMorpherNameStrArray  	(EyebrowMorpherNameStrArray.count-2) 	EyebrowMorpherNameStrArray.count
		PartMorpherMatchUIControlsFN 	tempEyeUIControlsArray 		EyeMorpherNameStrArray  		6 		EyeMorpherNameStrArray.count
		PartMorpherMatchUIControlsFN 	tempMouthUIControlsArray	MouthSayMorpherNameStrArray  	1										MouthSayMorpherNameStrArray.count
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
		local tempMouthArray  =  MouthSayMorpherNameStrArray  + MouthStyleMorpherNameStrArray
		PartMorpherMatchUIDDlistFN		DDMouthStyles				tempMouthArray			1		tempMouthArray.count
-------------------------------------------------------------		
		PartMorpherMatchUIDDlistFN		DDButtEffectStyles		EffectMorpherNameStrArray			1		EffectMorpherNameStrArray.count
		
		
		PartMorpherMatchUIDDlistFN      DDFacialStyles          FacialMorpherNameStrArray    1        FacialMorpherNameStrArray.count
	)
	
	
	
	--通过morpher的名字，让对应部分的morpher通道与头部的morpher通道做关联
	fn ConnectMorpherChannelOfToolsFn =
	(
		/*
		select $*_Body_H_001
		selectmore $Mouth_Say_Part
		local MorpherNameStringArray = GetMorpherNameArrayByPartMouthArrayFn MouthSayMorpherNameStrArray
		for hsh in MorpherNameStringArray do
		(
			SetMorpherValuecConnectFn selection[1] selection[2] hsh
		)
		*/
		local tempMorpherArray = MouthSayMorpherNameStrArray+MouthStyleMorpherNameStrArray
		select $*_Body_H_001
		selectmore $Mouth_Part
		local MorpherNameStringArray = GetMorpherNameArrayByPartMouthArrayFn tempMorpherArray
		for hsh in MorpherNameStringArray do
		(
			SetMorpherValuecConnectFn selection[1] selection[2] hsh
		)
		select $*_Body_H_001
		selectmore $Eye_Part
		local MorpherNameStringArray = GetMorpherNameArrayByPartMouthArrayFn EyeMorpherNameStrArray
		for hsh in MorpherNameStringArray do
		(
			SetMorpherValuecConnectFn selection[1] selection[2] hsh
		)	
		select $*_Body_H_001
		selectmore $Eyebrow_Part
		local MorpherNameStringArray = GetMorpherNameArrayByPartMouthArrayFn EyebrowMorpherNameStrArray
		for hsh in MorpherNameStringArray do
		(
			SetMorpherValuecConnectFn selection[1] selection[2] hsh
		)
		
		select $*_Body_H_001
		selectmore $Facial_Part
		local MorpherNameStringArray = GetMorpherNameArrayByPartMouthArrayFn FacialMorpherNameStrArray
		for hsh in MorpherNameStringArray do
		(
			SetMorpherValuecConnectFn selection[1] selection[2] hsh
		)
		
		
		
		select $*_Eye_001
		selectmore $Pupil_Part
		local MorpherNameStringArray = GetMorpherNameArrayByPartMouthArrayFn PupilMorpherNameStrArray
		for hsh in MorpherNameStringArray do
		(
			SetMorpherValuecConnectFn selection[1] selection[2] hsh
		)
		if isPupilEffectPart do
		(
			select $*_Pupil_Effect_001
			selectmore $Pupil_Effect_Part
			local MorpherNameStringArray = GetMorpherNameArrayByPartMouthArrayFn PupilEffectMorpherNameStrArray
			for hsh in MorpherNameStringArray do
			(
				SetMorpherValuecConnectFn selection[1] selection[2] hsh
			)
			select $Pupil_Part
			selectmore $Pupil_Effect_Part
			local MorpherNameStringArray = GetMorpherNameArrayByPartMouthArrayFn PupilMorpherNameStrArray
			for hsh in MorpherNameStringArray do
			(
				local tempMorpherID = GetMorpherIDByStringFn selection[1] hsh
				hsh = substituteString hsh "Pupil" "Effect_Pupil"
				local tempMorpherID2 = GetMorpherIDByStringFn selection[2] hsh

				if tempMorpherID != undefined and tempMorpherID2 != undefined do
				(
					local tempMorpherIDControllerNameStr = selection[1].modifiers[#Morpher][tempMorpherID].name
					tempMorpherIDControllerNameStr = substituteString  tempMorpherIDControllerNameStr "[" "_"
					tempMorpherIDControllerNameStr = substituteString  tempMorpherIDControllerNameStr "]" "_"
					tempMorpherIDControllerNameStr = substituteString  tempMorpherIDControllerNameStr " " "_"
					tempMorpherIDControllerNameStr = substituteString  tempMorpherIDControllerNameStr "(" "_"
					tempMorpherIDControllerNameStr = substituteString  tempMorpherIDControllerNameStr ")" "_"
					paramWire.connect selection[1].modifiers[#Morpher][tempMorpherID] selection[2].modifiers[#Morpher][tempMorpherID2] tempMorpherIDControllerNameStr
				)
			)
		)
		if isEyeEffectPart do
		(
			select $*_Eye_Effect_001
			selectmore $Eye_Effect_Part
			local MorpherNameStringArray = GetMorpherNameArrayByPartMouthArrayFn EyeEffectMorpherNameStrArray
			for hsh in MorpherNameStringArray do
			(
				SetMorpherValuecConnectFn selection[1] selection[2] hsh
			)
		)	
	)
	--把控制器的动画复制给头部
	fn ProjectBtnCopyMorpherAnimateFn =
	(	
		/*
		select $*_Body_H_001
		selectmore $Mouth_Say_Part
		CopyMorpherAnimateFn  selection[1] selection[2]  MouthSayMorpherNameStrArray
		*/
		local tempMouthStyleMorpherName = MouthSayMorpherNameStrArray + MouthStyleMorpherNameStrArray
		select $*_Body_H_001
		selectmore $Mouth_Part
		CopyMorpherAnimateFn selection[1] selection[2] tempMouthStyleMorpherName
		
		select $*_Body_H_001
		selectmore $Eye_Part
		CopyMorpherAnimateFn selection[1] selection[2] EyeMorpherNameStrArray	
		
		
		select $*_Body_H_001
		selectmore $Eyebrow_Part
		CopyMorpherAnimateFn selection[1] selection[2] EyebrowMorpherNameStrArray
		
		select $*_Body_H_001
		selectmore $Facial_Part
		CopyMorpherAnimateFn selection[1] selection[2] FacialMorpherNameStrArray
		
		select $*_Eye_001
		selectmore $Pupil_Part
		CopyMorpherAnimateFn selection[1] selection[2] PupilMorpherNameStrArray
		
		
		
		
		if isPupilEffectPart do
		(
			select $*_Pupil_Effect_001
			selectmore $Pupil_Effect_Part
			CopyMorpherAnimateFn selection[1] selection[2] PupilEffectMorpherNameStrArray
		)
		
		if isEyeEffectPart do
		(
			select $*_Eye_Effect_001
			selectmore $Eye_Effect_Part
			CopyMorpherAnimateFn selection[1] selection[2] EyeEffectMorpherNameStrArray
		)	
	)
	--把头部的动画分别复制给对应的部位
	fn ProjectBtnCopyMorpherAnimateFn2 =
	(	
		/*
		select $Mouth_Say_Part
		DelMorpherChannelCotrollerKeysFn $
		selectmore $*_Body_H_001
		
		CopyMorpherAnimateFn  selection[1] selection[2]  MouthSayMorpherNameStrArray
		*/
		local tempMouthStyleMorpherName = MouthSayMorpherNameStrArray + MouthStyleMorpherNameStrArray
		select $Mouth_Part
		DelMorpherChannelCotrollerKeysFn $
		selectmore $*_Body_H_001
		CopyMorpherAnimateFn selection[1] selection[2] tempMouthStyleMorpherName
		
		select $Eye_Part
		DelMorpherChannelCotrollerKeysFn $
		selectmore $*_Body_H_001
		CopyMorpherAnimateFn selection[1] selection[2] EyeMorpherNameStrArray	
		
		select $Eyebrow_Part
		DelMorpherChannelCotrollerKeysFn $
		selectmore $*_Body_H_001
		CopyMorpherAnimateFn selection[1] selection[2] EyebrowMorpherNameStrArray
		
		select $Facial_Part
		DelMorpherChannelCotrollerKeysFn $
		selectmore $*_Body_H_001
		CopyMorpherAnimateFn selection[1] selection[2] FacialMorpherNameStrArray
		
		
		
		
		select $Pupil_Part
		DelMorpherChannelCotrollerKeysFn $
		selectmore $*_Eye_001
		CopyMorpherAnimateFn selection[1] selection[2] PupilMorpherNameStrArray
		
		if isPupilEffectPart do
		(
			select $Pupil_Effect_Part
			DelMorpherChannelCotrollerKeysFn $
			selectmore $*_Pupil_Effect_001
			CopyMorpherAnimateFn selection[1] selection[2] PupilEffectMorpherNameStrArray
		)
		
		if isEyeEffectPart do
		(
			select $Eye_Effect_Part
			DelMorpherChannelCotrollerKeysFn $
			selectmore $*_Eye_Effect_001
			CopyMorpherAnimateFn selection[1] selection[2] EyeEffectMorpherNameStrArray
		)	
	)
	--清楚所有关联绑定关系
	fn ProjectBtnClearConnectFn =
	(
		--清楚与脸部的关联关系
		clearSelection()
		select $*_Body_H_001
		if selection.count == 1 do
		(
			ClearMorpherConnectFn $
		)
		clearSelection()
		select $*EffectPart_001
		if selection.count == 1 do
		(
			ClearMorpherConnectFn $
		)		
		clearSelection()
		select $*Eye_001
		if selection.count == 1 do
		(
			ClearMorpherConnectFn $
		)	
		if isPupilEffectPart do
		(
			select $*Pupil_Effect_001
			ClearMorpherConnectFn $
		)
		if isEyeEffectPart do
		(
			select $*Eye_Effect_001
			ClearMorpherConnectFn $
		)
	)
	fn ClearFacialKeysFn =
	(
		--清楚与脸部的关联关系
		clearSelection()
		select $*_Body_H_001
		if selection.count == 1 do
		(
			DelMorpherChannelCotrollerKeysFn $
			DelMaterialKeysFn $
			ResetMorpherChannelFn $ 0.0
			deleteKeys $
		)	
		clearSelection()
		select $*Eye_001
		if selection.count == 1 do
		(
			DelMorpherChannelCotrollerKeysFn $
			ResetMorpherChannelFn $ 0.0
			deleteKeys $
		)
		clearSelection()
		select $*EffectPart_001
		if selection.count == 1 do
		(
			ClearMorpherConnectFn $
			ResetMorpherChannelFn $ 0.0
			deleteKeys $
		)		
		if isPupilEffectPart do
		(
			select $*Pupil_Effect_001
			DelMorpherChannelCotrollerKeysFn $
			ResetMorpherChannelFn $ 100
			deleteKeys $
		)
		if isEyeEffectPart do
		(
			select $*Eye_Effect_001
			DelMorpherChannelCotrollerKeysFn $
			ResetMorpherChannelFn $ 0.0
			deleteKeys $
		)
			
	)
	fn ClearCopyPartFacialKeysFn =
	(
		--清楚与脸部的关联关系
		clearSelection()
		select $*_Body_H_001
		if selection.count == 1 do
		(
			DelMorpherChannelCotrollerKeysFn $
			DelMaterialKeysFn $
			ResetMorpherChannelFn $ 0.0
			deleteKeys $
		)	
		clearSelection()
		select $Eye_001
		if selection.count == 1 do
		(
			DelMorpherChannelCotrollerKeysFn $
			ResetMorpherChannelFn $ 0.0
			deleteKeys $
		)
		clearSelection()
		select $*EffectPart_001
		if selection.count == 1 do
		(
			ClearMorpherConnectFn $
			ResetMorpherChannelFn $ 0.0
			deleteKeys $
		)		
		if isPupilEffectPart do
		(
			select $*Pupil_Effect_001
			DelMorpherChannelCotrollerKeysFn $
			ResetMorpherChannelFn $ 100
			deleteKeys $
		)
		if isEyeEffectPart do
		(
			select $*Eye_Effect_001
			DelMorpherChannelCotrollerKeysFn $
			ResetMorpherChannelFn $ 0.0
			deleteKeys $
		)
			
	)
	
	--工具打开的时候要做的工作
	fn ProjectOpenFn =
	(
		ProjectPathEDT.text = GetProjectPathFn()
		if ProjectPathEDT.text.count == 0 do
		(
			messagebox "文件是空文件"
			return -1
		)
		--创建瞳孔贴图和特效片贴图需要的控制器
		clearSelection()
		select $*Pupil_Effect_001
		if selection.count == 1 do
		(	
			isPupilEffectPart = true
			try
			(
				if ((classof $.EyeTextureTrans) as string) == "<AttributeDef:EyeTextureTrans>" do
				(
					print "已经存在控件"
				)	
			)
			catch
			(
				ca = attributes EyeTextureTrans
				(
					Parameters aa rollout:bb 
					(
						texIndex type:#Integer ui:TexID
					)
					rollout bb "显示贴图控制"
					(
						spinner TexID "贴图ID" Type:#integer range:[0,100,0]
					)	
				)
				custAttributes.add $ ca
			)
		)
		clearSelection()
		select  $*Eye_Effect_001
		if selection.count == 1 do
		(
			isEyeEffectPart = true		
			try
			(
				if ((classof $.EyeTextureTrans) as string) == "<AttributeDef:EyeTextureTrans>" do
				(
					print "已经存在控件"
				)	
			)
			catch
			(
				ca = attributes EyeTextureTrans
				(
					Parameters aa rollout:bb 
					(
						texIndex type:#Integer ui:TexID
					)
					rollout bb "显示贴图控制"
					(
						spinner TexID "贴图ID" Type:#integer range:[0,100,0]
					)
				)
				custAttributes.add $ ca
			)	
		)
		clearSelection()
		select  $*Body_H_001
		if selection.count == 1 do
		(
			--isEyeEffectPart = true		
			try
			(
				if ((classof $.EyeTextureTrans) as string) == "<AttributeDef:EyeTextureTrans>" do
				(
					print "已经存在控件"
				)	
			)
			catch
			(
				ca = attributes EyeTextureTrans
				(
					Parameters aa rollout:bb 
					(
						texIndex type:#Integer ui:TexID
					)
					rollout bb "显示贴图控制"
					(
						spinner TexID "贴图ID" Type:#integer range:[0,100,0]
					)
				)
				custAttributes.add $ ca
			)	
		)
		clearSelection()
		select  $*Eye_001
		if selection.count == 1 do
		(
			--isEyeEffectPart = true		
			try
			(
				if ((classof $.EyeTextureTrans) as string) == "<AttributeDef:EyeTextureTrans>" do
				(
					print "已经存在控件"
				)	
			)
			catch
			(
				ca = attributes EyeTextureTrans
				(
					Parameters aa rollout:bb 
					(
						texIndex type:#Integer ui:TexID
					)
					rollout bb "显示贴图控制"
					(
						spinner TexID "贴图ID" Type:#integer range:[0,100,0]
					)
				)
				custAttributes.add $ ca
			)	
		)
		ToolOpenMatchUINameFn()
		--aaa()函数是给脸赋予一个单独的材质球，这样可以让红晕动画的帧单独显示
		aaa()
		--创建单独控件的物体
		local IndexID = 0
		select $*_Body_H_001
		if selection.count == 1 then
		(
			for hsh in 1 to 4  do
			(	
				IndexID += 1
				CreatControlMoprherObjFn selection[1] facialPartMorpherObjNameStrArray[hsh] hsh
			)
		)
		else
		(
			messagebox "没有脸的模型，请确认文件是否正确"
			return undefined
		)
		
		select $*Eye_001
		if selection.count == 1 do
		(
			IndexID += 1
			CreatControlMoprherObjFn selection[1] facialPartMorpherObjNameStrArray[IndexID] IndexID
		)	
		if isPupilEffectPart do
		(
			IndexID += 1
			select $*Pupil_Effect_001
			CreatControlMoprherObjFn selection[1] facialPartMorpherObjNameStrArray[IndexID] IndexID
		)
		if isEyeEffectPart do
		(
			IndexID += 1
			select $*Eye_Effect_001
			CreatControlMoprherObjFn selection[1] facialPartMorpherObjNameStrArray[IndexID] IndexID
		)
		--创建关联关系
		ConnectMorpherChannelOfToolsFn()
		--
		AnimateNameDDL.items = ProjectAnimateNames
		AnimateNameEDT.text = AnimateNameDDL.items[1]
		FacialAnimateNameDDL.items = ProjectFacialAnimateNames
	)
	fn ToolUIFlushRedByMaterialValueFn =
	(
		try
		(
			select $*_Body_H_001
			SLDFlushRedIntensity.value = (($.Material._FlushIntensity.r/255) *100)
			SLDFlushBlackIntensity.value = (($.Material._FlushIntensity.g/255) *100)
			SLDFlushBIntensity.value = (($.Material._FlushIntensity.b/255) *100)
			SLDFlushAIntensity.value = (($.Material._FlushIntensity.a/255) *100)
			
			CPFlushRedColor.color = $.Material._RedFlushColor
			CPFlushBlackColor.color = $.Material._BlackFlushColor
			CPFlushBColor.color = $.Material._FlushColorB
			CPFlushAColor.color = $.Material._FlushColorA
			SLDFlushRedIntensity.value = $.Material._FlushRange
			CHKFlushState.state = $.Material._FaceFlushToggle
		)
		catch
		(
			messagebox "脸部材质球不对"
		)
		
	)
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

	
	--#("Mouth_Say_Part","Mouth_Part","Eye_Part","Eyebrow_Part","Pupil_Part","Pupil_Effect_Part","Eye_Effect_Part")
	
	
	/*
	on DDMouthAddStylesWeight changed val do
	(
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ DDMouthAddStyles.items[DDMouthAddStyles.selection] MouthStyleMorpherNameStrArray DDMouthAddStylesWeight.value
	)
	
	on DDMouthAddStyles selected sel do
		(
	
	)
	*/

	
	
	
	
	
	
	on FacialAnimationMakingDetailsTool open do
	(
		ImportInfoDataFn (getThisScriptFilename())
		ClearFacialKeysFn()
		prosound.init true
		--ImportInfoDataFn()
		ProjectOpenFn()
		PupilEffectInitValueFn()
		ToolUIFlushRedByMaterialValueFn()
	)
	on FacialAnimationMakingDetailsTool close do
	(
		ProjectBtnClearConnectFn()
		--清楚创建出来的多余物体
		DelControlMoprherObjFn facialPartMorpherObjNameStrArray
		--清楚瞳孔贴图和特效片贴图需要的控制器
		if isEyeEffectPart do
		(
			select  $*Eye_Effect_001
			if selection.count == 1 do
			(	
				try
				(	
					custAttributes.delete $ (classof $.EyeTextureTrans)
				)
				catch
				(
					print "眼睛特效片没有这个控件"
				)			
			)
		)
		if isPupilEffectPart do
		(
			select $*Pupil_Effect_001
			if selection.count == 1 do
			(	
				try
				(	
					custAttributes.delete $ (classof $.EyeTextureTrans)
				)
				catch
				(
					print "瞳孔特效片没有这个控件"
				)
			)
		)	
	)
	on RefurbishBtn pressed do
	(
		clearSelection()
		select $*Body_H_001
		if selection.count == 1 do
		(
			CHKFlushState.state = $.Material._FaceFlushToggle
			SLDFlushBlackRange.value = $.Material._FlushRange*100
			CPFlushBlackColor.color = $.Material._BlackFlushColor
			CPFlushRedColor.color = $.Material._RedFlushColor
			SLDFlushBlackIntensity.value = ($.Material._FlushIntensity.g/255)*100
			SLDFlushRedIntensity.value = ($.Material._FlushIntensity.r/255)*100
			--眉毛列表
			local morpherNameStr = GetMorpherNameByUICaptionFn EyebrowMorpherNameStrArray DDButtEyebrowStyles.items[DDButtEyebrowStyles.selection]
			local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
			if morpherChannelID != undefined do
			(
				DDButtEyebrowStylesWeight.value = WM3_MC_GetValue $.modifiers[#Morpher] morpherChannelID
			)
			--眼睛列表
			local morpherNameStr = GetMorpherNameByUICaptionFn EyeMorpherNameStrArray DDButtEyeStyles.items[DDButtEyeStyles.selection]
			local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
			if morpherChannelID != undefined do
			(
				DDButtEyeStylesWeight.value =  WM3_MC_GetValue $.modifiers[#Morpher]  morpherChannelID
			)	
			--嘴型列表权重归零
			local tempMouthMorpherArray = MouthSayMorpherNameStrArray + MouthStyleMorpherNameStrArray
			local morpherNameStr = GetMorpherNameByUICaptionFn tempMouthMorpherArray DDMouthStyles.items[DDMouthStyles.selection]
			local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
			if morpherChannelID != undefined do
			(
				DDMouthStylesWeight.value = WM3_MC_GetValue $.modifiers[#Morpher] morpherChannelID
			)
	/*			
			local morpherNameStr = GetMorpherNameByUICaptionFn tempMouthMorpherArray DDMouthAddStyles.items[DDMouthAddStyles.selection]
			local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
			if morpherChannelID != undefined do
			(
				DDMouthAddStylesWeight.value   =WM3_MC_GetValue $.modifiers[#Morpher] morpherChannelID	
			)
	*/			
		)
		clearSelection()
		select $*Eye_001
		if selection.count == 1 do
		(
			local morpherNameStr = GetMorpherNameByUICaptionFn PupilMorpherNameStrArray DDPupilDirs.items[DDPupilDirs.selection]
			local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
			if morpherChannelID != undefined do
			(	
				SldPupilDirWeight.value =WM3_MC_GetValue $.modifiers[#Morpher] morpherChannelID
			)
			
		)
		if isEyeEffectPart do
		(	
			clearSelection()
			select $*Eye_Effect_001
			if selection.count == 1 do
			(
				spnEyeEffectTexID.value = $.baseObject.EyeTextureTrans.texIndex
				local morpherNameStr = GetMorpherNameByUICaptionFn EyeEffectMorpherNameStrArray DDEyeEffectControlWay.items[DDEyeEffectControlWay.selection]
				local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
				if morpherChannelID != undefined do
				(
					DDEyeEffectControlWeight.value = WM3_MC_GetValue $.modifiers[#Morpher]  morpherChannelID
				)	
			)
		)
		if isPupilEffectPart do
		(
			clearSelection()
			select $*Pupil_Effect_001
			if selection.count == 1 do
			(
				SPNPupilEffectTexID.value = $.baseObject.EyeTextureTrans.texIndex
				local morpherNameStr = GetMorpherNameByUICaptionFn PupilEffectMorpherNameStrArray DDPupilEffectControl.items[DDPupilEffectControl.selection]
				local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
				if morpherChannelID != undefined do
				(
					DDPupilEffectControlWeight.value = WM3_MC_GetValue $.modifiers[#Morpher] morpherChannelID	
				)	
			)
		)
	)
	on FacialAnimateNameDDL selected sel do
	(
		
		ProjectBtnClearConnectFn()
		ClearFacialKeysFn()
		
		ImportXafFn FacialAnimateNameDDL.items[sel] ProjectPathEDT.text 100
		ProjectBtnCopyMorpherAnimateFn2()
		ConnectMorpherChannelOfToolsFn()
		
		
		
		--PupilEffectInitValueFn()
		--ToolUIFlushRedByMaterialValueFn()
	)
	on ProjectPathBTN pressed do
	(
		a = getSavePath()
		if a ==null then
			messageBox "请选择路径"
		else
		(	
			b = a +"\\"
			ProjectPathEDT.text = b
			--getDic["FilePath"] = b
		)
	)
	on WavOffsetSPN changed val do
	(
		SoundStartFn WavOffsetSPN.value 1
	)
	on AnimateNameEDT entered text do
	(	
		ImportBipFn	AnimateNameEDT.text ProjectPathEDT.text
		ImportSoundFn AnimateNameEDT.text ProjectPathEDT.text
	)
	on ExportFacilAnimateBTN pressed do
	(
		--清楚与脸部的关联关系
		ProjectBtnClearConnectFn()
		--把控制部位的动画传值给脸部
		ProjectBtnCopyMorpherAnimateFn()
		--导出fbx
		--ExportFacialFbxFn FacialAnimateNameDDL.items[FacialAnimateNameDDL.selection]  ProjectPathEDT.text
		--导出xaf
		ExportXafFn FacialAnimateNameDDL.items[FacialAnimateNameDDL.selection]  ProjectPathEDT.text
		--把动画数据再传回控制部位
		ProjectBtnCopyMorpherAnimateFn2()
		--关联控制部位跟脸的关系
		ConnectMorpherChannelOfToolsFn()
		messagebox "导出动画完成"
	)
	on AnimateNameDDL selected sel do
	(
		AnimateNameEDT.text = AnimateNameDDL.items[sel]
		ImportBipFn	AnimateNameEDT.text ProjectPathEDT.text
		ImportSoundFn AnimateNameEDT.text ProjectPathEDT.text
	)
	on ImportMouthXafBTN pressed do
	(
		select $Mouth_Part
		ImportMouthSayXafFN AnimateNameEDT.text ProjectPathEDT.text $
	)
	on StandBTN pressed do
	(
		ImportBipFn	"stand_loop" ProjectPathEDT.text
	)
	on SailingBTN pressed do
	(
		ImportBipFn	"sailing_loop" ProjectPathEDT.text
	)
	on ResetAllAnimateBtn pressed do
	(
		messagebox "还在开发中" 
		--ResetFlushRedOfMaterialFn()
		--ToolUIFlushRedByMaterialValueFn()
	)
	on EyeAnimatePartBtn pressed do
	(
		clearSelection()
		if $Eye_Part == undefined then
		(
			messagebox "文件内没有该物体"
		)
		else
		(
			select $Eye_Part
		)
	)
	on PupilAnimatePartBtn pressed do
	(
		clearSelection()
		if $Pupil_Part == undefined then
		(
			messagebox "文件内没有该物体"
		)s
		else
		(
			select $Pupil_Part
		)
	)
	on PupilEffectAnimatePartBtn pressed do
	(
		clearSelection()
		if $Pupil_Effect_Part == undefined then
		(
			messagebox "文件内没有该物体"
		)
		else
		(
			select $Pupil_Effect_Part
		)
	)
	on EyeEffectAnimatePartBtn pressed do
	(
		clearSelection()
		if $Eye_Effect_Part == undefined then
		(
			messagebox "文件内没有该物体"
		)
		else
		(
			select $Eye_Effect_Part
		)
	)
	on FlushAnimatePartBtn pressed do
	(
		clearSelection()
		if $*Body_H_001 == undefined then
		(
			messagebox "文件内没有该物体"
		)
		else
		(
			select $*Body_H_001
		)
	)
	on EyebrowAnimatePartBtn pressed do
	(
		clearSelection()
		if $Eyebrow_Part == undefined then
		(
			messagebox "文件内没有该物体"
		)
		else
		(
			select $Eyebrow_Part
		)
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
	on SldMouthAddScale changed val do
	(
		local tempMorpherArray = MouthStyleMorpherNameStrArray + MouthSayMorpherNameStrArray
		select $Mouth_Part
		SetMorpherValueByUICaptionFn $ SldMouthAddScale.caption tempMorpherArray SldMouthAddScale.value
	)
	on DDButtEyebrowStyles selected sel do
	(
		print(DDButtEyebrowStyles.items[sel])
		DDButtEyebrowStylesWeight.value = GetMorpherValueByUICaptionFn $Eyebrow_Part EyebrowMorpherNameStrArray DDButtEyebrowStyles.items[sel]
		
	)
	on SpnPupilDirWeight changed val do
		(
	
	)
	on DDMouthStyles selected sel do
	(
		print(DDMouthStyles.items[sel])
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
		--print (DDPupilStyles.items[sel])
	)
	on SldPupilStyleWeight changed val do
	(
		SetEyeMorpherValueByUICaptionFn  DDPupilStyles.items[DDPupilStyles.selection]  SldPupilStyleWeight.value
		
		select $Pupil_Part
		SetMorpherValueByUICaptionFn $  DDPupilStyles.items[DDPupilStyles.selection] PupilMorpherNameStrArray SldPupilStyleWeight.value
		
	)
	on DDButtEyebrowStylesWeight changed val do
	(
		select $Eyebrow_Part
		SetMorpherValueByUICaptionFn $ DDButtEyebrowStyles.items[DDButtEyebrowStyles.selection] EyebrowMorpherNameStrArray DDButtEyebrowStylesWeight.value
	)
	on DDEyeEffectControlWay selected sel do
	(
		if isEyeEffectPart do
		(
			DDEyeEffectControlWeight.value = GetMorpherValueByUICaptionFn $Eye_Effect_Part EyeEffectMorpherNameStrArray DDEyeEffectControlWay.items[sel]	
		)	
	)
	on DDEyeEffectControlWeight changed val do
	(
		if isEyeEffectPart do
		(
			select $Eye_Effect_Part
			SetMorpherValueByUICaptionFn $ DDEyeEffectControlWay.items[DDEyeEffectControlWay.selection] EyeEffectMorpherNameStrArray DDEyeEffectControlWeight.value
		)	
	)
	on DDPupilEffectControl selected sel do
	(
		if isPupilEffectPart do
		(
			DDPupilEffectControlWeight.value = GetMorpherValueByUICaptionFn $Pupil_Effect_Part PupilEffectMorpherNameStrArray DDPupilEffectControl.items[sel]	
		)
	)
	on DDPupilEffectControlWeight changed val do
	(
		if isPupilEffectPart do
		(
			select $Pupil_Effect_Part
			SetMorpherValueByUICaptionFn $ DDPupilEffectControl.items[DDPupilEffectControl.selection] PupilEffectMorpherNameStrArray DDPupilEffectControlWeight.value
		)	
	)
	on SPNPupilEffectTexID changed val do
	(
		if isPupilEffectPart do
		(
			clearSelection()
			select $*Pupil_Effect_001
			if selection.count == 1 do
			(	
				$.baseObject.EyeTextureTrans.texIndex = SPNPupilEffectTexID.value
				local a = ""
				if (SPNPupilEffectTexID.value+1)<10 then
				(	
					a = maxfilepath  + (substring $.name 1 ($.name.count-3))+ "00"+ ((SPNPupilEffectTexID.value+1) as string) +".tga"
				)	
				else
				(
					a = maxfilepath  + (substring $.name 1 ($.name.count-3))+ "0"+ ((SPNPupilEffectTexID.value+1) as string) +".tga"
				)
				try
				(
					$.material.diffusemap.filename = a
					$.material.opacitymap.filename = a
				)
				catch
				(
					messagebox "瞳孔特效片的材质球不对"
				)
			)
		)	
	)
	on spnEyeEffectTexID changed val do
	(
		if isEyeEffectPart do
		(
			clearSelection()
			select $*Eye_Effect_001
			if selection.count == 1 do
			(	
				$.baseObject.EyeTextureTrans.texIndex = spnEyeEffectTexID.value
				local a = ""
				if (spnEyeEffectTexID.value+1) <10 then
				(
					a = maxfilepath  + (substring $.name 1 ($.name.count-3))+ "00"+ ((spnEyeEffectTexID.value+1) as string) +".tga"									
				)
				else
				(
					a = maxfilepath  + (substring $.name 1 ($.name.count-3))+ "0"+ ((spnEyeEffectTexID.value+1) as string) +".tga"	
				)
				try
				(
					$.material.diffusemap.filename = a
					$.material.opacitymap.filename = a
				)
				catch
				(
					messagebox "眼睛特效片的材质球不对"
				)
				
			)
		)	
	)
	on SLDFlushRedIntensity changed val do
	(
		select $*Body_H_001
		$.Material._FlushIntensity.r = ((SLDFlushRedIntensity.value/100)*255)
	)
	on SLDFlushBlackIntensity changed val do
	(
		select $*Body_H_001
		$.Material._FlushIntensity.g = ((SLDFlushBlackIntensity.value/100)*255)
	)
	on CPFlushRedColor changed col do
	(
		select $*Body_H_001
		$.Material._RedFlushColor = CPFlushRedColor.color
	)
	on CPFlushBlackColor changed col do
	(
		select $*Body_H_001
		$.Material._BlackFlushColor = CPFlushBlackColor.color
	)
	on SLDFlushBlackRange changed val do
	(
		select $*Body_H_001
		$.Material._FlushRange = SLDFlushBlackRange.value/100
	)
	on CHKFlushState changed state do
	(
		select $*Body_H_001
		if CHKFlushState.state == on then
		(	
			$.Material._FaceFlushToggle = on
		)
		else
		(
			$.Material._FaceFlushToggle = off
		)
	)
	on RestFlushBtn pressed do
	(
		ResetFlushRedOfMaterialFn()
		ToolUIFlushRedByMaterialValueFn()
		$.material._FaceFlushToggle = on
	)
	on DelFlushAnimateBtn pressed do
	(
		ResetFlushRedOfMaterialFn()
		ToolUIFlushRedByMaterialValueFn()
		select $*_Body_H_001
		deleteKeys $.material
		
	)
	on RedFlushAnimateSetBtn pressed do
	(
		ResetFlushRedOfMaterialFn()
		select $*Body_H_001
		$.material._FaceFlushToggle = on
		$.material._FlushIntensity = color 255 0 0 0
		$.material._RedFlushColor = color 255 0 0 255
		$.material._BlackFlushColor = color 0 0 0 255
		$.material._FlushColorB = color 0 0 0 255
		$.material._FlushColorA = color 0 0 0 255
		$.Material._FlushRange = 1.0
		ToolUIFlushRedByMaterialValueFn()
	)
	on BlackFlushAnimateSetBtn pressed do
	(
		ResetFlushRedOfMaterialFn()
		select $*Body_H_001
		$.material._FaceFlushToggle = on
		$.material._FlushIntensity = color 0 255 0 0
		$.material._RedFlushColor = color 255 0 0 255
		$.material._BlackFlushColor = color 0 0 0 255
		$.material._FlushColorB = color 0 0 0 255
		$.material._FlushColorA = color 0 0 0 255
		$.Material._FlushRange = 1.0
		ToolUIFlushRedByMaterialValueFn()
	)
	on MouthSayAnimatePartBtn pressed do
	(
		clearSelection()
		if $Mouth_Part == undefined then
		(
			messagebox "文件内没有该物体"
		)
		else
		(
			select $Mouth_Part
		)
	)
	on CPFlushBColor changed col do
	(
		select $*Body_H_001
		$.Material._FlushColorB = CPFlushBColor.color
	)
	on CPFlushAColor changed col do
	(
		select $*Body_H_001
		$.Material._FlushColorA = CPFlushAColor.color
	)
	on SLDFlushBIntensity changed val do
	(
		select $*Body_H_001
		$.Material._FlushIntensity.b = ((SLDFlushBIntensity.value/100)*255)
	)
	on SLDFlushAIntensity changed val do
	(
		select $*Body_H_001
		$.Material._FlushIntensity.a = ((SLDFlushAIntensity.value/100)*255)
	)
	on SPNFlushEffectTexID changed val do
	(
		clearSelection()
		select $*Body_H_001
		if selection.count == 1 do
		(	
			$.baseObject.EyeTextureTrans.texIndex = SPNFlushEffectTexID.value
			if (SPNPupilEffectTexID.value+1)<10 then
			(	
				a = "body_h_"+ "00"+ ((SPNFlushEffectTexID.value+1) as string)
				$.material = sceneMaterials[a]
				--$.material.opacitymap.filename = a
			)	
			else
			(
				a = "body_h_" + "0"+ ((SPNFlushEffectTexID.value+1) as string)
				$.material = sceneMaterials[a]
				--$.material.opacitymap.filename = a
			)			
		)
	)
	on SPNEyeTexID changed val do
	(
		clearSelection()
		select $*Eye_001
		if selection.count == 1 do
		(	
			$.baseObject.EyeTextureTrans.texIndex = SPNEyeTexID.value
			if (spnEyeEffectTexID.value+1) <10 then
			(
				a = "Eye_" + "00"+ ((SPNEyeTexID.value+1) as string)								
				$.material =sceneMaterials[a]
				--$.material.opacitymap.filename = a	
			)
			else
			(
				a = "Eye_" + "0"+ ((SPNEyeTexID.value+1) as string)
				$.material =sceneMaterials[a]
				--$.material.opacitymap.filename = a	
			)
		)
	)
	on DDButtEffectStyles selected sel do
	(
		if $*EffectPart_001 != undefined do
		(
			select $*EffectPart_001
			DDButtEffectStylesWeight.value = GetMorpherValueByUICaptionFn $ EffectMorpherNameStrArray DDButtEffectStyles.items[sel]
		)	
	)
	on DDButtEffectStylesWeight changed val do
	(
		if $*EffectPart_001 != undefined do
		(
			select $*EffectPart_001
			SetMorpherValueByUICaptionFn $ DDButtEffectStyles.items[DDButtEffectStyles.selection] EffectMorpherNameStrArray DDButtEffectStylesWeight.value
		)
	)
	on DDFacialStyles selected sel do
	(
		DDMouthStylesWeight.value = GetMorpherValueByUICaptionFn $Facial_Part FacialMorpherNameStrArray DDFacialStyles.items[sel]
	)
	on DDFacialStylesWeight changed val do
	(
		select $Facial_Part
		SetMorpherValueByUICaptionFn $ DDFacialStyles.items[DDFacialStyles.selection] FacialMorpherNameStrArray DDFacialStylesWeight.value
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
)
createdialog FacialAnimationMakingDetailsTool
/*
gfgfag
gf
g
a
g
ad
gf
ag

g
f
g
ad
ga
g
fa
g
fad
