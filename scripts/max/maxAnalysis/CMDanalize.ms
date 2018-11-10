
-------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------
-- Author        : gaoaihan         
-- Modify        : yumiao   
-- Last modified : 2017-07-25 18:00
-- Filename      : analize.ms
-- Description   : fix json format of log file
-------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------
prjPath = maxFilePath 
Type = "Web"

if (doesFileExist(prjPath) == false) 
then makeDir prjPath
----------------------------read Version---------------------
Pre_settingFile = OpenFile (prjPath + "analysis.log") mode:"r"
Version = readline Pre_settingFile
close Pre_settingFile
logprint = substring Version 1 (Version.count - 1)

--get frames if version>2016-------
fra="0"
if((MaxVersion() )[1] >= 18000) then 
(
    fraIndex = findString Version "frames"
    fra = substring Version (fraIndex+8) (fraIndex+20)
    fraIndex = findString fra ","
    fra = substring fra 1 (fraIndex-2)
    fraIndex = findString fra "\""
    fra = substring fra (fraIndex+1) fra.count
)

if((MaxVersion() )[1] < 18000) then 
    logprint += ",\"settings\":{"
else 
    logprint = substring logprint 1 (logprint.count - 1)

function getFullResourcePath inputResource=
(
    local theFilename = inputResource
    local isExist = FileResolutionManager.getFullFilePath &theFilename #Other
    if (isExist) then
    (
        theFilename = theFilename as name
        return theFilename
    )
    else
    (
        inputResource = inputResource as name
        return inputResource
    )
)
function replaceString str1 str2 str3=
(
        while ((i = findstring str1 str2) != undefined) do  
        (  
            str1 = replace str1 i str2.count str3  
        )  
        return str1  
)
function sequeceanalyze reportArray theMetname=
(        
    local seqfile = theMetname
    local isfind = 0
    if(seqfile != "" and seqfile != undefined and getFilenameFile seqfile != "") then
    (    
        seqfile = (getFullResourcePath seqfile) as string
        local matchfile = getFilenameFile seqfile
        if((trimright matchfile "0123456789").count > 0)
        then matchfile = trimright matchfile "0123456789"
        else if(matchfile.count > 4)
        then matchfile = substring matchfile 1 (matchfile.count - 4)
        else matchfile = substring matchfile 1 1
        if(matchfile != "" and getFilenameType seqfile != "") then
        for f in (a = getFiles ((getFilenamePath seqfile) + "*" + (getFilenameType seqfile))) do 
            if ((findString (getFilenameFile f) (matchfile as string)) != undefined) then 
            (
                appendIfunique reportArray f
                isfind = 1
            )
        if (matchfile != "" and getFilenameType seqfile == "") then
        for f in (a = getFiles ((getFilenamePath seqfile) +"*" + (getFilenameType seqfile))) do 
            if ((findString (getFilenameFile f) (matchfile as string)) != undefined) then
            (
                appendIfunique reportArray f
                isfind = 1
            )
        if isfind == 0 then
        (
            if(matchfile != "" and getFilenameType seqfile != "") then
            for f in (a = getFiles (maxfilepath + "*" + (getFilenameType seqfile))) do 
                if ((findString (getFilenameFile f) (matchfile as string)) != undefined) then 
                (
                    appendIfunique reportArray f
                    isfind = 1
                )
            if (matchfile != "" and getFilenameType seqfile == "") then
            for f in (a = getFiles (maxfilepath + "*" + (getFilenameType seqfile))) do 
                if ((findString (getFilenameFile f) (matchfile as string)) != undefined) then
                (
                    appendIfunique reportArray f
                    isfind = 1
                )
        )
        if isfind == 0 do
        ( 
            if getFilenameType seqfile == ""
            then seqfile += ".bin"
            appendIfunique reportArray seqfile
        )
    )
)

isCurrentVray=False
if ((renderers.current.classid)as string == "#(1941615238, 2012806412)") or ((renderers.current.classid)as string == "#(1941615238L, 2012806412L)") then 
(
    isCurrentVray=True
)

-----------------resolution------------------
width = renderWidth
height = renderHeight
vrayResolution = 0
if isCurrentVray then 
(
    if renderers.current.output_on and renderers.current.output_getsetsfrommax == false then
    (
        vrayResolution = 1
        vraywidth = renderers.current.output_width 
        vrayheight = renderers.current.output_height
        if (vraywidth*vrayheight)>(width*height ) then
        (
            width = vraywidth
            height = vrayheight
        )
    )
)
if((MaxVersion())[1] >= 18000) 
then logprint += ","

resolution = "\"outputwidthheight\":{\"width\":\"" + width as string + "\",\"height\":\"" + height as string + "\"}," 
logprint +="\"vrayResolution\":\"" + vrayResolution as string + "\"," 

