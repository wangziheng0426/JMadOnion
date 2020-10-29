

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


--通用ButtonUI命名
fn PartMorpherMatchUIControlsFN UIControlArray MorpherNameArray startCount endCount =
(	
	UIControlArray[1].caption = "正常"
	local tempMorpherNameArray = #()
	for hsh in startCount to endCount do
	(
		if hsh <= MorpherNameArray.count then
		(	
			append tempMorpherNameArray MorpherNameArray[hsh][2]
		)
		else
		(
			messagebox "输入的系列号越界了"
			return undefined
		)
		
	)
	local tempMorpherCount = tempMorpherNameArray.count
	local tempCountUI =  UIControlArray.count - 1
	if tempCountUI > tempMorpherCount then
	(
		messagebox "输入的序列号有问题"	
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
--通用列表UI命名
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
			messagebox "输入的系列号越界了"
			return undefined
		)
	)
	DDListUIControl.items = tempDDlistArray
)


