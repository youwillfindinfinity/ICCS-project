from cc3d.core.PySteppables import *
from cc3d.core.XMLUtils import ElementCC3D

def configure_simulation(relaxationmcs, nx, ny, max_steps):
    # Create root XML element
    compucell3d_xml = ElementCC3D("CompuCell3D", {"Revision": "20210612", "Version": "4.2.5"})

    # Metadata
    metadata = compucell3d_xml.ElementCC3D("Metadata")
    metadata.ElementCC3D("NumberOfProcessors", {}, "8")
    metadata.ElementCC3D("DebugOutputFrequency", {}, "10")

    # Potts Section
    potts = compucell3d_xml.ElementCC3D("Potts")
    potts.ElementCC3D("Dimensions", {"x": "500", "y": "500", "z": "1"})
    potts.ElementCC3D("Steps", {}, max_steps)
    potts.ElementCC3D("Temperature", {}, "100.0")
    potts.ElementCC3D("NeighborOrder", {}, "1")
    potts.ElementCC3D("Boundary_y", {}, "Periodic")
    potts.ElementCC3D("Boundary_x", {}, "Periodic")

    # Cell Types Plugin
    cell_type_plugin = compucell3d_xml.ElementCC3D("Plugin", {"Name": "CellType"})
    cell_type_plugin.ElementCC3D("CellType", {"TypeId": "0", "TypeName": "Medium"})
    cell_type_plugin.ElementCC3D("CellType", {"Freeze": "", "TypeId": "1", "TypeName": "endothelial"})
    cell_type_plugin.ElementCC3D("CellType", {"TypeId": "2", "TypeName": "neutrophil"})
    cell_type_plugin.ElementCC3D("CellType", {"TypeId": "3", "TypeName": "monocyte"})
    cell_type_plugin.ElementCC3D("CellType", {"TypeId": "4", "TypeName": "fibroblast"})
    cell_type_plugin.ElementCC3D("CellType", {"TypeId": "5", "TypeName": "neutrophila"})
    cell_type_plugin.ElementCC3D("CellType", {"TypeId": "6", "TypeName": "neutrophilndn"})
    cell_type_plugin.ElementCC3D("CellType", {"TypeId": "7", "TypeName": "monocyter"})
    cell_type_plugin.ElementCC3D("CellType", {"TypeId": "8", "TypeName": "macrophage1"})
    cell_type_plugin.ElementCC3D("CellType", {"TypeId": "9", "TypeName": "macrophage2"})
    cell_type_plugin.ElementCC3D("CellType", {"TypeId": "10", "TypeName": "myofibroblast"})

    # CenterOfMass Plugin
    compucell3d_xml.ElementCC3D("Plugin", {"Name": "CenterOfMass"})

    # PixelTracker Plugin
    compucell3d_xml.ElementCC3D("Plugin", {"Name": "PixelTracker"})

    # Contact Plugin
    contact_plugin = compucell3d_xml.ElementCC3D("Plugin", {"Name": "Contact"})
    
    # Adhesion energies (example for Medium and endothelial)
    contact_plugin.ElementCC3D("Energy", {"Type1": "Medium", "Type2": "Medium"}, 10.0)
    contact_plugin.ElementCC3D("Energy", {"Type1": "Medium", "Type2": "endothelial"}, 10.0)
    
    # Add all other energy terms as needed (similar to XML)

    contact_plugin.ElementCC3D("NeighborOrder", {}, 4)

    # Connectivity Plugin
    connectivity_plugin = compucell3d_xml.ElementCC3D("Plugin", {"Name": "Connectivity"})
    connectivity_plugin.ElementCC3D("Penalty", {}, 10000000)

    # DiffusionSolverFE Steppable
    diffusion_solver = compucell3d_xml.ElementCC3D("Steppable", {"Type": "DiffusionSolverFE"})
    
    diffusion_field = diffusion_solver.ElementCC3D("DiffusionField", {"Name": "cytokine"})
    
    diffusion_data = diffusion_field.ElementCC3D("DiffusionData")
    
    diffusion_data.ElementCC3D("FieldName", {}, 'cytokine')
