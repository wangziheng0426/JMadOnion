fn GetModifierIndexFN obj modifierType =
(
	if obj.modifiers.count > 0 then
	(
		for i in  1 to obj.modifiers.count do
		(
			if classof obj.modifiers[i] == modifierType do
			(
				return i
			)
		)
		return undefined
	)
	else
	(
		return undefined
	)
)
fn GetMorpherNumFn obj =
(
	local index = 0
	if (classof Obj.modifiers[1]) == Morpher do
	(
		for i in 1 to 100 do
		(
			local tempMorpherName =WM3_MC_GetName Obj.modifiers[1] i
			if tempMorpherName != "- empty -" and tempMorpherName != "- �� -" do
			(
				index = index + 1
			)
		)
	)
	return index		
)




--ʰȡ����
fn SetMorpherSingleChannelFn Morobj TempMorpherString ChannelID=
(
	local isTrue = false
	local b = TempMorpherString
	for kk in 1 to 25 do
	(
		local bb = b
		if kk < 10 then
		(
			bb =toLower( b +  "_0"+ (kk as string))
		)
		else
		(
			bb = toLower( b +  "_"+ (kk as string))
		)
		local m = execute ("$" + bb)
		if m != undefined do
		(
			if isTrue == false then
			(
				WM3_MC_BuildFromNode  Morobj.morpher ChannelID m
				isTrue = true
			)
			else
			(
				WM3_AddProgressiveMorphNode Morobj.morpher ChannelID m 
			)
		)
	)
	if isTrue do
	(
		WM3_MC_setName Morobj.morpher ChannelID b
	)	
)

-- ���ñ����ںϱ��Σ���ɾ��ԭ�б����ںϣ�Ȼ�����´���
fn SetMorpherChnnelByNameArrayFn obj morpherTargetArray =
(
	local tempModifierIndex = GetModifierIndexFN obj Morpher
	if tempModifierIndex != undefined then
	(
		deleteModifier obj tempModifierIndex
		addmodifier obj (Morpher name:"Morpher")
	)	
	else
	(
		addmodifier $ (Morpher name:"Morpher")
	)
	local icount = 0
	for i in 1 to MorpherTargetArray.count do
	(	
    --14:57 2019/12/31  ��ҪСдת��
		b = MorpherTargetArray[i][1]
		local m = execute ("$" + b)
		if m != undefined then
		(	
			icount +=1 
			WM3_MC_BuildFromNode obj.morpher icount m	
			local FF = WM3_MC_HasData obj.morpher icount
			if FF == false  do
			(
				messagebox (m.name+"ʰȡ����")
				return undefined
				--print  "cc"
			)
		)
		else
		(
			icount += 1
			SetMorpherSingleChannelFn obj b icount
			local Mstr = WM3_MC_GetName $.morpher icount
			if Mstr != b do
			(
				icount  = icount-1
			)
		)
	)
)
fn GetMorpherNameArrayByPartMouthArrayFn PartMouthArray=
(
	local tempArray = #()
	for hsh in PartMouthArray do
	(
		append tempArray hsh[1]
	)
	return tempArray
)

fn GetMorpherNameByUICaptionFn morpherNameArray UIControlCaption =
(
	for hsh in morpherNameArray do
	(
		if hsh[2] == UIControlCaption do
		(
			return hsh[1]
		)
	)
	return undefined
)

----ͨ�ú���	
fn GetMorpherIDByStringFn Obj MorpherName =
(
	if (classof Obj.modifiers[1]) == Morpher do
	(
		for i in 1 to 100 do
		(
			local tempMorpherName =WM3_MC_GetName Obj.modifiers[1] i
			if tempMorpherName == MorpherName do
			(
				--constomValue = constomValue as float
				--WM3_MC_SetValue Obj.modifiers[1] i  constomValue 
				return i
			)
		)
	)	
	return undefined
)

