

fn CommondCollectUIControlsFN ComstomRollout  ConstomStr ComstomArray= 
(
	for b in ComstomRollout.controls do
	(
		a = (findString b.name ConstomStr) as string
		if  a == "1"  do
		(	
			append ComstomArray b
		)
		/*
		c = (findString b.name "ButtEyeStyle") as string
		if  c == "1"  do
		(	
			append tempEyeUIControlsArray b
		)
		d = (findString b.name "BtnPupilDir") as string
		if  d == "1"  do
		(	
			append tempPupilUIControlsArray b
		)
		g = (findString b.name "BtnMouthStyle") as string
		if  g == "1"  do
		(	
			append tempMouthUIControlsArray b
		)
		*/
	)
)


--ͨ��ButtonUI����
fn PartMorpherMatchUIControlsFN UIControlArray MorpherNameArray startCount endCount =
(	
	UIControlArray[1].caption = "����"
	local tempMorpherNameArray = #()
	for hsh in startCount to endCount do
	(
		if hsh <= MorpherNameArray.count then
		(	
			append tempMorpherNameArray MorpherNameArray[hsh][2]
		)
		else
		(
			messagebox "�����ϵ�к�Խ����"
			return undefined
		)
		
	)
	local tempMorpherCount = tempMorpherNameArray.count
	local tempCountUI =  UIControlArray.count - 1
	if tempCountUI > tempMorpherCount then
	(
		messagebox "��������к�������"	
		return undefined
	)
	else
	(
		for i in 2 to UIControlArray.count do
		(
			UIControlArray[i].caption = tempMorpherNameArray[i-1]
		)
	)
)
--ͨ���б�UI����
fn PartMorpherMatchUIDDlistFN DDListUIControl MorpherNameArray startCount endCount =
(
	local tempDDlistArray = #()
	for hsh in startCount to endCount do
	(
		if hsh <= MorpherNameArray.count then
		(	
			append tempDDlistArray MorpherNameArray[hsh][2]
		)
		else
		(
			messagebox "�����ϵ�к�Խ����"
			return undefined
		)
	)
	DDListUIControl.items = tempDDlistArray
)

