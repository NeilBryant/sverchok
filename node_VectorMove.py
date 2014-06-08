import bpy
from node_s import *
from util import *
from mathutils import Vector, Matrix

class VectorMoveNode(Node, SverchCustomTreeNode):
    ''' Vector Move vectors '''
    bl_idname = 'VectorMoveNode'
    bl_label = 'Vectors Move'
    bl_icon = 'OUTLINER_OB_EMPTY'
    
    mult_ = bpy.props.FloatProperty(name='multiplier', default=1.0, options={'ANIMATABLE'}, update=updateNode)
    
    def init(self, context):
        self.inputs.new('VerticesSocket', "vertices", "vertices")
        self.inputs.new('VerticesSocket', "vectors", "vectors")
        self.inputs.new('StringsSocket', "multiplier", "multiplier").prop_name='mult_'
        self.outputs.new('VerticesSocket', "vertices", "vertices")
        

    def update(self):
        # inputs
        if 'vertices' in self.inputs and self.inputs['vertices'].links and \
            type(self.inputs['vertices'].links[0].from_socket) == VerticesSocket:
            vers_ = SvGetSocketAnyType(self,self.inputs['vertices'])
            vers = Vector_generate(vers_)
        else:
            vers = []
        
        if 'vectors' in self.inputs and self.inputs['vectors'].links and \
            type(self.inputs['vectors'].links[0].from_socket) == VerticesSocket:
   
            vecs_ = SvGetSocketAnyType(self,self.inputs['vectors'])
            vecs = Vector_generate(vecs_)
        else:
            vecs = []
            
        if 'multiplier' in self.inputs and self.inputs['multiplier'].links and \
            type(self.inputs['multiplier'].links[0].from_socket) == StringsSocket:

            mult = SvGetSocketAnyType(self,self.inputs['multiplier'])
        else:
            mult = [[1.0]]
        
        # outputs
        if 'vertices' in self.outputs and self.outputs['vertices'].links:
           mov = self.moved(vers, vecs, mult)
           SvSetSocketAnyType(self,'vertices',mov)
    
    def moved(self, vers, vecs, mult):
        r = len(vers) - len(vecs)
        rm = len(vers) - len(mult)
        moved = []
        if r > 0:
            vecs.extend([vecs[-1] for a in range(r)])
        if rm > 0:
            mult.extend([mult[-1] for a in range(rm)])
        for i, ob in enumerate(vers):       # object
            d = len(ob) - len(vecs[i])
            dm = len(ob) - len(mult[i])
            if d > 0:
                vecs[i].extend([vecs[i][-1] for a in range(d)])
            if dm > 0:
                mult[i].extend([mult[i][-1] for a in range(dm)])
            temp = []
            for k, vr in enumerate(ob):     # vectors
                #print('move',str(len(ob)), str(len(vecs[i])), str(vr), str(vecs[i][k]))
                v = ((vr + vecs[i][k]*mult[i][k]))[:]
                temp.append(v)   #[0]*mult[0], v[1]*mult[0], v[2]*mult[0]))
            moved.append(temp)
        #print ('move', str(moved))
        return moved
                
    def update_socket(self, context):
        self.update()


    

def register():
    bpy.utils.register_class(VectorMoveNode)
    
def unregister():
    bpy.utils.unregister_class(VectorMoveNode)

if __name__ == "__main__":
    register()
