Parallelization of Spatial Immune Response after Burn Injury simulations


Authors:Roland V. Bumbuc<sup>1,2,3</sup>*, Vivek M. Sheraton<sup>3</sup>†

Affiliations:

1.Department of Plastic, Reconstructive and Hand Surgery, Amsterdam Movement Sciences (AMS) Institute, Amsterdam UMC, Location VUmc, Amsterdam, The Netherlands

2.Department of Molecular Cell Biology and Immunology, Amsterdam Infection and Immunity (AII) Institute, Amsterdam UMC, Location VUmc, Amsterdam, The Netherlands

3.Computational Science Lab, Informatics Institute, University of Amsterdam, UvA - LAB42, Amsterdam, The Netherlands


Correspondence:
Vivek M. Sheraton (v.s.muniraj@uva.nl)

Keywords:
Burn wound immune response, Cytokine dynamics, Spatial modeling, Parallel computing, CompuCell3D, FiPy, Agent-based models, Mathematical modeling, Immune system simulation, Partial differential equations


Burn injuries are marked by a prolonged and intricate inflammatory response that can last for months, making it essential to understand and predict their dynamics to improve treatment strategies
and outcomes. In this study, we explored post-burn immune response simulations using a hybrid model combining Finite volume and Cellular Potts model-based methods We analyze complementary parallelization 
strategies employed using CompuCell3D (CC3D) and MPI. Three unique parallelization strategies were explored, namely fully serial, partly parallel, and fully parallel combinations of CC3D-MPI implementations.
The simulation results provide critical insight into the performance of the model simulations for varying endothelial cell counts and processor numbers. The parallelized version consistently reduced the 
runtime by an average of 45 % compared to the partially parallel computations, demonstrating its effectiveness in handling larger workloads.

## Software Implementation

All source code(`Code`) used to generate the results and figures in the paper can be accessed by contacting the original authors. The calculations and figure generation are all run in Python 3.10. 


## Getting the Figures and Code

You can download a copy of all the files in this repository by cloning the repository:

git clone https://github.com/youwillfindinfinity/ICCS-project.git

or by clicking on `Code` > `Download ZIP`.

The figures and text are open source. The authors reserve the rights to the article content.

CompuCell3D v4.4.1 for cellular automata

FiPy v3.4.4 for PDE-based cytokine dynamics

MPI4Py v3.1.4 for distributed memory parallelization

Benchmark results and scaling analyses are stored in a Results directory hidden in this repository, raw data can be requested by sending an email to r.v.bumbuc@uva.nl
