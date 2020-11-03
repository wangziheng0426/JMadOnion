rollout FacialAnimationMakingDetailsTool "动画调整工具" width:499 height:300
(
	--特殊效果的模块
	GroupBox 'grp22' "特殊效果" pos:[5,4] width:474 height:289 align:#left
	spinner 'SPNPupilEffectTexID' "瞳孔图片ID" pos:[21,54] width:59 height:16 type:#integer align:#left
	spinner 'spnEyeEffectTexID' "眼睛图片ID" pos:[21,78] width:59 height:16 range:[0,100,0] type:#integer align:#left
	slider 'SLDFlushRedIntensity' "红晕明显程度调整" pos:[21,163] width:153 height:44 align:#left
	slider 'SLDFlushBlackIntensity' "黑脸明显程度调整" pos:[22,216] width:153 height:44 range:[0,100,0] align:#left
	colorPicker 'CPFlushRedColor' "红晕颜色" pos:[179,179] width:125 height:22 color:(color 0 0 155) align:#left
	colorPicker 'CPFlushBlackColor' "黑脸颜色" pos:[179,231] width:126 height:22 color:(color 0 0 155) align:#left
	slider 'SLDFlushBlackRange' "红晕黑脸的范围" pos:[21,114] width:153 height:44 range:[0,100,0] align:#left
	checkbox 'CHKFlushState' "是否开启红晕" pos:[20,25] width:94 height:21 align:#left
	
	on FacialAnimationMakingDetailsTool open do
	(
		clearSelection()
		select $*Pupil_Effect_001
		if selection.count == 1 do
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
		
		clearSelection()
		select  $*Eye_Effect_001
		if selection.count == 1 do
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
			
		
		
		
		--红晕和控件相关内容重置
		select $*Body_H_001
		SLDFlushRedIntensity.value = (($.Material._FlushIntensity.r/255) *100)
		SLDFlushBlackIntensity.value = (($.Material._FlushIntensity.g/255) *100)
		CPFlushRedColor.color = $.Material._RedFlushColor
		CPFlushBlackColor.color = $.Material._BlackFlushColor
		SLDFlushRedIntensity.value = $.Material._FlushRange
		CHKFlushState.state = $.Material._FaceFlushToggle
		$.material.name = "Material"
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
	on FacialAnimationMakingDetailsTool close do
	(
		clearSelection()
		select  $*Eye_Effect_001
		if selection.count == 1 do
		(	
			custAttributes.delete $ (classof $.EyeTextureTrans)
		)
		clearSelection()
		select $*Pupil_Effect_001
		if selection.count == 1 do
		(	
			custAttributes.delete $ (classof $.EyeTextureTrans)
		)
	)
	on SPNPupilEffectTexID changed val do
	(
		clearSelection()
		select $*Pupil_Effect_001
		if selection.count == 1 do
		(	
			$.baseObject.EyeTextureTrans.texIndex = SPNPupilEffectTexID.value
			if (SPNPupilEffectTexID.value+1)<10 then
			(	
				a = maxfilepath  + (substring $.name 1 ($.name.count-3))+ "00"+ ((SPNPupilEffectTexID.value+1) as string) +".tga"
				$.material.diffusemap.filename = a
				$.material.opacitymap.filename = a
			)	
			else
			(
				a = maxfilepath  + (substring $.name 1 ($.name.count-3))+ "0"+ ((SPNPupilEffectTexID.value+1) as string) +".tga"
				$.material.diffusemap.filename = a
				$.material.opacitymap.filename = a
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
			if (spnEyeEffectTexID.value+1) <10 then
			(
				a = maxfilepath  + (substring $.name 1 ($.name.count-3))+ "00"+ ((spnEyeEffectTexID.value+1) as string) +".tga"									
				$.material.diffusemap.filename = a
				$.material.opacitymap.filename = a	
			)
			else
			(
				a = maxfilepath  + (substring $.name 1 ($.name.count-3))+ "0"+ ((spnEyeEffectTexID.value+1) as string) +".tga"
				$.material.diffusemap.filename = a
				$.material.opacitymap.filename = a	
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
)
createDialog FacialAnimationMakingDetailsTool




