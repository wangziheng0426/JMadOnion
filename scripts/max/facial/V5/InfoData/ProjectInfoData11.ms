MouthSayMorpherNameStrArray = #(
	#("sayLarge" ,  "A1"  ),#("sayI"  ,"I1")   , #("saySmall" ,"U1"    ), #("sayE" ,"E1" ), #("sayMedium","O" ),
	#("sayLarge_001","A2"),#("sayI_001","I2" ), #("saySmall_001","U2" ), #("sayE_001","E2" )
	)
--����
MouthStyleMorpherNameStrArray = #(
	#("Mouth_Triangle_up","��������"),#("Mouth_Triangle_down","������"),#("Mouth_Triangle_downopen","�������ſ�"),
	
	--MouthSayMorpherNameStrArray + MouthStyleMorpherNameStrArray
	
	
	
	
	
	#("Right_Mouth_special_011" , "����Ʋ"),#("Left_Mouth_special_011" , "����Ʋ"),#("Mouth_special_011" , "��Ʋ"),
	#("Right_Mouth_special_012" , "���쳤"),#("Left_Mouth_special_012" , "���쳤"),#("Mouth_special_012","�쳤"),
	#("Right_Mouth_special_013","����Ʋ"),#("Left_Mouth_special_013","����Ʋ"),#("Mouth_special_013","��Ʋ"),
    #("Right_Mouth_special_016","���죨�ң�"),#("Left_Mouth_special_016","���죨��"),#("Mouth_special_016","����"), 
	#("Mouth_special_014","����"),#("Mouth_special_015","�ѿ�"),
	#("Mouth_Style_catmouth","è��"),#("Mouth_Style_catmouthopen","è���ſ�")
	)
--�������
EyeMorpherNameStrArray = #(
	#("Right_Eye_close","�ұ���"),#("Left_Eye_close","�����"),
	#("Right_Eye_close_001","��΢Ц����"),#("Left_Eye_close_001","��΢Ц����"),
	
	#("Eye_Effect","��ЧƬ���ֱ�����"),
	#("Double_Eye_close","����"),#("Double_Eye_close_001","΢Ц����"),
	#("Eye_special_011","K����"),#("Eye_special_012","����"),#("Eye_special_013","������"),#("Eye_special_014","һ����"),#("Eye_special_015","������")
	)
--�۾�����
EyebrowMorpherNameStrArray = #(
	#("Eyebrow_up","üë����"),#("Eyebrow_down","üë����"),#("Eyebrow_gather","üë����"),
	#("Eyebrow_special_011","����"),#("Eyebrow_special_012","ŭ"),#("Eyebrow_special_013","����"),#("Eyebrow_special_014","M����")
	)
--üë����
FacialMorpherNameStrArray = #(#("Facial_special_011","��������"))
--����������
PupilMorpherNameStrArray = #(
	#("Right_Pupil_up","��"),#("Right_Pupil_down","��"),#("Right_Pupil_right","��"),#("Right_Pupil_left","��"),#("Right_Pupil_scale","��С"),#("Right_Pupil_appear","��ʧ"),
	#("Left_Pupil_up","��"),#("Left_Pupil_down","��"),#("Left_Pupil_right","��"),#("Left_Pupil_left","��"),#("Left_Pupil_scale","��С"),#("Left_Pupil_appear","��ʧ"),
	#("Pupil_Style_001","������")
	)
--ͫ��
	
PupilEffectMorpherNameStrArray = #(
	#("Right_Effect_Pupil_up","��"),#("Right_Effect_Pupil_down","��"),#("Right_Effect_Pupil_right","��"),#("Right_Effect_Pupil_left","��"),#("Right_Effect_Pupil_scale","��С"),#("Right_Effect_Pupil_appear","��ʧ"),
	#("Left_Effect_Pupil_up","��"),#("Left_Effect_Pupil_down","��"),#("Left_Effect_Pupil_right","��"),#("Left_Effect_Pupil_left","��"),#("Left_Effect_Pupil_scale","��С"),#("Left_Effect_Pupil_appear","��ʧ"),
	#("Effect_Pupil_appear_parallel","ƽ�г���"),#("Effect_Pupil_appear_symmetry","�ԳƳ���")
	)
--ͫ����ЧƬ
EyeEffectMorpherNameStrArray = #(#("Effect_Eye_appear_symmetry","�ԳƳ���"),#("Effect_Eye_appear_parallel","ƽ�г���"))





















	
facialPartMorpherObjNameStrArray = #("Mouth_Part","Eye_Part","Eyebrow_Part","Pupil_Part","Pupil_Effect_Part","Eye_Effect_Part")	


--ֻ�����ں�����
ProjectFacialAnimateNames = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","night","spattack","spattack_b","torpedo1","torpedo2","torpedo_n","gun_a1","gun_a2","gun_b","gun_ss","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")
ProjectAnimateNames	 = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","night","spattack","spattack_b","torpedo1","torpedo2","torpedo_n","gun_a1","gun_a2","gun_b","gun_ss","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")	
--ֻ������
ProjectModelFacialAnimateNames02 = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","night","spattack","spattack_b","gun_a1","gun_a2","gun_b","gun_ss","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")
ProjectModelAnimateNames02	 = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","air1","air2","night","spattack","spattack_b","torpedo1","torpedo2","torpedo_n","gun_a1","gun_a2","gun_b","gun_ss","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")	
--ֻ�к��յı��鶯������
ProjectModelFacialAnimateNames03 = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","air1","air2","night","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")
ProjectModelAnimateNames03	 = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","air1","air2","night","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")	
--NPC�ı��鶯������				
ProjectNPCFacialAnimateNames = #("get" ,"login","login_m","stand_loop","click1","click2","click3","turn","turn_l","back","backm","backmc","marry","wait","sailing_loop","action1","action2","scout_a","scout_b","item","closeenemy",
				"battle","air1","air2","night","spattack","spattack_b","torpedo1","torpedo2","torpedo_n","gun_a1","gun_a2","gun_b","gun_ss","pong_loop","asw","hit","miss","beaim","dodge","dodge_b","cover","behit_a","behit_b","behitbk_a",
				"behitbk_b","hurt_h","hurt_h_loop","mvp","mvp_loop","retreat","sink","bad","hold","stanby","defeat","defeat_loop","click_sp","behit_ci_loop","behit_ci_end","click_hi","bath_click","click_fs06")

ProjectNPCAnimateNames  = #()
				
--��¿����ı��鶯������	
ProjectNPCBossFacialAnimateNames = #("sailing_loop","action1","scout_a","spattack","spattack_b","torpedo1", "torpedo2","gun_a1","gun_a2","gun_b","pong_loop","beaim","dodge","dodge_b",
	"cover","behit_b","behitbk_b","mvp","mvp_loop","retreat","defeat","behit_ci_loop")				
ProjectNPCBossAnimateNames = #( "sailing_loop","action1","scout_a","spattack","spattack_b","torpedo1", "torpedo2","gun_a1","gun_a2","gun_b","pong_loop","beaim","dodge","dodge_b",
	"cover","behit_b","behitbk_b","mvp","mvp_loop","retreat","defeat","behit_ci_loop")				
				


				