import sys
import os
    
import maya.cmds as cmds

proj_path = r"E:\Varwin\EducationPacks\UnityProjects\EduPacks\Assets\Medieval\SceneInfo.txt"

class Content():

    def __init__(self, material, texture, color, mesh, fbx):

        self.material = material
        self.texture = texture
        self.color = color
        self.mesh = mesh
        self.fbx = fbx

def read_unity_project(path):

    project = open(path, "r")

    content_list = []
    for line in project.readlines():
        lst = line.split(";")
        material = lst[0]
        MainTex = lst[1]
        if lst[1] == "null":
            MainTex = None
        
        Color = lst[2].split("|")
        if lst[2]=="null":
            Color = "1|1|1|1".split("|")
        
        mesh = lst[3]
        fbx = lst[4].replace("\n","")

        content_list.append(Content(material, MainTex, Color, mesh, fbx))

    project.close()

    return content_list


def processing_file(filepath):

    cmds.file(filepath, i=True, mergeNamespacesOnClash=True, namespace=':')
    
    objects = []
    for obj in cmds.ls(objectsOnly=True):
        if cmds.objectType(obj, isType="transform"):
            try:
                cmds.parent(obj, world=True)
                print(obj)
            except:
                pass
        objects.append(obj)

    cmds.file(filepath, ea=True, type="FBX", force=True)

    for obj in objects:
        try:
            cmds.delete(obj)
        except:
            pass


content = read_unity_project(proj_path)
# alternative
# content = get_project_models(proj_path)

for i in content:
    fbx_path = i.fbx
    processing_file(fbx_path)

