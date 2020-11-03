
fn  CollectObjArrayOfPartFn ConstomArray ConstomStr=
(
	local tempArray = #()
	for str in ConstomArray do
	(
		clearSelection()
		--execute ("select $*_" + str)
		execute (ConstomStr+ str)
		if selection.count == 1 do
		(	
			append tempArray (execute ("$"+$.name))
		)
	)
	return tempArray
)
fn SoundStartFn setTime soundIndex= 
(
	if prosound.NumTracks() >= soundIndex then
	(	
		prosound.setstart soundIndex setTime
		bbbb = prosound.filelength soundIndex
		prosound.setend soundIndex (setTime  + bbbb) 
	)
	else
	(
		messageBox "没有选中的声音"
	)		
)
fn ImportSoundFn animate_S ConstomStr=
(
	local temp_bbb =substituteString maxfilename "001.max" ""
	sound_path_S = ConstomStr  + "\\sound\\" +  "CV_" + temp_bbb + animate_S + ".wav"
	print sound_path_S
	if prosound.NumTracks() >= 1 do
	(	
		for sound_item in 1 to prosound.NumTracks() do
		(
			prosound.delete 1
			prosound.delete 1
		)		
	)
	if (prosound.append  sound_path_S ) == true then
	(
		prosound.append  sound_path_S
		prosound.delete 1
	)
	else
	(
		messageBox "可能没有这个对应动作的声音，或者动作命名错误"
	)
)
fn ImportBipFn	animate_S constomString=
(
	animationRange = interval 0 30
	local temp_bbb =substituteString maxfilename "001.max" ""
	bip_path_S = constomString + "\\bip\\" +animate_S + ".bip"
	if $Bip001 != undefined then
	(
		select $Bip001
		if (biped.loadbipfile $.controller  bip_path_S) == true then
		(
			biped.loadbipfile $.controller  bip_path_S
		)
		else
		(
			messageBox "可能没有这个对应动作的bip，或者动作命名错误"
		)
	)
	else
	(
		messagebox "文件不是绑定文件"
	)
)
--导入xaf的共用方法
fn ImportXafFn animate_S path_S MorpherNum=
(
	bip_path_S = path_S +"\\xaf\\"  + animate_S + ".xaf"
	print 	bip_path_S
	select $*Body_H_001
	selectmore $*Pupil_Effect_001
	selectmore $*Eye_Effect_001
	selectmore $*Eye_001
	selectmore $*EffectPart_001
	a = LoadSaveAnimation.loadAnimation  bip_path_S  $
	if a ==true  then
	(
		for obj in selection do
		(
			selectKeys obj.modifiers[morpher]
			deleteKeys obj.modifiers[morpher] #selection
			for i in 1 to MorpherNum do
			(
				if (WM3_MC_HasData obj.modifiers[morpher] i) == true do
				(
					WM3_MC_SetValue obj.modifiers[morpher] i 0.0
				)	
			)				
		)
		LoadSaveAnimation.loadAnimation  bip_path_S  $ 
	)
	else
	(
		messageBox "还没有制作这个表情文件"	
	)
)
fn ImportMouthSayXafFN animate_S path_S obj= 
(
	bip_path_S = path_S +"\\MouthXaf\\"  + animate_S + ".xaf"
	if obj.modifiers[Morpher][2].keys == undefined or obj.modifiers[Morpher][2].keys.count == 0 do
	(	
		a = LoadSaveAnimation.loadAnimation  bip_path_S  obj 
		if a ==true  then
		(
			--LoadSaveAnimation.loadAnimation  bip_path_S  $ insert:true
			print "声音导入成功"
		)
		else
		(
			messageBox "没有这个口型文件"	
		)					
	)
)	
--导出fbx的共用方法
fn ExportFacialFbxFn animate_S path_S=
(
	bip_path_S = path_S +"\\facial\\"  + animate_S + ".fbx"	
	sliderTime = 0f	
	$Bip001.controller.figureMode = true
	--清除链接关系，保证数据干净
	
	
	select $*Body_H_001
	max unlink
	--清除位移控制器的数据
	selectKeys $.controller
	deleteKeys $.controller #selection
	
	select $*Eye_001
	selectKeys $.controller
	deleteKeys $.controller #selection
	select $*Pupil_Effect_001
	if selection.count == 1 do
	(
		selectKeys $.controller
		deleteKeys $.controller #selection
	)	
	clearSelection()
	select $*Eye_Effect_001
	if selection.count == 1 do
	(
		selectKeys $.controller
		deleteKeys $.controller #selection
	)
	clearSelection()
	select $*EffectPart_001
	if selection.count == 1 do
	(
		selectKeys $.controller
		deleteKeys $.controller #selection
	)
	select $*Body_H_001
	--选择所有表情文件的部分
	selectmore $*Pupil_Effect_001
	selectmore $*Eye_Effect_001
	selectmore $*Eye_001
	selectmore $*EffectPart_001
	--导出表情动画
	FbxExporterSetParam "Animation" true
	FbxExporterSetParam "UpAxis" "Y"
	exportFile bip_path_S #noPrompt selectedOnly:true
	--恢复到初始的绑定关系中
	select $*Body_H_001
	$.controller.rotation.x =0
	$.controller.rotation.y =0
	$.controller.rotation.z =0
	$.parent = $Bip001_Head
	$Bip001.controller.figureMode = false
)
--导出xaf的共用方法
fn ExportXafFn animate_S path_S=
(
	bip_path_S = path_S +"\\xaf\\"  + animate_S + ".xaf"
	sliderTime = 0f	
	$Bip001.controller.figureMode = true	
	select $*Body_H_001
	max unlink
	$.controller.rotation.x =0
	$.controller.rotation.y =0
	$.controller.rotation.z =0
	$.pos = [0,0,0]
	selectKeys $.controller
	deleteKeys $.controller #selection
	
	select $*Eye_001
	selectKeys $.controller
	deleteKeys $.controller #selection
	clearSelection()
	select $*Pupil_Effect_001
	if selection.count == 1 do
	(
		selectKeys $.controller
		deleteKeys $.controller #selection
	)	
	clearSelection()
	select $*Eye_Effect_001
	if selection.count == 1 do
	(
		selectKeys $.controller
		deleteKeys $.controller #selection
	)
	clearSelection()
	select $*EffectPart_001
	if selection.count == 1 do
	(
		selectKeys $.controller
		deleteKeys $.controller #selection
	)
	
	select $*Body_H_001
	
	
	selectmore $*Pupil_Effect_001
	selectmore $*Eye_Effect_001
	selectmore $*Eye_001
	selectmore $*EffectPart_001
	LoadSaveAnimation.saveAnimation  bip_path_S  $ #() #()
	select $*Body_H_001
	$.parent = $Bip001_Head
	$Bip001.controller.figureMode = false
)


