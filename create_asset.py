# Copyright (C) 2026 Andrea Liliana Griffiths
# SPDX-License-Identifier: AGPL-3.0-only

import bpy, math, json
from mathutils import Vector
from pathlib import Path

ROOT=Path(__file__).parent
# Start clean; this file only authors the standalone experiment.
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for d in bpy.data.materials: bpy.data.materials.remove(d)

COLORS={
 'white':(.88,.82,.78,1),'pink':(.95,.3,.55,1),'gold':(1,.67,.2,1),
 'dark':(.13,.10,.16,1),'cyan':(.3,.77,.86,1),'purple':(.58,.35,.78,1),
 'red':(.96,.3,.36,1),'orange':(1,.52,.28,1),'yellow':(1,.82,.35,1),
 'green':(.36,.78,.5,1),'blue':(.3,.52,.88,1),'road':(.2,.22,.29,1),
 'grass':(.18,.38,.34,1),'rail':(.43,.48,.58,1)
}
mats={}
for n,c in COLORS.items():
 m=bpy.data.materials.new(n); m.diffuse_color=c; m.metallic=0; m.roughness=.82; mats[n]=m

def finish(o,n,mat,scale=None,rot=None):
 o.name='WEB_'+n
 if scale: o.scale=scale
 if rot: o.rotation_euler=rot
 o.data.materials.append(mats[mat]); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for p in o.data.polygons: p.use_smooth=True
 return o

def cube(n,loc,scale,mat,rot=None):
 bpy.ops.mesh.primitive_cube_add(location=loc); o=finish(bpy.context.object,n,mat,scale,rot)
 bevel=o.modifiers.new('finger-softened edges','BEVEL'); bevel.width=.12; bevel.segments=2
 bpy.context.view_layer.objects.active=o; bpy.ops.object.modifier_apply(modifier=bevel.name)
 return o
def ico(n,loc,scale,mat,sub=1):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=1,location=loc); return finish(bpy.context.object,n,mat,scale)
def cone(n,loc,r1,depth,mat,rot=None,verts=6):
 bpy.ops.mesh.primitive_cone_add(vertices=verts,radius1=r1,radius2=0,depth=depth,location=loc); return finish(bpy.context.object,n,mat,None,rot)
def cyl(n,loc,r,depth,mat,rot=None,verts=8):
 bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=depth,location=loc); o=finish(bpy.context.object,n,mat,None,rot)
 bevel=o.modifiers.new('soft clay rim','BEVEL'); bevel.width=.06; bevel.segments=2
 bpy.context.view_layer.objects.active=o; bpy.ops.object.modifier_apply(modifier=bevel.name)
 return o

# Kart, facing +Y. Deliberately low-poly and readable at game scale.
cube('chassis',(0,0,.38),(.82,1.38,.2),'pink',(.02,-.025,.018))
cube('nose',(0,1.24,.53),(.62,.42,.2),'cyan',(-.03,.02,-.015))
cube('seat',(0,-.38,.72),(.54,.48,.38),'purple',(.02,0,.025))
for x in (-.94,.94):
 for y in (-.82,.88): cyl(f'wheel_{x}_{y}',(x,y,.35),.38,.3,'dark',(0,math.pi/2,0))
# Unicorn driver: body/head/muzzle, ears, horn, mane and tail.
ico('body',(0,.05,1.13),(.5,.64,.66),'white')
ico('head',(.02,.58,1.83),(.47,.53,.5),'white')
ico('muzzle',(-.02,.98,1.69),(.35,.29,.25),'white')
cone('horn',(0,.73,2.42),.14,.85,'gold',(-.18,0,0),5)
cone('earL',(-.3,.53,2.24),.14,.38,'white',(-.18,0,-.18),5)
cone('earR',(.3,.53,2.24),.14,.38,'white',(-.18,0,.18),5)
for i,(z,col) in enumerate(zip((2.18,1.98,1.78,1.55),('red','yellow','green','blue'))):
 ico('mane'+str(i),(-.39,.28,z),(.14,.2,.2),col)
for x in (-.16,.16): ico('eye'+str(x),(x,1.045,1.94),(.045,.035,.06),'dark')
for i,col in enumerate(('red','orange','yellow','green','blue','purple')):
 cone('tail'+str(i),((i-2.5)*.055,-.76,1.34-i*.025),.075,.7,col,(math.pi/2+.35,0,0),5)
