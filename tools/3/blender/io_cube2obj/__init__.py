# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
bl_info = {
    "name": "Wavefront OBJ exporter for Sauerbraten/Cube2/Tesseract",
    "author": "angjminer with code borrowed from Campbell Barton ,wavefront obj exporter",
    "blender": (2, 5, 8),
    "location": "File > Import-Export",
    "description": "Export OBJ, Export obj.cfg, "
                   "",
    "warning": "",
    #"wiki_url": "",
    "tracker_url": "",
    #"support": 'OFFICIAL',
    #"support": 'TESTING',    
    "category": "Import-Export-Cube2"}


import os
import time
import bpy
import mathutils
import bpy_extras.io_utils
def export_cfg(scene, filepath, objname):
    source_dir = os.path.dirname(bpy.data.filepath)
    dest_dir = os.path.dirname(filepath)

    file = open(filepath, "w", encoding="utf8", newline="\n")
    fw = file.write

    fw('// Blender cube2 : %r\n' % (os.path.basename(filepath) or "None"))#(os.path.basename(bpy.data.filepath) or "None"))
    fw('//this is a basic cfg file to get you going\n')
    fw('\n')
    fw('//dont forget to load the model in your map cfg. eg:\n')
    fw('//mapmodelreset\n')
    fw('//   mapmodel "3/dev/pomcube"//starting from but not including media/model/mapmodel/ "your/file/folder"\n')
    fw('\n')
    fw('objload %s\n\n' % objname) 
    for ob in bpy.data.objects:
        if ob.select:
            for mat in ob.material_slots[:]:
                for mtex in mat.material.texture_slots:#reversed(mat.material.texture_slots):
                    if mtex and mtex.texture.type == 'IMAGE':
                        image = mtex.texture.image
                        if image:
                            if mtex.use_map_color_diffuse:
                                print('found dif')
                                fw('objskin %s %s//the diffuse texture\n' % (ob.name, image.filepath[2:]))
                            if mtex.use_map_specular:
                                fw('objspec %s %s\n' % (ob.name, image.filepath[2:]))
                            if mtex.use_map_normal:
                                fw('objbumpmap %s %s//your normalmap\n' % (ob.name, image.filepath[2:]))
                                fw('//objparamap %s %s//uncomment if you are using the "3" fork of tesseract, heightmap should be in the alpha channel of the normalmap\n' % (ob.name, image.filepath[2:]))
                    #else:
                        #fw('#fixme/no image in material slot# objskin %s "image name"\n' % ob.name)
                        #fw('\n')
    fw('\n')            
    fw('//here are some commonly used commands along with default values\n')
    fw('//uncomment to enable\n')
    fw('\n')
    fw('//mdlparascale 0.05 10 0//uncomment if you are using the "3" fork of tesseract and have paramap enabled above, scale(0.05) should be between 0.09 and 0.009, steps/passes(10) should be kept under 20, (0) is unused atm.\n')
    fw('//mdlcullface 1//1 enable 0 disable\n')
    fw('//mdlcolor 1 1 1//red green blue, you can over bright, but generally from 0 to 1\n')
    fw('//mdlcollide 1//if set to 0 your model will not obstruct movement, use to add detail that the player wont get caught on\n')
    fw('//mdltricollide 0//if set to 1 collision detection will be a closer match to you models shape\n')
    fw('//mdlspec 1.0//control specularity amount\n')
    fw('//mdlspin 0 0 0// spin along z, spin along y, spin along x  make model spin\n')
    fw('//mdlscale 100//scale model to this percent\n')
    fw('//mdltrans 0 0 0// translate the model the much from origin in xyz\n')
    fw('//mdlyaw 0//translate the model along z axis\n')
    fw('//mdlpitch 0//translate the model along y axis\n')
    fw('//mdlroll 0//translate the model along x axis\n')
    fw('\n')
    fw('//Cant find what you need?\n')
    fw('//check out the docs\n')
    fw('//http://sauerbraten.org/docs/models.html\n')

