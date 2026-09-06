# OpenFOAM_CHT_HeatExachanger

# Conjugate Heat Transfer Between Hot Oil and Cold Water Using OpenFOAM

## Overview

This project investigates **conjugate heat transfer (CHT)** between a hot oil stream and a cold water stream using **OpenFOAM 12**.

The geometry consists of a **three-dimensional cylindrical heat-transfer system** in which hot oil flows through the inner cylindrical region while cold water flows through the surrounding outer region.

The objective of the simulation is to study the coupled behaviour of:

* Fluid flow in the oil region
* Fluid flow in the water region
* Convective heat transfer within both fluids
* Heat transfer between the hot and cold streams
* Temperature development along the length of the system

The project is intended as a practical demonstration of multi-region thermal-fluid modelling using OpenFOAM.

---

# Commands To Run
* `blockMesh`
* `topoSet`
* `splitMeshRegions -cellZonesOnly -overwrite`
* `decomposePar -allRegions`
* `mpirun -np 4 foamMultiRun -parallel`

---

# Physical Configuration

The computational domain consists of two fluid regions:

### Region 1 — Hot Oil

The inner cylindrical region contains hot oil.

* Inner fluid radius: **0.05 m**
* Fluid: **Oil**
* Inlet temperature: **400 K**
* Inlet velocity: **0.05 m/s**

The relatively low oil velocity provides a longer residence time inside the heat-transfer region, allowing the oil to exchange heat with the surrounding cooling water.

### Region 2 — Cooling Water

The outer cylindrical region contains cold water and surrounds the oil region.

* Outer radius: **0.10 m**
* Fluid: **Water**
* Inlet temperature: **278 K**
* Inlet velocity: **1.0 m/s**

The higher water velocity continuously supplies relatively cold water to the heat-transfer region and transports absorbed thermal energy downstream.

---

# Geometry

The heat-transfer section has the following dimensions:

| Parameter           |      Value |
| ------------------- | ---------: |
| Total pipe length   | **0.75 m** |
| Outer system radius | **0.10 m** |
| Inner system radius | **0.05 m** |

The inner cylindrical domain represents the hot-oil flow region, while the surrounding annular domain represents the cooling-water region.

---

# Operating Conditions

The principal operating conditions used in the simulation are:

| Parameter          |     Oil — Region 1 |     Water — Region 2 |
| ------------------ | -----------------: | -------------------: |
| Fluid              |                Oil |                Water |
| Inlet temperature  |          **400 K** |            **278 K** |
| Inlet velocity     |       **0.05 m/s** |          **1.0 m/s** |
| Flow region        |     Inner cylinder | Outer annular region |
| Heat-transfer role |          Hot fluid |        Cooling fluid |

This relatively large temperature difference provides the driving force for heat transfer between the two streams.

---

As the fluids move through the heat-transfer section:

* The **oil temperature decreases**
* The **water temperature increases**
* The temperature difference between the fluids gradually decreases downstream

The resulting outlet temperatures depend on the fluid properties, flow velocities, residence times, geometry, and heat-transfer characteristics.

---

# Why Different Flow Velocities Are Used

The oil and water streams are intentionally assigned different inlet velocities.

### Oil: 0.05 m/s

The relatively low oil velocity increases its residence time inside the heat-transfer section.

A longer residence time gives the hot oil more opportunity to transfer energy to the surrounding cooling medium.

### Water: 1.0 m/s

The cooling water moves considerably faster.

This allows heated water to be transported away from the heat-transfer surface while relatively cold water continuously enters the system.

The velocity difference therefore produces very different thermal and hydrodynamic behaviour in the two regions.

---

# Numerical Model

The simulation is performed using:

* **OpenFOAM 12**
* Finite Volume Method (FVM)
* Three-dimensional computational domain
* Multi-region fluid and thermal modelling
* Temperature-dependent energy transport
* Velocity and pressure solution in the fluid regions
* Coupled thermal interaction between regions

The main quantities solved and analysed include:

* Velocity, \(U\)
* Pressure, \(p\)
* Temperature, \(T\)

---

# Boundary Conditions

## Oil Inlet

```text
Velocity    = 0.05 m/s
Temperature = 400 K
```

The inlet supplies hot oil to the inner cylindrical region.

## Oil Outlet

