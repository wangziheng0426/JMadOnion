rollout ProjectPanelRollout "��������" width:973 height:85
(
	button 'RefurbishBtn' "ˢ��" pos:[856,27] width:80 height:21 align:#left
	dropdownList 'FacialAnimateNameDDL' "���鶯������" pos:[611,5] width:111 height:41 align:#left
	button 'ProjectPathBTN' "����·��" pos:[7,8] width:63 height:18 align:#left
	edittext 'ProjectPathEDT' "" pos:[71,7] width:153 height:18 align:#left
	spinner 'WavOffsetSPN' "����ƫ��" pos:[240,32] width:65 height:16 range:[0,10000,0] type:#integer align:#left
	edittext 'AnimateNameEDT' "��������" pos:[232,7] width:152 height:16 align:#left
	button 'ExportFacilAnimateBTN' "���鶯������" pos:[735,27] width:97 height:22 align:#left
	dropdownList 'AnimateNameDDL' "��������" pos:[398,6] width:107 height:41 align:#left
	spinner 'MorpherUseableNumSPN' "Morpher����" pos:[31,33] width:64 height:16 type:#integer align:#left
	button 'ImportMouthXafBTN' "�������͵���" pos:[738,1] width:93 height:24 align:#left
	button 'StandBTN' "վ��" pos:[513,1] width:83 height:22 align:#left
	button 'SailingBTN' "����" pos:[514,26] width:83 height:22 align:#left
	--button 'ResetAllAnimateBtn' "���ö�������" pos:[854,3] width:87 height:19 align:#left
	--ѡ�񶯻����岿��
	button 'MouthSayAnimatePartBtn' "������" pos:[28,57] width:83 height:22 align:#left
	button 'EyeAnimatePartBtn' "��Ƥ" pos:[123,57] width:83 height:22 align:#left
	button 'PupilAnimatePartBtn' "ͫ��" pos:[305,55] width:83 height:22 align:#left
	button 'PupilEffectAnimatePartBtn' "ͫ����Ч" pos:[401,56] width:83 height:22 align:#left
	button 'EyeEffectAnimatePartBtn' "�۲���Ч" pos:[496,55] width:83 height:22 align:#left
	button 'FlushAnimatePartBtn' "����" pos:[591,55] width:83 height:22 align:#left
	button 'EyebrowAnimatePartBtn' "üë" pos:[213,56] width:83 height:22 align:#left
	
	
	
	
	
	
	--���ߴ򿪵�ʱ��Ҫ���Ĺ���
	fn ProjectOpenFn =
	(
		--isPupilEffectPart = false
		--isEyeEffectPart = false

		ProjectPathEDT.text = GetProjectPathFn()
		if ProjectPathEDT.text.count == 0 do
		(
			messagebox "�ļ��ǿ��ļ�"
			return -1
		)
		--����ͫ����ͼ����ЧƬ��ͼ��Ҫ�Ŀ�����
		
		--ToolOpenMatchUINameFn()
		--���������ؼ�������
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
			messagebox "û������ģ�ͣ���ȷ���ļ��Ƿ���ȷ"
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
		--����������ϵ
		
		--
		AnimateNameDDL.items = ProjectAnimateNames
		AnimateNameEDT.text = AnimateNameDDL.items[1]
		FacialAnimateNameDDL.items = ProjectFacialAnimateNames
	)

	
	
	on ProjectPanelRollout open do
	(
		
		ProjectBtnClearConnectFn()
		--������������Ķ�������
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
		--������������Ķ�������
		--print facialPartMorpherObjNameStrArray
		DelControlMoprherObjFn facialPartMorpherObjNameStrArray
		--���ͫ����ͼ����ЧƬ��ͼ��Ҫ�Ŀ�����
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
			--üë�б�
			local morpherNameStr = GetMorpherNameByUICaptionFn EyebrowMorpherNameStrArray DDButtEyebrowStyles.items[DDButtEyebrowStyles.selection]
			local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
			if morpherChannelID != undefined do
			(
				DDButtEyebrowStylesWeight.value = WM3_MC_GetValue $.modifiers[#Morpher] morpherChannelID
			)
			--�۾��б�
			local morpherNameStr = GetMorpherNameByUICaptionFn EyeMorpherNameStrArray DDButtEyeStyles.items[DDButtEyeStyles.selection]
			local morpherChannelID = GetMorpherIDByStringFn $ morpherNameStr
			if morpherChannelID != undefined do
			(
				DDButtEyeStylesWeight.value =  WM3_MC_GetValue $.modifiers[#Morpher]  morpherChannelID
			)	
			--�����б�Ȩ�ع���
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
			messageBox "��ѡ��·��"
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
		--����������Ĺ�����ϵ
		ProjectBtnClearConnectFn()
		--�ѿ��Ʋ�λ�Ķ�����ֵ������
		ProjectBtnCopyMorpherAnimateFn()
		--����fbx
		--ExportFacialFbxFn FacialAnimateNameDDL.items[FacialAnimateNameDDL.selection]  ProjectPathEDT.text
		--����xaf
		ExportXafFn FacialAnimateNameDDL.items[FacialAnimateNameDDL.selection]  ProjectPathEDT.text
		--�Ѷ��������ٴ��ؿ��Ʋ�λ
		ProjectBtnCopyMorpherAnimateFn2()
		--�������Ʋ�λ�����Ĺ�ϵ
		ConnectMorpherChannelOfToolsFn()
		messagebox "�����������"
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
		messagebox "���ڿ�����" 
		--ResetFlushRedOfMaterialFn()
		--ToolUIFlushRedByMaterialValueFn()
	)
	*/
	on MouthSayAnimatePartBtn pressed do
	(
		clearSelection()
		if $Mouth_Part == undefined then
		(
			messagebox "�ļ���û�и�����"
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
			messagebox "�ļ���û�и�����"
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
			messagebox "�ļ���û�и�����"
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
			messagebox "�ļ���û�и�����"
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
			messagebox "�ļ���û�и�����"
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
			messagebox "�ļ���û�и�����"
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
			messagebox "�ļ���û�и�����"
		)
		else
		(
			select $Eyebrow_Part
		)
	)
)
--createdialog ProjectPanelRollout