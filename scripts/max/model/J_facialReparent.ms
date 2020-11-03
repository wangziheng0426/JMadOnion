fn J_facialReparent = 
(
	unhide objects
	clearSelection()
	log=""
	bodyHPart=undefined
	eyePart=undefined
	facialShyPart=undefined
	
	eyeEffect=undefined
	pupilEffect=undefined
    for item in geometry do
    (
		if classof item == PolyMeshObject or classof item == Editable_Poly or classof item == Editable_mesh do
			(   if matchPattern  item.name pattern:("*Body_H_001")  and length(item.pivot)<1  do
				(	
					bodyHPart=item	
				)	
				if matchPattern  item.name pattern:("*Body_H_001")  and length(item.pivot)>1  do
				(
					log +=(item.name +" transform is not 0 \n")
				)	
				if matchPattern  item.name pattern:("*_Eye_001") do
				(
					eyePart=item
				)
				if matchPattern  item.name pattern:("*_Facial_Shy_001") do
				(
					facialShyPart=item
				)	
				if matchPattern  item.name pattern:("*_Eye_Effect_001") do
				(
					eyeEffect=item
				)
				if matchPattern  item.name pattern:("*Pupil_Effect_001") do
				(
					pupilEffect=item
				)					
			)
    )	
	
	
		if bodyHPart!=undefined do
		(
			if  bodyHPart.modifiers[#Skin] != undefined do
			(
				temp=bodyHPart.modifiers[#Skin].name
				deleteModifier bodyHPart bodyHPart.modifiers[#Skin]
				log +=(bodyHPart.name + temp+" deleted\n")						
				)
			bodyHPart.parent = $'Bip001 Head'
			log +=(bodyHPart.name +" parented to Bip001 Head\n")
		)
		if eyePart!=undefined and bodyHPart!=undefined do
		(	
			eyePart.parent =bodyHPart				
			log +=(eyePart.name +" parented to "+bodyHPart.name+" \n")
		)
		if facialShyPart!=undefined and bodyHPart!=undefined do
		(	
			facialShyPart.parent =bodyHPart				
			log +=(facialShyPart.name +" parented to "+bodyHPart.name+" \n")
		)
		if eyeEffect!=undefined and bodyHPart!=undefined do
		(	
			eyeEffect.parent =bodyHPart				
			log +=(eyeEffect.name +" parented to "+bodyHPart.name+" \n")
		)
		if pupilEffect!=undefined and bodyHPart!=undefined do
		(	
			pupilEffect.parent =bodyHPart				
			log +=(pupilEffect.name +" parented to "+bodyHPart.name+" \n")
		)
		
	if bodyHPart==undefined do
	(log +=(" Body_H_001 not found\\n"))
	if eyePart==undefined do
	(log +=(" Eye_001 not found\\n"))

)
J_facialReparent()
