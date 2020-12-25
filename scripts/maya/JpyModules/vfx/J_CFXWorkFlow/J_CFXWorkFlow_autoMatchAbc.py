    # -*- coding:utf-8 -*-
    ##  @package public
    #
    ##  @brief   自动导入abc并适配
    ##  @author 桔
    ##  @version 1.0
    ##  @date   15:47 2020/12/24
    #  History:  
    import maya.mel as mel
    import maya.cmds as cmds
    import maya.api.OpenMaya as om2
    import json,math,os
    import JpyModules
    #选择所有动画控制曲线，和要导出的模型
    def J_CFXWorkFlow_autoMatchAbc():
        mdAbcFile = cmds.fileDialog2(fileMode=1, caption="Import clothInfo")[0]
        if mdAbcFile=='':
            return
        sourceMeshs=J_getAllMeshUnderSelections(cmds.ls(sl=True))
        prFxName=os.path.basename(mdAbcFile).replace('.abc','')
        abcNode=''
        if cmds.objExists(prFxName+'_mdCache'):
            cmds.delete(prFxName+'_mdCache')
        groupNode=cmds.createNode('transform',name=(prFxName+'_mdCache'))
                
        if  mdAbcFile  is not None:
            abcNode=mel.eval('AbcImport -mode import -reparent '+groupNode+' \"'+mdAbcFile +'\";')
        allAbcMeshs=cmds.listConnections(abcNode,type='mesh')
        allAnimationMesh=[]
        for meshItem in allAbcMeshs:
            if cmds.polyEvaluate(meshItem,shell=True) >1:
                separateMeshs=cmds.polySeparate(meshItem)

                for separateMeshItem in separateMeshs:   
                    if cmds.objectType(separateMeshItem,isType='polySeparate'):
                        continue
                    allAnimationMesh.append(separateMeshItem)    
            else:
                allAnimationMesh.append(meshItem)  
                
        for meshItem in allAnimationMesh:       
            for sourceMeshItem in sourceMeshs :
                abcMeshVn=cmds.polyEvaluate(meshItem,vertex=True)
                sourceMeshVn=cmds.polyEvaluate(sourceMeshItem,vertex=True)
                abcFPP=cmds.xform((meshItem+'.vtx[0]'),query=True,ws=True,t=True) 
                sourceFPP=cmds.xform((sourceMeshItem+'.vtx[0]'),query=True,ws=True,t=True)
                if abcMeshVn==sourceMeshVn and math.fabs(abcFPP[0]-sourceFPP[0])<0.01 and math.fabs(abcFPP[1]-sourceFPP[1])<0.01:        
                    print 'xxx'             
                    cmds.transferAttributes(meshItem,sourceMeshItem,transferPositions=1,transferNormals=0,transferUVs=0 ,transferColors=0 ,sampleSpace=4 ,sourceUvSpace="map1" ,targetUvSpace="map1",searchMethod=3,flipUVs=0,colorBorders=1 )

    def J_getAllMeshUnderSelections(selectedNodes):
        allMesh=[]
        for item in selectedNodes:
            J_getChildNodes(item,allMesh)
        allMeshParents=[]
        for item in allMesh:
            if cmds.listRelatives(item,fullPath=True,parent=True)[0]!=None:
                allMeshParents.append(cmds.listRelatives(item,fullPath=True,parent=True)[0])
        return allMeshParents
    #递归找mesh
    def J_getChildNodes(currentNode,meshList):   
        childNodes=cmds.listRelatives(currentNode,fullPath=True,children=True)
        for item in childNodes:
            if cmds.objectType( item, isType='mesh' ):
                if cmds.getAttr((item+".intermediateObject"))==0:
                    meshList.append(item)
            if cmds.objectType( item, isType='transform' ):
                J_getChildNodes(item,meshList)
                
    if __name__=='__main__':
        J_CFXWorkFlow_autoMatchAbc()