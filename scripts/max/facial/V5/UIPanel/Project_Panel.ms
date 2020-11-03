rollout ProjectPanelRollout "工程设置" width:973 height:85
(
	button 'RefurbishBtn' "刷新" pos:[856,27] width:80 height:21 align:#left
	dropdownList 'FacialAnimateNameDDL' "表情动画名称" pos:[611,5] width:111 height:41 align:#left
	button 'ProjectPathBTN' "工程路径" pos:[7,8] width:63 height:18 align:#left
	edittext 'ProjectPathEDT' "" pos:[71,7] width:153 height:18 align:#left
	spinner 'WavOffsetSPN' "声音偏移" pos:[240,32] width:65 height:16 range:[0,10000,0] type:#integer align:#left
	edittext 'AnimateNameEDT' "动画名称" pos:[232,7] width:152 height:16 align:#left
	button 'ExportFacilAnimateBTN' "表情动画导出" pos:[735,27] width:97 height:22 align:#left
	dropdownList 'AnimateNameDDL' "动画名称" pos:[398,6] width:107 height:41 align:#left
	spinner 'MorpherUseableNumSPN' "Morpher数量" pos:[31,33] width:64 height:16 type:#integer align:#left
	button 'ImportMouthXafBTN' "语音口型导入" pos:[738,1] width:93 height:24 align:#left
	button 'StandBTN' "站立" pos:[513,1] width:83 height:22 align:#left
	button 'SailingBTN' "航行" pos:[514,26] width:83 height:22 align:#left
	--button 'ResetAllAnimateBtn' "重置动画参数" pos:[854,3] width:87 height:19 align:#left
	--选择动画物体部分
	button 'MouthSayAnimatePartBtn' "口型嘴" pos:[28,57] width:83 height:22 align:#left
	button 'EyeAnimatePartBtn' "眼皮" pos:[123,57] width:83 height:22 align:#left
	button 'PupilAnimatePartBtn' "瞳孔" pos:[305,55] width:83 height:22 align:#left
	button 'PupilEffectAnimatePartBtn' "瞳孔特效" pos:[401,56] width:83 height:22 align:#left
	button 'EyeEffectAnimatePartBtn' "眼部特效" pos:[496,55] width:83 height:22 align:#left
	button 'FlushAnimatePartBtn' "红晕" pos:[591,55] width:83 height:22 align:#left
	button 'EyebrowAnimatePartBtn' "眉毛" pos:[213,56] width:83 height:22 align:#left
	
	
	
	
	
	
	--工具打开的时候要做的工作
	fn ProjectOpenFn =
	(
		--isPupilEffectPart = false
		--isEyeEffectPart = false

		ProjectPathEDT.text = GetProjectPathFn()
		if ProjectPathEDT.text.count == 0 do
		(
			messagebox "文件是空文件"
			return -1
		)
		--创建瞳孔贴图和特效片贴图需要的控制器
		
		--ToolOpenMatchUINameFn()
		--创建单独控件的物体
		local IndexID = 0
		select $*_Body_H_001
		if selection.count == 1 then
		(
			for hsh in 1 to 4  do
			(	
				IndexID += 1
				CreatControlMoprherObjFn selection[1] facialPartMorpherObjNameStrArray[hsh] hsh true
			)
		)
		else
		(
			messagebox "没有脸的模型，请确认文件是否正确"
			return undefined
		)
		IndexID += 1
		clearSelection()
		select $*Eye_001
		if selection.count == 1 do
		(
			ClearMorpherConnectFn $
			
			CreatControlMoprherObjFn selection[1] facialPartMorpherObjNameStrArray[IndexID] IndexID false
		)
		IndexID += 1		
		clearSelection()
		select $*Pupil_Effect_001
		if selection.count == 1 do
		(
			ClearMorpherConnectFn $
			
			select $*Pupil_Effect_001
			CreatControlMoprherObjFn selection[1] facialPartMorpherObjNameStrArray[IndexID] IndexID false
		)
		IndexID += 1
		clearSelection()
		select $*Eye_Effect_001
		if selection.count == 1 do
		(
			ClearMorpherConnectFn $
			--IndexID += 1
			select $*Eye_Effect_001
			CreatControlMoprherObjFn selection[1] facialPartMorpherObjNameStrArray[IndexID] IndexID false
		)
		--创建关联关系
		
		--
		AnimateNameDDL.items = ProjectAnimateNames
		AnimateNameEDT.text = AnimateNameDDL.items[1]
		FacialAnimateNameDDL.items = ProjectFacialAnimateNames
	)

	
	
	on ProjectPanelRollout open do
	(
		
		ProjectBtnClearConnectFn()
		--清楚创建出来的多余物体
		DelControlMoprherObjFn facialPartMorpherObjNameStrArray
		ClearFacialKeysFn()
		prosound.init true
		--ImportInfoDataFn()
		CreateConstomAttributeFn()
		ProjectOpenFn()
		ConnectMorpherChannelOfToolsFn()		--PupilEffectInitValueFn()
		--ToolUIFlushRedByMaterialValueFn()
	)
	on ProjectPanelRollout close do
	(
		ProjectBtnClearConnectFn()
		--清楚创建出来的多余物体
		--print facialPartMorpherObjNameStrArray
		DelControlMoprherObjFn facialPartMorpherObjNameStrArray
		--清楚瞳孔贴图和特效片贴图需要的控制器
		DelConstomAttributeFn()
		
	)
	on RefurbishBtn pressed do
	(
		ProjectPathEDT.text = GetProjectPathFn()
		/*
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
	*/	
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
	/*
	on ResetAllAnimateBtn pressed do
	(
		messagebox "还在开发中" 
		--ResetFlushRedOfMaterialFn()
		--ToolUIFlushRedByMaterialValueFn()
	)
	*/
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
)
--createdialog ProjectPanelRollout
