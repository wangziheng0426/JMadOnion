MouthSayMorpherNameStrArray = #(
	#("sayLarge" ,  "A1"  ),#("sayI"  ,"I1")   , #("saySmall" ,"U1"    ), #("sayE" ,"E1" ), #("sayMedium","O" ),
	#("sayLarge_001","A2"),#("sayI_001","I2" ), #("saySmall_001","U2" ), #("sayE_001","E2" )
	)
--口型
MouthStyleMorpherNameStrArray = #(
	#("Mouth_Triangle_up","倒三角嘴"),#("Mouth_Triangle_down","三角嘴"),#("Mouth_Triangle_downopen","三角嘴张开"),
	
	--MouthSayMorpherNameStrArray + MouthStyleMorpherNameStrArray
	
	
	
	
	
	#("Right_Mouth_special_011" , "右上撇"),#("Left_Mouth_special_011" , "左上撇"),#("Mouth_special_011" , "上撇"),
	#("Right_Mouth_special_012" , "右伸长"),#("Left_Mouth_special_012" , "左伸长"),#("Mouth_special_012","伸长"),
	#("Right_Mouth_special_013","右下撇"),#("Left_Mouth_special_013","左下撇"),#("Mouth_special_013","下撇"),
    #("Right_Mouth_special_016","缩嘴（右）"),#("Left_Mouth_special_016","缩嘴（左）"),#("Mouth_special_016","缩嘴"), 
	#("Mouth_special_014","尴尬"),#("Mouth_special_015","难堪"),
	#("Mouth_Style_catmouth","猫嘴"),#("Mouth_Style_catmouthopen","猫嘴张开")
	)
--嘴巴造型
EyeMorpherNameStrArray = #(
	#("Right_Eye_close","右闭眼"),#("Left_Eye_close","左闭眼"),
	#("Right_Eye_close_001","右微笑闭眼"),#("Left_Eye_close_001","左微笑闭眼"),
	
	#("Eye_Effect","特效片出现备用眼"),
	#("Double_Eye_close","闭眼"),#("Double_Eye_close_001","微笑闭眼"),
	#("Eye_special_011","K生气"),#("Eye_special_012","惊讶"),#("Eye_special_013","死鱼眼"),#("Eye_special_014","一字眼"),#("Eye_special_015","折线眼")
	)
--眼睛造型
EyebrowMorpherNameStrArray = #(
	#("Eyebrow_up","眉毛向上"),#("Eyebrow_down","眉毛向下"),#("Eyebrow_gather","眉毛居中"),
	#("Eyebrow_special_011","高兴"),#("Eyebrow_special_012","怒"),#("Eyebrow_special_013","困惑"),#("Eyebrow_special_014","M尴尬")
	)
--眉毛造型
FacialMorpherNameStrArray = #(#("Facial_special_011","死鱼眼脸"))
--整体脸造型
PupilMorpherNameStrArray = #(
	#("Right_Pupil_up","上"),#("Right_Pupil_down","下"),#("Right_Pupil_right","右"),#("Right_Pupil_left","左"),#("Right_Pupil_scale","缩小"),#("Right_Pupil_appear","消失"),
	#("Left_Pupil_up","上"),#("Left_Pupil_down","下"),#("Left_Pupil_right","右"),#("Left_Pupil_left","左"),#("Left_Pupil_scale","缩小"),#("Left_Pupil_appear","消失"),
	#("Pupil_Style_001","死鱼眼")
	)
--瞳孔
	
PupilEffectMorpherNameStrArray = #(
	#("Right_Effect_Pupil_up","上"),#("Right_Effect_Pupil_down","下"),#("Right_Effect_Pupil_right","右"),#("Right_Effect_Pupil_left","左"),#("Right_Effect_Pupil_scale","缩小"),#("Right_Effect_Pupil_appear","消失"),
	#("Left_Effect_Pupil_up","上"),#("Left_Effect_Pupil_down","下"),#("Left_Effect_Pupil_right","右"),#("Left_Effect_Pupil_left","左"),#("Left_Effect_Pupil_scale","缩小"),#("Left_Effect_Pupil_appear","消失"),
	#("Effect_Pupil_appear_parallel","平行出现"),#("Effect_Pupil_appear_symmetry","对称出现")
	)
--瞳孔特效片
EyeEffectMorpherNameStrArray = #(#("Effect_Eye_appear_symmetry","对称出现"),#("Effect_Eye_appear_parallel","平行出现"))





















	
facialPartMorpherObjNameStrArray = #("Mouth_Part","Eye_Part","Eyebrow_Part","Pupil_Part","Pupil_Effect_Part","Eye_Effect_Part")	


--只有主炮和鱼雷
ProjectFacialAnimateNames = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","night","spattack","spattack_b","torpedo1","torpedo2","torpedo_n","gun_a1","gun_a2","gun_b","gun_ss","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")
ProjectAnimateNames	 = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","night","spattack","spattack_b","torpedo1","torpedo2","torpedo_n","gun_a1","gun_a2","gun_b","gun_ss","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")	
--只有主炮
ProjectModelFacialAnimateNames02 = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","night","spattack","spattack_b","gun_a1","gun_a2","gun_b","gun_ss","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")
ProjectModelAnimateNames02	 = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","air1","air2","night","spattack","spattack_b","torpedo1","torpedo2","torpedo_n","gun_a1","gun_a2","gun_b","gun_ss","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")	
--只有航空的表情动画数据
ProjectModelFacialAnimateNames03 = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","air1","air2","night","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")
ProjectModelAnimateNames03	 = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","air1","air2","night","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")	
--NPC的表情动画数据				
ProjectNPCFacialAnimateNames = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","air1","air2","night","spattack","spattack_b","torpedo1","torpedo2","torpedo_n","gun_a1","gun_a2","gun_b","gun_ss","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")

ProjectNPCAnimateNames  = #()
				
--红奥克兰的表情动画数据	
ProjectNPCBossFacialAnimateNames = #("sailing_loop","action1","scout_a","spattack","spattack_b","torpedo1", "torpedo2","gun_a1","gun_a2","gun_b","pong_loop","beaim","dodge","dodge_b",
	"cover","behit_b","behitbk_b","mvp","mvp_loop","retreat","defeat","behit_ci_loop")				
ProjectNPCBossAnimateNames = #( "sailing_loop","action1","scout_a","spattack","spattack_b","torpedo1", "torpedo2","gun_a1","gun_a2","gun_b","pong_loop","beaim","dodge","dodge_b",
	"cover","behit_b","behitbk_b","mvp","mvp_loop","retreat","defeat","behit_ci_loop")				
				


				