-----------------frames------------------
frameRange= ""
sf = "0"
ef = "0"
if rendTimeType == 1 then
(
    bf = "0"
    if((MaxVersion() )[1] < 18000) then
    (
        frameRange = "\"frames\":\"" + sf + "\","
    )
    else
    (
        frameRange = "\"frames\":\"" + fra + "\","
    )
    
)
else if rendTimeType == 2 then
(
    sf = trimright (animationRange.start  as string) "f" 
    ef = trimright (animationRange.end as string) "f"
    bf = rendNThFrame as string 
    if((MaxVersion() )[1] < 18000) then
    (
        if sf == ef then 
        (frameRange = "\"frames\":\"" + sf + "\",\"framesoffset\":\"" + bf + "\",")
        else 
        (    
            if bf != "1" then
            (frameRange = "\"frames\":\"" + sf + "~" + ef + ":" + bf + "\"," + "\"framesoffset\":\"" + bf + "\",")
            else (frameRange = "\"frames\":\"" + sf + "~" + ef + "\"," + "\"framesoffset\":\"" + bf + "\",")                
        )
    )
    else
    (
        if bf != "1" then
        (frameRange = "\"frames\":\"" + fra + ":" + bf + "\",\"framesoffset\":\"" + bf + "\",")
        else
        (frameRange = "\"frames\":\"" + fra + "\",\"framesoffset\":\"" + bf + "\",")
    )
)
else if rendTimeType == 3 then
(
      sf = trimright (rendStart as string) "f"
    ef = trimright (rendEnd as string) "f"
    bf = rendNThFrame as string 
    if((MaxVersion() )[1] < 18000) then
    (
        if sf == ef then
        (frameRange = "\"frames\":\"" + sf + "\",\"framesoffset\":\"" + bf + "\",")
        else 
        (    
            if bf != "1" then
            (frameRange = "\"frames\":\"" + sf + "~" + ef + ":" + bf + "\"," + "\"framesoffset\":\"" + bf + "\",")
            else (frameRange = "\"frames\":\"" + sf + "~" + ef + "\"," + "\"framesoffset\":\"" + bf + "\",")
        )
    )
    else
    (    
        if bf != "1" then
        (frameRange = "\"frames\":\"" + fra + ":" + bf + "\",\"framesoffset\":\"" + bf + "\",")
        else (frameRange = "\"frames\":\"" + fra + "\",\"framesoffset\":\"" + bf + "\",")
    )
)
else if rendTimeType == 4 then
(
    sf = replaceString rendPickupFrames "-" "~"
    if ((MaxVersion() )[1] < 18000) then
        frameRange = "\"frames\":\"" + (sf as string) + "\","
    else
        frameRange = "\"frames\":\"" + (sf as string) + "\","
    tempb = filterString sf "~"
    tempc = ""
    for i in tempb do
        tempc += i+","
    tempd = filterString tempc ","
    sf = tempd[1]
    ef = tempd[tempd.count]
)

-----------------------output type-----------------------------
OutputFile = rendOutputFilename
outputType = ""
printType = ""
outputType = getFilenameType OutputFile
if outputType == "" or outputType == undefined do
    outputType = ".tga"
printType = "\"outputType\":\"" + (trimleft (outputType as string) "." ) + "\""

-------------------------gamma---------------------------------
if (IDisplayGamma.colorCorrectionMode as string) != "gamma" 
then gamma = "\"gamma\":" + "\"0\","
else gamma = "\"gamma\":" + "\"1\","
InGamma = "\"fileInGamma\":\"" + fileInGamma as string + "\","
OutGamma = "\"fileOutGamma\":\"" + fileOutGamma as string + "\","
logprint += gamma 
logprint += InGamma 
logprint += OutGamma 

wronggamma = 0
if (IDisplayGamma.colorCorrectionMode as string) == "gamma" do
(
    maxVer = (maxVersion())[1]
    if (rendOutputFilename == "" or rendOutputFilename == undefined) and maxVer < 16000 
    then wronggamma = 1
)
wronggammaoutput = "\"wrongGamma\":\"" + wronggamma as string + "\","
logprint += wronggammaoutput 

-----------------cameras------------------
cam = getActiveCamera()
activeCamera = ""
PrintActiveCamera = ""
if rendUseActiveView == false and rendViewIndex != undefined do
    (  
        cam = viewport.getCamera index:rendViewIndex
        activeCamera = cam
    )
if rendViewIndex == undefined do
    (
        activeCamera = ""
    )
if cam == undefined then
(
    activeCamera = ""

)
else
(
    activeCamera = cam.name
)
if ((activeCamera as string) != "" )then
(
    PrintActiveCamera = "\"renderCameras\": [{" + "\"cameraName\":\"" + (activeCamera as string) + "\","
    PrintActiveCamera = PrintActiveCamera + resolution + frameRange + printType + "}],"
)
else(
    PrintActiveCamera = "\"renderCameras\": [" + "]," 
)
logprint += PrintActiveCamera 

PcameraFlag = 0
PcameraName = "\"otherCameras\":[" 
for obj in Cameras do
(
    if (iskindof obj Camera) do
    (
        if ((obj.name as string) != (activeCamera as string))do
        (
            PcameraName += "{\"cameraName\":\"" + obj.name as string + "\","
            PcameraName = PcameraName + resolution + frameRange + printType + "},"
            PcameraFlag = 1
        )
    )
)
if PcameraFlag == 1
then PcameraName = substring PcameraName 1 (PcameraName.count-1)
PcameraName += "],"
logprint += PcameraName 