fn SetMorpherValuecConnectFn ControlledObj ControlObj MorpherNameString= 
(
	local tempMorpherID = GetMorpherIDByStringFn ControlledObj MorpherNameString
	local tempMorpherID2 = GetMorpherIDByStringFn ControlObj MorpherNameString
	if tempMorpherID != undefined and tempMorpherID2 != undefined do
	(
		local tempMorpherIDControllerNameStr = ControlledObj.modifiers[#Morpher][tempMorpherID].name
		tempMorpherIDControllerNameStr = substituteString  tempMorpherIDControllerNameStr "[" "_"
		tempMorpherIDControllerNameStr = substituteString  tempMorpherIDControllerNameStr "]" "_"
		tempMorpherIDControllerNameStr = substituteString  tempMorpherIDControllerNameStr " " "_"
		tempMorpherIDControllerNameStr = substituteString  tempMorpherIDControllerNameStr "(" "_"
		tempMorpherIDControllerNameStr = substituteString  tempMorpherIDControllerNameStr ")" "_"
		paramWire.connect ControlObj.modifiers[#Morpher][tempMorpherID2] ControlledObj.modifiers[#Morpher][tempMorpherID] tempMorpherIDControllerNameStr
	)
)



fn ClearMorpherConnectFn obj =
(
	if (classof Obj.modifiers[1]) == Morpher do
	(
		for i in 1 to 100 do
		(
			local tempMorpherName =WM3_MC_GetName Obj.modifiers[1] i
			if tempMorpherName != "- empty -" and tempMorpherName != "- �� -" do
			(
				obj.modifiers[#Morpher][i].controller = Bezier_Float()
			)
		)
	)	
)





fn CopyMorpherAnimateFn targetObj sourceObj morpherNameArray =
(
	for morpherName in morpherNameArray do
	(
		local contorlMorpherID = GetMorpherIDByStringFn targetObj morpherName[1]
		local targetMorpherID =  GetMorpherIDByStringFn sourceObj morpherName[1]
		if contorlMorpherID != undefined and targetMorpherID != undefined do
		(
			local morpherKeysArray = sourceObj.modifiers[1][contorlMorpherID].keys
			if morpherKeysArray != undefined do
			(
				if morpherKeysArray.count > 0 and morpherKeysArray != undefined  do
				(
					for key in morpherKeysArray do
					(
						local tempTime = key.time
						local tempValue = key.value
						at time tempTime animate on targetObj.modifiers[#Morpher][targetMorpherID].value = tempValue
					)
				)
			)			
		)	
	)
)

fn DelMorpherChannelCotrollerKeysFn obj =
(
	try 
	(
		for i in 1 to 100 do
		(
			local tempMorpherName =WM3_MC_GetName obj.modifiers[1] i
			if tempMorpherName != "- empty -" and tempMorpherName != "- �� -" do
			(
				--WM3_MC_SetValue obj.modifiers[1] i 0.0
				deleteKeys obj.modifiers[#Morpher][i].controller
			)
		)
	)
	catch
	(
		print (obj.name + "û��morpher�޸���")
	)
)
--ͨ����ť�����ָ�ͨ������Ȩ����ֵ
fn SetMorpherValueByUICaptionFn obj UICaption MorpherNameStrArray constomValue=
(
	local morpherName = GetMorpherNameByUICaptionFn MorpherNameStrArray UICaption
	local morpherChannelId = GetMorpherIDByStringFn obj MorpherName
	if morpherChannelId != undefined do
	(	
		WM3_MC_SetValue obj.modifiers[1] morpherChannelId constomValue
	)
)
--ͨ����ť�����ָ���ȡͨ��Ȩ����ֵ
fn GetMorpherValueByUICaptionFn obj morpherNameArray UIControlCaption =
(
	for hsh in morpherNameArray do
	(
		if hsh[2] == UIControlCaption do
		(
			if (classof Obj.modifiers[1]) == Morpher do
			(
				for i in 1 to 100 do
				(
					local tempMorpherName =WM3_MC_GetName Obj.modifiers[1] i
					if tempMorpherName == hsh[1] do
					(
						--constomValue = constomValue as float
						local tempMorpherValue = WM3_MC_GetValue obj.modifiers[1] i 
						return tempMorpherValue
					)
				)
			)	
		)
	)
	return -1
)



	


fn MorpherResetFN= 
(
	for i in 1 to 100 do
	(
		WM3_MC_SetValue $.modifiers[#Morpher] i 0.0
	)
)

--����ͫ������ͨ������ֵ����֤�տ�ʼ��ʱ��ͫ�׵���ЧƬû����ʾ����

fn ResetMorpherChannelFn obj comstomValue=
(
	try 
	(
		for i in 1 to 100 do
		(
			local tempMorpherName =WM3_MC_GetName obj.modifiers[1] i
			if tempMorpherName != "- empty -" and tempMorpherName != "- �� -" do
			(
				WM3_MC_SetValue obj.modifiers[1] i comstomValue
				--deleteKeys obj.modifiers[#Morpher][i].controller
			)
		)
	)
	catch
	(
		print (obj.name + "û��morpher�޸���")
	)
)
--ͨ��morpher�����֣��ö�Ӧ���ֵ�morpherͨ����ͷ����morpherͨ��������
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
	clearSelection()
	select $*_Pupil_Effect_001
	if selection.count == 1 do
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
	clearSelection()
	select $*_Eye_Effect_001
	if selection.count == 1 do
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