from fipy import CellVariable, TransientTerm, DiffusionTerm, LinearGMRESSolver, ImplicitSourceTerm
from variablevals import *
from fipy import dump
from mpi4py import MPI
import petsc4py
petsc4py.init()
from petsc4py import PETSc
import os
import sys
import gc


print("+++++++++++++++++",sys.argv)
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

fileDirx = dump.read('foldername.dat')
# Define paths relative to the output directory
# fileDir = os.path.join(fileDirx,)
meshfile = os.path.join(fileDirx, "TMP", "mesh.dat")

# Ensure the directories exist
os.makedirs(os.path.dirname(meshfile), exist_ok=True)

# Load the mesh file
mesh = dump.read(meshfile)
# Define the center of the mesh
X, Y = mesh.faceCenters
# Define the boundaries of the domain
boundariesall = ((mesh.facesBottom & (X < boundaryat))|(mesh.facesTop & (X > nx-boundaryat)) | (mesh.facesRight & (Y > ny-boundaryat)) | (mesh.facesLeft & (Y < boundaryat)))


# Define the Variables being solved
il8 = dump.read(os.path.join(fileDirx, "TMP", 'cytokine_il8.dat'))
il1 = dump.read(os.path.join(fileDirx, "TMP", 'cytokine_il1.dat'))
il6 = dump.read(os.path.join(fileDirx, "TMP", 'cytokine_il6.dat'))
il10 = dump.read(os.path.join(fileDirx, "TMP", 'cytokine_il10.dat'))
tnf = dump.read(os.path.join(fileDirx, "TMP", 'cytokine_tnf.dat'))
tgf = dump.read(os.path.join(fileDirx, "TMP", 'cytokine_tgf.dat'))


# il8 = CellVariable(mesh = mesh,value= il8)
# il1 = CellVariable(mesh = mesh,value= il1)
# il6 = CellVariable(mesh = mesh,value= il6)
# il10 = CellVariable(mesh = mesh,value= il10)
# tnf = CellVariable(mesh = mesh,value= tnf)
# tgf = CellVariable(mesh = mesh,value= tgf)

valueboundaries = 0.0

# Constrain the variables within bounds
il8.constrain(valueboundaries, boundariesall)
il1.constrain(valueboundaries, boundariesall)
il6.constrain(valueboundaries, boundariesall)
il10.constrain(valueboundaries, boundariesall)
tnf.constrain(valueboundaries, boundariesall)
tgf.constrain(valueboundaries, boundariesall)

# Define thee solver used
mysolver=LinearGMRESSolver()

# Reading the variables
cellpresente = dump.read(fileDirx + "/" + 'TMP' + '/' + 'cellpresent_e.dat')
cellpresentndn = dump.read(fileDirx + "/" + 'TMP' + '/' + 'cellpresent_ndn.dat')
cellpresentna = dump.read(fileDirx + "/" + 'TMP' + '/' + 'cellpresent_na.dat')
cellpresentm1 = dump.read(fileDirx + "/" + 'TMP' + '/' + 'cellpresent_m1.dat')
cellpresentm2 = dump.read(fileDirx + "/" + 'TMP' + '/' + 'cellpresent_m2.dat')

# Define the equations
eqil8 = TransientTerm() == DiffusionTerm(coeff=Dil8) - ImplicitSourceTerm(muil8) + keil8*cellpresente + kndnil8*cellpresentndn - ImplicitSourceTerm(thetanail8*cellpresentna)
eqil1 = TransientTerm() == DiffusionTerm(coeff=Dil1) - ImplicitSourceTerm(muil1) + knail1*cellpresentna
eqil6 = TransientTerm() == DiffusionTerm(coeff=Dil6) - ImplicitSourceTerm(muil6) + km1il6*cellpresentm1
eqil10 = TransientTerm() == DiffusionTerm(coeff=Dil10) - ImplicitSourceTerm(muil10) + km2il10*cellpresentm1
eqtnf = TransientTerm() == DiffusionTerm(coeff=Dtnf) - ImplicitSourceTerm(mutnf) + knatnf*cellpresentna + km1tnf*cellpresentm1
eqtgf = TransientTerm() == DiffusionTerm(coeff=Dtgf) - ImplicitSourceTerm(mutgf) + km2tgf*cellpresentm2

# Solve for the duration(dt)
# for i in range(fipy_duration):
gc.collect()  
eqil8.solve(var= il8, dt=1.0,solver=mysolver)
eqil1.solve(var= il1, dt=1.0,solver=mysolver)
eqil6.solve(var= il6, dt=1.0,solver=mysolver)
eqil10.solve(var= il10, dt=1.0,solver=mysolver)
eqtnf.solve(var= tnf, dt=1.0,solver=mysolver)
eqtgf.solve(var= tgf, dt=1.0,solver=mysolver)

print (rank, len(mesh.cellCenters[0]), len(il8))



# dump.write(mesh, meshfile)
dump.write(il8, os.path.join(fileDirx, "TMP", 'cytokine_il8.dat'))
dump.write(il1, os.path.join(fileDirx, "TMP", 'cytokine_il1.dat'))
dump.write(il6, os.path.join(fileDirx, "TMP", 'cytokine_il6.dat'))
dump.write(il10, os.path.join(fileDirx, "TMP", 'cytokine_il10.dat'))
dump.write(tnf, os.path.join(fileDirx, "TMP", 'cytokine_tnf.dat'))
dump.write(tgf, os.path.join(fileDirx, "TMP", 'cytokine_tgf.dat'))