def write_some_data(filepath, objects, scene, write_cfg):
    print("Exporting Cube2 OBJ")
    file = open(filepath, 'w', encoding='utf-8')
    fw = file.write
    #the following code is from the wavefront obj exporter by Campbell Barton trimed down to the bare min by angjminer
    global_scale = 22
    axis_forward = 'X'
    axis_up = 'Y'
    from mathutils import Matrix
    global_matrix = Matrix()

    global_matrix[0][0] = \
    global_matrix[1][1] = \
    global_matrix[2][2] = global_scale

    global_matrix = (global_matrix * axis_conversion(to_forward=axis_forward, to_up=axis_up, ).to_4x4())    
    
    
    
    
    
    
    
    
    
    def veckey3d(v):
        return round(v.x, 6), round(v.y, 6), round(v.z, 6)
    #borrowed from obj exporter modified by angelo j miner
    def veckey3d2(v):
        #return round(v.x, 6), round(v.y, 6), round(v.z, 6)
        return round(v.x/32767.0), round(v.y/32767.0), round(v.z/32767.0)
    #def veckey3d2(v):
        #return v.x, v.y, v.z
    #def veckey3d21(v):
        #return round(v.x, 6), round(v.y, 6), round(v.z, 6)
    def veckey3d3(vn,fn):
        facenorm=fn
        return round((facenorm.x*vn.x)/2), round((facenorm.y*vn.y)/2), round((facenorm.z*vn.z)/2)      

    def veckey2d(v):
        return round(v[0], 6), round(v[1], 6)
    time1 = time.time()
    fw('#wavefornt obj file for cube2 engine\n')    
    #exporting cfg part will be here
    #if EXPORT_CFG:
    mtlfilepath = "%s/obj.cfg" % os.path.dirname(filepath)
    print('OBJ.cfg Export path: %r' % mtlfilepath)
    objname = "%s" % (os.path.basename(filepath))
    print('OBJname: %r' % (os.path.basename(filepath)))        


    # Initialize totals, these are updated each object
    totverts = totuvco = totno = 1

    face_vert_index = 1

    globalNormals = {}

    # A Dict of Materials
    # (material.name, image.name):matname_imagename # matname_imagename has gaps removed.
    mtl_dict = {}

    copy_set = set()

    # Get all meshes
    for ob_main in objects: 
        # ignore dupli children
        if ob_main.parent and ob_main.parent.dupli_type in {'VERTS', 'FACES'}:
            # XXX
            print(ob_main.name, 'is a dupli child - ignoring')
            continue    
        obs = []   
        if ob_main.dupli_type != 'NONE':
            # XXX
            print('creating dupli_list on', ob_main.name)
            ob_main.dupli_list_create(scene)

            obs = [(dob.object, dob.matrix) for dob in ob_main.dupli_list]

            # XXX debug print
            print(ob_main.name, 'has', len(obs), 'dupli children')
        else:
            obs = [(ob_main, ob_main.matrix_world)]

        for ob, ob_mat in obs:
            try:
                me = ob.to_mesh(scene, True, 'PREVIEW')
            except RuntimeError:
                me = None

            if me is None:
                continue
            me.transform(global_matrix * ob_mat)
            faceuv = len(me.uv_textures) > 0
            if faceuv:
                uv_layer = me.tessface_uv_textures.active.data[:]
            else:
                faceuv = False
            me_verts = me.vertices[:]

            # Make our own list so it can be sorted to reduce context switching
            face_index_pairs = [(face, index) for index, face in enumerate(me.tessfaces)]
            # faces = [ f for f in me.tessfaces ]
            edges = []
            if not (len(face_index_pairs) + len(edges) + len(me.vertices)):  # Make sure there is somthing to write

                # clean up
                bpy.data.meshes.remove(me)

                continue  # dont bother with this mesh.   
            #normals stuff
            #if EXPORT_NORMALS and face_index_pairs:
                #me.calc_normals()

            materials = me.materials[:]
            material_names = [m.name if m else None for m in materials]

            # avoid bad index errors
            if not materials:
                materials = [None]
                material_names = [""]         
            if faceuv:
                face_index_pairs.sort(key=lambda a: (a[0].material_index, hash(uv_layer[a[1]].image), a[0].use_smooth))
            elif len(materials) > 1:
                face_index_pairs.sort(key=lambda a: (a[0].material_index, a[0].use_smooth))
            else:
                # no materials
                face_index_pairs.sort(key=lambda a: a[0].use_smooth)
            # Set the default mat to no material and no image.
            contextMat = 0, 0  # Can never be this, so we will label a new material the first chance we get.
            contextSmooth = None  # Will either be true or false,  set bad to force initialization switch.
            fw('o %s\n' % ob.name)  # Write Object name
            # Vert
            for v in me_verts:
                fw('v %.6f %.6f %.6f\n' % v.co[:])
            # UV
            if faceuv:
                # in case removing some of these dont get defined.
                uv = uvkey = uv_dict = f_index = uv_index = None

                uv_face_mapping = [[0, 0, 0, 0] for i in range(len(face_index_pairs))]  # a bit of a waste for tri's :/

                uv_dict = {}  # could use a set() here
                uv_layer = me.tessface_uv_textures.active.data
                for f, f_index in face_index_pairs:
                    for uv_index, uv in enumerate(uv_layer[f_index].uv):
                        uvkey = veckey2d(uv)
                        try:
                            uv_face_mapping[f_index][uv_index] = uv_dict[uvkey]
                        except:
                            uv_face_mapping[f_index][uv_index] = uv_dict[uvkey] = len(uv_dict)
                            fw('vt %.6f %.6f\n' % uv[:])

                uv_unique_count = len(uv_dict)

                del uv, uvkey, uv_dict, f_index, uv_index
                # Only need uv_unique_count and uv_face_mapping
            #normals    
            for f, f_index in face_index_pairs:
                if f.use_smooth:
                    for v_idx in f.vertices:
                        v = me_verts[v_idx]
                        noKey = veckey3d2(v.normal)
                        if noKey not in globalNormals:
                            globalNormals[noKey] = totno
                            totno += 1
                            fw('vn %.6f %.6f %.6f\n' % noKey)
                else:
                    # Hard, 1 normal from the face.
                    noKey = veckey3d(f.normal)
                    if noKey not in globalNormals:
                        globalNormals[noKey] = totno
                        totno += 1
                        fw('vn %.6f %.6f %.6f\n' % noKey)
            fw('g %s\n' % ob.name)            
            if not faceuv:
                f_image = None
            for f, f_index in face_index_pairs:
                f_smooth = f.use_smooth
                f_mat = min(f.material_index, len(materials) - 1)

                if faceuv:
                    tface = uv_layer[f_index]
                    f_image = tface.image

                # MAKE KEY
                if faceuv and f_image:  # Object is always true.
                    key = material_names[f_mat], f_image.name
                else:
                    key = material_names[f_mat], None  # No image, use None instead.
                contextMat = key    

                if f_smooth != contextSmooth:
                    if f_smooth:  # on now off
                        fw('s 1\n')
                        contextSmooth = f_smooth
                    else:  # was off now on
                        fw('s off\n')
                        contextSmooth = f_smooth
                f_v_orig = [(vi, me_verts[v_idx]) for vi, v_idx in enumerate(f.vertices)]
                #if not EXPORT_TRI or len(f_v_orig) == 3:
                #if not len(f_v_orig) == 3:
                f_v_iter = (f_v_orig, )
                #else:
                    #f_v_iter = (f_v_orig[0], f_v_orig[1], f_v_orig[2]), (f_v_orig[0], f_v_orig[2], f_v_orig[3])

                # support for triangulation
                for f_v in f_v_iter:
                    fw('f')

                    if faceuv:
                        #if EXPORT_NORMALS:
                        if f_smooth:  # Smoothed, use vertex normals
                            for vi, v in f_v:
                                fw(" %d/%d/%d" %
                                           (v.index + totverts,
                                            totuvco + uv_face_mapping[f_index][vi],
                                            globalNormals[veckey3d2(v.normal)],
                                            ))  # vert, uv, normal

                        else:  # No smoothing, face normals
                          no = globalNormals[veckey3d(f.normal)]
                          for vi, v in f_v:
                             fw(" %d/%d/%d" % (v.index + totverts, totuvco + uv_face_mapping[f_index][vi], no, ))  # vert, uv, normal
                        #else:  # No Normals
                            #for vi, v in f_v:
                                #fw(" %d/%d" % (
                                    #     v.index + totverts,
                                        #   totuvco + uv_face_mapping[f_index][vi],
                                         #  ))  # vert, uv

                        face_vert_index += len(f_v)

                    else:  # No UV's
                        #if EXPORT_NORMALS:
                        if f_smooth:  # Smoothed, use vertex normals
                            for vi, v in f_v:
                                fw(" %d//%d" % ( v.index + totverts, globalNormals[veckey3d2(v.normal)], ))
                        else:  # No smoothing, face normals
                            no = globalNormals[veckey3d(f.normal)]
                            for vi, v in f_v:
                               fw(" %d//%d" % (v.index + totverts, no))
                       #else:  # No Normals
                           #for vi, v in f_v:
                               #fw(" %d" % (v.index + totverts))

                    fw('\n')










    file.close()
    if write_cfg:
      export_cfg(scene, mtlfilepath, objname)
    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import (ExportHelper, axis_conversion)
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportSomeData(Operator, ExportHelper):
    '''This appears in the tooltip of the operator and in the generated docs'''
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export OBJ"

    # ExportHelper mixin class uses this
    filename_ext = ".obj"

    filter_glob = StringProperty(
            default="*.obj",
            options={'HIDDEN'},
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
  
    write_cfg = BoolProperty(
            name="Write OBJ.CFG",
            description="Write Basic cfg file",
            default=True,
            )

    #type = EnumProperty(
            #name="Example Enum",
            #description="Choose between two items",
            #items=(('OPT_A', "First Option", "Description one"),
                   #('OPT_B', "Second Option", "Description two")),
            #default='OPT_A',
            #)
  
    def execute(self, context):
    # Exit edit mode before exporting, so current object states are exported properly.

       objects = context.selected_objects
   
       scene = context.scene
       return write_some_data(self.filepath, objects, scene, self.write_cfg)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportSomeData.bl_idname, text="export cube2 obj")


def register():
    bpy.utils.register_class(ExportSomeData)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportSomeData)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')
