--ui元素
listItems = #()
--主程序
fn J_deleteNegativeFrame = 
(
	for item in  objects do
	(
		if (classof item == Biped_Object) do
			(
			try count = item.transform.controller.keys.count catch()
			if count!=undefined do
				(
				for i=1 to count do
					(
					if (biped.getKey item.transform.controller i).time <0f do
						(
							append listItems item
							break
						)
						
					)
				)
			)
		if ( classof item == BoneGeometry or classof item == PolyMeshObject or classof item == Editable_Poly or classof item == Editable_mesh) do
			(
			try count =  numKeys item.pos.controller  catch()
			if count!=undefined do
				(
				for i=1 to count do
					(
					if (getKeyTime item.pos.controller i) <0f do
						(
							append listItems item
							break
						)
						
					)
				)
			)
	)
	createdialog deleteKeysDia
)
--删帧
fn J_deleteKeys =
(
	for item in  objects do
	(
		
		if (classof item == Biped_Object) do
			( 
			try count = item.transform.controller.keys.count catch()
			if count!=undefined do
				(
				biped_ctrl =item.transform.controller
				for i=1 to count do
					(
					if (biped.getKey item.transform.controller i).time <0f do
						(							
							(biped.getKey biped_ctrl i).selected=True
							print (biped.getKey biped_ctrl i).selected
						)
						
					)
					
				if biped_ctrl.keys.count>0 do
					(	
						print biped_ctrl.keys.count
					if (biped.getKey biped_ctrl 1).selected do
						biped.deleteKeys biped_ctrl  #selection
					)
				)
				
			)
		if ( classof item == BoneGeometry or classof item == PolyMeshObject or classof item == Editable_Poly or classof item == Editable_mesh) do
			(
			try count =  numKeys item.pos.controller  catch()
			if count!=undefined do
				(
				for i=1 to count do
					(
					if (getKeyTime item.pos.controller i) <0f do
						(
							selectKey item.pos.controller i
						)		
					if (getKeyTime item.rotation.controller i) <0f do
						(
							selectKey item.rotation.controller i
						)
					if (getKeyTime item.scale.controller i) <0f do
						(
							selectKey item.scale.controller i
						)
					)
				deleteKeys item.transform.controller #selection 
				)
			)	
	
	)
	DestroyDialog deleteKeysDia
	listItems=#()
	createdialog deleteKeysDia
)
--界面
rollout deleteKeysDia "Untitled" width:452 height:540
(

	listBox 'lbx2' "带有错误关键帧的物体" pos:[-1,0]  items:(for o in listItems collect o.name) width:448 height:30 align:#left
	button 'btn5' "删除所有负帧" pos:[11,470] width:150 height:40 align:#left
	button 'btn6' "关闭" pos:[280,470] width:150 height:40 align:#left

	on btn5 pressed  do
	(
	J_deleteKeys()
	)
	
	on btn6 pressed  do
	(
	DestroyDialog deleteKeysDia
	)

)

J_deleteNegativeFrame()