fn ResetFlushRedOfMaterialFn = 
(
	select $*Body_H_001
	try 
	(
		--$.material.name = "material"
		$.material._FaceFlushToggle = off
		$.material._FlushIntensity = color 0 0 0 0
		$.material._RedFlushColor = color 255 0 0 255
		$.material._BlackFlushColor = color 0 0 0 255
		$.material._FlushColorB = color 0 0 0 255
		$.material._FlushColorA = color 0 0 0 255
		$.Material._FlushRange = 0.0
	)
	catch
	(
		messagebox "脸部材质球有问题"
	)
		
	clearSelection()
	select  $*Eye_Effect_001
	if selection.count == 1 do
	(	
		$.EyeTextureTrans.texIndex = 0
	)
	clearSelection()
	select  $*Pupil_Effect_001
	if selection.count == 1 do
	(	
		$.EyeTextureTrans.texIndex = 0
	)
)

fn GetProjectPathFn =
(
	
	local a =  maxfilepath
	if a.count != 0 do
	(
		local aa = maxfilename
		local bb = substituteString aa ".max" ""
		local cc = a + bb
		return cc
	)
	return a
)

fn CreatControlMoprherObjFn obj changeNameStr index trueOrFlase=
(
	local tempObj = copy obj
	if trueOrFlase do
	(
		local tempMaterial = copy obj.material
		
		tempMaterial.name = changeNameStr
		tempObj.material = tempMaterial
	)
	tempObj.name = changeNameStr
	tempObj.parent = undefined
	local xPos = (index-1)*50
	tempObj.pos = [xPos,0,-1000]
	selectKeys tempObj.controller
	deleteKeys tempObj.controller #selection
)
fn DelControlMoprherObjFn objNameStringArray =
(
	local tempArray = #()
	for i in geometry do
	(
		--print i.name
		for objName in objNameStringArray do
		(
			if i.name == objName do
			(
				
				append  tempArray i
				exit
			)
		)
	)
	delete tempArray
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
	
	
	
	
	clearSelection()
	select $*_Pupil_Effect_001
	if selection.count == 1 do
	(
		select $*_Pupil_Effect_001
		selectmore $Pupil_Effect_Part
		CopyMorpherAnimateFn selection[1] selection[2] PupilEffectMorpherNameStrArray
	)
	
	clearSelection()
	select $*_Eye_Effect_001
	if selection.count == 1 do
	(
		select $*_Eye_Effect_001
		selectmore $Eye_Effect_Part
		CopyMorpherAnimateFn selection[1] selection[2] EyeEffectMorpherNameStrArray
	)	
)
--把头部的动画分别复制给对应的部位
fn ProjectBtnCopyMorpherAnimateFn2 =
(	
	
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
	
	clearSelection()
	select $*_Pupil_Effect_001
	if selection.count == 1 do
	(
		select $Pupil_Effect_Part
		DelMorpherChannelCotrollerKeysFn $
		selectmore $*_Pupil_Effect_001
		CopyMorpherAnimateFn selection[1] selection[2] PupilEffectMorpherNameStrArray
	)
	
	clearSelection()
	select $*_Eye_Effect_001
	if selection.count == 1 do
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
	local tempArray = CollectObjArrayOfPartFn AnimatePartNameArray "select $*_"
	--print tempArray
	if tempArray.count >0 do
	(
		for tempEach in tempArray do
		(
			ClearMorpherConnectFn tempEach
		)
	)
)
fn ClearFacialKeysFn =
(
	sliderTime = 0f	
	--清楚与脸部的关联关系
	local tempArray = CollectObjArrayOfPartFn AnimatePartNameArray "select $*_"
	if tempArray.count >0 do
	(
		for tempEach in tempArray do
		(
			local isPupilEffectPart = false
			if matchPattern  tempEach.name pattern:"*Pupil_Effect_001" do
			(
				isPupilEffectPart = true
			)
			select tempEach
			DelMorpherChannelCotrollerKeysFn $
			DelMaterialKeysFn $
			if isPupilEffectPart then
			(
				ResetMorpherChannelFn $ 100.0
			)	
			else
			(
				ResetMorpherChannelFn $ 0.0
			)
			deleteKeys $
		)
	)
		
)
fn ClearCopyPartFacialKeysFn =
(
	sliderTime = 0f	
	local tempArray = CollectObjArrayOfPartFn facialPartMorpherObjNameStrArray ""
	if tempArray.count >0 do
	(
		for tempEach in tempArray do
		(
			local isPupilEffectPart = false
			if tempEach.name == "Pupil_Effect_Part" do
			(
				isPupilEffectPart = true
			)
			select tempEach
			DelMorpherChannelCotrollerKeysFn $
			DelMaterialKeysFn $
			if isPupilEffectPart then
			(
				ResetMorpherChannelFn $ 100.0
			)	
			else
			(
				ResetMorpherChannelFn $ 0.0
			)
			deleteKeys $
		)
	)
)



