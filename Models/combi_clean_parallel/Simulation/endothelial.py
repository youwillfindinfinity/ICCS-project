from cc3d import CompuCellSetup
from variablevals import *      
from endothelialSteppables import endothelialSteppable
from cc3d.core.PySteppables import SteppableBasePy


def configure_simulation(relaxationmcs, nx, ny, max_steps):
    from cc3d.core.XMLUtils import ElementCC3D
    # Create the root element for CompuCell3D XML
    xml_3d = ElementCC3D("CompuCell3D", {"Revision": "20210612", "Version": "4.2.5"})
    
    # Metadata
    metadata = xml_3d.ElementCC3D("Metadata")
    metadata.ElementCC3D("NumberOfProcessors", {}, 14)
    metadata.ElementCC3D("DebugOutputFrequency", {}, relaxationmcs)

    # Potts Section
    potts = xml_3d.ElementCC3D("Potts")
    potts.ElementCC3D("Dimensions", {"x": nx, "y": ny, "z": 1})
    potts.ElementCC3D("Steps", {}, max_steps)
    potts.ElementCC3D("Temperature", {}, 100.0)
    potts.ElementCC3D("NeighborOrder", {}, 1)
    potts.ElementCC3D("Boundary_x", {}, "Periodic")
    potts.ElementCC3D("Boundary_y", {}, "Periodic")

    # CellType Plugin
    cell_type_plugin = xml_3d.ElementCC3D("Plugin", {"Name": "CellType"})
    cell_types = [
        (0, "Medium"),
        (1, "endothelial"),
        (2, "neutrophil"),
        (3, "monocyte"),
        (4, "fibroblast"),
        (5, "neutrophila"),
        (6, "neutrophilndn"),
        (7, "monocyter"),
        (8, "macrophage1"),
        (9, "macrophage2"),
        (10, "myofibroblast"),
    ]
    for cell_type in cell_types:
        cell_type_plugin.ElementCC3D("CellType", {"TypeId": cell_type[0], "TypeName": cell_type[1]})

    # CenterOfMass Plugin
    xml_3d.ElementCC3D("Plugin", {"Name": "CenterOfMass"})

    # PixelTracker Plugin
    xml_3d.ElementCC3D("Plugin", {"Name": "PixelTracker"})

    # Contact Plugin
    contact_plugin = xml_3d.ElementCC3D("Plugin", {"Name": "Contact"})
    types = [t[1] for t in cell_types]
    
    for i in range(len(types)):
        for j in range(i, len(types)):
            energy = 10.0 if i == 0 or j == 0 else 100.0
            contact_plugin.ElementCC3D("Energy", {"Type1": types[i], "Type2": types[j]}, energy)
    
    contact_plugin.ElementCC3D("NeighborOrder", {}, 4)

    # Connectivity Plugin
    connectivity_plugin = xml_3d.ElementCC3D("Plugin", {"Name": "Connectivity"})
    connectivity_plugin.ElementCC3D("Penalty", {}, 10000000)

    # DiffusionSolverFE Steppable
    diffusion_solver = xml_3d.ElementCC3D("Steppable", {"Type": "DiffusionSolverFE"})
    diffusion_field = diffusion_solver.ElementCC3D("DiffusionField", {"Name": "cytokine"})
    
    diffusion_data = diffusion_field.ElementCC3D("DiffusionData")
    diffusion_data.ElementCC3D("FieldName", {}, "cytokine")
    diffusion_data.ElementCC3D("GlobalDiffusionConstant", {}, 0.0)
    diffusion_data.ElementCC3D("GlobalDecayConstant", {}, 0)

    # Chemotaxis Plugin
    chemotaxis_plugin = xml_3d.ElementCC3D("Plugin", {"Name": "Chemotaxis"})
    chemotaxis_plugin.ElementCC3D("ChemicalField", {"Name": "cytokine"})

    # Set the simulation XML description
    CompuCellSetup.set_simulation_xml_description(xml_3d)


    
configure_simulation(relaxationmcs, nx, ny, max_steps)    

CompuCellSetup.register_steppable(steppable=endothelialSteppable(frequency=relaxationmcs))


        
from endothelialSteppables import celldivisionSteppable
CompuCellSetup.register_steppable(steppable=celldivisionSteppable(frequency=int(relaxationmcs)))


CompuCellSetup.run()
