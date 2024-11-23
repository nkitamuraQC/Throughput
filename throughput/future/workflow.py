from pylat.crystal_lattice import SpaceGroupSupplement
from pylat.lattice_model import LatticeModel_gen
from pylat.qe_controller import QEController
from pylat.respack import RESPACKController
from throughput.determine_window_from_dos import (
    for_single_dos,
    convert_to_fortran_notation,
)
import os


def get_window(qe, target_wan):
    pdos_prefix = qe.prefix + ".pdos_atm"
    starts = []
    ends = []
    for fname in os.listdir():
        if pdos_prefix in fname:
            for k, v in target_wan.items():
                v = v.lower()
                if k in fname and v in fname:
                    if v == "d":
                        target_start = 2
                        target_end = 7
                    if v == "p":
                        target_start = 2
                        target_end = 5
                    s, e = for_single_dos(
                        fname, target_start=target_start, target_end=target_end
                    )
                    starts.append(s)
                    ends.append(e)
    start = convert_to_fortran_notation(min(starts))
    end = convert_to_fortran_notation(max(ends))
    return start, end


def get_initial_guess(qe, target_wan, gauss=0.2):
    o_dic = {"d": ["dxy", "dyz", "dzx", "dz2", "dx2"], "p": ["px", "py", "pz"]}
    init_guess = []
    for idx, at in enumerate(qe.geoms):
        orbs = o_dic[target_wan[at[0]].lower()]
        tmp = []
        for orb in orbs:
            tmp.append([idx, orb, gauss])
        init_guess += tmp
    return init_guess


def get_n_wannier(qe, target_wan):
    n_dic = {"d": 5, "p": 3}
    n_wannier = 0
    for at in qe.geoms:
        if at[0] in target_wan:
            n_wannier += n_dic[target_wan[at[0]].lower()]
    return n_wannier


def main(cifname, pseudo_dict, target_wan):
    qe = QEController(cifname, pseudo_dict)
    inp = qe.make_input()
    qe.write_input(inp)
    qe.exec()
    qe.exec_dos()
    qe.exec_pdos()

    ## calculation.pdos_atm#1(Fe)_wfc#4(d)
    start, end = get_window(qe, target_wan)
    n_wannier = get_n_wannier(qe, target_wan)
    init_guess = get_initial_guess(qe, target_wan)

    res = RESPACKController(qe)
    res.Lower_energy_window = start
    res.Upper_energy_window = end
    res.N_wannier = n_wannier
    res.gauss = init_guess
    res.N_initial_guess = len(init_guess)
    res.prepare()
    res.execusion()
    return


if __name__ == "__main__":
    cif = ""
    pseudo_dict = {
        "Fe": "Fe.pbe-spn-kjpaw_psl.1.0.0.UPF",
        "Se": "Se.pbe-dn-kjpaw_psl.1.0.0.UPF",
    }
    target_wan = {"Fe": "d"}
    main(cif, pseudo_dict, target_wan)
