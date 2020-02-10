# -*- coding: utf-8 -*-
"""
main routine
It can be called either through a filepath (see below)
or in a batch mode as well as directly from the GUI interface
"""
import sys
import json
from DiscreteLatticeMechCore import Solver, Writer


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Usage: {} <input filename (json)>".format(sys.argv[0]))
        # sys.exit(1)
        filepath = 'Inputs/InputData_SquareEx.json'
    else:
        filepath = sys.argv[1]

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except IOError as error:
        print("could not open input file {}".format(filepath))
        sys.exit(1)

    """
    # an example of how data can be defined as a dictionary and passed to the solver
    data = {
        "NumberElements": 10,
        "e_1": [1, 0],
        "e_2": [0.5, 0.866],
        "e_3": [-0.5, 0.866],
        "e_4": [0.866, -0.5],
        "e_5": [-0.866, -0.5],
        "e_6": [-0.5, -0.866],
        "e_7": [-0.5, 0.866],
        "e_8": [0.866, -0.5],
        "e_9": [0.866, 0.5],
        "e_10": [0, 1],
        "Y_1": [1, 0],
        "Y_2": [0, 1],
        "NumberNodes": 8,
        "Ob": [1, 3, 2, 8, 7, 7, 6, 4, 3, 5],
        "Eb": [2, 2, 8, 5, 5, 1, 1, 6, 4, 4],
        "Delta1": [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        "Delta2": [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        "Ka": [21, 21, 21, 21, 21, 21, 21, 21, 21, 21],
        "Kb": [0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21],
        "Lb": [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        "tb": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "L1": 17.3205,
        "L2": 17.3205
    }
    """
    print(json.dumps(data, indent=4, sort_keys=False))

    solver = Solver()
    solver.solve(data)

    # Write to file
    writer = Writer()
    writer.WriteTensorsToFile(solver.InputData, solver.CMatTensor, solver.FlexMatTensor)
    writer.WriteEffectivePropertiesToFile(solver.Bulk, solver.Ex, solver.Ey, solver.Poissonyx, solver.Poissonxy, solver.G, solver.rho)
    writer.PlotEffectiveProperties(solver.Bulk, solver.Ex, solver.Ey, solver.Poissonyx, solver.Poissonxy, solver.G)
