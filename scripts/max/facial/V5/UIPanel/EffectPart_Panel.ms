rollout EffectPartRollout "特效部分" width:973 height:218
(
	
	spinner 'SPNPupilEffectTexID' "瞳孔特效图片ID" pos:[7,33] width:42 height:16 type:#integer align:#left
	spinner 'spnEyeEffectTexID' "眼睛特效图片ID" pos:[6,52] width:41 height:16 range:[0,100,0] type:#integer align:#left
	slider 'SLDFlushRedIntensity' "红晕明显程度调整" pos:[8,116] width:82 height:44 align:#left
	slider 'SLDFlushBlackIntensity' "黑脸明显程度调整" pos:[9,163] width:82 height:44 range:[0,100,0] align:#left
	colorPicker 'CPFlushRedColor' "" pos:[85,136] width:44 height:22 color:(color 0 0 155) align:#left
	colorPicker 'CPFlushBlackColor' "" pos:[85,181] width:44 height:22 color:(color 0 0 155) align:#left
	slider 'SLDFlushBlackRange' "红晕黑脸的范围" pos:[6,68] width:100 height:44 range:[0,100,0] align:#left
	--checkbox 'CHKFlushState' "是否开启红晕" pos:[8,69] width:94 height:21 align:#left
	button 'OpenFlushBtn' "开启红晕" pos:[10,9] width:90 height:20 align:#left
	
	button 'DelFlushAnimateBtn' "删除红晕动画" pos:[405,22] width:90 height:20 align:#left
	button 'CloseFlushBtn' "关闭脸红" pos:[108,9] width:90 height:20 align:#left
	
	--GroupBox 'XUQIU' "备份需求" pos:[11,620] width:955 height:60 align:#left
	colorPicker 'CPFlushBColor' "" pos:[214,133] width:44 height:22 color:(color 0 0 155) align:#left
	colorPicker 'CPFlushAColor' "" pos:[212,178] width:44 height:22 color:(color 0 0 155) align:#left
	slider 'SLDFlushBIntensity' "B通道强度调整" pos:[137,116] width:82 height:44 range:[0,100,0] align:#left
	slider 'SLDFlushAIntensity' "A通道强度调整" pos:[134,162] width:82 height:44 range:[0,100,0] align:#left
	spinner 'SPNFlushEffectTexID' "红晕图片ID" pos:[142,32] width:42 height:16 range:[0,1,0] type:#integer align:#left
	spinner 'SPNEyeTexID' "瞳孔贴图ID" pos:[143,53] width:41 height:16 range:[0,100,0] type:#integer align:#left
	dropdownList 'DDButtEffectStyles' "脸部特效" pos:[281,22] width:106 height:41 align:#left
	slider 'DDButtEffectStylesWeight' "特效强度调整" pos:[279,69] width:108 height:44 range:[0,100,0] align:#left
	GroupBox 'grp2' "快捷设置" pos:[397,5] width:570 height:208 align:#left
	--button 'RefurbishEffectPartBtn' "刷新参数" pos:[6,9] width:103 height:21 align:#left
	GroupBox 'grp14' "" pos:[2,-1] width:264 height:215 align:#left
	GroupBox 'grp17' "" pos:[274,3] width:120 height:211 align:#left
	
	/*
	fn 
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
	*/
	
	
	
	
	fn ToolUIFlushRedByMaterialValueFn =
	(
		try
		(
			select $*_Body_H_001
			SLDFlushRedIntensity.value = (($.Material._FlushIntensity.r/255) *100)
			SLDFlushBlackIntensity.value = (($.Material._FlushIntensity.g/255) *100)
			
			
			CPFlushRedColor.color = $.Material._RedFlushColor
			CPFlushBlackColor.color = $.Material._BlackFlushColor
			
			SLDFlushRedIntensity.value = $.Material._FlushRange
			--CHKFlushState.state = $.Material._FaceFlushToggle
			try
			(
				SLDFlushBIntensity.value = (($.Material._FlushIntensity.b/255) *100)
				SLDFlushAIntensity.value = (($.Material._FlushIntensity.a/255) *100)
				CPFlushBColor.color = $.Material._FlushColorB
				CPFlushAColor.color = $.Material._FlushColorA
			)
			catch
			(
				print "旧材质球"
			)
		)
		catch
		(
			messagebox "脸部材质球不对"
		)
		
	)
	
	
	
	
	/*
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
	*/
	/*
	on RefurbishEffectPartBtn pressed  do
	(
		ToolUIFlushRedByMaterialValueFn()
		
	)
	*/

	on EffectPartRollout open do
	(
		PartMorpherMatchUIDDlistFN		DDButtEffectStyles		EffectMorpherNameStrArray			1		EffectMorpherNameStrArray.count
		SPNPupilEffectTexID.value = 0
        
		ResetFlushRedOfMaterialFn()
		ToolUIFlushRedByMaterialValueFn()
	)
	on EffectPartRollout close do
		(
	
	)
	on SPNPupilEffectTexID changed val do
	(
		clearSelection()
		select $*Pupil_Effect_001
		if selection.count == 1 do
		(	
			$.baseObject.EyeTextureTrans.texIndex = SPNPupilEffectTexID.value
			local a = ""
            local b = ""
			if (SPNPupilEffectTexID.value+1)<10 then
			(	
				a = maxfilepath  + (substring $.name 1 ($.name.count-3))+ "00"+ ((SPNPupilEffectTexID.value+1) as string) +".tga"
                b = "Pupil_Effect"+ "00"+ ((SPNPupilEffectTexID.value+1) as string) 
			)	
			else
			(
				a = maxfilepath  + (substring $.name 1 ($.name.count-3))+ "0"+ ((SPNPupilEffectTexID.value+1) as string) +".tga"
                b = "Pupil_Effect"+ "0"+ ((SPNPupilEffectTexID.value+1) as string) 
			)
			try
			(
				$.material.diffusemap.filename = a
				$.material.opacitymap.filename = a
			)
			catch
			(
                $.material = sceneMaterials[b] 
				--messagebox "瞳孔特效片的材质球不对"
			)
		)
	)
	on spnEyeEffectTexID changed val do
	(
		clearSelection()
		select $*Eye_Effect_001
		if selection.count == 1 do
		(	
			$.baseObject.EyeTextureTrans.texIndex = spnEyeEffectTexID.value
			local a = ""
            local b = ""
			if (spnEyeEffectTexID.value+1) <10 then
			(
				a = maxfilepath  + (substring $.name 1 ($.name.count-3))+ "00"+ ((spnEyeEffectTexID.value+1) as string) +".tga"	
                b = "Eye_Effect"+ "00"+ ((spnEyeEffectTexID.value+1) as string) 
				--$.material = sceneMaterials[a]                
			)
			else
			(
				a = maxfilepath  + (substring $.name 1 ($.name.count-3))+ "0"+ ((spnEyeEffectTexID.value+1) as string) +".tga"	
                b = "Eye_Effect"+ "0"+ ((spnEyeEffectTexID.value+1) as string) 
				--jdghjfhjdjthgdjhgdjhgdjdjdg               
			)
			try
			(
				$.material.diffusemap.filename = a
				$.material.opacitymap.filename = a
			)
			catch
			(
                $.material = sceneMaterials[b] 
				--messagebox "眼睛特效片的材质球不对"
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
	on OpenFlushBtn pressed do
	(
		ResetFlushRedOfMaterialFn()
		ToolUIFlushRedByMaterialValueFn()
		$.material._FaceFlushToggle = on
		ToolUIFlushRedByMaterialValueFn()
	)
	on DelFlushAnimateBtn pressed do
	(
		ResetFlushRedOfMaterialFn()
		ToolUIFlushRedByMaterialValueFn()
		select $*_Body_H_001
		deleteKeys $.material
		
	)
	on CloseFlushBtn pressed do
	(
		ResetFlushRedOfMaterialFn()
		select $*Body_H_001
		$.material._FaceFlushToggle = off
		$.material._FlushIntensity = color 255 0 0 0
		$.material._RedFlushColor = color 255 0 0 255
		$.material._BlackFlushColor = color 0 0 0 255
		try
		(
			$.material._FlushColorB = color 0 0 0 255
			$.material._FlushColorA = color 0 0 0 255
		)
		catch
		(
			print "旧材质球"
		)	
		$.Material._FlushRange = 1.0
		ToolUIFlushRedByMaterialValueFn()
	)
	on CPFlushBColor changed col do
	(
		select $*Body_H_001
		try
		(
			$.Material._FlushColorB = CPFlushBColor.color
		)
		catch
		(
			print "旧材质球"
		)	
		
	)
	on CPFlushAColor changed col do
	(
		select $*Body_H_001
		try
		(
			$.Material._FlushColorA = CPFlushAColor.color
		)
		catch
		(
			print "旧材质球"
		)	
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
			if (SPNFlushEffectTexID.value+1)<10 then
			(	
				a = "Body_H_"+ "00"+ ((SPNFlushEffectTexID.value+1) as string) 
				--print a
				--$.material = sceneMaterials[a]
				--$.material.opacitymap.filename = a
			)	
			else
			(
				a = "body_h_"+ "0"+ ((SPNFlushEffectTexID.value+1) as string) 
				--$.material = sceneMaterials[a]
				--$.material.opacitymap.filename = a
			)
            $.material = sceneMaterials[a]			
		)
		ToolUIFlushRedByMaterialValueFn()
	)
	on SPNEyeTexID changed val do
	(
		clearSelection()
		select $*Eye_001
		if selection.count == 1 do
		(	
			$.baseObject.EyeTextureTrans.texIndex = spnEyeTexID.value
			if (spnEyeEffectTexID.value+1) <10 then
			(
				a = "Eye_" + "00"+ ((spnEyeTexID.value+1) as string)								
			)
			else
			(
				a = "Eye_" + "0"+ ((spnEyeTexID.value+1) as string)
			)
            $.material = sceneMaterials[a]
		)
	)
	on DDButtEffectStyles selected sel do
	(
		--print DDButtEffectStyles.items[sel]
		select $*EffectPart_001
		DDButtEffectStylesWeight.value = GetMorpherValueByUICaptionFn $ EffectMorpherNameStrArray DDButtEffectStyles.items[sel]
	)
	on DDButtEffectStylesWeight changed val do
	(
		select $*EffectPart_001
		SetMorpherValueByUICaptionFn $ DDButtEffectStyles.items[DDButtEffectStyles.selection] EffectMorpherNameStrArray DDButtEffectStylesWeight.value
	)
)

--createdialog EffectPartRollout


/*
dsf
dsaf
edas
f
esad
fsd
a
fdas
f
ads