----------------------frameconfig----------------------------
if((MaxVersion() )[1] < 18000) then
    logprint += "\"framesrangeconfig\":{\"startFrame\":\"" + sf + "\",\"endFrame\":\"" + ef + "\"},"

--------------------renderviewlock and presset--------------
renderviewlock = 0
if(rendUseActiveView == false) then
    renderviewlock = 1
viewlock = "\"RendViewLock\":\"" + renderviewlock as string + "\","
logprint += viewlock

--------------------maxfix--------------
maxfix = 0
if renderviewlock == 1 then
    maxfix = 1
isMaxfix = "\"maxfix\":\"" + maxfix as string + "\","
logprint += isMaxfix

---------------------------------regionrend-------------------------------------------------------
RegionRendering = 0
RegionType = "view"
RegionPadding = 0
RegionLeft = 0
RegionRight = renderWidth
regionTop = 0
RegionBottom = renderHeight
if(getRenderType() as string == "region") do
(
    RegionType = "CROP"
    RegionRendering = 1
)
try(
EditRenderRegion.EditRegion()
nv = viewport.activeViewport
boxsize = filterstring (viewport.getRegionRect nv as string) " "
boxsize[5] = substring boxsize[5] 1 (boxsize[5].count-1)
RegionLeft = boxsize[2] as integer
RegionRight = boxsize[2] as integer+boxsize[4] as integer
regionTop = boxsize[3] as integer
RegionBottom = boxsize[3] as integer +boxsize[5]as integer 
)
catch(
RegionRendering = 0
)
regionrendprint = "\"RegionRendering\":" + RegionRendering as string + ",\"RegionType\":\"" + RegionType + "\",\"RegionPadding\":" + RegionPadding as string + ",\"RegionLeft\":" + RegionLeft as string + ",\"RegionRight\":" + RegionRight as string + ",\"regionTop\":" + regionTop as string + ",\"RegionBottom\":" + RegionBottom as string + ","
if RegionRendering == 1 then
    logprint += regionrendprint 
else logprint += "\"RegionRendering\":\"0\","

