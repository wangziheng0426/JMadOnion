fn J_createMorpher =
(
	for item in geometry do
	(
		if (matchPattern  item.name pattern:("*_Body_H_001") and item.parent.name =="Bip001 Head" and classof item.modifiers[0]!= undefined ) do
		(
			addmodifier item (Morpher ())
		)
		
	)
	
)
J_createMorpher()