fn CreateConstomAttributeFn =
(
	--创建瞳孔贴图和特效片贴图需要的控制器
	local tempArray = CollectObjArrayOfPartFn ConstomAttributePartNameArray "select $*_"
	if tempArray.count >0 do
	(
		for tempEach in tempArray do
		(
			select tempEach
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
	)	
)


fn DelConstomAttributeFn =
(
	local tempArray = CollectObjArrayOfPartFn ConstomAttributePartNameArray "select $*_"
	if tempArray.count >0 do
	(
		for tempEach in tempArray do
		(
			select tempEach
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
)



/*
fn  CollectObjArrayOfConstomAttributeFn =
(
	ConstomAttributePartNameArray
	local tempArray = #()
	clearSelection()
	select $*Pupil_Effect_001
	if selection.count == 1 do
	(	
		append tempArray (execute ("$"+$.name))
	)
	clearSelection()
	select  $*Eye_Effect_001
	if selection.count == 1 do
	(
		append tempArray (execute ("$"+$.name))
	)
	clearSelection()
	select  $*Body_H_001
	if selection.count == 1 do
	(		
		append tempArray (execute ("$"+$.name))
	)
	clearSelection()
	select  $*Eye_001
	if selection.count == 1 do
	(	
		append tempArray (execute ("$"+$.name))	
	)
	return tempArray
)
*/



