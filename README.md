Parallelization and Optimization of Spatial Immune Response Simulations in Burn Wound Healing
Authors:
Roland V. Bumbuc<sup>1,2,3,4</sup>*, Vivek M. Sheraton<sup>3,4</sup>†

Affiliations:

Department of Plastic, Reconstructive and Hand Surgery, Amsterdam Movement Sciences (AMS) Institute, Amsterdam UMC, Location VUmc, Amsterdam, The Netherlands

Department of Molecular Cell Biology and Immunology, Amsterdam Infection and Immunity (AII) Institute, Amsterdam UMC, Location VUmc, Amsterdam, The Netherlands

Computational Science Lab, Informatics Institute, University of Amsterdam, UvA - LAB42, Amsterdam, The Netherlands

Center for Experimental and Molecular Medicine (CEMM), Amsterdam UMC, Amsterdam, The Netherlands

Correspondence:
Vivek M. Sheraton (v.s.muniraj@uva.nl)

Keywords:
Burn wound immune response, Cytokine dynamics, Spatial modeling, Parallel computing, CompuCell3D, FiPy, Agent-based models, Mathematical modeling, Immune system simulation, Partial differential equations

This work will be submitted to the International Conference on Computational Science (ICCS) 2025.

Abstract
Background: Spatial computational models of immune responses to burn injuries require intricate coupling of agent-based frameworks (e.g., CompuCell3D) and partial differential equation solvers (e.g., FiPy). However, these simulations are computationally intensive, necessitating optimized parallelization strategies for scalability.

Purpose: This study aims to develop and benchmark parallelization protocols for burn wound immune response simulations, focusing on computational efficiency and scalability in hybrid agent-PDE models.

Methods: We optimized the parallelization of cytokine dynamics by decoupling spatial PDE solutions from cellular agent interactions. Simulations were run across multiple processor configurations (1–128 cores) using MPI and hybrid OpenMP/MPI approaches. Key performance metrics included total simulation time, scaling efficiency, and workload distribution.

Results: Our parallelization strategy achieved a 4.4x speedup at 16 processors and 45% runtime reduction compared to serial implementations. Optimal performance was observed at 32–64 processors for large-scale simulations (>5000 cells). Decoupling cytokine PDE resolution reduced communication overhead by 38%, enabling efficient scaling on supercomputing architectures.

Conclusion: This work establishes robust parallel computing guidelines for spatial immune response models, significantly enhancing simulation throughput for burn wound healing studies. The proposed optimization framework facilitates large-scale, high-fidelity simulations of immune-cell-cytokine interactions in biologically realistic scenarios.

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
