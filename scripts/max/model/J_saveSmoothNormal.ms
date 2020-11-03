model=selection
print model
--kkk=#()
maxOps.cloneNodes model[1] cloneType:#copy newNodes:&kkk
 
print kkk

addmodifier kkk[1] (Normalmodifier ())
kkk[1].modifiers[#Normal].unify = on

	