The oil leaves the computational domain through the downstream outlet.

The outlet boundary permits the developed flow and temperature field to leave the domain.

## Water Inlet

```text
Velocity    = 1.0 m/s
Temperature = 278 K
```

Cold water enters the outer region and absorbs thermal energy from the hot-oil region.

## Water Outlet

The heated cooling water leaves the computational domain through the corresponding outlet.

---

# Post-Processing

Simulation results are analysed using **Paraview** and Python-based post-processing tools.

---

# Project Objectives

The main objectives of this project are to:

1. Build a complete three-dimensional heat-transfer geometry using OpenFOAM.
2. Create separate computational regions for oil and water.
3. Define thermophysical properties and boundary conditions.
4. Simulate coupled fluid-flow and heat-transfer behaviour.
5. Analyse the temperature evolution of both fluids.
6. Evaluate outlet temperatures and heat-transfer performance.
7. 
8. Develop a reusable workflow for multi-region thermal simulations in OpenFOAM.

---

# Repository Structure

A typical case structure is:

```text
OpenFOAM-CHT-Heat-Transfer/
├──SameDirectionFlow
│	│
│	├── 0/
│   │   ├── region1/
│   │   │ 	└── Initial and boundary conditions
│   │	├── region2/
│   │   │ 	└── Initial and boundary conditions
│   │	└── pipeWall/
│   │    	└── Initial and boundary conditions
│	│
│	├── constant/
│   │	├── polyMesh/
│   │	├── region1/
│   │   │ 	└── Thermophysical and turbulent properties
│   │ 	├──	region2/
│   │   │ 	└── Thermophysical and turbulent properties
│   │ 	└──	pipeWall/
│   │    	└── Thermophysical properties
│	│
│	└── system/
│   	├── region1/
│       │	├── fvSchemes
│       │	└── fvSolution
│   	├── region2/
│       │	├── fvSchemes
│       │	└── fvSolution
│   	├── pipeWall/
│       │	├── fvSchemes
│       │	└── fvSolution
│   	├── blockMeshDict
│   	├── topoSetDict
│   	├── controlDict
│   	├── decomposeParDict
│   	├── fvSchemes
│   	└── fvSolution
│
├──OppositeDirectionFlow
│	│
│	├── 0/
│   │   ├── region1/
│   │   │ 	└── Initial and boundary conditions
│   │	├── region2/
│   │   │ 	└── Initial and boundary conditions
│   │	└── pipeWall/
│   │    	└── Initial and boundary conditions
│	│
│	├── constant/
│   │	├── polyMesh/
│   │	├── region1/
│   │   │ 	└── Thermophysical and turbulent properties
│   │ 	├──	region2/
│   │   │ 	└── Thermophysical and turbulent properties
│   │ 	└──	pipeWall/
│   │    	└── Thermophysical properties
│	│
│	└── system/
│   	├──region1/
│       │	├── fvSchemes
│       │	└── fvSolution
│   	├──region2/
│       │	├── fvSchemes
│       │	└── fvSolution
│   	├──pipeWall/
│       │	├── fvSchemes
│       │	└── fvSolution
│   	├── blockMeshDict
│   	├── topoSetDict
│   	├── controlDict
│   	├── decomposeParDict
│   	├── fvSchemes
│   	└── fvSolution
│
├── scripts/
│   └── Python post-processing tools
│
├── images/
│   └── Geometry and simulation results
│
├── README.md
│
└── .gitignore
```

---

# Software

* **OpenFOAM 12**
* **ParaView**
* **Python**
* **Linux** 

Python may be used for automated extraction and visualisation of quantities such as temperature versus time and temperature at different points in any region.

Can be run using the command 
`python3 plot_temperature_vs_time.py --point coordiantes --region regionName` 

For example: `python3 plot_temperature_vs_time.py --point -0.25 0 0 --region pipeWall`

---

# Future Work

Possible extensions of the project include:

* Comparison of parallel-flow and counter-flow configurations
* Investigation of different oil and water velocities
* Reynolds-number analysis
* Laminar versus turbulent flow comparison
* Different wall materials
* Mesh-independence studies
* Comparison with analytical heat-exchanger correlations
* Investigation of the influence of different oil and water velocities.

---

# Author

**Satya Sai Phani Santosh Pilaka**

