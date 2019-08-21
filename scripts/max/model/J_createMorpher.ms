fn J_createMorpher =
(
	for item in geometry do
	(
		if (matchPattern  item.name pattern:("*_Body_H_001") and item.parent.name =="Bip001 Head" ) do
		(
			if ( item.modifiers[#Skin]!= undefined) do
			(
				deleteModifier item item.modifiers[#Skin]
			)
			if ( item.modifiers[#Morpher]!= undefined) do
			(
				deleteModifier item item.modifiers[#Morpher]
			)		
			
			temp=copy item
			addmodifier item (Morpher ())
			select item
			max modify mode
			WM3_MC_BuildFromNode (item.modifiers[#Morpher]) 1 temp  
		)
		
	)
	
)
J_createMorpher()