--------------------vray config------------
VROutputOn = 0
VRRawOutput = 0
VRRawFile = ""
VRSplitOn = 0
VRSplitFile = ""
VRSplitRGB = 0
VRSplitAlpha = 0
if isCurrentVray then 
(
    logprint += "\"vrayconfig\":{"
    dontRendImage = 0
    if renderers.current.options_dontRenderImage == true
    then dontRendImage = 1
    vrrend = "\"dontRendImage\":" + "\"" + dontRendImage as string + "\"," 
    logprint += vrrend 
    
    if renderers.current.output_on == true
    then VROutputOn=1
    logprint += "\"VROutputOn\":" + "\"" + VROutputOn as string + "\","
    
    if VROutputOn == 1 then
    (
        if renderers.current.output_saveRawFile == true
        then VRRawOutput = 1
        VRRawFile = renderers.current.output_rawFileName
        if VRRawFile == "" or VRRawFile == undefined
        then VRRawFile = getFilenameFile maxfilename + ".vrimg"
        VRRawFile = filenameFromPath VRRawFile
        if renderers.current.output_splitgbuffer == true
        then VRSplitOn = 1
        VRSplitFile = renderers.current.output_splitfilename
        if VRSplitFile == undefined or (VRSplitFile == "") then 
        (
            VRSplitFile = ""
            VRSplitOn = 0
        )
        else 
            VRSplitFile = filenameFromPath VRSplitFile
        
        if renderers.current.output_splitRGB == true
        then VRSplitRGB = 1
        if renderers.current.output_splitAlpha == true
        then VRSplitAlpha = 1
    )
    logprint += "\"VRRawOutput\":" + "\"" + VRRawOutput as string +"\",\"VRRawFile\":" + "\"" + VRRawFile as string + "\","
    logprint += "\"VRSplitOn\":" + "\"" + VRSplitOn as string +"\",\"VRSplitFile\":" + "\"" + VRSplitFile as string + "\","
    logprint += "\"VRSplitRGB\":" + "\"" + VRSplitRGB as string +"\",\"VRSplitAlpha\":" + "\"" + VRSplitAlpha as string + "\","

    --------------------raytrace and unsupported material and map ------------------
    mats = #()
    RTmats = #()
    UNmats = #()
    for matClass in material.classes do
    (
        for m in (getclassinstances matClass processAllAnimatables:true processChildren:true) do
            append mats m
    )
    for m in mats do
    (
        if (ClassOF m) as string == "RaytraceMaterial" do
            append RTmats m
        if (ClassOF m) as string == "Blend" do --or (ClassOF m) as string == "Autodesk_Material" or (ClassOF m) as string == "Architectural" 
            append UNmats m
    )

    RTmaps = #()
    function getAllTexture inputMaterials=
    (
        local allTexture = #()
        for eachMat in inputMaterials do
        (
            for i = 1 to (getNumSubTexmaps eachMat) do
            (
                try (if (getNumSubTexmaps (getSubTexmap eachMat i)) != 0 then
                    (
                        join allTexture (getAllTexture #((getSubTexmap eachMat i)))
                    )
                ) catch ()
                append allTexture (getSubTexmap eachMat i)
            )
        )
        return allTexture
    )
    allTexture = getAllTexture mats

    for tex in allTexture do
        if (classof tex) as string == "Raytrace"  do
            append  RTmaps tex

-- rename it in future---------------------------
    isRayTrace = 0
    if UNmats.count >0 then 
        isRayTrace = 1

    vrraytrace = "\"isRayTrace\":" + "\"" + isRayTrace as string + "\"," 
    logprint += vrraytrace
    unsupportmats = "\"unSupportMats\":" + "\"" + (UNmats.count as string )+ "\"," 
    logprint += unsupportmats
-------------------vray GI type   --------------------------
    if ( renderers.current.gi_on == false )
    then photonsInfo = 0
    else 
    (
        vrGItype1 = renderers.current.gi_primary_type
        vrGItype2 = renderers.current.gi_secondary_type
        vrGItype = "\"VR_GItype\":" + "\"" + vrGItype1 as string + "*" + vrGItype2 as string + "\","
        logprint += vrGItype 
        
----------------------------VR IRmapmode  VRmapname   missVRfile-----------------------------------------
        if ( vrGItype1 == 0) do
        (
            missVRfile = 0
            IRmapname = ""
            IRmaps = #()
            if (renderers.current.adv_irradmap_mode == 2 or renderers.current.adv_irradmap_mode == 7) 
            then IRmapname = renderers.current.adv_irradmap_loadFileName 
            if (renderers.current.adv_irradmap_mode == 6 or renderers.current.adv_irradmap_mode == 7) 
            then photonsInfo = 2
            else photonsInfo = 1
            if IRmapname == undefined
            then IRmapname = ""
            if IRmapname == "" 
            then missVRfile = 1
            else
            (    
                sequeceanalyze IRmaps IRmapname 
                if IRmaps.count == 0
                then sequeceanalyze IRmaps (maxFilePath+(filenameFromPath IRmapname)) 
                if(IRmaps.count == 0)
                then missVRfile = 1
            )
            VR_photonsInfo = "\"VR_photonsInfo\":" + "\"" + photonsInfo as string + "\","
            logprint += VR_photonsInfo 
            VR_VRmapMode = "\"VR_VRmapMode\":" + "\"" + renderers.current.adv_irradmap_mode as string + "\","
            logprint += VR_VRmapMode 
            VR_VRmapname = "\"VR_VRmapname\":" + "\"" + (filenameFromPath IRmapname) + "\","
            logprint += VR_VRmapname 
            VR_MissVRfile = "\"VR_MissVRfile\":" + "\"" + missVRfile as string + "\","
            logprint += VR_MissVRfile 
        )
----------------------------VR LCmapmode  VRLmapname   missVRLfile--------------------------------------------
        if ( vrGItype2 == 3 or vrGItype1 == 3) do
        (    
            missVRLfile = 0
            VR_VRLmapmode = "\"VR_VRLmapmode\":" + "\"" + renderers.current.lightcache_mode as string + "\","
            logprint += VR_VRLmapmode 
            if (renderers.current.lightcache_mode == 2 ) then
            (    
                LCmapName = renderers.current.lightcache_loadFileName 
                if LCmapname == undefined
                then LCmapname = ""
                if(LCmapName != "" and doesFileExist LCmapName == false and doesFileExist (maxFilePath + (filenameFromPath LCmapName)) == false)
                then missVRLfile = 1
                if(LCmapName == undefined or LCmapName == "")
                then missVRLfile = 1
                VR_VRLmapname = "\"VR_VRLmapname\":" + "\"" + (filenameFromPath LCmapname) as string + "\","
                logprint += VR_VRLmapname 
                VR_MissVRLfile = "\"VR_MissVRLfile\":" + "\"" + missVRLfile as string + "\","
                logprint += VR_MissVRLfile 
            )
        )
    )
    logprint = substring logprint 1 (logprint.count - 1)
    logprint += "},"
)
else 
(
    logprint += "\"vrayconfig\":{},"
)
---------------------------------RenderLayers----------------------------------------------------
renderLayers = #()
otherLayers = #()
layer = #()
m = 1
n = 1
logprint += "\"layers\":{"
PotherLayers = "\"otherLayers\": ["
PrenderLayers = "\"renderLayers\": ["
for i = 0 to layerManager.count - 1 do
(
    layer = layerManager.getLayer i
    layerName = layer.name as string
    if layer.renderable then
    (
        if m != 1 then
            PrenderLayers += ","
        renderLayers[m] = layerName
        PrenderLayers += "\"" + renderLayers[m] + "\""
        m += 1
    )
    else
    (
        if n != 1 then
            PotherLayers += ","
        otherLayers[n] = layerName
        PotherLayers += "\""+otherLayers[n] + "\""
        n += 1
    )

    i = i + 1
)
PrenderLayers += "],"
PotherLayers  += "]}" 
logprint += PrenderLayers 
logprint += PotherLayers

------------------------------RenderElement -------------------------------------------------------------
logprint +=  ",\"renderElements\":["
REcount = 0
if isCurrentVray then 
(
    rems = maxOps.GetCurRenderElementMgr()
    if rems!=undefined  and rems.GetElementsActive() do
    (
        if VROutputOn==0 then
        (
            for i = 0 to rems.numrenderelements() - 1 do
            (
                reObject = rems.GetRenderElement i
                if reObject.enabled do
                (
                    elementName = rems.GetRenderElementFilename i as string
                    if elementName == "undefined" or elementName == ""
                    then elementName = "D:/" + (getFilenameFile maxfilename)+"_" + reObject.elementName+"." + (trimleft (outputType as string) "." )
                    if ( findstring (filenameFromPath elementName) ".") == undefined 
                    then elementName = elementName + "." + (trimleft (outputType as string) "." )
                    if REcount == 0 
                    then logprint += "{\"index\":\"" + REcount as string + "\",\"REname\":\"" + reObject.elementName as string + "\",\"REoutputName\":\""+ (filenameFromPath elementName) + "\"}"
                    else logprint += ",{\"index\":\"" + REcount as string + "\",\"REname\":\"" + reObject.elementName as string + "\",\"REoutputName\":\""+ (filenameFromPath elementName) + "\"}"
                    REcount += 1
                )
            )
        )
        else if VRSplitOn == 1 then
        (
            for i = 0 to rems.numrenderelements() - 1 do
            (
                reObject = rems.GetRenderElement i
                if reObject.enabled do
                (
                    elementName = reObject.elementName
                    if elementName == "VRayAlpha" then 
                    (
                        if VRSplitAlpha == 1 do
                        (
                            elementName = "Alpha"
                            elementFile = (getFilenameFile VRSplitFile) + "." + elementName + (getFilenameType VRSplitFile)
                            if REcount == 0 
                            then logprint += "{\"index\":\"" + REcount as string + "\",\"REname\":\"" + elementName as string + "\",\"REoutputName\":\"" + (filenameFromPath elementFile) +"\"}"
                            else logprint += ",{\"index\":\"" + REcount as string + "\",\"REname\":\"" + elementName as string + "\",\"REoutputName\":\"" + (filenameFromPath elementFile) + "\"}"
                        )
                    )
                else
                    (
                        elementFile = (getFilenameFile VRSplitFile) + "." + elementName + (getFilenameType VRSplitFile)
                        if REcount == 0 
                        then logprint += "{\"index\":\"" + REcount as string + "\",\"REname\":\"" + elementName as string + "\",\"REoutputName\":\"" + (filenameFromPath elementFile) +"\"}"
                        else logprint += ",{\"index\":\"" + REcount as string + "\",\"REname\":\"" + elementName as string + "\",\"REoutputName\":\"" + (filenameFromPath elementFile) + "\"}"
                    )
                    REcount += 1
                )
            )       
        )
    )
)
logprint += "]"
if isCurrentVray and VRSplitOn == 1 then 
(
    if VRSplitRGB == 1 then
    (
        elementFile = (getFilenameFile VRSplitFile) + ".RGB_color" + (getFilenameType VRSplitFile)
        logprint += ",\"extraElementRGB\":\""+elementFile+"\""
    )
    if (VRSplitAlpha == 1) and (alphaExist == 0) then
    (
        elementFile = (getFilenameFile VRSplitFile) + ".Alpha" + (getFilenameType VRSplitFile)
        logprint += ",\"extraElementAlpha\":\""+elementFile+"\""
    )
)
logprint += "}" 
----------------------------------AllfilePath-------------------------------------------------------------------
printlogs = ""
reportArray = #()
bitmapArray = getClassInstances BitmapTexture
for eachMap in bitmapArray do
(
    MapName = eachMap.filename
    if (MapName != undefined) do
    (
        appendIfunique reportArray (getFullResourcePath (MapName as string))
    )
)

textureList = #()
ATSOps.GetFiles &textureList
i = 1
for eachTex in textureList do
(
    appendIfunique reportArray (getFullResourcePath (eachTex as string))
)

----------------------------------ifl image file list-----------------------------------------------------------
addArray=""
for i=1 to reportArray.count do
(
    local theMetname = getFullResourcePath ((reportArray[i])as string)
    local IflArray=#()
    if ((getFilenameType theMetname)==".ifl") then
    (
        if(doesFileExist theMetname==true  ) do
        (
            IflFile=OpenFile (theMetname) mode:"r"
            i=1
            while ((eof iflFile)==false)do
            (
                IflArray[i]=readline IflFile
                i=i+1
            )
            close IflFile
        
            for IflMet in IflArray do
            (
                addArray=getFullResourcePath (IflMet as string)
                if (doesFileExist addArray == true) do
                    appendIfunique reportArray (addArray)
            )
        )
    )
    ------------------------------move vrmap to avoid repeat twice-----------------------
    else if((getFilenameType reportArray[i])==".vrmap")or((getFilenameType reportArray[i])==".vrlmap")or((getFilenameType reportArray[i])==".vrpmap")
    then reportArray[i]=""
)
    
--------------------------------------VR IR map seq------------------------------------------------------
if isCurrentVray do
(
    if ( renderers.current.gi_on == true ) do
    (
        if ( renderers.current.gi_primary_type==0) then 
        (
            IRmaps=#()
            if (renderers.current.adv_irradmap_mode==2 or renderers.current.adv_irradmap_mode==7 )
            then IRmap=renderers.current.adv_irradmap_loadFileName
            if IRmap==undefined
            then IRmap =""
            sequeceanalyze IRmaps IRmap 
            if IRmaps.count==0
            then sequeceanalyze IRmaps (maxFilePath+(filenameFromPath IRmap)) 
            if IRmaps.count !=0 then
                for imap in IRmaps do
                    appendIfunique reportArray imap
            else 
                appendIfunique reportArray IRmap
        )
        if ( renderers.current.gi_primary_type==3 or renderers.current.gi_secondary_type==3) then 
        (
            if renderers.current.lightcache_mode==2
            then LCmap=renderers.current.lightcache_loadFileName
            if(LCmap!="" and LCmap!=undefined ) do
            (
                if(doesFileExist LCmap==false and doesFileExist (maxFilePath+(filenameFromPath LCmap))==true )
                then LCmap=maxFilePath+(filenameFromPath LCmap)
                appendIfunique reportArray LCmap
            )
        )
        if ( renderers.current.gi_primary_type==1 or renderers.current.gi_secondary_type==1) then 
        (
            if renderers.current.photonMap_mode==1
            then PTmap=renderers.current.photonMap_loadFileName
            if(PTmap!="" and PTmap!=undefined ) do
            (
                if(doesFileExist PTmap==false and doesFileExist (maxFilePath+(filenameFromPath PTmap))==true )
                then PTmap=maxFilePath+(filenameFromPath PTmap)
                appendIfunique reportArray PTmap
            )
        )
        if ( renderers.current.caustics_on==true ) then 
        (
            if renderers.current.photonMap_mode==1
            then CTmap=renderers.current.caustics_loadFileName
            if(CTmap!="" and CTmap!=undefined ) do
            (
                if(doesFileExist CTmap==false and doesFileExist (maxFilePath+(filenameFromPath CTmap))==true )
                then CTmap=maxFilePath+(filenameFromPath CTmap)
                appendIfunique reportArray CTmap
            )
        )
    )
)    

----------------------------------------ForKrakatoa--------------------------------------------------------
if (((renderers.current.classid ) as string) == "#(-1204370534, -399920359)") do
(
    krakaarray=#()
    for o in objects do
        if ClassOf o == KrakatoaPRTLoader
        then appendIfunique krakaarray o
    if krakaarray.count!=0 do
    (
        for i=1 to krakaarray.count do
        (
            for p=1 to krakaarray[i].filelist.count do
            (
                theMetname = krakaarray[i].filelist[p]
                if (krakaarray[i].loadSingleFrame==off)
                then sequeceanalyze reportArray theMetname 
            )
        )    
    )
    KrakatoaDepthSequence=FranticParticles.GetProperty "Matte:DepthMapFiles"
    if(KrakatoaDepthSequence!=undefined and KrakatoaDepthSequence!="") do
    (
        theMetname=KrakatoaDepthSequence
        appendIfunique reportArray (theMetname as string)
        sequeceanalyze reportArray theMetname 
    )
)
------------------------------------analyse objects------------------------------------------------------------------------------------------------------
RFC=#()
RFT=#()
tpSystems=#()
fume=0
RealFlow=#()
PFcache=#()
phoenixprtarray=#()
phoenixsimarray=#()
Xmesh=#()
for o in objects do
(
    if ClassOf o == RF_Cache 
    then appendIfunique RFC o
    else if ClassOf o == RF_Trace 
    then appendIfunique RFT o
    else if ClassOf o == Thinking 
    then appendIfunique tpSystems o
    else if ClassOf o == FumeFX 
    then fume+=1
    else if ClassOf o == MeshLoader or ClassOf o == ParticleLoader 
    then appendIfunique RealFlow o
        else if ClassOf o == Cache_Disk 
    then appendIfunique PFcache o
    else if ClassOf o == PRTObject 
    then appendIfunique phoenixprtarray o
    else if ClassOf o == PHXSimulator 
    then appendIfunique phoenixsimarray o
    else if Classof o == FireSmokeSim 
    then appendIfunique phoenixsimarray o
    else if Classof o == LiquidSim 
    then appendIfunique phoenixsimarray o
    else if ClassOf o == XMeshLoader
    then appendIfunique Xmesh o
)

----------------------------------------Rayfire---------------------------------------------------------
for m in RFC do
  if m.filename != undefined do 
    appendIfunique reportArray (getFullResourcePath (m.filename as string))
for m in RFT do
  if m.bitmap!= undefined do 
    appendIfunique reportArray (getFullResourcePath ((trimleft (m.bitmap as string) "BitMap:")))
        
----------------------------------------ThinkingParticle---------------------------------------------------------
for curTP in tpSystems do
(
    local TpFilename=""
    for i=1 to (curTP.masterdynamic.DynamicSets.count)do
    (
        for j=1 to (curTP.masterdynamic.DynamicSets[i].Operators.count)do
        (
            try
                (
                    TpFilename=((curTP.masterdynamic.DynamicSets[i]).Operators[j]).filename
                )
            catch
                ( 
                    print "other InOutNode"
                )
        )
    )
    if (TpFilename!="") do 
        for Tp in TpFilename do
            sequeceanalyze reportArray Tp 
)

----------------------------------ForFumefx--------------------------------------------------------------------------------------------------------
if (fume!=0) do
(
    for i=1 to reportArray.count do
    (
        theMetname = (reportArray[i]) as string
        if (((getFilenameType theMetname)==".fxd") or ((getFilenameType theMetname)==".fim") or ((getFilenameType theMetname)==".fdc"))
        then sequeceanalyze reportArray theMetname 
    )
)

----------------------------------ForRealFlow--------------------------------------------------------------------------------------------------------
for i=1 to RealFlow.count do
(
    if ClassOf RealFlow[i] == MeshLoader 
    then theMetname = RealFlow[i].Path + RealFlow[i].Prefix
    else if ClassOf RealFlow[i] == ParticleLoader 
    then theMetname = RealFlow[i].binPath + "/" + RealFlow[i].binPrefix
    sequeceanalyze reportArray theMetname 
)

---------------------------------------forPFcache-------------------------------------------------------------------------------------------
for i=1 to PFcache.count do
(
    theMetname = PFcache[i].Write_To_File
    if theMetname!=undefined
    then sequeceanalyze reportArray theMetname 
)
------------------------------------ForPhoenixFD-----------------------------------------------------------------------------------------------------
for i=1 to phoenixprtarray.count do
(
    theMetname = phoenixprtarray[i].filesrc as string
    sequeceanalyze reportArray theMetname 
)    
for i=1 to phoenixsimarray.count do
(
    theMetname = phoenixsimarray[i].rendinput as string
    if (phoenixsimarray[i].rendinput=="$(same_as_output)" or phoenixsimarray[i].rendinput=="$(simoutput)")
    then theMetname = getFullResourcePath (phoenixsimarray[i].simoutput as string)
    if (theMetname=="$(scene_dir)" or theMetname == "$(implicit)")
    then theMetname=maxFilePath+maxFileName+"_Phoenix2_frames\ND"+phoenixsimarray[i].handle+"_"+phoenixsimarray[i]+"_####.aur"
    if(getFilenameType theMetname=="")
    then theMetname=theMetname+"_#.aur"
    theMetname=substring theMetname 1 (theMetname.count-4)
    xuhao=0
    while(theMetname[theMetname.count]=="#") do
        (
            xuhao+=1
            theMetname=substring theMetname 1 (theMetname.count-1)
        )
    for j=1 to xuhao do
        theMetname=theMetname+"0"
    theMetname=theMetname+".aur"
    appendIfunique reportArray (theMetname as string)
    sequeceanalyze reportArray theMetname 
)    

------------------------------------ForXmeshLoader--------------------------------------------------------------------------------------------------

for i=1 to Xmesh.count do
(
    Xrenderseq=Xmesh[i].renderSequence
    Xproxyseq=Xmesh[i].proxySequence
    if(Xmesh[i].autogenProxyPath==on ) do 
    (
        xmeshnamenum=getFilenameFile Xrenderseq
        xmeshname=substring xmeshnamenum 1 (xmeshnamenum.count-4)
        xmeshnum=substring xmeshnamenum (xmeshnamenum.count-3) xmeshnamenum.count
        Xproxyseq=getFilenamePath Xrenderseq +xmeshname+"_proxy\\"+xmeshname+"_proxy"+xmeshnum+getFilenameType Xrenderseq
    )
    if(Xmesh[i].loadSingleFrame == off) do
    (
        sequeceanalyze reportArray Xrenderseq 
        sequeceanalyze reportArray Xproxyseq 
    )
)

-------------------------------------------------------make files unique--------------------------------------------------------------------------------
for i=1 to reportArray.count do
(
    reportArray[i]=reportArray[i] as string
    tempstring=filterString reportArray[i] "\\"
    reportArray[i]=""
    for j in tempstring do
        reportArray[i]+=j+"/"
    reportArray[i]=substring reportArray[i] 1 (reportArray[i].count-1)
)
reportArray=makeUniqueArray reportArray


----------------------------------print analysis.json----------------------------------------------------------------------------------------------
FileArray=#()

phoenixfdaurArray=#()
vrmapArray=#()
IESfileArray=#()
particleprtArray=#()
fumefxfxdArray=#()
realflowArray=#()
PFcacheArray=#()
rayfirerfcArray=#()
geometryArray=#()
global missNum=0
global reportArrayNum=0
function printjson arrayname arrayprintname anatype=    --for diffrent type file to print 
(
    local fileprintarray=arrayname
    local filetruename=arrayprintname
    local filemissingnum=0
    local anaresult="[]"
    local analysetype=anatype
    global missNum
    global reportArrayNum
    if (fileprintarray.count!=0) do
    (
        anaresult="["
        for j=1 to fileprintarray.count do
        (
            isexist="found"
            if(doesFileExist fileprintarray[j]==false) do
            (
                if (doesFileExist (maxFilePath+(filenameFromPath fileprintarray[j])))==true then
                (
                    fileprintarray[j]=maxFilePath+(filenameFromPath fileprintarray[j])
                )
                else 
                (
                    isexist="missing"
                    filemissingnum+=1
                )
            )
            local fname=filenameFromPath fileprintarray[j]
            local fpath=getFilenamePath fileprintarray[j]
            for k=1 to fpath.count do
                if (fpath[k]=="\\") do
                    fpath[k]="/"
            if(analysetype=="Web")
            then anaresult+= ("{\"checkResult\":\""+isexist+"\",\"filename\":\""+fname+"\"}")
            else if (analysetype=="Client")
            then anaresult+= ("{\"checkResult\":\""+isexist+"\",\"path\":\""+fpath+"\",\"filename\":\""+fname+"\"}")
            if(fileprintarray[j]!=fileprintarray[fileprintarray.count]) 
            then anaresult+= ","
            else anaresult+= "]"
        )
        printlogs+= "\""+filetruename+"\":{"
        printlogs+="\"summary\":{"
        printlogs+="\"missingFiles\":\""+(filemissingnum as string)+"\","
        printlogs+="\"allFiles\":\""+(fileprintarray.count as string)+"\"},"
        printlogs+="\"files\":"
        printlogs+= anaresult 
        printlogs+= "}," 
    )    
    reportArrayNum+=fileprintarray.count
    missNum+=filemissingnum
)

for i=1 to reportArray.count do                              --set diffrent type file to diffrent array
( 
    if (reportArray[i]!=undefined and reportArray[i] != "undefined" and reportArray[i] != "" and filenameFromPath reportArray[i] != maxFileName and reportArray[i] !=rendOutputFilename ) do
    (    
        if(getFilenameType reportArray[i]==".aur")
        then(
            appendIfunique phoenixfdaurArray reportArray[i]
        )else if(getFilenameType reportArray[i]==".fxd" or getFilenameType reportArray[i]==".fdc" or getFilenameType reportArray[i]==".fim")
        then(
            appendIfunique fumefxfxdArray reportArray[i]
        )else if(getFilenameType reportArray[i]==".bin" or getFilenameType reportArray[i]==".rpc" or getFilenameType reportArray[i]==".pxy")
        then(
            appendIfunique realflowArray reportArray[i]
                )else if(getFilenameType reportArray[i]==".pfc" )
        then(
            appendIfunique PFcacheArray reportArray[i]
        )else if(getFilenameType reportArray[i]==".rfc" or getFilenameType reportArray[i]==".mat")
        then(
            appendIfunique rayfirerfcArray reportArray[i]
        )else if(getFilenameType reportArray[i]==".prt")
        then(
            appendIfunique particleprtArray reportArray[i]
        )else if(getFilenameType reportArray[i]==".obj" or getFilenameType reportArray[i]==".mesh" or getFilenameType reportArray[i]==".vrmesh" or getFilenameType reportArray[i]==".pts")
        then(
            appendIfunique geometryArray reportArray[i]
        )else if(getFilenameType reportArray[i]==".vrmap" or getFilenameType reportArray[i]==".vrlmap" or getFilenameType reportArray[i]==".vrpmap")
        then(
            appendIfunique vrmapArray reportArray[i]
        )else if(getFilenameType reportArray[i]==".ies" or getFilenameType reportArray[i]==".IES")
        then(
            appendIfunique IESfileArray reportArray[i]
        )else if(getFilenameType reportArray[i]!="")
        then(
            appendIfunique FileArray reportArray[i]
        )
    )
)

---------------------------------print every type files and close --------------------------------------------------------
printlogs+= ",\"analysis_log\":{"
printjson FileArray "Bitmap" Type
printjson vrmapArray "VR_GIMap" Type
printjson IESfileArray "IESfile" Type
printjson particleprtArray "ParticleFile" Type
printjson phoenixfdaurArray "PhoenixFDFile" Type
printjson fumefxfxdArray "FumefxFile" Type
printjson realflowArray "RealflowCache" Type
printjson PFcacheArray "PaticleFlowCache" Type
printjson rayfirerfcArray "RayfireFile" Type
printjson geometryArray "GeometryFile" Type

--------------------------------print global allFiles number and missingFiles number--------------------------------------------
printlogs+= "\"global\":{" 
printlogs+="\"missingFiles\":\""+(missNum as string)+"\","
printlogs+="\"allFiles\":\""+(reportArrayNum as string)+"\"}"

if (reportArrayNum!=0) 
then printlogs=substring printlogs 1 (printlogs.count-1)
if (reportArrayNum==0) 
then printlogs+="}}"
else printlogs+="}}}"
logprint += printlogs

---------------replace Invalid symbal--------------------------------
for k=1 to logprint.count do
(
    if (logprint[k]=="\\") 
    then logprint[k]="/"
    else if (logprint[k]=="	") 
    then logprint[k]="    "
)

-----------------------------CreatFile------------------------------
logFile= OpenFile (prjPath + "\analysis.log") mode:"w+" encoding:#utf8 writeBOM:false
format "%" logprint to:logfile
close logFile

-----------------------------------Kill 3dsmax Process--------------------------------------------------------------
((dotnetClass "System.Diagnostics.Process").GetCurrentProcess()).Kill()

-- a="\\192.168.128.50\\render\yume\\XMeshLoader\a0000.obj"
-- filenameFromPath a  "a0000.obj"
-- getFilenamePath a   "\192.168.128.50\render\yume\XMeshLoader\""
-- getFilenameFile a   "a0000"
-- getFilenameType a   ".obj"