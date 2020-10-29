
/*
Author: 郝山虎
History: 2019年3月14，增加了存储数据的功能，为了解决制作过程中重复工作的情况
Note:max内表情制作工具，方便不会max的同学快速制作人物动画表情,修改内容：
	1、表情数据导出的时候，xaf数据结构有误，具体操作为，断开头部父子链接，再导出数据
	2、增加了刷新面板参数的功能
	3、修改了导出xaf和fbx的方法，防止导出表情按钮被点击之后，表情动画被破坏掉
Tel：13121939037
*/



	json=python.import("json")
		--导入python的json模块
	bi = Python.Import("__builtin__")
		--导入python的一些数据模块
	fff = newRolloutFloater "fdkaslfkdalfklakfa" 0 0
	--fff = newRolloutFloater "fdkaslfkdalfklakfa" 975 800
	closeRolloutFloater fff	
		------------------------------------------
	FacialPosSaveNameArray = #()
	FacialPosValue = #()
	getDic = bi.dict()
	--保存表情信息进入文本
	fn FacialDataSaveToJsonFN CustomFacialNameString DictName=
	(
		clearSelection()
		select $*_Body_H_001
		selectmore  $*_Eye_001
		selectmore  $*_Eye_Effect_001
		selectmore  $*Pupil_Effect_001
		DictName[CustomFacialNameString] =bi.dict aa:(bi.dict bb:(bi.dict ID:"value"))
		dd = sliderTime as string	
		DictName[CustomFacialNameString][dd]=bi.dict aa:"aa"
		for OBJ in selection do
		(
			DictName[CustomFacialNameString][dd][OBJ.name] = bi.dict aa:"aa"
			for i in 1 to 80 do
			(
				if (WM3_MC_GetValue OBJ.modifiers[Morpher] i) > 0.0 do
				(
					aa = i as string
					DictName[CustomFacialNameString][dd][OBJ.name][aa] =(WM3_MC_GetValue OBJ.modifiers[Morpher] i)
				)		
			)
			DictName[CustomFacialNameString][dd][OBJ.name].pop "aa"
			
		)
		DictName[CustomFacialNameString].pop "aa"
		DictName[CustomFacialNameString][dd].pop "aa"	
		--return ss
	)
	--根据表情pos名称，访问表情信息文本数据，将数据存入自定义数组中
	fn  AskForFacailPosNameFN CustomFacailPosNameString DictName =
	(
		FacialPosValue = #()
		if 	(DictName[CustomFacailPosNameString]) != undefined then
		(
			CustomTime=(DictName[CustomFacailPosNameString].keys())
			(
				for FacailPartID in 1 to CustomTime.count do
				(
					if (DictName[CustomFacailPosNameString][CustomTime[FacailPartID]]) != undefined  then		
					(
						FacailPart = (DictName[CustomFacailPosNameString][CustomTime[FacailPartID]].keys())
						
						for ValueID in 1 to FacailPart.count do
						(
							append FacialPosValue #(FacailPart[ValueID])
							if (DictName[CustomFacailPosNameString][CustomTime[FacailPartID]][FacailPart[ValueID]]) != undefined then
							(	
								MorpherChannel =(DictName[CustomFacailPosNameString][CustomTime[FacailPartID]][FacailPart[ValueID]].keys()) 
								for MorpherChannelID in 1 to MorpherChannel.count do
								(
									append FacialPosValue[ValueID] #((MorpherChannel[MorpherChannelID]),(DictName[CustomFacailPosNameString][CustomTime[FacailPartID]][FacailPart[ValueID]][MorpherChannel[MorpherChannelID]]))
								)
							)
							else
							(
								print "没有morpher数据"
							)
						)
					)
					else
					(
						print (CustomTime[FacailPartID]+"部位没有morpher数据存储")
					)
				)
			)
		)
		else
		(
			print "没有叫这个名字的morpher数据"
		)
	)
	--收集文本内的表情pos名称，存入自定义数组中
	fn CollectFacialPosNameFN DictName =
	(
		FacialPosSaveNameArray = #()
		if 	DictName != undefined then
		(
			print ((DictName.keys()).count)
			for FacialNameID in 1 to (DictName.keys()).count do
			(
				if (DictName.keys())[FacialNameID] != "FilePath" do
				(
					append FacialPosSaveNameArray ((DictName.keys())[FacialNameID])
				)
			)
			print FacialPosSaveNameArray.count
		)
		else
		(
			print "没有数据"
		)
	)
	--解析表情数据
	fn ResolveJsonDataFN CoustomArray=
	(
		if CoustomArray.count > 0 then
		(
			for FacailPartID in 1 to CoustomArray.count do
			(
				execute ("select $" + CoustomArray[FacailPartID][1])
				--print ("select $" + FacialPosValue[FacailPartID][1])
				if CoustomArray[FacailPartID].count > 1 then
				(
					for ChannelValueID in 2 to  CoustomArray[FacailPartID].count do
					(
						WM3_MC_SetValue $.modifiers[#Morpher] (CoustomArray[FacailPartID][ChannelValueID][1] as Integer) (CoustomArray[FacailPartID][ChannelValueID][2] as float)
						--print (FacialPosValue[FacailPartID][ChannelValueID][1])
					)
				)
				else
				(
					print "没有通道数据"
				)
			)
		)
		else
		(
			messagebox "没有文件"
		)
	)
	--刷新表情pos面板，高耦合函数
	fn ResetFaicalPosNameUIFN CoustomArray CoustomRolloutName =
	(
		--removeRollout FacialPosSaveStyles
		--FacialPosSaveStyles = rolloutCreator "FacialPosSaveStyles" "表情样式"
		FacialPosSaveStyles = rolloutCreator "FacialPosSaveStyles" "表情样式"
		FacialPosSaveStyles.begin()
		local hangkuan = 70
		local liegao = 25
		FacialPosSaveStyles.addControl #editText #FacialPosNameEDT "表情名称" paramStr: "pos:[0,0] width:133 height:17 align:#left"
		
		FacialPosSaveStyles.addControl #button #BTNCreateFacialPosName "创建表情pos数据" paramStr:"pos:[140,0] width:98 height:17 align:#left"
		FacialPosSaveStyles.addHandler #BTNCreateFacialPosName #pressed filter:on codeStr:("FacialDataSaveToJsonFN FacialPosNameEDT.text getDic \n removeRollout FacialPosSaveStyles  \n  CollectFacialPosNameFN getDic  \n ResetFaicalPosNameUIFN FacialPosSaveNameArray fff")
		--FacialPosSaveStyles.addHandler #FacialPosSaveStyles #open codeStr:"print FacialAnimationMakingDetailsTool.ProjectPathEDT.text"
		--FacialPosSaveStyles.addHandler #BTNCreateFacialPosName #pressed filter:on codeStr:("print fff.FacialAnimationMakingDetailsTool.ProjectPathBTN.text")
		--print ("ResetFaicalPosNameUIFN " + (CoustomArray as string) + "FacialPosSaveStyles")
		--getDic[\"FilePath\"] = FacialAnimationMakingDetailsTool.ProjectPathEDT.text  \n ResetFaicalPosNameUIFN FacialPosSaveNameArray fff
		if CoustomArray.count > 0 do
		(
			for i in 1 to  CoustomArray.count do
			( 
				local FaicalPosName = ("FaicalPosName"+(i as string)) as name
				FacialPosSaveStyles.addControl #button FaicalPosName (CoustomArray[i]) paramStr:("pos:["+ ((hangkuan *(i-1)) as string) + ",20]") 
				FacialPosSaveStyles.addHandler FaicalPosName #pressed filter:on codeStr:("AskForFacailPosNameFN " + (FaicalPosName as string) + ".caption  getDic \n ResolveJsonDataFN FacialPosValue \n fff.rollouts[1].AIKeyFacialPosFN fff.rollouts[1].MorpherUseableNumSPN.value 1 \n fff.rollouts[1].AIKeyFN fff.rollouts[1].MorpherUseableNumSPN.value 2" )
			) 
		)
		FacialPosSaveStyles.end()
		addRollout FacialPosSaveStyles CoustomRolloutName
		--addRollout FacialPosSaveStyles fff
	)
	---首先检查路径是否为空，如果为空，跳过，如果不为空，检查文件是否存在，如果存在，执行CollectFacialPosNameFN函数，收集表情pos名称，如果不存在，创建文件
	fn CheckFileIsTrueFN UIContorlName=
	(
		local TempFileIsTrue = getfiles (maxfilepath + "/info.jsn") 
		if TempFileIsTrue.count == 0 then
		(
			--file=bi.open "d://bb.jsn" "w"
			--有路径的话没有文件，就创建一个文件
			if UIContorlName.text.count != 0 then
			(
				file=bi.open (maxfilepath +"/info.jsn") "w"
				getDic["FilePath"] = UIContorlName.text
				mm=json.dumps getDic
				file.write mm 
				file.close()
			)
			else
			(
				messagebox "请先输入工程路径"
			)
		)
		else
		(
			--有文件的话就把文件内的读出来，放在字典里
			file=bi.open (maxfilepath+"/info.jsn") "r" 
			ss = file.read()
			--读取文件内数据
			getDic = json.loads ss
			--解序列化，是数据变成字典
			file.close()
			--关闭文件
			CollectFacialPosNameFN getDic
			--print getDic
			if getDic["FilePath"] != undefined then
			(
				--然后找到“filepath”的关键字对应的字符串，然后把字符串赋值给工程路径
				UIContorlName.text = getDic["FilePath"]
				--把字典内的表情pos名字存储出来
				--CollectFacialPosNameFN CoustomDict FacialPosSaveName
			)	
			else
			(
				if UIContorlName.text.count != 0 then
				(
					file=bi.open (maxfilepath +"/info.jsn") "w"
					getDic["FilePath"] = UIContorlName.text
					mm=json.dumps CoustomDict
					file.write mm 
					file.close()
				)
				else
				(
					messagebox "请先输入工程路径"
				)
			)
		)
	)
	fn SaveDataToCach =
	(
		file=bi.open (maxfilepath +"/info.jsn") "w"
		mm=json.dumps getDic
		file.write mm 
		file.close()
	)
	




rollout HsHExpressionToolCollection "表情制作工具集合" width:434 height:67
(
	button 'PaiXuButt' "排序" pos:[11,26] width:69 height:25 align:#left
	button 'ShiQuButt' "拾取" pos:[85,27] width:57 height:25 align:#left
	GroupBox 'grp1' "morpher制作工具" pos:[3,6] width:152 height:54 align:#left
	--button HuiChebutt "回撤" pos:[13,59] width:98 height:23
	GroupBox 'grp3' "表情动画编辑" pos:[161,6] width:263 height:55 align:#left
	button 'DemandButt' "需求制作" pos:[166,28] width:66 height:22 align:#left
	--button AnimateButt "动画调整" pos:[238,27] width:64 height:22
	button 'KFacilAnimateBTN' "K表情动画制作" pos:[308,27] width:93 height:21 align:#left
	
	
	
	-----------------------------------------------------------------
	------------
	-------排列mopher区域
	-------------------变量数据区---------------------------	
	
	local	FacialStandardsNameList=#(
				"sayLarge","sayI","saySmall","sayE","sayMedium",
				"Right_Eye_close","Left_Eye_close","Double_Eye_close","Right_Eye_close_001","Left_Eye_close_001","Double_Eye_close_001","Eye_Effect",
				"Eyebrow_up","Eyebrow_down","Eyebrow_gather",
				"Right_Pupil_up","Right_Pupil_down","Right_Pupil_right","Right_Pupil_left","Right_Pupil_scale","Right_Pupil_appear",
				"Left_Pupil_up","Left_Pupil_down","Left_Pupil_right","Left_Pupil_left","Left_Pupil_scale","Left_Pupil_appear",
				
				"Right_Effect_Pupil_up","Right_Effect_Pupil_down","Right_Effect_Pupil_right","Right_Effect_Pupil_left","Right_Effect_Pupil_scale","Right_Effect_Pupil_appear",
				"Left_Effect_Pupil_up","Left_Effect_Pupil_down","Left_Effect_Pupil_right","Left_Effect_Pupil_left","Left_Effect_Pupil_scale","Left_Effect_Pupil_appear",
				"Effect_Pupil_appear_symmetry","Effect_Pupil_appear_parallel",
				"Effect_Eye_appear_symmetry","Effect_Eye_appear_parallel",
				---标准区
				"Mouth_smiled","Eye_smiled","Eyebrow_smiled",
				"Mouth_anger","Eye_anger","Eyebrow_anger",
				"Mouth_sad","Eye_sad","Eyebrow_sad",
				"Mouth_smug","Eye_smug","Eyebrow_smug",
				"Mouth_pain","Eye_pain","Eyebrow_pain",
				"Mouth_shy","Eye_shy","Eyebrow_shy",
				"Mouth_shock","Eye_shock","Eyebrow_shock",
				"Mouth_doubt","Eye_doubt","Eyebrow_doubt",
				"Mouth_grievance","Eye_grievance","Eyebrow_grievance",
				"Mouth_serious","Eye_serious","Eyebrow_serious",
				"Mouth_calm","Eye_calm","Eyebrow_calm",
				"Mouth_nifty","Eye_nifty","Eyebrow_nifty",
				"Mouth_tsukomi","Eye_tsukomi","Eyebrow_tsukomi",
				"Mouth_panic","Eye_panic","Eyebrow_panic",
				"Mouth_confidence","Eye_confidence","Eyebrow_confidence",
				"Mouth_frustration","Eye_frustration","Eyebrow_frustration",
				"Mouth_squint","Eye_squint","Eyebrow_squint",
				"Mouth_helpless","Eye_helpless","Eyebrow_helpless",
				---特殊区
				"Mouth_special_001","Eye_special_001","Eyebrow_special_001",
				"Mouth_special_002","Eye_special_002","Eyebrow_special_002",
				"Mouth_special_003","Eye_special_003","Eyebrow_special_003",
				"Mouth_special_004","Eye_special_004","Eyebrow_special_004",
				"Mouth_special_005","Eye_special_005","Eyebrow_special_005",
				"Mouth_special_006","Eye_special_006","Eyebrow_special_006",
				"Mouth_special_007","Eye_special_007","Eyebrow_special_007",
				"Mouth_special_008","Eye_special_008","Eyebrow_special_008",
				"Mouth_special_009","Eye_special_009","Eyebrow_special_009",
				"Mouth_special_010","Eye_special_010","Eyebrow_special_010",
				"Mouth_special_011","Eye_special_011","Eyebrow_special_011",
				"Mouth_special_012","Eye_special_012","Eyebrow_special_012",
				"Mouth_special_013","Eye_special_013","Eyebrow_special_013",
				"Mouth_special_014","Eye_special_014","Eyebrow_special_014",
				"Mouth_special_015","Eye_special_015","Eyebrow_special_015",
				"Mouth_special_016","Eye_special_016","Eyebrow_special_016",
				"Mouth_special_017","Eye_special_017","Eyebrow_special_017",
				"Mouth_special_018","Eye_special_018","Eyebrow_special_018",
				"Mouth_special_019","Eye_special_019","Eyebrow_special_019",
				"Mouth_special_020","Eye_special_020","Eyebrow_special_020")
	local	LabelgongnengPosArray = #([9,62],[9,87],[9,118],[9,145],[9,222])
	local	LabelbiaozhunPosArray = #([16,328],[16,385],[16,443])
	local	LabelteshuPosArray = #([409,65],[409,149],[409,228])
	local	PartFacilArray = #("Mouth","Eye","Eyebrow","Pupil","Effect")
	local	fenquString = #("gongneng","biaozhun","teshu")
	local	FacilGeneralStandards = #("smiled","anger","sad","smug","pain","shy","shock","doubt","grievance","serious","calm","nifty","tsukomi","panic","confidence","frustration","squint","helpless")
	local	FacilFuncMouthArray = #("sayLarge","sayI","saySmall","sayE","sayMedium")
	local	FacilFuncEyeArray = #("Right_Eye_close","Left_Eye_close","Double_Eye_close","Right_Eye_close_001","Left_Eye_close_001","Double_Eye_close_001","Eye_Effect")
	local	FacilFuncEyebrowArray = #("Eyebrow_up","Eyebrow_down","Eyebrow_gather")
	--FacilFuncPupilArray = #(#("Right_Pupil_up","Right_Pupil_down","Right_Pupil_right","Right_Pupil_left","Right_Pupil_scale"),#("Left_Pupil_up","Left_Pupil_down","Left_Pupil_right","Left_Pupil_left","Left_Pupil_scale"),#("Pupil_appea"))
	local FacilFuncPupilArray = #("Right_Pupil_up","Right_Pupil_down","Right_Pupil_right","Right_Pupil_left","Right_Pupil_scale","Right_Pupil_appear",
									"Left_Pupil_up","Left_Pupil_down","Left_Pupil_right","Left_Pupil_left","Left_Pupil_scale","Left_Pupil_appear")
	local FacilFuncEffectArray = #("Right_Effect_Pupil_up","Right_Effect_Pupil_down","Right_Effect_Pupil_right","Right_Effect_Pupil_left","Right_Effect_Pupil_scale","Right_Effect_Pupil_appear",
								 " Left_Effect_Pupil_up","Left_Effect_Pupil_down","Left_Effect_Pupil_right","Left_Effect_Pupil_left","Left_Effect_Pupil_scale","Left_Effect_Pupil_appear",
								 "Effect_Pupil_appear_symmetry","Effect_Pupil_appear_parallel","Effect_Eye_appear_symmetry","Effect_Eye_appear_parallel")
	local	ButtonCountNumber = 0					 
					
	local CanZhaowuPos = [0,0,0]
	local rci
	-----------------------------------------------------------------
	------------
	-------排列mopher区域
	-------------------变量数据区---------------------------





								 
	-----------------------------------------------------------------
	------------
	-------拾取mopher区域
	-------------------变量数据区---------------------------				
								 
	local  morpher_target = #(
				"sayLarge","sayI","saySmall","sayE","sayMedium",
				"Right_Eye_close","Left_Eye_close","Double_Eye_close","Right_Eye_close_001","Left_Eye_close_001","Double_Eye_close_001","Eye_Effect",
				"Eyebrow_up","Eyebrow_down","Eyebrow_gather",
					
					
					
				
				"Mouth_smiled","Eye_smiled","Eyebrow_smiled",
				"Mouth_anger","Eye_anger","Eyebrow_anger",
				"Mouth_sad","Eye_sad","Eyebrow_sad",
				"Mouth_smug","Eye_smug","Eyebrow_smug",
				"Mouth_pain","Eye_pain","Eyebrow_pain",
				"Mouth_shy","Eye_shy","Eyebrow_shy",
				"Mouth_shock","Eye_shock","Eyebrow_shock",
				"Mouth_doubt","Eye_doubt","Eyebrow_doubt",
				"Mouth_grievance","Eye_grievance","Eyebrow_grievance",
				"Mouth_serious","Eye_serious","Eyebrow_serious",
				"Mouth_calm","Eye_calm","Eyebrow_calm",
				"Mouth_nifty","Eye_nifty","Eyebrow_nifty",
				"Mouth_tsukomi","Eye_tsukomi","Eyebrow_tsukomi",
				"Mouth_panic","Eye_panic","Eyebrow_panic",
				"Mouth_confidence","Eye_confidence","Eyebrow_confidence",
				"Mouth_frustration","Eye_frustration","Eyebrow_frustration",
				"Mouth_squint","Eye_squint","Eyebrow_squint",
				"Mouth_helpless","Eye_helpless","Eyebrow_helpless",
				"Mouth_special_001","Eye_special_001","Eyebrow_special_001",
				"Mouth_special_002","Eye_special_002","Eyebrow_special_002",
				"Mouth_special_003","Eye_special_003","Eyebrow_special_003",
				"Mouth_special_004","Eye_special_004","Eyebrow_special_004",
				"Mouth_special_005","Eye_special_005","Eyebrow_special_005",
				"Mouth_special_006","Eye_special_006","Eyebrow_special_006",
				"Mouth_special_007","Eye_special_007","Eyebrow_special_007",
				"Mouth_special_008","Eye_special_008","Eyebrow_special_008",
				"Mouth_special_009","Eye_special_009","Eyebrow_special_009",
				"Mouth_special_010","Eye_special_010","Eyebrow_special_010",
				"Mouth_special_011","Eye_special_011","Eyebrow_special_011",
				"Mouth_special_012","Eye_special_012","Eyebrow_special_012",
				"Mouth_special_013","Eye_special_013","Eyebrow_special_013",
				"Mouth_special_014","Eye_special_014","Eyebrow_special_014",
				"Mouth_special_015","Eye_special_015","Eyebrow_special_015",
				"Mouth_special_016","Eye_special_016","Eyebrow_special_016",
				"Mouth_special_017","Eye_special_017","Eyebrow_special_017",
				"Mouth_special_018","Eye_special_018","Eyebrow_special_018",
				"Mouth_special_019","Eye_special_019","Eyebrow_special_019",
				"Mouth_special_020","Eye_special_020","Eyebrow_special_020"
				)
	local 	MorpherEyeEffectArray = #("Effect_Eye_appear_symmetry","Effect_Eye_appear_parallel")	
	local  MorpherPupilEffectArray  =#("Right_Effect_Pupil_up","Right_Effect_Pupil_down","Right_Effect_Pupil_right","Right_Effect_Pupil_left","Right_Effect_Pupil_scale","Right_Effect_Pupil_appear",
										"Left_Effect_Pupil_up","Left_Effect_Pupil_down","Left_Effect_Pupil_right","Left_Effect_Pupil_left","Left_Effect_Pupil_scale","Left_Effect_Pupil_appear",
										"Effect_Pupil_appear_symmetry","Effect_Pupil_appear_parallel")	
	local  MorpherPupilArray	= #("Right_Pupil_up","Right_Pupil_down","Right_Pupil_right","Right_Pupil_left","Right_Pupil_scale","Right_Pupil_appear",
									"Left_Pupil_up","Left_Pupil_down","Left_Pupil_right","Left_Pupil_left","Left_Pupil_scale","Left_Pupil_appear")	
	local PartOfFacilArray = #("Body_H_","Eye_","Pupil_Effect_","Eye_Effect_")			
	local  TempShiQuMorpherInfo = #()	
	-----------------------------------------------------------------
	------------
	-------拾取mopher区域
	-------------------变量数据区---------------------------	
								 
								 
	

					
	-----------------------------------------------------------------
	------------
	-------表情动画制作区--------------------
	-------------------变量数据区---------------------------							 
	
	local animate_names = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","air1","air2","night","spattack","spattack_b","torpedo1","torpedo2","torpedo_n","gun_a1","gun_a2","gun_b","gun_ss","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi")
			--local sound_Arr = #()
	-----------------------------------------------------------------
	------------
	-------表情动画制作区--------------------
	-------------------变量数据区---------------------------

	
	
	--ModulateAnimateRoll = rolloutCreator "FaciaAnimationModulateAll" "FaciaAnimationAll"


	local ss = rolloutCreator "FaciaAnimationModulateAll" "FaciaAnimationAll"				
								 
	-----------------------------------------------------------------
	------------
	-------排列mopher区域
	-------------------生成Label的方法---------------------------								 
	fn shengchengpos ConstomString ConstomPosArray ConstomCaptionArray =
	(
		aConstomString = ConstomString
		aPosString = ConstomPosArray as string
		aCaption   =  ConstomCaptionArray
		aControlName = (aConstomString + aCaption) as name	
		rci.addControl 	#label aControlName aCaption  paramStr:("pos:" + aPosString + "width:52 height:21")
	)
	-------------------通过按钮给物体排序的方法-------------------
	fn MorpherListFN IntervalLineSpace LineNum IntervalListSpace ListNum IFConstomString ConstomString= 
	(
		TargetPos = CanZhaowuPos + [(IntervalListSpace*ListNum),0,(0-(IntervalLineSpace*LineNum))]
		--print CanZhaowuPos
		--ChangeNameOfObj.name = ConstomInputString
		--print selection.count
		if selection.count > 0 then
		(	
			if selection.count == 1 then
			(	
				
				$.name = ConstomString
				
			)
			else
			(
				for obj in selection do
				(
					obj.pos = TargetPos
					--print obj.name
					if ((findstring obj.name IFConstomString) as string) != "undefined" do
					(
						obj.name = ConstomString
					)
				)
			)
		)
		else
		(
			messagebox "请选择物体"
		)
	)
	-------------------通过按钮给物体排序的逻辑-------------------
	fn  MorpherSortFN  ConstomInputStringID=
	(
		 FacialStandardsNameList = HsHExpressionToolCollection.FacialStandardsNameList
		 PartFacilArray = HsHExpressionToolCollection.PartFacilArray
		
		--print FacialStandardsNameList
		local IntervalLineSpace = 50
		local IntervalListSpace = 50
		
		if ConstomInputStringID < 44 do
		(
			--print "功能区排序"
			--嘴巴排序
			if ConstomInputStringID < 6 do
			(
				HsHExpressionToolCollection.MorpherListFN  IntervalLineSpace 1 IntervalListSpace ConstomInputStringID "Body_H_" FacialStandardsNameList[ConstomInputStringID]
			)	
			--眼皮排序
			if ConstomInputStringID > 5 and ConstomInputStringID < 13 do
			(
				HsHExpressionToolCollection.MorpherListFN  IntervalLineSpace 2 IntervalListSpace (ConstomInputStringID-5) "Body_H_" FacialStandardsNameList[ConstomInputStringID]
				
			)
			--眉毛排序
			if ConstomInputStringID > 12 and ConstomInputStringID < 16 do
			(
				HsHExpressionToolCollection.MorpherListFN  IntervalLineSpace 3 IntervalListSpace (ConstomInputStringID-12)  "Body_H_" FacialStandardsNameList[ConstomInputStringID]
			
			)
			--瞳孔排序
			if ConstomInputStringID > 15 and ConstomInputStringID < 28 do
			(
				
				HangShu = (Int((ConstomInputStringID - 16)/6))+4
				print HangShu
				LieShu  = (mod (ConstomInputStringID - 16) 6)+1
				print LieShu
				HsHExpressionToolCollection.MorpherListFN  IntervalLineSpace HangShu IntervalListSpace LieShu "_Eye_0"  FacialStandardsNameList[ConstomInputStringID]
			)
			--特效瞳孔排序
			if ConstomInputStringID > 27 and ConstomInputStringID < 42 do
			(
				HangShu = (int((ConstomInputStringID - 28)/6))+8
				LieShu  = (mod (ConstomInputStringID - 28) 6)+1
				HsHExpressionToolCollection.MorpherListFN  IntervalLineSpace HangShu IntervalListSpace LieShu "_Pupil_Effect_"  FacialStandardsNameList[ConstomInputStringID]
			)
			--特效眼睛排序
			if ConstomInputStringID > 41 and ConstomInputStringID < 44 do
			(
				HangShu = int((ConstomInputStringID - 42)/5)+10
				LieShu  = ConstomInputStringID - 42
				--print HangShu
				--print LieShu
				HsHExpressionToolCollection.MorpherListFN  IntervalLineSpace HangShu IntervalListSpace LieShu "_Eye_Effect_"  FacialStandardsNameList[ConstomInputStringID]
				
			)	
		)
		if ConstomInputStringID > 43 and ConstomInputStringID < 98 do
		(
			HangShu =(int((ConstomInputStringID - 44)/(FacilGeneralStandards.count)))+1
			LieShu = (mod (ConstomInputStringID - 44) (FacilGeneralStandards.count)) +9	
			ConstomString = PartFacilArray[HangShu] +"_"+FacilGeneralStandards[(LieShu-8)]	
			HsHExpressionToolCollection.MorpherListFN  IntervalLineSpace HangShu IntervalListSpace LieShu "Body_H_"  ConstomString
		)
		if ConstomInputStringID >97 and ConstomInputStringID <158 do
		(
			HangShu =(int((ConstomInputStringID - 98)/20)) +1
			LieShu = int((mod (ConstomInputStringID - 98) 20) +9 + (FacilGeneralStandards.count))
			
			if (LieShu-26) > 9 then
			(	
				ConstomString = PartFacilArray[HangShu] + "_special_"	+"0"+ ((LieShu-26)as string)
				HsHExpressionToolCollection.MorpherListFN  IntervalLineSpace HangShu IntervalListSpace LieShu "Body_H_"  ConstomString
				
			)
			else
			(
				ConstomString = PartFacilArray[HangShu] + "_special_"	+"00"+ ((LieShu-26) as string)
				HsHExpressionToolCollection.MorpherListFN  IntervalLineSpace HangShu IntervalListSpace LieShu "Body_H_"  ConstomString			
			)
			
		)	
	)
	----------创建特殊的按钮----------------------
	fn ButtonProduceFN IDX1 IDX2 IDX3 IDX4 IDX5 ConstomString=
	(
		ButtonCountNumber += 1
		aaCostomButtonName = (ConstomString +(IDX1 as string)+ (IDX2 as string)) as name
		--aaCostomButtonCaption = IDX2 as string
		aaCostomButtonCaption =ButtonCountNumber as string
		--aaCostomButtonCaption =FacialStandardsNameList[ButtonCountNumber] 
		aaCostomButtonPos = (IDX3 + [IDX4,IDX5]) as string
		rci.addControl #button aaCostomButtonName aaCostomButtonCaption paramStr:("pos:" + aaCostomButtonPos +"width:37 height:19")
		rci.addHandler aaCostomButtonName #pressed filter:on codeStr:("HsHExpressionToolCollection.MorpherSortFN " + ButtonCountNumber as string)
		--rci.addHandler aaCostomButtonName #pressed filter:on codeStr:"print @dffeafdafrefdasfewf@"
		--print ("MorpherSortFN " + ButtonCountNumber as string)		
	)
	----------创建标准的按钮----------------------
	fn ButtonStandProduceFN IDX1 IDX2 IDX3 IDX4 IDX5 ConstomString ConstomWidth Constomheight=
	(
		ButtonCountNumber += 1
		aaCostomButtonName = (ConstomString +(IDX1 as string)+ (IDX2 as string)) as name
		aaCostomButtonCaption = IDX2 as string
		--aaCostomButtonCaption = ButtonCountNumber as string	
		aaCostomButtonPos = (IDX3 + [IDX4,IDX5]) as string
		rci.addControl #button aaCostomButtonName aaCostomButtonCaption paramStr:("pos:" + aaCostomButtonPos+"width:"+(ConstomWidth as string)+" height:"+ (Constomheight as string))
		rci.addHandler aaCostomButtonName #pressed filter:on codeStr:("HsHExpressionToolCollection.MorpherSortFN " + ButtonCountNumber as string)
		--rci.addHandler aaCostomButtonName #pressed filter:on codeStr:"print @dffeafdafrefdasfewf@"
		--print ("MorpherSortFN " + ButtonCountNumber as string)
	)
	
	
	
	
	
	--------排列mopher区域
	------------
	--------------------------------------------------------------------

	fn ShiQuCollectMorpherInfoFN ConstomArray=
	(
		
		for i in 1 to 80 do
		(	
			if (WM3_MC_HasData $.modifiers[#Morpher] i) == true do
			(	
				append ConstomArray #((WM3_MC_GetName $.modifiers[#Morpher] i),(WM3_MC_GetValue $.modifiers[#Morpher] i))
				--print (WM3_MC_GetValue $.modifiers[#Morpher] i)
			)
		)
	)

	fn ShiQuFuZhiFN ConstomArray= 
	(
		for i in 1 to ConstomArray.count do
		(
			for k in 1 to 80 do
			(
				if ConstomArray[i][1] == (WM3_MC_GetName $.modifiers[#Morpher] k) do
				(
					--print (WM3_MC_GetName $.modifiers[#Morpher] k)
					--print (ConstomArray[i][1])
					--print ConstomArray[i][2]
					WM3_MC_SetValue $.modifiers[#Morpher] k ConstomArray[i][2]
				)
				
			)
		)
	)
	
	
	fn CollectMorpherInfoFN ConstomArray=
	(
		select $*Body_H_001
		
		for i in 1 to 80 do
		(	
			if (WM3_MC_HasData $.modifiers[#Morpher] i) == true do
			(	
				--MorpherCount+=1
				append ConstomArray #((WM3_MC_GetName $.modifiers[#Morpher] i),(WM3_MC_GetValue $.modifiers[#Morpher] i))
				--print (WM3_MC_GetValue $.modifiers[#Morpher] i)
			)
			
		)
	)
	
	fn RelationMorpherValueFN ConstomString ConstomValue=
	(
		select $*Body_H_001
		for i in 1 to 80 do
		(
			if (WM3_MC_GetName $.modifiers[#Morpher] i) == ConstomString do
			(
				WM3_MC_SetValue $.modifiers[#Morpher] i ConstomValue
			)
		)	
	)
	fn UIRelationFN= 
	(
		select $*Body_H_001
		for i in 1 to FaciaAnimationModulateAll.controls.count do
		(	
			print "ssss"
			FaciaAnimationModulateAll.controls[i].value =(WM3_MC_GetValue $.modifiers[#Morpher] i)
		)
	)
	
	
	
	
	
	
	
	
	fn HsHMorPickFN MorpherTargetArray=
	(	
		icount = 0
		for i in 1 to MorpherTargetArray.count do
		(
				
			for m in Geometry do 
			(	
				b = toLower MorpherTargetArray[i]
				c = toLower m.name
				if b ==c do
				(
					--print "chengongl"
					icount +=1
					--select $*body_h_001
					WM3_MC_BuildFromNode $.morpher icount m	
				)
				
			)
			
		)
	)	
	
	fn HAIOrder ConstomSring ConstomNumber = 
	(
		if selection.count == 1 then
		(	
			--MessageBox "Isn't this cool" title:"Wow"
			--print ConstomSring
			local 	StartPointX = -470
			local 	StartPointZ = 380
			local  Constominterval = 40
			posChuShi = [0,0,0]
			posChuShi = $.pos 
			if ConstomNumber <10 then
			(
				--MessageBox "排列特殊"
				hangshu = (int (ConstomNumber-1)/3)+1
				lieshu = (mod (ConstomNumber-1) 3) +1
				--print hangshu
				--print lieshu
				$.pos.x = StartPointX + (Constominterval*(lieshu-0.5))
				$.pos.z = StartPointZ - ((hangshu-0.5)*Constominterval)
				$.name = ConstomSring
			)
			else
			(
				--MessageBox "正常排序"
				hangshu = (mod (ConstomNumber-1) 3)+1
				lieshu = (int (ConstomNumber-1)/3) +1
				--print hangshu
				--print lieshu
				$.pos.x = StartPointX + (Constominterval*(lieshu-0.5))
				$.pos.z = StartPointZ - ((hangshu-0.5)*Constominterval)
				$.name = ConstomSring
			)
		)
		else
		(
			if selection.count == 0 do
			(
				messagebox "没有选中物体"
			)
			if selection.count >1  do
			(
				messagebox "只能选中一个物体"
			)
		)
	)
	fn ceshi =
	(
		MessageBox "排列特殊"
	)
	
	
	
	-----------------------------------------------------------------
	------------
	-------通用方法
	-------------------方法区---------------------------
	----调整声音播放开始时间的方法
	fn sound_start_fn set_time= 
	(
		
		if prosound.NumTracks() >= 1 then
		(	
			prosound.setstart 1 set_time
			bbbb = prosound.filelength 1
			prosound.setend 1 (set_time  + bbbb) 
		)
		else
		(
		
			messageBox "没有声音"
		)	
		
		
	)
	-----导入bip动画的方法
	fn import_bip_sound_fn	animate_S ConstomUIContorl=
	(
		
		animationRange = interval 0 30
		temp_aaa = ""
		temp_bbb =substituteString maxfilename "001.max" temp_aaa
		sound_path_S = ConstomUIContorl.text  + "\\sound\\" +  "CV_" + temp_bbb + animate_S + ".wav"
		bip_path_S = ConstomUIContorl.text + "\\bip\\" +animate_S + ".bip"
		
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
		else
		(
			messagebox "文件不是绑定文件"
		)
	)
	--导入xaf的共用方法
	fn import_xaf_fn animate_S path_S MorpherNum=
	(
		bip_path_S = path_S +"\\xaf\\"  + animate_S + ".xaf"			
		select $*Body_H_001
		selectmore $*Pupil_Effect_001
		selectmore $*Eye_Effect_001
		selectmore $*Eye_001
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
			select $*Body_H_001
			selectmore $*Pupil_Effect_001
			selectmore $*Eye_Effect_001
			selectmore $*Eye_001
			for obj in selection do
			(
				--print obj.name
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
			messageBox "还没有制作这个表情文件"	
		)
		
		
	)
	fn ImportMouthXafFN animate_S path_S= 
	(
		bip_path_S = path_S +"\\MouthXaf\\"  + animate_S + ".xaf"
		select $*Body_H_001
		if $.modifiers[Morpher][2].keys == undefined then
		(
			
			LoadSaveAnimation.loadAnimation  bip_path_S  $ 
			print "声音导入成功"
		)
		else		
		(
			if $.modifiers[Morpher][2].keys.count <1 do
			(	
				
				select $*Body_H_001
				a = LoadSaveAnimation.loadAnimation  bip_path_S  $ 
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
	)	
	--导出fbx的共用方法
	fn export_facialFbx_fn animate_S path_S=
	(
		bip_path_S = path_S +"\\facial\\"  + animate_S + ".fbx"	
		sliderTime = 0f	
		$Bip001.controller.figureMode = true
		select $*Body_H_001
		max unlink
		selectKeys $.controller
		deleteKeys $.controller #selection
		selectmore $*Pupil_Effect_001
		selectmore $*Eye_Effect_001
		selectmore $*Eye_001
		--LoadSaveAnimation.saveAnimation  bip_path_S  $ #() #()
		FbxExporterSetParam "Animation" true
		FbxExporterSetParam "UpAxis" "Y"
		exportFile bip_path_S #noPrompt selectedOnly:true
		
		select $*Body_H_001
		$.controller.rotation.x =0
		$.controller.rotation.y =0
		$.controller.rotation.z =0
		
		$.parent = $Bip001_Head
		
		$Bip001.controller.figureMode = false
	)
	--导出xaf的共用方法
	fn export_xaf_fn animate_S path_S=
	(
		bip_path_S = path_S +"\\xaf\\"  + animate_S + ".xaf"
		sliderTime = 0f	
		$Bip001.controller.figureMode = true	
		select $*Body_H_001
		max unlink
		$.controller.rotation.x =0
		$.controller.rotation.y =0
		$.controller.rotation.z =0
		selectKeys $.controller
		deleteKeys $.controller #selection
		
		
		
		
		selectmore $*Pupil_Effect_001
		selectmore $*Eye_Effect_001
		selectmore $*Eye_001
		LoadSaveAnimation.saveAnimation  bip_path_S  $ #() #()
		select $*Body_H_001
		$.parent = $Bip001_Head
		$Bip001.controller.figureMode = false
		/*
		select $*Body_H_001
		
		--删除材质球的动画数据，并且重置参数

		$.material._FaceFlushToggle = off
		$.material._FlushRange = 0
		$.material._FlushIntensity = color 0 0 0 0
		$.material._RedFlushColor = color 255 0 0 255
		$.material._BlackFlushColor = color 0 0 0 255
		
		select $*Body_H_001
		deleteKeys $.material
		$.parent = $Bip001_Head
		
		--清除眼睛特效和瞳孔特效贴片上的数值
		clearSelection()
		select  $*Eye_Effect_001
		if selection.count == 1 do
		(	
			$.EyeTextureTrans.texIndex = 0
			if $.EyeTextureTrans.texIndex.keys != undefined do
			(	
				deleteKeys $.EyeTextureTrans.texIndex.keys
			)
		)
		clearSelection()
		select  $*Pupil_Effect_001
		if selection.count == 1 do
		(	
			$.EyeTextureTrans.texIndex = 0
			if $.EyeTextureTrans.texIndex.keys != undefined do
			(	
				deleteKeys $.EyeTextureTrans.texIndex.keys
			)
		)
		*/
	)
	
	
	
	
	on HsHExpressionToolCollection open  do
	(
		--local FilePathOfProject = maxfilepath + 
		json=python.import("json")
		--导入python的json模块
		bi = Python.Import("__builtin__")
		--导入python的一些数据模块
	)
	on PaiXuButt pressed do
	(
		
		rci = rolloutCreator "myRollout" "My Rollout"
		rci.width=951
		rci.height=500
		rci.begin()
		
		
		rci.addControl #button #StartPos "参照物" paramStr:"pos:[14,7] width:118 height:27"
		rci.addHandler #StartPos #pressed filter:on codeStr:"HsHExpressionToolCollection.CanZhaowuPos = $.pos"
								 
														 
		rci.addControl #groupBox #mygroup1 "功能区" paramStr:"pos:[4,41] width:384 height:257"
		rci.addControl #groupBox #mygroup2 "特殊区" paramStr:"pos:[404,42] width:524 height:257"
		rci.addControl #groupBox #mygroup3 "标准区" paramStr:"pos:[5,303] width:925 height:190"
	
		--创建按钮---------------------------
		-----------------------------------
		------------------------------------
		for i in 1 to fenquString.count do
		(
			local ButtonJianGe = 40
			local ButtonJianGeShu = 25
			local LabelgongnengPosArray = HsHExpressionToolCollection.LabelgongnengPosArray
			local fenquString =HsHExpressionToolCollection.fenquString
			local PartFacilArray = HsHExpressionToolCollection.PartFacilArray
			local FacilFuncMouthArray = HsHExpressionToolCollection.FacilFuncMouthArray
			local FacilFuncEyebrowArray =HsHExpressionToolCollection.FacilFuncEyebrowArray
			local FacilFuncEyeArray =HsHExpressionToolCollection.FacilFuncEyeArray
			local LabelteshuPosArray = HsHExpressionToolCollection.LabelteshuPosArray
			local LabelbiaozhunPosArray = HsHExpressionToolCollection.LabelbiaozhunPosArray
			if i==1 do
			(
				for k in 1 to LabelgongnengPosArray.count do
				(
					HsHExpressionToolCollection.shengchengpos fenquString[i] LabelgongnengPosArray[k] PartFacilArray[k]
					local a = LabelgongnengPosArray[k] +[10,0]
					if k == 1 do
					(
						for m in 1 to FacilFuncMouthArray.count do
						(
							
							ButtonProduceFN k m a (ButtonJianGe*m) 0 (fenquString[i]+PartFacilArray[k])
						)
					)
					if	k == 2	do
					(
						for m in 1 to FacilFuncEyeArray.count do
						(
							ButtonProduceFN k m a (ButtonJianGe*m) 0 (fenquString[i]+PartFacilArray[k])
						)
					)
					if	k==3 do
					(
						for m in 1 to FacilFuncEyebrowArray.count do
						(
							ButtonProduceFN k m a (ButtonJianGe*m) 0 (fenquString[i]+PartFacilArray[k])
						)
					)
					if	k==4 do
					(
						
						for m in 1 to FacilFuncPupilArray.count do
						(
							ButtonProduceFN k m a (ButtonJianGe*((mod (m-1) 6) +1)) (ButtonJianGeShu*(int((m-1)/6))) (fenquString[i]+PartFacilArray[k])
						)
					)
					if	k==5 do
					(
						for m in 1 to FacilFuncEffectArray.count do
						(
							if m<15 then
							(	
								ButtonProduceFN k m a (ButtonJianGe*((mod (m-1) 6) +1)) (ButtonJianGeShu*(int((m-1)/6))) (fenquString[i]+PartFacilArray[k])
							)		
							else
							(
								ButtonProduceFN k m a (ButtonJianGe*(m-8)) (ButtonJianGeShu*2)	 (fenquString[i]+PartFacilArray[k])
							)
						)
					)				
				)	
			)
			if i == 2 do
			(
				for k in 1 to LabelbiaozhunPosArray.count do
				( 
					
					HsHExpressionToolCollection.shengchengpos  fenquString[i] LabelbiaozhunPosArray[k] PartFacilArray[k]
					local a = LabelbiaozhunPosArray[k] +[10,0]
					for m in 1 to FacilGeneralStandards.count do
					(
						--ButtonStandProduceFN k m a (ButtonJianGe*((mod (m-1) 10) +1)) (ButtonJianGeShu*(int((m-1)/10))) (fenquString[i]+PartFacilArray[k]) 37 19 
						ButtonStandProduceFN k FacilGeneralStandards[m] a (60*((mod (m-1) 14) +1)) (ButtonJianGeShu*(int((m-1)/14))) (fenquString[i]+PartFacilArray[k]) 55 19
						--ButtonProduceFN k m a (ButtonJianGe*(m-6)) (ButtonJianGeShu*2)	 (fenquString[i]+PartFacilArray[k])
					)
				)
			)
			if i == 3 do
			(
				for k in 1 to LabelteshuPosArray.count do
				(
					HsHExpressionToolCollection.shengchengpos  fenquString[i] LabelteshuPosArray[k] PartFacilArray[k]
					local a = LabelteshuPosArray[k] +[10,0]
					for m in 1 to 20 do
					(
						--print "m"
						ButtonStandProduceFN k m a (ButtonJianGe*((mod (m-1) 10) +1)) (ButtonJianGeShu*(int((m-1)/10))) (fenquString[i]+PartFacilArray[k]) 37 19
						--ButtonProduceFN k m a (ButtonJianGe*(m-6)) (ButtonJianGeShu*2)	 (fenquString[i]+PartFacilArray[k])
					)	
				)
			)
		)
		ButtonCountNumber = 0
		createDialog (rci.end())
	
	)
	on ShiQuButt pressed do
	(
		
	
				
		if selection.count >0 then
		(	
			a =1
			if selection.count ==1 then
			(
				for Part in 1 to HsHExpressionToolCollection.PartOfFacilArray.count do
				(
					if ((findstring selection[1].name HsHExpressionToolCollection.PartOfFacilArray[Part]) as string) != "undefined" then
					(
						if Part ==1 do
						(
							if selection[1].modifiers.count > 0 then
							(	
								if (classof (selection[1].modifiers[a])) == Morpher then
								(
									HsHExpressionToolCollection.ShiQuCollectMorpherInfoFN HsHExpressionToolCollection.TempShiQuMorpherInfo
									print TempShiQuMorpherInfo
									deleteModifier $ 1
									addmodifier $ (Morpher name:"Morpher")
									HsHExpressionToolCollection.HsHMorPickFN HsHExpressionToolCollection.morpher_target
									HsHExpressionToolCollection.ShiQuFuZhiFN HsHExpressionToolCollection.TempShiQuMorpherInfo
								)
								else
								(
									addmodifier $ (Morpher name:"Morpher")
									HsHExpressionToolCollection.HsHMorPickFN HsHExpressionToolCollection.morpher_target
								)
							)
							else
							(
								addmodifier $ (Morpher name:"Morpher")
								HsHExpressionToolCollection.HsHMorPickFN HsHExpressionToolCollection.morpher_target
							)
						)
						if Part ==2 do
						(
							if selection[1].modifiers.count > 0 then
							(	
								if (classof (selection[1].modifiers[a])) == Morpher then
								(
									HsHExpressionToolCollection.ShiQuCollectMorpherInfoFN HsHExpressionToolCollection.TempShiQuMorpherInfo
									print TempShiQuMorpherInfo
									deleteModifier $ 1
									addmodifier $ (Morpher name:"Morpher")
									HsHExpressionToolCollection.HsHMorPickFN   HsHExpressionToolCollection.MorpherPupilArray
									HsHExpressionToolCollection.ShiQuFuZhiFN HsHExpressionToolCollection.TempShiQuMorpherInfo
								)
								else
								(
									addmodifier $ (Morpher name:"Morpher")
									HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherPupilArray
								)
							)
							else
							(
								addmodifier $ (Morpher name:"Morpher")
								HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherPupilArray
							)
						)
						if Part ==3 do
						(
							if selection[1].modifiers.count > 0 then
							(	
								if (classof (selection[1].modifiers[a])) == Morpher then
								(
									HsHExpressionToolCollection.ShiQuCollectMorpherInfoFN HsHExpressionToolCollection.TempShiQuMorpherInfo
									
									deleteModifier $ 1
									addmodifier $ (Morpher name:"Morpher")
									HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherPupilEffectArray
									HsHExpressionToolCollection.ShiQuFuZhiFN HsHExpressionToolCollection.TempShiQuMorpherInfo
								)
								else
								(
									addmodifier $ (Morpher name:"Morpher")
									HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherPupilEffectArray
								)
							)
							else
							(
								addmodifier $ (Morpher name:"Morpher")
								HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherPupilEffectArray
							)
						)
						if Part ==4 do
						(
							if selection[1].modifiers.count > 0 then
							(	
								if (classof (selection[1].modifiers[a])) == Morpher then
								(
									HsHExpressionToolCollection.ShiQuCollectMorpherInfoFN HsHExpressionToolCollection.TempShiQuMorpherInfo
									
									deleteModifier $ 1
									addmodifier $ (Morpher name:"Morpher")
									HsHExpressionToolCollection.HsHMorPickFN HsHExpressionToolCollection.MorpherEyeEffectArray
									HsHExpressionToolCollection.ShiQuFuZhiFN HsHExpressionToolCollection.TempShiQuMorpherInfo
								)
								else
								(
									addmodifier $ (Morpher name:"Morpher")
									HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherEyeEffectArray
								)
							)
							else
							(
								addmodifier $ (Morpher name:"Morpher")
								HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherEyeEffectArray
							)
						)
					)
				)
				
			)
			else
			(
				aaa = #()
				for i in selection do
				(
					append aaa i
					
				)
				print aaa
				for obj in aaa do
				(
					for Part in 1 to PartOfFacilArray.count do
					(
						if ((findstring obj.name PartOfFacilArray[Part]) as string) != "undefined" then
						(
							select obj
							if Part ==1 do
							(
								if obj.modifiers.count > 0 then
								(	
									if (classof (obj.modifiers[a])) == Morpher then
									(
										
										HsHExpressionToolCollection.ShiQuCollectMorpherInfoFN HsHExpressionToolCollection.TempShiQuMorpherInfo
										
										deleteModifier $ 1
										addmodifier $ (Morpher name:"Morpher")
										HsHExpressionToolCollection.HsHMorPickFN HsHExpressionToolCollection.morpher_target
										HsHExpressionToolCollection.ShiQuFuZhiFN HsHExpressionToolCollection.TempShiQuMorpherInfo
									)
									else
									(
										
										addmodifier $ (Morpher name:"Morpher")
										HsHExpressionToolCollection.HsHMorPickFN HsHExpressionToolCollection.morpher_target
									)
								)
								else
								(
									
									addmodifier $ (Morpher name:"Morpher")
									HsHExpressionToolCollection.HsHMorPickFN HsHExpressionToolCollection.morpher_target
								)
							)
							if Part ==2 do
							(
								if obj.modifiers.count > 0 then
								(	
									if (classof (obj.modifiers[a])) == Morpher then
									(
										HsHExpressionToolCollection.ShiQuCollectMorpherInfoFN HsHExpressionToolCollection.TempShiQuMorpherInfo
										
										deleteModifier $ 1
										addmodifier $ (Morpher name:"Morpher")
										HsHExpressionToolCollection.HsHMorPickFN   HsHExpressionToolCollection.MorpherPupilArray
										HsHExpressionToolCollection.ShiQuFuZhiFN HsHExpressionToolCollection.TempShiQuMorpherInfo
									)
									else
									(
										addmodifier $ (Morpher name:"Morpher")
										HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherPupilArray
									)
								)
								else
								(
									addmodifier $ (Morpher name:"Morpher")
									HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherPupilArray
								)
							)
							if Part ==3 do
							(
								if obj.modifiers.count > 0 then
								(	
									if (classof obj.modifiers[a]) == Morpher then
									(
										HsHExpressionToolCollection.ShiQuCollectMorpherInfoFN HsHExpressionToolCollection.TempShiQuMorpherInfo
									
										deleteModifier $ 1
										addmodifier $ (Morpher name:"Morpher")
										HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherPupilEffectArray
										HsHExpressionToolCollection.ShiQuFuZhiFN HsHExpressionToolCollection.TempShiQuMorpherInfo
									)
									else
									(
										addmodifier $ (Morpher name:"Morpher")
										HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherPupilEffectArray
									)
								)
								else
								(
									addmodifier $ (Morpher name:"Morpher")
									HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherPupilEffectArray
								)
							)	
						
							if Part ==4 do
							(
								if obj.modifiers.count > 0 then
								(	
									if (classof obj.modifiers[a]) == Morpher then
									(
										HsHExpressionToolCollection.ShiQuCollectMorpherInfoFN HsHExpressionToolCollection.TempShiQuMorpherInfo
										
										deleteModifier $ 1
										addmodifier $ (Morpher name:"Morpher")
										HsHExpressionToolCollection.HsHMorPickFN HsHExpressionToolCollection.MorpherEyeEffectArray
										HsHExpressionToolCollection.ShiQuFuZhiFN HsHExpressionToolCollection.TempShiQuMorpherInfo
									)
									else
									(
										addmodifier $ (Morpher name:"Morpher")
										HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherEyeEffectArray
									)
								)
								else
								(
									addmodifier $ (Morpher name:"Morpher")
									HsHExpressionToolCollection.HsHMorPickFN  HsHExpressionToolCollection.MorpherEyeEffectArray
								)
							)
						)	
					)
				)
			)
		)
		else
		(
			messagebox "没有选中物体"
		)
		
	)
	on DemandButt pressed do
	(
		
		rollout FacialAnimationTool "表情动画编辑工具" width:980 height:439
		(
			
	
	
			button refurbish "刷新" pos:[210,35] width:85 height:17
	
	
			button pick_tex_path "表情图片路径:" pos:[12,12] width:85 height:16
	
	
			edittext tex_path "" pos:[94,12] width:252 height:16
	
	
			GroupBox grp1 "基本表情." pos:[3,57] width:973 height:372
	
	
			spinner morpher_count "morpher数量" pos:[88,34] width:116 height:16 range:[10,50,20] type:#integer
			dropdownList animte_name "动画名称" pos:[835,16] width:133 height:41
			button xaf_export "表情动画导出" pos:[713,34] width:105 height:20
			edittext animate_name_ET "输出动画名称" pos:[540,34] width:169 height:21 enabled:true
			
			spinner spn3 "声音偏移" pos:[353,35] width:104 height:16 range:[-50,10000,0]
			
			
			
	
			bitmap bmp1 "Bitmap" pos:[10,74] width:80 height:80 
	 
	 
	 
	 
			button btn1 "xi" pos:[10,163] width:73 height:16 
	 
	 
	 
	 
	 
	 
		 
		 
		 
			
	
			bitmap bmp2 "Bitmap" pos:[115,74] width:80 height:80
			button btn2 "xi" pos:[115,163] width:73 height:16 
	 
	 
	 
	 
	 
	 
		 
		 
		 
			
	
			button btn3 "xi" pos:[212,163] width:73 height:16
			bitmap bmp3 "Bitmap" pos:[212,74] width:80 height:80
			
	
	
	
			button btn4 "xi" pos:[300,163] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp4 "Bitmap" pos:[300,74] width:80 height:80
			
	
	
	
			button btn5 "xi" pos:[394,163] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp5 "Bitmap" pos:[394,74] width:80 height:80
			
	
			
			
			button btn6 "xi" pos:[495,163] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp6 "Bitmap" pos:[495,74] width:80 height:80
			
	
			
			
			button btn7 "xi" pos:[590,163] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp7 "Bitmap" pos:[590,74] width:80 height:80
			
	
	
	
	
			button btn8 "xi" pos:[680,163] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp8 "Bitmap" pos:[680,74] width:80 height:80
			
	
	
			button btn9 "xi" pos:[785,163] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp9 "Bitmap" pos:[785,74] width:80 height:80
			
	
			button btn10 "xi" pos:[880,163] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp10 "Bitmap" pos:[880,74] width:80 height:80
			
	
			button btn11 "xi" pos:[10,280] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp11 "Bitmap" pos:[10,190] width:80 height:80
			
	
			button btn12 "xi" pos:[115,280] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp12 "Bitmap" pos:[115,190] width:80 height:80
			
	
			button btn13 "xi" pos:[212,280] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp13 "Bitmap" pos:[212,190] width:80 height:80
			
	
			button btn14 "xi" pos:[300,280] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp14 "Bitmap" pos:[300,190] width:80 height:80
			
	
			button btn15 "xi" pos:[394,280] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp15 "Bitmap" pos:[394,190] width:80 height:80
			
	
			button btn16 "xi" pos:[495,280] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp16 "Bitmap" pos:[495,190] width:80 height:80
			
	
			button btn17 "xi" pos:[590,280] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp17 "Bitmap" pos:[590,190] width:80 height:80
			
	
			button btn18 "xi" pos:[680,280] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp18 "Bitmap" pos:[680,190] width:80 height:80
			
	
			button btn19 "xi" pos:[785,280] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp19 "Bitmap" pos:[785,190] width:80 height:80
			
	
			button btn20 "xi" pos:[880,280] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp20 "Bitmap" pos:[880,190] width:80 height:80
			
	
			button btn21 "xi" pos:[10,399] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp21 "Bitmap" pos:[10,312] width:80 height:80
			
	
			button btn22 "xi" pos:[115,399] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp22 "Bitmap" pos:[115,312] width:80 height:80
			
	
			button btn23 "xi" pos:[212,399] width:73 height:16 
	 
	 
	 
	 
			bitmap bmp23 "Bitmap" pos:[212,312] width:80 height:80
			
			button btn24 "xi" pos:[299,399] width:73 height:16
			bitmap bmp24 "Bitmap" pos:[300,312] width:80 height:80
			button btn25 "xi" pos:[390,399] width:73 height:16
			bitmap bmp25 "Bitmap" pos:[390,312] width:80 height:80
			button btn26 "xi" pos:[485,400] width:73 height:16
			bitmap bmp26 "Bitmap" pos:[485,313] width:80 height:80
			button btn27 "xi" pos:[580,401] width:73 height:16
			bitmap bmp27 "Bitmap" pos:[580,314] width:80 height:80
			
			
			
			
			
			
	
			
			
			
			local	mingcheng = #("main" ,"close_right","close_left","close_down","close_up","smiled" ,"anger" ,"sad","smug","pain","shy",
				"shock","doubt","grievance","serious","calm","nifty","tsukomi","panic","frustration","squint","special_001",
				"special_002","special_003","special_004","special_005","special_006","special_007","special_008","special_009","special_010","special_011")
			local xuqiuwuti = #()
			--channel_ID = #()
	
			local anniu_shuzhu = #()
			
			
			local TempMorpherArray = #()
			
				
			
				
				
			
			
			
			
			
			
			
			
			fn export_bip_fn animate_S path_S=
			(
				bip_path_S = path_S +"\\bip\\"  + animate_S + ".bip"			
				select $Bip001
				
				biped.saveBipFile $.controller bip_path_S
			)
			
			
			
			
			
					
			
			
			
				
			
			
			
			
			fn btn_name =
			(
				--给按钮赋予名称
				local idx =0
				for b in FacialAnimationTool.controls do
				(
					
					a = (findString b.name "btn") as string
					
					
					if  a == "1"  do
					(
		--				
						
						idx += 1
						
						b.caption = mingcheng[idx]
					)
					
				)
			)
			fn map_name path_name=
			(
			--给图片赋予名称	
				
				local idx_map =0
				for b_map in FacialAnimationTool.controls do
				(
					
					a_map = (findString b_map.name "bmp") as string
					
					
					if  a_map == "1"  do
					(
						b_map.fileName="D:\\temp.png"
						idx_map += 1
						
						a_path_s = path_name + mingcheng[idx_map] +".png"
						if_s = openBitMap a_path_s
						if if_s != "undefined" then
						(
							b_map.fileName = a_path_s
						)
						else
						(
							
							b_map.fileName="D:\\temp.png"
											
							--	print "成功了"
						--	---b_map.bitmap = color:blue 
						)
						--bmp_chushi = openbitmap b_map.fileName
						--bmp_target = bitmap 80 80
						--copy bmp_chushi bmp_target
						--b_map.fileName=null
					)	
				)
			)
			
			
			
			
			
			
			fn target_morpher =
			(
				--选中物体名称在mingcheng数组内的模型，并且存储在xuqiuwuti内的物体名称和物体
				for obj in geometry do
				(
					if (findItem mingcheng obj.name) >0 do
					(
						
						append xuqiuwuti #(obj.name ,obj )
					)
				)
			)
			
			
			
			
			
			
			
			
			
			fn anniumingming =
			--看这个函数的名字已经不需要解释了吧
			(
				local idx =0
				for b in FacialAnimationTool.controls do
				(
					a = (findString b.name "btn") as string
					if  a == "1"  do
					(			
						
						idx += 1
						print idx
						b.caption = mingcheng[idx]
					)		
				)				
			)
			
			
			
			fn bitmap_fuzhi =
			--拾取图片的路径
			(
	
				bmp1.fileName = "main.png"	
			)
			fn reset_morpher =
			--morpher权重归零
			(
				clearSelection()
				if selection.count ==0 then
				(
					select $*Body_H_001 
					if selection.count ==1 do
					(
						animate on
						(
							for i in 6 to morpher_count.value do
							(	
								at time sliderTime (WM3_MC_SetValue $.morpher i 0.0)
							)	
						)
					)
					if selection.count ==0 do
					(
						
						messageBox"没有该物体"
					)
					if selection.count >1 do
					(
						
						messageBox"有物体重名"
					)
				)
				else
				(
					max spacebar
					select $*Body_H_001 
					if selection.count ==1 do
					(
						animate on
						(
							for i in 6 to morpher_count.value do
								at time sliderTime (WM3_MC_SetValue $.morpher i 0.0)
						)
					)
					if selection.count ==0 do
					(
						
						messageBox"没有该物体"
					)
					if selection.count >1 do
					(
						
						messageBox"有物体重名"
					)
					
				)
			)
			fn select_target_morpher  obj_name= 
			--jishu函数为获取组合morpher通道和权重
			(
				clearSelection()
				--创建临时数据，存储目标表情模型的morpher通道和权重信息
				for mu_obj in 1 to xuqiuwuti.count do
				(
					if 	obj_name == xuqiuwuti[mu_obj][1] then
					(
						select xuqiuwuti[mu_obj][2]
					)
	
				)
				--通过按钮传入的命名字符串，找到目标表情模型，并且选中
		
			)
			
	
			
			fn set_animate M_count= 
			(
				
				if selection.count == 1 then
				(
					local channel_ID = #()	
					for i in 1 to M_count do
					(
					--得到选中的模型上所有的morpher信息
						if (WM3_MC_GetValue $.modifiers[1] i) > 0 and (WM3_MC_GetValue $.modifiers[1] i) != false do 
						--取选中模型 morpher值大于0的通道
						(	
							append channel_ID #(i ,(WM3_MC_GetValue $.modifiers[1] i))
									
							--存储当前选中模型的数据为数组的一个元素
						)
					)
					
					if channel_ID.count > 0 do
					(
						select $*Body_H_001
						animate on
						(
							for k in 1 to channel_ID.count do
								at time sliderTime (WM3_MC_SetValue $.modifiers[2] channel_ID[k][1] channel_ID[k][2])
						)	
					)	
					
				)
				else
				(
					
					messageBox "没有这个目标morpher"	
				)
				
			)
			
			
			--一些公用的方法
			fn if_sel_fn fn_constom obj= 
			(
				clearSelection()
				select $*Body_H_001 
				if selection.count ==1 do
				(
					fn_constom
				)
				if selection.count ==0 do
				(
					
					messageBox"没有该物体"
				)
				if selection.count >1 do
				(
					
					messageBox"有物体重名"
				)		
			)
			--暂时没有用开始
			fn morpher_set_fn =
			(
				animate on
					(
						for i in 1 to morpher_count.value do
							at time sliderTime (WM3_MC_SetValue $.morpher i 0.0)
					)
			)
			--暂时没有用结束
			
			----公用方法结束
			fn jihe_fn M_value bnt_name= 
			(
				reset_morpher()
				select_target_morpher bnt_name
				set_animate M_value		
			)
	
			
			
			
			
			
	
			
			
			on FacialAnimationTool open do
			(
				
				HsHExpressionToolCollection.CollectMorpherInfoFN TempMorpherArray
				morpher_count.value = TempMorpherArray.count
				TempMorpherArray =  #()
				prosound.init true
				animte_name.items = HsHExpressionToolCollection.animate_names
				btn_name()
				map_name tex_path.text
				target_morpher()
				
			)
			on refurbish pressed do
			(
				HsHExpressionToolCollection.CollectMorpherInfoFN TempMorpherArray
				morpher_count.value = TempMorpherArray.count
				TempMorpherArray =  #()
				xuqiuwuti = #()
				btn_name()
				map_name tex_path.text
				target_morpher()	
			
			
			)
			on pick_tex_path pressed do
			(	
				--指定图片集的路径
				--a = getOpenFileName types:".wav"
				a = getSavePath()
				if a ==null then
					messageBox "请选择路径"
				else
				(	
					b = a +"\\"
					tex_path.text = b
					map_name tex_path.text
					--sound_Arr =#()
					--sound_Arr = getfiles "*.wav"
					--print sound_Arr	
				)
			)
			on spn3 changed val do
			(
				HsHExpressionToolCollection.sound_start_fn spn3.value
			)
			on morpher_count changed value do
			(
				xuqiuwuti = #()
				btn_name()
				map_name tex_path.text
				target_morpher()
			)
			on animte_name selected sel do
			(
				
				a =animte_name.items[sel]
				animate_name_ET.text = a
				
				HsHExpressionToolCollection.import_bip_sound_fn a tex_path
				HsHExpressionToolCollection.import_xaf_fn  animate_name_ET.text  tex_path.text morpher_count.value
			
			)
			on xaf_export pressed do
			(
				
				HsHExpressionToolCollection.export_facialFbx_fn animate_name_ET.text  tex_path.text
				HsHExpressionToolCollection.export_xaf_fn animate_name_ET.text  tex_path.text
			)
			on animate_name_ET entered text do
			(
				HsHExpressionToolCollection.import_bip_sound_fn animate_name_ET.text tex_path
				HsHExpressionToolCollection.import_xaf_fn  animate_name_ET.text  tex_path.text morpher_count.value
			)
			on btn1 pressed do
			(
				reset_morpher()
			)
			on btn2 pressed do
			(
			
				jihe_fn morpher_count.value btn2.caption
			
			)
			on btn3 pressed do
			(
				jihe_fn morpher_count.value btn3.caption
			)
			on btn4 pressed do
			(
				jihe_fn morpher_count.value btn4.caption
				
			)
			on btn5 pressed do
			(
			
				jihe_fn morpher_count.value btn5.caption
			
			)
			on btn6 pressed do
			(
			
				jihe_fn morpher_count.value btn6.caption
			
			)
			on btn7 pressed do
			(
			
				jihe_fn morpher_count.value btn7.caption
			)
			on btn8 pressed do
			(
				jihe_fn morpher_count.value btn8.caption
			)
			on btn9 pressed do
			(
				jihe_fn morpher_count.value btn9.caption
			)
			on btn10 pressed do
			(
				jihe_fn morpher_count.value btn10.caption
			)
			on btn11 pressed do
			(
				jihe_fn morpher_count.value btn11.caption
			)
			on btn12 pressed do
			(
				jihe_fn morpher_count.value btn12.caption
			)
			on btn13 pressed do
			(
				jihe_fn morpher_count.value btn13.caption
			)
			on btn14 pressed do
			(
				jihe_fn morpher_count.value btn14.caption
			)
			on btn15 pressed do
			(
			
				jihe_fn morpher_count.value btn15.caption
			
			)
			on btn16 pressed do
			(
				jihe_fn morpher_count.value btn16.caption
			)
			on btn17 pressed do
			(
				jihe_fn morpher_count.value btn17.caption
			
			)
			on btn18 pressed do
			(
				jihe_fn morpher_count.value btn18.caption
			
			)
			on btn19 pressed do
			(
				jihe_fn morpher_count.value btn19.caption
			
			)
			on btn20 pressed do
			(
			
				jihe_fn morpher_count.value btn20.caption
			)
			on btn21 pressed do
			(
				jihe_fn morpher_count.value btn21.caption
			)
			on btn22 pressed do
			(
				jihe_fn morpher_count.value btn22.caption
			
			)
			on btn23 pressed do
			(
			
				jihe_fn morpher_count.value btn23.caption
			
			)
			on btn24 pressed do
			(
			
				jihe_fn morpher_count.value btn24.caption
			
			)
			on btn25 pressed do
			(
			
				jihe_fn morpher_count.value btn25.caption
			
			)
			on btn26 pressed do
			(
			
				jihe_fn morpher_count.value btn26.caption
			
			)
			on btn27 pressed do
			(
			
				jihe_fn morpher_count.value btn27.caption
			
			)
	
		)
		createDialog FacialAnimationTool
	
	
	
	
	
		
	)
	on KFacilAnimateBTN pressed do
	(
		fff = newRolloutFloater "fdkaslfkdalfklakfa" 975 800
		rollout FacialAnimationMakingDetailsTool "动画调整工具" width:976 height:613
		(
			GroupBox 'grp1' "眉毛" pos:[8,62] width:474 height:201 align:#left
			GroupBox 'grp2' "眉毛样式" pos:[11,80] width:461 height:45 align:#left
			button 'ButtEyebrowStyle01' "Button" pos:[27,100] width:82 height:20 align:#left
			button 'ButtEyebrowStyle02' "Button" pos:[116,99] width:82 height:20 align:#left
			button 'ButtEyebrowStyle03' "Button" pos:[205,99] width:82 height:20 align:#left
			button 'ButtEyebrowStyle04' "Button" pos:[295,98] width:82 height:20 align:#left
			--button 'ButtEyebrowStyle05' "Button" pos:[384,97] width:82 height:20 align:#left
			GroupBox 'grp3' "细调" pos:[12,133] width:460 height:121 align:#left
			
			GroupBox 'grp4' "眼部" pos:[3,270] width:474 height:333 align:#left
			GroupBox 'grp5' "瞳孔方向" pos:[11,422] width:461 height:103 align:#left
			GroupBox 'grp6' "细调" pos:[12,527] width:460 height:68 align:#left
			slider 'SldPupilDirWeight' "位置权重" pos:[142,543] width:100 height:44 range:[0,100,0] align:#left
			dropdownList 'DDPupilDirs' "瞳孔位置" pos:[22,546] width:118 height:41 align:#left
			
			button 'BtnPupilDir' "正常" pos:[275,463] width:82 height:20 align:#left
			button 'BtnPupilDir01' "上" pos:[274,439] width:82 height:20 align:#left
			button 'BtnPupilDir02' "下" pos:[274,490] width:82 height:20 align:#left
			button 'BtnPupilDir03' "左" pos:[182,464] width:82 height:20 align:#left
			button 'BtnPupilDir04' "右" pos:[365,464] width:82 height:20 align:#left
			button 'BtnPupilDir05' "左上" pos:[181,439] width:82 height:20 align:#left
			button 'BtnPupilDir06' "右上" pos:[365,438] width:82 height:20 align:#left
			button 'BtnPupilDir07' "左下" pos:[182,491] width:82 height:20 align:#left
			button 'BtnPupilDir08' "右下" pos:[365,490] width:82 height:20 align:#left
			
			
			radiobuttons 'RdoPupilSync' "眼睛同步" pos:[23,441] width:51 height:46 labels:#("开启", "关闭") default:1 columns:1 align:#left
			radiobuttons 'RdoPupilRandL' "眼睛方向" pos:[90,440] width:51 height:46 labels:#("左眼", "右眼") default:1 columns:1 align:#left
			GroupBox 'grp19' "口型" pos:[493,63] width:474 height:200 align:#left
			GroupBox 'grp20' "口型样式" pos:[500,80] width:461 height:45 align:#left
			button 'BtnMouthStyle01' "Button" pos:[542,98] width:53 height:20 align:#left
			button 'BtnMouthStyle02' "Button" pos:[609,98] width:53 height:20 align:#left
			button 'BtnMouthStyle03' "Button" pos:[672,97] width:53 height:20 align:#left
			button 'BtnMouthStyle04' "Button" pos:[736,97] width:53 height:20 align:#left
			button 'BtnMouthStyle05' "Button" pos:[803,97] width:53 height:20 align:#left
			button 'BtnMouthStyle06' "Button" pos:[872,96] width:53 height:20 align:#left
			GroupBox 'grp21' "细调" pos:[500,129] width:460 height:118 align:#left
			slider 'DDMouthAddStylesWeight' "叠加权重调整" pos:[637,140] width:119 height:44 range:[0,100,0] align:#left
			dropdownList 'DDMouthAddStyles' "情绪叠加" pos:[510,147] width:118 height:41 align:#left
			
			
			dropdownList 'DDButtEyebrowStyles' "眉毛方位" pos:[21,153] width:118 height:41 align:#left
			spinner 'SpnPupilDirWeight' "权重值" pos:[35,496] width:98 height:16 align:#left
			dropdownList 'DDMouthStyles' "口型" pos:[509,194] width:118 height:41 align:#left
			slider 'DDMouthStylesWeight' "口型调整" pos:[637,190] width:119 height:44 range:[0,100,0] align:#left
			GroupBox 'grp26' "眼皮样式" pos:[10,327] width:461 height:91 align:#left
			button 'ButtEyeStyle01' "Button" pos:[24,343] width:82 height:20 align:#left
			button 'ButtEyeStyle02' "Button" pos:[113,342] width:82 height:20 align:#left
			button 'ButtEyeStyle03' "Button" pos:[202,342] width:82 height:20 align:#left
			button 'ButtEyeStyle04' "Button" pos:[292,341] width:82 height:20 align:#left
			button 'ButtEyeStyle05' "Button" pos:[381,340] width:82 height:20 align:#left
			dropdownList 'DDButtEyeStyles' "眼皮" pos:[21,371] width:102 height:41 align:#left
			slider 'DDButtEyeStylesWeight' "眼皮权重值" pos:[125,367] width:115 height:44 range:[0,100,0] align:#left
			--radiobuttons 'RDOPupilLinkEye' "瞳孔眼皮关联" pos:[21,288] width:106 height:30 labels:#("同步", "异步") columns:2 align:#left
			
			
			
			
			
			slider 'DDButtEyebrowStylesWeight' "眉毛方位权重" pos:[140,149] width:118 height:44 range:[0,100,0] align:#left
			dropdownList 'DDEyeEffectControlWay' "特殊眼皮" pos:[246,368] width:102 height:41 align:#left
			slider 'DDEyeEffectControlWeight' "特殊眼皮权重" pos:[351,365] width:111 height:44 range:[0,100,0] align:#left
			dropdownList 'DDPupilEffectControl' "瞳孔特效" pos:[239,545] width:118 height:41 align:#left
			slider 'DDPupilEffectControlWeight' "位置权重" pos:[358,541] width:109 height:44 range:[0,100,0] align:#left
			button 'ProjectPathBTN' "工程路径" pos:[7,8] width:63 height:18 align:#left
			edittext 'ProjectPathEDT' "" pos:[71,7] width:153 height:18 align:#left
			spinner 'WavOffsetSPN' "声音偏移" pos:[203,31] width:65 height:16 align:#left
			edittext 'AnimateNameEDT' "动画名称" pos:[358,32] width:152 height:16 align:#left
			button 'ExportFacilAnimateBTN' "表情动画导出" pos:[521,29] width:97 height:22 align:#left
			dropdownList 'AnimateNameDDL' "动画名称" pos:[629,9] width:111 height:41 align:#left
			spinner 'MorpherUseableNumSPN' "Morpher数量" pos:[28,33] width:64 height:16 type:#integer align:#left
			button 'ImportMouthXafBTN' "声音导入" pos:[746,28] width:93 height:24 align:#left
			button 'StandBTN' "站立" pos:[851,2] width:83 height:22 align:#left
			button 'SailingBTN' "航行" pos:[851,29] width:83 height:22 align:#left
			
			
			
			
			--眼皮
			--dropdownList ddl5 "特殊效果" pos:[21,144] width:118 height:41
			
			
			
			--特殊效果的模块
			GroupBox 'grp22' "特殊效果" pos:[493,315] width:474 height:289 align:#left
			spinner 'SPNPupilEffectTexID' "瞳孔图片ID" pos:[509,365] width:59 height:16 type:#integer align:#left
			spinner 'spnEyeEffectTexID' "眼睛图片ID" pos:[509,389] width:59 height:16 range:[0,100,0] type:#integer align:#left
			slider 'SLDFlushRedIntensity' "红晕明显程度调整" pos:[509,474] width:153 height:44 align:#left
			slider 'SLDFlushBlackIntensity' "黑脸明显程度调整" pos:[510,527] width:153 height:44 range:[0,100,0] align:#left
			colorPicker 'CPFlushRedColor' "红晕颜色" pos:[667,490] width:125 height:22 color:(color 0 0 155) align:#left
			colorPicker 'CPFlushBlackColor' "黑脸颜色" pos:[667,542] width:126 height:22 color:(color 0 0 155) align:#left
			slider 'SLDFlushBlackRange' "红晕黑脸的范围" pos:[509,425] width:153 height:44 range:[0,100,0] align:#left
			checkbox 'CHKFlushState' "是否开启红晕" pos:[508,336] width:94 height:21 align:#left
			
			--GroupBox 'XUQIU' "备份需求" pos:[11,620] width:955 height:60 align:#left
			button 'RefurbishBtn' "刷新" pos:[242,6] width:80 height:21 align:#left
			
			
			
			
			
			
			
			
			local CommonStandStyleArray =#(#("正常"),
											#("制作区规则",
												#("标准区表情共用命名",
													#(
														#("高兴","smiled"),
														#("怒","anger"),
														#("哀","sad"),
														#("得意","smug"),
														#("痛苦","pain"),
														#("害羞","shy"),
														#("认真","serious"),
														#("吃惊","shock"),
														#("疑问","doubt"),
														#("伤心","grievance"),
														#("平静","calm"),
														#("俏皮","nifty"),
														#("吐槽","tsukomi"),
														#("慌张","panic"),
														#("自信","confidence"),
														#("委屈","frustration"),
														#("眯眼","squint"),
														#("无奈","helpless")
														---#("特殊区","special")
													)
												),
												#("脸的方位",
													#(
														#("左","Right"),
														#("右","Left")
													)	
												),
												#("脸的部位",
													#(
														#("嘴巴","Mouth"),
														#("眼睛","Eye"),
														#("眉毛","Eyebrow"),
														#("瞳孔","Pupil"),
														#("特效","Effect")
													)	
												),
												#("部位方向",
													#(
														#("上","up"),
														#("下","down"),
														#("左","left"),
														#("右","right"),
														#("集中","gather")
													)	
												)
												
											),
											#("功能区",
												#("口型",
													#(
														#("A","sayLarge"),
														#("I","sayI"),
														#("U","saySmall"),
														#("E","sayE"),
														#("O","sayMedium")
													)	
												),
												#("眼睛",
													#(
														#("左闭眼","Right_Eye_close"),
														#("右闭眼","Left_Eye_close"),
														#("左微笑闭眼","Right_Eye_close_001"),
														#("右微笑闭眼","Left_Eye_close_001"),
														#("正常闭眼","Double_Eye_close"),
														#("微笑闭眼","Double_Eye_close_001"),
														#("特效备用","Eye_Effect")
													)	
												),
												#("眉毛",
													#(
														#("向上","Eyebrow_up"),
														#("向下","Eyebrow_down"),
														#("集中","Eyebrow_gather")
													)	
												),
												#("瞳孔",
													#("左瞳孔",
														#(
															#("上","Right_Pupil_up"),	
															#("下","Right_Pupil_down"),
															#("左","Right_Pupil_right"),
															#("右","Right_Pupil_left"),
															#("缩小","Right_Pupil_scale"),
															#("消失","Right_Pupil_appear")
														)
													),
													#("右瞳孔",
														#(
															#("上","Left_Pupil_up"),	
															#("下","Left_Pupil_down"),
															#("左","Left_Pupil_right"),
															#("右","Left_Pupil_left"),
															#("缩小","Left_Pupil_scale"),
															#("消失","Left_Pupil_appear")															
														)
													)
													--#("消失","Pupil_appear")
												),
												#("特效",
													
													#("瞳孔",
														#("方位",
															#("左特效",
																#(
																	#("上","Right_Effect_Pupil_up"),	
																	#("下","Right_Effect_Pupil_down"),	
																	#("左","Right_Effect_Pupil_right"),
																	#("右","Right_Effect_Pupil_left"),
																	#("缩小","Right_Effect_Pupil_scale"),
																	#("出现","Right_Effect_Pupil_appear")
																)		
															),
															#("右特效",
																#(
																	#("上","Left_Effect_Pupil_up"),	
																	#("下","Left_Effect_Pupil_down"),	
																	#("左","Left_Effect_Pupil_right"),
																	#("右","Left_Effect_Pupil_left"),
																	#("缩小","Left_Effect_Pupil_scale"),
																	#("出现","Left_Effect_Pupil_appear")
																)		
															)
														),
														#("平行出现","Effect_Pupil_appear_symmetry"),
														#("对称出现","Effect_Pupil_appear_parallel")
													),
													#("特殊眼睛",
														#(
															#("平行出现","Effect_Eye_appear_symmetry"),
															#("对称出现","Effect_Eye_appear_parallel")	
														)
													)
												)	
											),
											#("KEN叔区",
												#("口型",
													#(
														#("k微笑","Mouth_special_011"),
														#("k怒","Mouth_special_012"),
														#("k闭嘴（下弯）","Mouth_special_013"),
														#("k笑容（白齿）","Mouth_special_014")
													)	
												),
												#("眼睛",
													#(
														#("k生气","Eye_special_011"),
														#("k张眼（惊）","Eye_special_012"),
														#("k半目","Eye_special_013"),
														#("k闭眼（无奈）","Eye_special_014")
														
													)	
												),
												#("眉毛",
													#(
														#("k高兴","Eyebrow_special_011"),
														#("k怒","Eyebrow_special_012"),
														#("k困惑","Eyebrow_special_013"),
														#("k认真","Eyebrow_special_014")
													)	
												)
											)
										)
				
				
			local EyeCloseMorpherName = #("Double_Eye_close","Double_Eye_close_001","Eye_special_014")	
			local RightEyeCloseMorpherName = #("Right_Eye_close","Right_Eye_close_001")
			local LeftEyeCloseMorpherName = #("Left_Eye_close","Left_Eye_close_001")
			--数组的备注，查询这里即可
			--(
				--CommonStandStyleArray[2][2][2]   表情命名规则数组
				--CommonStandStyleArray[2][3][2]   脸的左右命名
				--CommonStandStyleArray[2][4][2]   脸的部分命名
				--CommonStandStyleArray[2][5][2]   方向命名
				--CommonStandStyleArray[2][6]      特殊区命名的头部
					
					
				--CommonStandStyleArray[3][2][2]	  功能区口型命名
				--CommonStandStyleArray[3][3][2]	  功能区眼睛命名
				--CommonStandStyleArray[3][4][2]	  功能区眉毛方向命名
				--CommonStandStyleArray[3][5][2]	  功能区瞳孔命名
				--CommonStandStyleArray[3][6][2][2][2][2]  功能区左边瞳孔上的叠加特效命名
				--CommonStandStyleArray[3][6][2][2][3][2]  功能区右边瞳孔上的叠加特效命名
				--CommonStandStyleArray[3][6][2][3]        功能区瞳孔上的叠加特效消失命名
				
				--CommonStandStyleArray[3][6][3][2][1]	功能区特殊眼睛消失命名
				--CommonStandStyleArray[3][6][3][2][2]	功能区特殊眼睛大小命名
			--)
			
			
			--收集UI按钮的预备数组
			local tempEyebrowUIControlsArray = #()
			local tempEyeUIControlsArray = #()
			local tempPupilUIControlsArray = #()
			local tempMouthUIControlsArray = #()
			--收集UI按钮的预备数组
			
			--
			local EyebrowAfterDelArray = #()
			local EyeAfterDelArray = #()
			local PupilAfterDelArray = #()
			local MouthAfterDelArray = #()
			local PupilEffectAfterDelArray = #()
			local EyeEffectAfterDelArray = #()
	
			
			
			fn RDOPupilLinkEyeFN CoustomValue MorpherNameString WeightValue= 
			(
				if RDOPupilLinkEye.state == 2 then
				(
					exit
				)
				else
				(	
					for i in EyeCloseMorpherName do
					(
						if i == MorpherNameString then
						(
							select $*Eye_001
							WM3_MC_SetValue $.modifiers[#Morpher] 6 (CoustomValue*WeightValue)
							WM3_MC_SetValue $.modifiers[#Morpher] 12 (CoustomValue*WeightValue)
							clearSelection()
							select $*Pupil_Effect_001
							if selection.count == 1 and ((WM3_MC_GetValue $.modifiers[#Morpher] 13) != 0) and ((WM3_MC_GetValue $.modifiers[#Morpher] 14) != 0) do
							(
								WM3_MC_SetValue $.modifiers[#Morpher] 6 (CoustomValue * WeightValue)
								WM3_MC_SetValue $.modifiers[#Morpher] 12 (CoustomValue * WeightValue)
							)
							exit
						)
						else
						(
							for i in  RightEyeCloseMorpherName do 
							(	
								if i == MorpherNameString then
								(
									select $*Eye_001
									WM3_MC_SetValue $.modifiers[#Morpher] 6 (CoustomValue*WeightValue)
									clearSelection()
									select $*Pupil_Effect_001
									if selection.count == 1 and ((WM3_MC_GetValue $.modifiers[#Morpher] 13) != 0) and ((WM3_MC_GetValue $.modifiers[#Morpher] 14) != 0) do
									(
										WM3_MC_SetValue $.modifiers[#Morpher] 6 (CoustomValue*WeightValue)
									)
									exit
								)
								else
								(
									for i in LeftEyeCloseMorpherName do
									(	
										if i == MorpherNameString do 
										(	
											select $*Eye_001
											WM3_MC_SetValue $.modifiers[#Morpher] 12 (CoustomValue*WeightValue)
											clearSelection()
											select $*Pupil_Effect_001
											if selection.count == 1 and ((WM3_MC_GetValue $.modifiers[#Morpher] 13) != 0) and ((WM3_MC_GetValue $.modifiers[#Morpher] 14) != 0) do
											(
												WM3_MC_SetValue $.modifiers[#Morpher] 12 (CoustomValue*WeightValue)
											)
											exit
										)
									)
								)
							)		
						)
					)
				)	
			)
			
			
			
			
			
			
			
			
			
			fn CollectUIControlsFN = 
			(
				for b in FacialAnimationMakingDetailsTool.controls do
				(
					a = (findString b.name "ButtEyebrowStyle") as string
					if  a == "1"  do
					(	
						append tempEyebrowUIControlsArray b
					)
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
				)
			)
			--通用UI命名
			fn MorpherMatchUIControlsFN ConstomUIArray ConstomMorpherArray ConstomValue =
			(	
				ConstomUIArray[1].caption = "正常"
				if (ConstomUIArray.count-1) <= (ConstomMorpherArray.count-ConstomValue) then
				(
					
					for i in 1 to (ConstomUIArray.count-1) do
					(
						local id_x = ConstomValue+i
						ConstomUIArray[(i+1)].caption = ConstomMorpherArray[id_x][1]
					)
				)
				else
				(
					messagebox "morpher数量不足支持该工具使用"	
				)
				
				
				
			)
			
			--通用UI命名
			fn ListArray ConstomUIDrpDown ConstomMorpherArray =
			(
				local aa = #()
				
				if ConstomMorpherArray.count>0 do
				(	
					for i in ConstomMorpherArray do
					(
						append aa  i[1]
					)
				)
				ConstomUIDrpDown.items = aa
			)
			
			fn PartAfterDelAddID AfterDelArray ConstomString= 
			(
				
				for h in 1 to 3 do 
				(		
					if CommonStandStyleArray[2][4][2][h][2] == ConstomString do
					(
						select $*Body_H_001
						if AfterDelArray.count >1 do 
						(
							for k in AfterDelArray do 
							(	
								for i in 1 to 60 do
								(
									if (WM3_MC_GetName $.modifiers[#Morpher] i) == k[2].name do
									(
										append k i
									)	
								)
							)
						)
					)	
				)	
				if "Pupil" == ConstomString do
				(
					select $*Eye_001
					if AfterDelArray.count >1 do 
					(
						for k in AfterDelArray do 
						(	
							for i in 1 to 60 do
							(
								if (WM3_MC_GetName $.modifiers[#Morpher] i) == k[2].name do
								(
									append k i
								)	
							)
						)
					)
				)	
						
						
				if "PupilEffect" == ConstomString do
				(
					select $*Pupil_Effect_001
					if AfterDelArray.count >1 do 
					(
						for k in AfterDelArray do 
						(	
							for i in 1 to 60 do
							(
								if (WM3_MC_GetName $.modifiers[#Morpher] i) == k[2].name do
								(
									append k i
								)	
							)
						)
					)
				)	
				
				if "EyeEffect" == ConstomString do
				(
					select $*Eye_Effect_001
					if AfterDelArray.count >1 do 
					(
						for k in AfterDelArray do 
						(	
							for i in 1 to 60 do
							(
								if (WM3_MC_GetName $.modifiers[#Morpher] i) == k[2].name do
								(
									append k i
								)	
							)
						)
					)
				)	
			)
	
			fn DDListFN DDConstomList ConstomArray=	
			(
					a = DDConstomList.selection
					--print  ConstomArray[a][3]
					return ConstomArray[a][3]	
	
			)
			
			
			
			--收集处理场景内的morpher数据
			--按照顺序收集场景内有关眉毛的部分
			fn EyebrowMatchMorpherArrayFN = 
			(
				--收集眉毛方向，以及命名
				for k in 1 to CommonStandStyleArray[2][5][2].count do
				(	
					tempmingzi = "Eyebrow_" + CommonStandStyleArray[2][5][2][k][2]
					for i in Geometry  do 
					(
						if i.name == tempmingzi do
						(
							append EyebrowAfterDelArray #(CommonStandStyleArray[2][5][2][k][1],i) 
						)	
					)		
				)
				--收集跟肯叔的眉毛需求，以及命名
				for k in 11 to 20 do
				(	
					tempmingzi = "Eyebrow_special_0" + (k as string)
					for i in Geometry  do 
					(
						if i.name == tempmingzi do
						(
							if k < 15 then
							(
								append EyebrowAfterDelArray #(CommonStandStyleArray[4][4][2][(k-10)][1],i) 
							)
							else
							(
								print (k-10)
								CoustomNameString = "K样式" + ((k-14) as string)
								append EyebrowAfterDelArray #(CoustomNameString,i) 
							)
						)	
					)		
				)
				--收集标准区跟眉毛有关的morpher
				for k in CommonStandStyleArray[2][2][2] do
				(
					tempmingzi = "Eyebrow_" + k[2]
					for i in Geometry do 
					(
						if i.name == tempmingzi do
						(
							append EyebrowAfterDelArray #(k[1],i)
						)	
					)
				)
				--收集特殊区的眉毛，已及命名
				for k in 1 to 9 do
				(	
					tempmingzi = "Eyebrow_special_00" + (k as string)
					for i in Geometry  do 
					(
						if i.name == tempmingzi do
						(
							CoustomNameString = "样式" + (k as string)
							append EyebrowAfterDelArray #(CoustomNameString,i) 
							
						)	
					)		
				)
				tempmingzi = "Eyebrow_special_0" + "10"
				for i in Geometry  do 
				(
					if i.name == tempmingzi do
					(
						CoustomNameString = "样式" + "10"
						append EyebrowAfterDelArray #(CoustomNameString,i) 
					)	
				)		
				MorpherMatchUIControlsFN tempEyebrowUIControlsArray EyebrowAfterDelArray 3
				ListArray DDButtEyebrowStyles EyebrowAfterDelArray
				PartAfterDelAddID EyebrowAfterDelArray "Eyebrow"
				--print EyebrowAfterDelArray
			)
			--按照顺序收集场景内有关眼皮的部分
			fn EyeMatchMorpherArrayFN = 
			(
				--收集肯叔需求的前两个
				for k in 1 to 2 do
				(
					for i in Geometry do 
					(
						--print CommonStandStyleArray[3][3][2][(k+4)][2]
						if i.name == CommonStandStyleArray[3][3][2][(k+4)][2] do
						(
							append EyeAfterDelArray #(CommonStandStyleArray[3][3][2][(k+4)][1],i) 
						)	
					)
				)
				--收集肯叔需求
				for k in 11 to 20 do
				(	
					tempmingzi = "Eye_special_0" + (k as string)
					for i in Geometry  do 
					(
						if i.name == tempmingzi do
						(
							if k < 15 then
							(
								append EyeAfterDelArray #(CommonStandStyleArray[4][3][2][(k-10)][1],i) 
							)
							else
							(
								--print (k-10)
								CoustomNameString = "K样式" + ((k-14) as string)
								append EyeAfterDelArray #(CoustomNameString,i) 
							)
						)	
					)		
				)
				
				--左右眼单闭得模型
				for k in 1 to 4 do
				(
					for i in Geometry do 
					(
						--print CommonStandStyleArray[3][3][2][(k+4)][2]
						if i.name == CommonStandStyleArray[3][3][2][k][2] do
						(
							append EyeAfterDelArray #(CommonStandStyleArray[3][3][2][k][1],i) 
						)	
					)
				)
				--收集标准区跟眼皮有关的morpher
				for k in CommonStandStyleArray[2][2][2] do
				(
					tempmingzi = "Eye_" + k[2]
					for i in Geometry do 
					(
						if i.name == tempmingzi do
						(
							append EyeAfterDelArray #(k[1],i)
						)	
					)
				)
				
				--收集特殊区的眼皮，已及命名
				for k in 1 to 9 do
				(	
					tempmingzi = "Eye_special_00" + (k as string)
					for i in Geometry  do 
					(
						if i.name == tempmingzi do
						(
							CoustomNameString = "样式" + (k as string)
							append EyeAfterDelArray #(CoustomNameString,i) 
							
						)	
					)		
				)
				tempmingzi = "Eye_special_0" + "10"
				for i in Geometry  do 
				(
					if i.name == tempmingzi do
					(
						CoustomNameString = "样式" + "10"
						append EyeAfterDelArray #(CoustomNameString,i) 
					)	
				)		
				
				
				---收集特效眼皮
					for i in Geometry  do 
					(
						a = toLower i.name
						b = toLower CommonStandStyleArray[3][3][2][7][2]
						if  a == b do
						(
							---messagebox "特效眼睛"
							append EyeAfterDelArray #(CommonStandStyleArray[3][3][2][7][1],i)
						)	
					)
				
				MorpherMatchUIControlsFN tempEyeUIControlsArray EyeAfterDelArray 0
				ListArray DDButtEyeStyles EyeAfterDelArray
				PartAfterDelAddID EyeAfterDelArray "Eye"
			)
			--按照顺序收集场景内有关瞳孔的部分
			fn PupilMatchMorpherArrayFN = 
			(
				--收集左瞳孔
				for k in CommonStandStyleArray[3][5][2][2] do 
				(	
					for i in Geometry do
					(
						if i.name == k[2] do
						(
							append PupilAfterDelArray #(k[1],i)
						)
					)			
				)
				--收集右瞳孔
				for k in CommonStandStyleArray[3][5][3][2] do 
				(	
					for i in Geometry do
					(
						if i.name == k[2] do
						(
							append PupilAfterDelArray #(k[1],i)
						)
					)			
				)
				
				local aa = #()
				--append aa "正常"
				if PupilAfterDelArray.count >10 do
				(
					for i in 1 to 6 do
					(
						append aa  PupilAfterDelArray[(i+6)][1]
					)
				)	
				DDPupilDirs.items = aa
				PartAfterDelAddID PupilAfterDelArray "Pupil"
				
			)	
			--按照顺序收集场景内有关口型的部分
			fn MouthMatchMorpherArrayFN = 
			(
				
				--五个元音口型
				for k in CommonStandStyleArray[3][2][2] do
				(
					
					for i in Geometry do 
					(
						a = toLower i.name
						b = toLower k[2]
						if a == b do
						(
							append MouthAfterDelArray #(k[1],i)
						)	
					)
				)
				
				--收集肯叔需求
				
				for k in 11 to 20 do
				(	
					tempmingzi = "Mouth_special_0" + (k as string)
					for i in Geometry  do 
					(
						if i.name == tempmingzi do
						(
							if k < 15 then
							(
								append MouthAfterDelArray #(CommonStandStyleArray[4][2][2][(k-10)][1],i) 
							)
							else
							(
								CoustomNameString = "K样式" + ((k-14) as string)
								append MouthAfterDelArray #(CoustomNameString,i) 
							)
						)	
					)		
				)
				--收集标准区跟嘴巴有关的morpher
				for k in CommonStandStyleArray[2][2][2] do
				(
					tempmingzi = "Mouth_" + k[2]
					for i in Geometry do 
					(
						if i.name == tempmingzi do
						(
							append MouthAfterDelArray #(k[1],i)
						)	
					)
				)
				--收集特殊区的眼皮，已及命名
				for k in 1 to 9 do
				(	
					tempmingzi = "Mouth_special_00" + (k as string)
					for i in Geometry  do 
					(
						if i.name == tempmingzi do
						(
							CoustomNameString = "样式" + (k as string)
							append MouthAfterDelArray #(CoustomNameString,i) 
							
						)	
					)		
				)
				tempmingzi = "Mouth_special_0" + "10"
				for i in Geometry  do 
				(
					if i.name == tempmingzi do
					(
						CoustomNameString = "样式" + "10"
						append MouthAfterDelArray #(CoustomNameString,i) 
					)	
				)
				
				MorpherMatchUIControlsFN tempMouthUIControlsArray MouthAfterDelArray 0
				local aa = #()
				for i in 1 to 3 do
				(
					append aa  MouthAfterDelArray[(5+i)][1]
				)
				DDMouthAddStyles.items = aa
				ListArray DDMouthStyles MouthAfterDelArray
				PartAfterDelAddID MouthAfterDelArray "Mouth"
			)
			--按照顺序收集场景内有关瞳孔特效的部分
			fn PupilEffectMatchMorpherArrayFN =
			(
				--收集左边瞳孔特效
				for k in CommonStandStyleArray[3][6][2][2][2][2] do 
				(	
					
					for i in Geometry do 
					(
						a = toLower i.name
						b = toLower k[2]
						if a == b do
						(
							--print "左边"
							append PupilEffectAfterDelArray #(k[1],i)
						)	
					)
				)
				--收集右边瞳孔特效
				for k in CommonStandStyleArray[3][6][2][2][3][2] do 
				(	
					
					for i in Geometry do 
					(
						a = toLower i.name
						b = toLower k[2]
						if a == b do
						(
							--print "右边"
							append PupilEffectAfterDelArray #(k[1],i)
						)	
					)
				)
				
				
					
				for i in Geometry do 
				(
					a = toLower i.name
					b = toLower "Effect_Pupil_appear_symmetry"
					if a == b do
					(
						append PupilEffectAfterDelArray #("对称出现",i)
					)	
				)
				for i in Geometry do 
				(
					a = toLower i.name
					b = toLower "Effect_Pupil_appear_parallel"
					if a == b do
					(
						append PupilEffectAfterDelArray #("平行出现",i)
					)	
				)
				local aa = #()
				for i in 13 to PupilEffectAfterDelArray.count do
				(
					append aa PupilEffectAfterDelArray[i][1]
				)
				DDPupilEffectControl.items = aa
				PartAfterDelAddID PupilEffectAfterDelArray "PupilEffect"
			)
			----按照顺序收集场景内有关眼睛特效的部分
			
			fn EyeEffectMatchMorpherArrayFN =
			(
				for k in CommonStandStyleArray[3][6][3][2]  do 
				(	
					
					for i in Geometry do 
					(
						
						a = toLower i.name
						b = toLower k[2]
						if a == b do
						(
							append EyeEffectAfterDelArray #(k[1],i)
						)	
					)
				)
				PartAfterDelAddID EyeEffectAfterDelArray "EyeEffect"
				local aa = #()
				for i in EyeEffectAfterDelArray do
				(
					append aa i[1]
				)
				DDEyeEffectControlWay.items = aa
			)
			
			
			
			
	
			
			--收集处理场景内的morpher数据
			
			--fn CollectMorpherInfoFN ConstomArray=
			--(
			--	select $*Body_H_001
				
			--	for i in 1 to 60 do
			--	(	
			--		if (WM3_MC_HasData $.modifiers[#Morpher] i) == true doe
			--		(	
			--			--MorpherCount+=1
			--			append ConstomArray #((WM3_MC_GetName $.modifiers[#Morpher] i),(WM3_MC_GetValue $.modifiers[#Morpher] i))
			--			--print (WM3_MC_GetValue $.modifiers[#Morpher] i)
			--		)
			--		
			--	)
			--)
			fn AIKeyFacialPosFN MorpherNum WayID = 
			(
				if WayID == 1 do
				(
					clearSelection()					
					select $*Body_H_001
					for i in 6 to MorpherNum do
					(
						if $.modifiers[#Morpher][i].value == 0.0 do
						(
							at time 0 animate on $.modifiers[#Morpher][i].value = 0
						)		
						addNewKey $.modifiers[#Morpher][i] sliderTime
					)	
				)
				if WayID == 2 do
				(
					clearSelection()
					select $*Eye_001 
					addNewKey $.modifiers[#Morpher] sliderTime
					clearSelection()
					select $*Pupil_Effect_001 
					if selection.count == 1 do
					(
						addNewKey $.modifiers[#Morpher] sliderTime
					)	
					clearSelection()
					select $*Eye_Effect_001 
					(
						addNewKey $.modifiers[#Morpher] sliderTime
					)
				)	
			)
			
			fn AIKeyFN MorpherNum WayID = 
			(
				if WayID == 1 do
				(	
					for i in 6 to MorpherNum do
					(
						addNewKey $.modifiers[#Morpher][i] sliderTime
					)	
				)
				if WayID == 2 do
				(
					addNewKey $.modifiers[#Morpher] sliderTime
				)	
			)
			
			fn RelationMorpherValueFN IDx ConstomValue= 
			(
				--select $*Body_H_001
				WM3_MC_SetValue $.modifiers[#Morpher] IDx ConstomValue
			)
			
			
			fn  PupilelationMorpherPosWeightFN IDx ConstomValue= 
			(
				select $*Eye_001
				if RdoPupilSync.state == 1 do
				(
					WM3_MC_SetValue $.modifiers[#Morpher] IDx ConstomValue
					WM3_MC_SetValue $.modifiers[#Morpher] (IDx+6) ConstomValue	
				)
				if RdoPupilSync.state == 2 do
				(
					if RdoPupilRandL.state ==1 do
					(
						WM3_MC_SetValue $.modifiers[#Morpher] IDx ConstomValue	
					)
					if RdoPupilRandL.state ==2 do
					(
						WM3_MC_SetValue $.modifiers[#Morpher] (IDx+6) ConstomValue
					)	
				)	
			)
			fn  PupilEffectRelationMorpherPosWeightFN IDx ConstomValue= 
			(
				--local CoustomValue = 6
				--local UpCoustomValue = CoustomValue +1
				select $*Pupil_Effect_001
				if RdoPupilSync.state == 1 do
				(
					WM3_MC_SetValue $.modifiers[#Morpher] IDx ConstomValue
					WM3_MC_SetValue $.modifiers[#Morpher] (IDx+6) ConstomValue
				)
				if RdoPupilSync.state == 2 do
				(
					if RdoPupilRandL.state ==1 do
					(
						WM3_MC_SetValue $.modifiers[#Morpher] IDx ConstomValue
					)
					if RdoPupilRandL.state ==2 do
					(
						WM3_MC_SetValue $.modifiers[#Morpher] (IDx+6) ConstomValue
					)
				)	
			)
			fn  PupilRelationMorpherDirValueFN IDx ConstomValue=
			(
				select $*Eye_001
				a = WM3_MC_GetValue $.modifiers[#Morpher] IDx
				b = ConstomValue +a
				if b >100 then
				(	
					b = 100.0
					return b
				)
				else
				(
					return b
				)			
			)	
			
			fn MorpherResetFN ConstomAarray WayIDx= 
			(
				for i in 1 to ConstomAarray.count do
				(
					WM3_MC_SetValue $.modifiers[#Morpher] ConstomAarray[i][3] 0.0
				)
				if WayIDx == 1 do
				(
					for i in 6 to ConstomAarray.count do
					(	
						addNewKey $.modifiers[#Morpher][i] sliderTime
					)	
				)
				if WayIDx == 2 do
				(
					addNewKey $.modifiers[#Morpher] sliderTime
				)	
			)
			
			fn SetMorpherWeight UIDDIDx UIContorl ConstomArray=
			(
				UIContorl.value = WM3_MC_GetValue $.modifiers[#Morpher] ConstomArray[UIDDIDx.selection][3] 	
			)
			
			
			fn PupilDirBtnFN ChannelID ConstomValue = 
			(
				clearSelection()
				select $*Pupil_Effect_001 
				
				if selection.count == 1 then
				(
					PupilelationMorpherPosWeightFN ChannelID ConstomValue
					PupilEffectRelationMorpherPosWeightFN  ChannelID ConstomValue
				)
				else
				(	
					PupilelationMorpherPosWeightFN ChannelID ConstomValue
				)
				addNewKey $.modifiers[#Morpher] sliderTime	
				
			)
			
			
			fn ClearEyePupilEffectFN =
			(
				clearSelection()
				select $*Pupil_Effect_001
				if selection.count == 1 do
				(	
					select $*Pupil_Effect_001
					WM3_MC_SetValue $.modifiers[#Morpher] 13 100.0
					WM3_MC_SetValue $.modifiers[#Morpher] 14 100.0
					--print"瞳孔特效"
				)
				clearSelection()
				select $*Eye_Effect_001
				if selection.count == 1 do
				(	
					select $*Eye_Effect_001
					WM3_MC_SetValue $.modifiers[#Morpher] 1 0.0
					WM3_MC_SetValue $.modifiers[#Morpher] 2 0.0
					--print"眼部特效"	
				)
				
			)
				
							
			
			
			
			
			
			
			
			
			
			
			--on ButtEyebrowStyle05 pressed do
			--(
			--	select $*Body_H_001
			--	RelationMorpherValueFN EyebrowAfterDelArray[4+3][3] 100.0
			--	AIKeyFN  MorpherUseableNumSPN.value 1
			--)
			
			
			
			
			on FacialAnimationMakingDetailsTool open do
			(
				local aaTempMorpherArray = #()
				HsHExpressionToolCollection.CollectMorpherInfoFN aaTempMorpherArray
				MorpherUseableNumSPN.value = aaTempMorpherArray.count
				TempMorpherArray = #()
				prosound.init true
				AnimateNameDDL.items = HsHExpressionToolCollection.animate_names
				--
				CollectUIControlsFN()
				
				MouthMatchMorpherArrayFN()
				EyeMatchMorpherArrayFN()
				EyebrowMatchMorpherArrayFN()
				PupilMatchMorpherArrayFN()
				
				
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
					PupilEffectMatchMorpherArrayFN()
					ClearEyePupilEffectFN()	
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
					EyeEffectMatchMorpherArrayFN()
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
				
				$.material._FaceFlushToggle = off
				$.material._FlushIntensity = color 255 255 0 0
				$.material._RedFlushColor = color 255 0 0 255
				$.material._BlackFlushColor = color 0 0 0 255
				deleteKeys $.material
				
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
				SaveDataToCach()
			)
			on ButtEyebrowStyle01 pressed do
			(
				select $*Body_H_001
				MorpherResetFN EyebrowAfterDelArray 1
			)
			on ButtEyebrowStyle02 pressed do
			(
				select $*Body_H_001
				RelationMorpherValueFN EyebrowAfterDelArray[1+3][3] 100.0
				AIKeyFN  MorpherUseableNumSPN.value 1
			)
			on ButtEyebrowStyle03 pressed do
			(
				select $*Body_H_001
				RelationMorpherValueFN EyebrowAfterDelArray[2+3][3] 100.0
				AIKeyFN  MorpherUseableNumSPN.value 1
			)
			on ButtEyebrowStyle04 pressed do
			(
				select $*Body_H_001
				RelationMorpherValueFN EyebrowAfterDelArray[3+3][3] 100.0
				AIKeyFN  MorpherUseableNumSPN.value 1
			)
			on SldPupilDirWeight changed val do
			(
				PupilDirBtnFN PupilAfterDelArray[DDPupilDirs.selection][3] SldPupilDirWeight.value	
				--PupilEffectRelationMorpherPosWeightFN PupilAfterDelArray[DDPupilDirs.selection][3] SldPupilDirWeight.value
				--print PupilAfterDelArray[DDPupilDirs.selection][3]
			)
			on DDPupilDirs selected sel do
			(
				--select $*Eye_001
				--SetMorpherWeight DDPupilDirs SldPupilDirWeight PupilAfterDelArray
			)
			on BtnPupilDir pressed do
			(
				select $*Eye_001
				MorpherResetFN PupilAfterDelArray 2
				clearSelection()
				select $*Pupil_Effect_001
				if selection.count == 1 do
				(
					MorpherResetFN PupilEffectAfterDelArray 2
					ClearEyePupilEffectFN()	
				)
				
			)
			on BtnPupilDir01 pressed do
			(
				local TempValue = PupilRelationMorpherDirValueFN 1 SpnPupilDirWeight.value
				PupilDirBtnFN 1 TempValue
			)
			on BtnPupilDir02 pressed do
			(
				local TempValue = PupilRelationMorpherDirValueFN 2 SpnPupilDirWeight.value
				PupilDirBtnFN 2 TempValue
			)
			on BtnPupilDir03 pressed do
			(
				local TempValue = PupilRelationMorpherDirValueFN 3 SpnPupilDirWeight.value
				PupilDirBtnFN 3 TempValue
			)
			on BtnPupilDir04 pressed do
			(
				local TempValue = PupilRelationMorpherDirValueFN 4 SpnPupilDirWeight.value
				PupilDirBtnFN 4 TempValue
			)
			on BtnPupilDir05 pressed do
			(
				local TempValue = PupilRelationMorpherDirValueFN 1 SpnPupilDirWeight.value
				PupilDirBtnFN 1 TempValue
				local TempValue = PupilRelationMorpherDirValueFN 3 SpnPupilDirWeight.value
				PupilDirBtnFN 3 TempValue
			)
			on BtnPupilDir06 pressed do
			(
				local TempValue = PupilRelationMorpherDirValueFN 1 SpnPupilDirWeight.value
				PupilDirBtnFN 1 TempValue
				local TempValue = PupilRelationMorpherDirValueFN 4 SpnPupilDirWeight.value
				PupilDirBtnFN 4 TempValue
			)
			on BtnPupilDir07 pressed do
			(
				local TempValue = PupilRelationMorpherDirValueFN 2 SpnPupilDirWeight.value
				PupilDirBtnFN 2 TempValue
				local TempValue = PupilRelationMorpherDirValueFN 3 SpnPupilDirWeight.value
				PupilDirBtnFN 3 TempValue	
			)
			on BtnPupilDir08 pressed do
			(
				local TempValue = PupilRelationMorpherDirValueFN 2 SpnPupilDirWeight.value
				PupilDirBtnFN 2 TempValue
				local TempValue = PupilRelationMorpherDirValueFN 4 SpnPupilDirWeight.value
				PupilDirBtnFN 4 TempValue
			)
			on RdoPupilSync changed stat do
			(
				--print RdoPupilSync.state
			)
			on RdoPupilRandL changed stat do
			(
				--print RdoPupilRandL.state
			)
			on BtnMouthStyle01 pressed do
			(
				select $*Body_H_001
				MorpherResetFN MouthAfterDelArray 1
			)
			on BtnMouthStyle02 pressed do
			(
				select $*Body_H_001
				RelationMorpherValueFN MouthAfterDelArray[1][3] 100.0
				AIKeyFN  MorpherUseableNumSPN.value 1
			)
			on BtnMouthStyle03 pressed do
			(
				select $*Body_H_001
				RelationMorpherValueFN MouthAfterDelArray[2][3] 100.0
				AIKeyFN  MorpherUseableNumSPN.value 1
			)
			on BtnMouthStyle04 pressed do
			(
				select $*Body_H_001
				RelationMorpherValueFN MouthAfterDelArray[3][3] 100.0
				AIKeyFN  MorpherUseableNumSPN.value 1
			)
			on BtnMouthStyle05 pressed do
			(	
				select $*Body_H_001
				RelationMorpherValueFN MouthAfterDelArray[4][3] 100.0
				AIKeyFN  MorpherUseableNumSPN.value 1				
			)
			on BtnMouthStyle06 pressed do
			(
				select $*Body_H_001
				RelationMorpherValueFN MouthAfterDelArray[5][3] 100.0
				AIKeyFN  MorpherUseableNumSPN.value 1
			)
			on DDMouthAddStylesWeight changed val do
			(
				select $*Body_H_001
				RelationMorpherValueFN MouthAfterDelArray[(DDMouthAddStyles.selection+5)][3] DDMouthAddStylesWeight.value
				AIKeyFN  MorpherUseableNumSPN.value 1
			)
			on DDMouthAddStyles selected sel do
			(
				select $*Body_H_001
				SetMorpherWeight DDMouthAddStyles DDMouthAddStylesWeight MouthAfterDelArray
				--addNewKey $.modifiers[#Morpher] sliderTime
			)
			on DDButtEyebrowStyles selected sel do
			(
				select $*Body_H_001
				SetMorpherWeight DDButtEyebrowStyles DDButtEyebrowStylesWeight EyebrowAfterDelArray
				--addNewKey $.modifiers[#Morpher] sliderTime
			)
			on SpnPupilDirWeight changed val do
			(
			
			)
			on DDMouthStyles selected sel do
			(
				select $*Body_H_001
				SetMorpherWeight DDMouthStyles DDMouthStylesWeight MouthAfterDelArray
				--addNewKey $.modifiers[#Morpher] sliderTime				
			)
			on DDMouthStylesWeight changed val do
			(
				select $*Body_H_001
				RelationMorpherValueFN MouthAfterDelArray[DDMouthStyles.selection][3] DDMouthStylesWeight.value
				AIKeyFN  MorpherUseableNumSPN.value 1
			)
			on ButtEyeStyle01 pressed do
			(
				select $*Body_H_001
				MorpherResetFN EyeAfterDelArray 1
				--RDOPupilLinkEyeFN 0.0 EyeCloseMorpherName[1] 0.2
				select $*Body_H_001
			)
			on ButtEyeStyle02 pressed do
			(
				select $*Body_H_001
				RelationMorpherValueFN EyeAfterDelArray[1][3] 100.0
				AIKeyFN  MorpherUseableNumSPN.value 1
				--RDOPupilLinkEyeFN 100 EyeAfterDelArray[1][2].name 0.2
				select $*Body_H_001
			)
			on ButtEyeStyle03 pressed do
			(
				select $*Body_H_001
				RelationMorpherValueFN EyeAfterDelArray[2][3] 100.0
				AIKeyFN  MorpherUseableNumSPN.value 1
				--RDOPupilLinkEyeFN 100 EyeAfterDelArray[2][2].name 0.2
				select $*Body_H_001
			)
			on ButtEyeStyle04 pressed do
			(
				select $*Body_H_001
				RelationMorpherValueFN EyeAfterDelArray[3][3] 100.0
				AIKeyFN  MorpherUseableNumSPN.value 1
				--RDOPupilLinkEyeFN 100 EyeAfterDelArray[3][2].name 0.2
				select $*Body_H_001
			)
			on ButtEyeStyle05 pressed do
			(
				select $*Body_H_001
				RelationMorpherValueFN EyeAfterDelArray[4][3] 100.0
				AIKeyFN  MorpherUseableNumSPN.value 1
				--RDOPupilLinkEyeFN 100 EyeAfterDelArray[4][2].name 0.2
				select $*Body_H_001
			)
			on DDButtEyeStyles selected sel do
			(
				select $*Body_H_001
				SetMorpherWeight DDButtEyeStyles DDButtEyeStylesWeight EyeAfterDelArray
			)
			on DDButtEyeStylesWeight changed val do
			(
				select $*Body_H_001
				RelationMorpherValueFN EyeAfterDelArray[DDButtEyeStyles.selection][3] DDButtEyeStylesWeight.value
				AIKeyFN  MorpherUseableNumSPN.value 1
				--RDOPupilLinkEyeFN DDButtEyeStylesWeight.value EyeAfterDelArray[DDButtEyeStyles.selection][2].name 0.20
				select $*Body_H_001
			)
			on DDButtEyebrowStylesWeight changed val do
			(
				select $*Body_H_001
				RelationMorpherValueFN EyebrowAfterDelArray[DDButtEyebrowStyles.selection][3] DDButtEyebrowStylesWeight.value
				AIKeyFN  MorpherUseableNumSPN.value 1
			)
			on DDEyeEffectControlWay selected sel do
			(
				clearSelection()
				select  $*Eye_Effect_001
				if selection.count == 1 then
				(	
					SetMorpherWeight DDEyeEffectControlWay DDEyeEffectControlWeight EyeEffectAfterDelArray
				)
				else
				(
					messagebox "没有特效眼睛"
				)
			)
			on DDEyeEffectControlWeight changed val do
			(
				clearSelection()
				select  $*Eye_Effect_001
				if selection.count == 1 then
				(	
					RelationMorpherValueFN EyeEffectAfterDelArray[DDEyeEffectControlWay.selection][3] DDEyeEffectControlWeight.value
					AIKeyFN  MorpherUseableNumSPN.value 2
				)
				else
				(
					messagebox "没有特效眼睛"
				)
			)
			on DDPupilEffectControl selected sel do
			(
				clearSelection()
				select $*Pupil_Effect_001
				if selection.count == 1 then
				(	
					DDPupilEffectControlWeight.value = WM3_MC_GetValue $.modifiers[#Morpher] PupilEffectAfterDelArray[(DDPupilEffectControl.selection + 12)][3]
					addNewKey $.modifiers[#Morpher] sliderTime
				)
				else
				(
					messagebox "没有瞳孔特效"	
				)
			)
			on DDPupilEffectControlWeight changed val do
			(
				clearSelection()
				select $*Pupil_Effect_001
				if selection.count == 1 then
				(	
					WM3_MC_SetValue $.modifiers[#Morpher] (PupilEffectAfterDelArray[(DDPupilEffectControl.selection + 12)][3]) DDPupilEffectControlWeight.value
					addNewKey $.modifiers[#Morpher] sliderTime
				)
				else
				(
					messagebox "没有瞳孔特效"	
				)
				
			)
			on ProjectPathBTN pressed do
			(
				a = getSavePath()
				if a ==null then
					messageBox "请选择路径"
				else
				(	
					b = a +"\\"
					ProjectPathEDT.text = b
					getDic["FilePath"] = b
				)
			)
			on WavOffsetSPN changed val do
			(
				HsHExpressionToolCollection.sound_start_fn WavOffsetSPN.value
			)
			on AnimateNameEDT entered text do
			(	
				--重置面板
				sliderTime = 0f
				CHKFlushState.state = off
				SLDFlushBlackRange.value = 0
				SLDFlushRedIntensity.value = 0
				SLDFlushBlackIntensity.value = 0
				CPFlushRedColor.color = color 255 0 0 255
				CPFlushBlackColor.color = color 0 0 0 255
				
				select $*Body_H_001
				$.material._FaceFlushToggle = off
				$.material._FlushIntensity = color 255 255 0 0
				$.material._RedFlushColor = color 255 0 0 255
				$.material._BlackFlushColor = color 0 0 0 255
				
				
				
				deleteKeys $.material
				--清除眼睛特效和瞳孔特效贴片上因为数值变化而产生的数据
				clearSelection()
				select  $*Eye_Effect_001
				if selection.count == 1 do
				(	
					spnEyeEffectTexID.value = 0	
					if $.EyeTextureTrans.texIndex.keys != undefined do
					(	
						deleteKeys $.EyeTextureTrans.texIndex.keys
					)
				)
				clearSelection()
				select  $*Pupil_Effect_001
				if selection.count == 1 do
				(
					SPNPupilEffectTexID.value = 0					
					if $.EyeTextureTrans.texIndex.keys != undefined do
					(	
						deleteKeys $.EyeTextureTrans.texIndex.keys
					)
				)
				--print "aaaaaaa"
				HsHExpressionToolCollection.import_bip_sound_fn AnimateNameEDT.text ProjectPathEDT
				HsHExpressionToolCollection.import_xaf_fn  AnimateNameEDT.text  ProjectPathEDT.text MorpherUseableNumSPN.value
				ClearEyePupilEffectFN()
			)
			on ExportFacilAnimateBTN pressed do
			(
				HsHExpressionToolCollection.export_facialFbx_fn AnimateNameEDT.text  ProjectPathEDT.text
				HsHExpressionToolCollection.export_xaf_fn AnimateNameEDT.text  ProjectPathEDT.text
				/*
				--重置面板
				sliderTime = 0f
				
				CHKFlushState.state = off
				SLDFlushBlackRange.value = 0
				SLDFlushRedIntensity.value = 0
				SLDFlushBlackIntensity.value = 0
				CPFlushRedColor.color = color 255 0 0 255
				CPFlushBlackColor.color = color 0 0 0 255
				
				select $*Body_H_001
				$.material._FaceFlushToggle = off
				$.material._FlushIntensity = color 255 255 0 0
				$.material._RedFlushColor = color 255 0 0 255
				$.material._BlackFlushColor = color 0 0 0 255
				
				
				deleteKeys $.material
				
				--清除眼睛特效和瞳孔特效贴片上因为数值变化而产生的数据
				clearSelection()
				select  $*Eye_Effect_001
				if selection.count == 1 do
				(	
					spnEyeEffectTexID.value = 0	
					if $.EyeTextureTrans.texIndex.keys != undefined do
					(	
						deleteKeys $.EyeTextureTrans.texIndex.keys
					)
				)
				clearSelection()
				select  $*Pupil_Effect_001
				if selection.count == 1 do
				(
					SPNPupilEffectTexID.value = 0					
					if $.EyeTextureTrans.texIndex.keys != undefined do
					(	
						deleteKeys $.EyeTextureTrans.texIndex.keys
					)
				)
				*/
			)
			on AnimateNameDDL selected sel do
			(
				--重置面板
				sliderTime = 0f
				CHKFlushState.state = off
				SLDFlushBlackRange.value = 0
				SLDFlushRedIntensity.value = 0
				SLDFlushBlackIntensity.value = 0
				CPFlushRedColor.color = color 255 0 0 255
				CPFlushBlackColor.color = color 0 0 0 255
				
				select $*Body_H_001
				$.material._FaceFlushToggle = off
				$.material._FlushIntensity = color 255 255 0 0
				$.material._RedFlushColor = color 255 0 0 255
				$.material._BlackFlushColor = color 0 0 0 255
				deleteKeys $.material
				
				
				--清除眼睛特效和瞳孔特效贴片上因为数值变化而产生的数据
				clearSelection()
				select  $*Eye_Effect_001
				if selection.count == 1 do
				(	
					spnEyeEffectTexID.value = 0	
					if $.EyeTextureTrans.texIndex.keys != undefined do
					(	
						deleteKeys $.EyeTextureTrans.texIndex.keys
					)
				)
				clearSelection()
				select  $*Pupil_Effect_001
				if selection.count == 1 do
				(
					SPNPupilEffectTexID.value = 0					
					if $.EyeTextureTrans.texIndex.keys != undefined do
					(	
						deleteKeys $.EyeTextureTrans.texIndex.keys
					)
				)
				
				
				a =AnimateNameDDL.items[sel]
				AnimateNameEDT.text = a
				HsHExpressionToolCollection.import_bip_sound_fn a ProjectPathEDT
				HsHExpressionToolCollection.import_xaf_fn  AnimateNameEDT.text  ProjectPathEDT.text MorpherUseableNumSPN.value
				ClearEyePupilEffectFN()	
			)
			on ImportMouthXafBTN pressed do
			(
				
				HsHExpressionToolCollection.ImportMouthXafFN AnimateNameEDT.text ProjectPathEDT.text
				
			)
			on StandBTN pressed do
			(
				
				--重置面板
				sliderTime = 0f
				CHKFlushState.state = off
				SLDFlushBlackRange.value = 0
				SLDFlushRedIntensity.value = 0
				SLDFlushBlackIntensity.value = 0
				CPFlushRedColor.color = color 255 0 0 255
				CPFlushBlackColor.color = color 0 0 0 255
				
				select $*Body_H_001
				$.material._FaceFlushToggle = off
				$.material._FlushIntensity = color 255 255 0 0
				$.material._RedFlushColor = color 255 0 0 255
				$.material._BlackFlushColor = color 0 0 0 255
				deleteKeys $.material
				
				
				
				--清除眼睛特效和瞳孔特效贴片上因为数值变化而产生的数据
				clearSelection()
				select  $*Eye_Effect_001
				if selection.count == 1 do
				(	
					spnEyeEffectTexID.value = 0	
					if $.EyeTextureTrans.texIndex.keys != undefined do
					(	
						deleteKeys $.EyeTextureTrans.texIndex.keys
					)	
				)
				clearSelection()
				select  $*Pupil_Effect_001
				if selection.count == 1 do
				(
					SPNPupilEffectTexID.value = 0					
					if $.EyeTextureTrans.texIndex.keys != undefined do
					(	
						deleteKeys $.EyeTextureTrans.texIndex.keys
					)
				)
				--print "aaaaaaa"
				HsHExpressionToolCollection.import_bip_sound_fn "stand_loop" ProjectPathEDT
				HsHExpressionToolCollection.import_xaf_fn  "ffff"  ProjectPathEDT.text MorpherUseableNumSPN.value
				ClearEyePupilEffectFN()
			)
			on SailingBTN pressed do
			(
				--重置面板
				sliderTime = 0f
				CHKFlushState.state = off
				SLDFlushBlackRange.value = 0
				SLDFlushRedIntensity.value = 0
				SLDFlushBlackIntensity.value = 0
				CPFlushRedColor.color = color 255 0 0 255
				CPFlushBlackColor.color = color 0 0 0 255
				
				select $*Body_H_001
				
				$.material._FaceFlushToggle = off
				$.material._FlushIntensity = color 255 255 0 0
				$.material._RedFlushColor = color 255 0 0 255
				$.material._BlackFlushColor = color 0 0 0 255
				
			
				deleteKeys $.material
				--清除眼睛特效和瞳孔特效贴片上因为数值变化而产生的数据
				clearSelection()
				select  $*Eye_Effect_001
				if selection.count == 1 do
				(	
					spnEyeEffectTexID.value = 0	
					if $.EyeTextureTrans.texIndex.keys != undefined do
					(	
						deleteKeys $.EyeTextureTrans.texIndex.keys
					)	
				)
				clearSelection()
				select  $*Pupil_Effect_001
				if selection.count == 1 do
				(
					SPNPupilEffectTexID.value = 0					
					if $.EyeTextureTrans.texIndex.keys != undefined do
					(	
						deleteKeys $.EyeTextureTrans.texIndex.keys
					)
				)
				--print "aaaaaaa"
				HsHExpressionToolCollection.import_bip_sound_fn "sailing_loop" ProjectPathEDT
				HsHExpressionToolCollection.import_xaf_fn  "ffff"  ProjectPathEDT.text MorpherUseableNumSPN.value
				ClearEyePupilEffectFN()
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
			on RefurbishBtn pressed  do
			(
				clearSelection()
				select $*Body_H_001
				if selection.count == 1 do
				(
					CHKFlushState.state = $.Material._FaceFlushToggle
					SLDFlushBlackRange.value = $.Material._FlushRange*100
					CPFlushBlackColor.color = $.Material._BlackFlushColor
					CPFlushRedColor.color = $.Material._RedFlushColor
					SLDFlushBlackIntensity.value = ($.Material._FlushIntensity.g/255)*100
					SLDFlushRedIntensity.value = ($.Material._FlushIntensity.r/255)*100
					DDButtEyebrowStylesWeight.value = WM3_MC_GetValue $.modifiers[#Morpher] EyebrowAfterDelArray[DDButtEyebrowStyles.selection][3]
					DDButtEyeStylesWeight.value =  WM3_MC_GetValue $.modifiers[#Morpher]  EyeAfterDelArray[DDButtEyeStyles.selection][3] 
					DDMouthStylesWeight.value = WM3_MC_GetValue $.modifiers[#Morpher] MouthAfterDelArray[DDMouthStyles.selection][3] 
					DDMouthAddStylesWeight.value   =WM3_MC_GetValue $.modifiers[#Morpher] MouthAfterDelArray[(DDMouthAddStyles.selection+5)][3] 
						
				)
				clearSelection()
				select $*Eye_001
				if selection.count == 1 do
				(
					SldPupilDirWeight.value =WM3_MC_GetValue $.modifiers[#Morpher] PupilAfterDelArray[DDPupilDirs.selection][3] 
					
				)
				clearSelection()
				select $*Eye_Effect_001
				if selection.count == 1 do
				(
					spnEyeEffectTexID.value = $.baseObject.EyeTextureTrans.texIndex
					DDEyeEffectControlWeight.value = WM3_MC_GetValue $.modifiers[#Morpher]  EyeEffectAfterDelArray[DDEyeEffectControlWay.selection][3] 
				)	
				clearSelection()
				select $*Pupil_Effect_001
				if selection.count == 1 do
				(
					SPNPupilEffectTexID.value = $.baseObject.EyeTextureTrans.texIndex
					DDPupilEffectControlWeight.value = WM3_MC_GetValue $.modifiers[#Morpher] (PupilEffectAfterDelArray[(DDPupilEffectControl.selection + 12)][3])
					
				)
				select $*Body_H_001		
			)
		)
		addRollout FacialAnimationMakingDetailsTool fff
		CheckFileIsTrueFN  FacialAnimationMakingDetailsTool.ProjectPathEDT
		
		--------------------------创建字典--------
		
		ResetFaicalPosNameUIFN FacialPosSaveNameArray fff
		--print FacialAnimationMakingDetailsTool.ProjectPathEDT.text
	)
)
createDialog HsHExpressionToolCollection