# Steering wheel.
cyl('steer',(0,.68,1.16),.28,.08,'dark',(math.pi/2,0,0),8)

# Track concept objects are kept in the .blend and preview, but excluded from compact web geometry.
def torus(name,major,minor,z,mat):
 bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=48,minor_segments=6,location=(0,0,z)); o=bpy.context.object; o.name=name; o.scale.y=.68; o.data.materials.append(mats[mat]); return o
torus('TRACK_road',7.0,1.55,0,'road')
torus('TRACK_outer_rail',8.48,.13,.2,'cyan')
torus('TRACK_inner_rail',5.52,.13,.2,'pink')
# Start stripe.
for i in range(8): cube('TRACK_start'+str(i),((i-3.5)*.38,-5.05,.08),(.18,.55,.04),'white' if i%2 else 'dark')

# Ground (preview only).
cube('GROUND',(0,0,-.3),(10,8,.25),'grass')
# Thumb-shaped cloud clumps make the authored scene explicitly claymation-like.
for ci,(cx,cy,cz) in enumerate(((-7,2,3.8),(6,4,4.5),(-3,6,5.2))):
 for j,(dx,dz,s) in enumerate(((-.65,0,.7),(0,.2,1),(.72,.02,.62))):
  ico(f'CLOUD_{ci}_{j}',(cx+dx,cy,cz+dz),(s,1.05*s,.62*s),'white')

# Export only WEB_ geometry after triangulation, quantized to centimeters.
asset=[]; tri_count=0; vert_count=0
for o in sorted((x for x in bpy.context.scene.objects if x.type=='MESH' and x.name.startswith('WEB_') and not x.name.startswith(('WEB_TRACK','WEB_GROUND','WEB_CLOUD'))),key=lambda x:x.name):
 me=o.data.copy(); me.transform(o.matrix_world); me.calc_loop_triangles()
 verts=[[round(v.co.x,2),round(v.co.y,2),round(v.co.z,2)] for v in me.vertices]
 faces=[list(t.vertices) for t in me.loop_triangles]
 color=list(o.data.materials[0].diffuse_color[:3])
 asset.append([verts,faces,[round(v*255) for v in color]])
 tri_count+=len(faces); vert_count+=len(verts); bpy.data.meshes.remove(me)
(ROOT/'game'/'kart.js').parent.mkdir(parents=True,exist_ok=True)
(ROOT/'game'/'kart.js').write_text('// Copyright (C) 2026 Andrea Liliana Griffiths\n// SPDX-License-Identifier: AGPL-3.0-only\nK='+json.dumps(asset,separators=(',',':')))
(ROOT/'asset-metrics.json').write_text(json.dumps({'objects':len(asset),'vertices':vert_count,'triangles':tri_count},indent=2))

# Preview camera and lights.
world=bpy.context.scene.world or bpy.data.worlds.new('World'); bpy.context.scene.world=world; world.color=(.015,.02,.045)
bpy.ops.object.camera_add(location=(11,-14,11)); cam=bpy.context.object; cam.data.lens=50; bpy.context.scene.camera=cam
def point_at(o,p): o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
point_at(cam,(0,0,.7))
bpy.ops.object.light_add(type='AREA',location=(-4,-4,10)); bpy.context.object.data.energy=1100; bpy.context.object.data.shape='DISK'; bpy.context.object.data.size=7
bpy.ops.object.light_add(type='AREA',location=(7,-2,5)); bpy.context.object.data.energy=700; bpy.context.object.data.color=(.3,.55,1); bpy.context.object.data.size=5
scene=bpy.context.scene; scene.render.engine='BLENDER_WORKBENCH'; scene.render.resolution_x=640; scene.render.resolution_y=480; scene.render.resolution_percentage=100
scene.display.shading.light='STUDIO'; scene.display.shading.color_type='MATERIAL'; scene.display.shading.show_shadows=True; scene.display.shading.show_cavity=True; scene.display.shading.cavity_type='WORLD'
scene.display.shading.background_type='WORLD'; scene.display.shading.show_specular_highlight=True
scene.render.image_settings.file_format='PNG'; scene.render.filepath=str(ROOT/'blender-preview.png'); scene.render.film_transparent=False
scene.view_settings.look='AgX - Medium High Contrast'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'rainbow-drift.blend'))
bpy.ops.render.render(write_still=True)
print(f'EXPORTED objects={len(asset)} vertices={vert_count} triangles={tri_count}')
