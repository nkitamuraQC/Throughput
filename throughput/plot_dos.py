###
import plotclass


def plot_dos_(filename_list, outname, choice1=2, choice2=5, range_=[-10,0], fermi_list=None):
    dos_list = []
    e_list = []
    count = 0
    for fn in filename_list:
        fermi = fermi_list[count]
        e, dos = read_dos(fn, choice1=choice1, choice2=choice2, range_=range_, fermi=fermi)
        dos_list.append(dos)
        e_list.append(e)
        count += 1
    #print(dos_list)
    #print(e_list)
    length = range_[1] - range_[0]
    pltcls = plotclass.plotclass()
    np = 10
    pltcls.print_xlabel = [i * length / np + range_[0] for i in range(np)]
    pltcls.legend = orb_list
    pltcls.plot_all([e_list[0]], dos_list, labelx="energy",labely="DOS",filename=outname)
    return

def plot_dos(filename_list, orb_list, outname, choice1=2, choice2=5, range_=[-10,0], fermi_list=None):
    dos_list = []
    e_list = []
    count = 0
    for fn in filename_list:
        fermi = fermi_list[count]
        e, dos, _ = read_dos(fn, choice1=choice1, choice2=choice2, range_=range_, fermi=fermi)
        dos_list.append(dos)
        e_list.append(e)
        count += 1
    #print(dos_list)
    #print(e_list)
    length = range_[1] - range_[0]
    pltcls = plotclass.plotclass()
    np = 10
    pltcls.print_xlabel = [i * length / np + range_[0] for i in range(np)]
    pltcls.legend = orb_list
    pltcls.plot_all([e_list[0]], dos_list, labelx="Energy (eV)",labely="PDOS",filename=outname)
    return

def read_dos(fn, choice1=2, choice2=5, range_=None, fermi=None):
    rf = open(fn, "r")
    lines = rf.readlines()
    e_ret = []
    dos_ret = []
    integral = 0.0
    for i in range(1,len(lines)):
        e = float(lines[i].split()[0]) - fermi
        _ = lines[i].split()[1]
        dos_ = lines[i].split()[choice1:choice2]
        val = 0.0
        for i in range(len(dos_)):
            val += float(dos_[i])
        #dos = []
        #dos.append(val)
        tmp = []
        if e > range_[0] and e < range_[1]:
            e_ret.append(e)
            dos_ret.append(val)
            #print(val)
            #tmp.append(sum(dos_))
    integral += sum(dos_ret)
    return e_ret, dos_ret, integral

def find(val, list_):
    for i in range(len(list_)):
        if list_[i] == val:
            break
    return i


def main():
    import os
    #choice = [2, 3, 4]
    fermi_list = [3.5972,3.6789,3.8181,3.9987,3.0010,3.2285,3.5934]
    atom = [54]
    #outname = "DOS_F2p_{orb}_{choice}_{atom}.png"
    outname = "DOS_F2p_ALL_59_fermi_wide.png"  
    cwd = os.getcwd()
    name = "pdos.dat.pdos_atm#59(F)_wfc#2(p)"
    wd1 = "{cwd}/PF6/".format(cwd=cwd) + name
    wd2 = "{cwd}/AsF6/".format(cwd=cwd) + name
    wd3 = "{cwd}/SbF6/".format(cwd=cwd) + name
    wd4 = "{cwd}/TaF6/".format(cwd=cwd) + name
    filename_list = [wd1, wd2, wd3, wd4]
    orb_list = [r"PF$_6$ F 2p$_y$ orbital", r"AsF$_6$ F 2p$_y$ orbital", r"SbF$_6$ F 2p$_y$ orbital", r"TaF$_6$ F 2p$_y$ orbital"]
    count = 0
    plot_dos(filename_list, orb_list, outname, fermi_list=fermi_list, range_=[-10.0, 0.0])
    return



def main2_fermi():
    import os
    #choice = [2, 3, 4]
    fermi_list = [3.5972,3.6789,3.8181,3.9987,3.0010,3.2285,3.5934]
    atom = [54]
    #outname = "DOS_F2p_{orb}_{choice}_{atom}.png"
    outname = "DOS_F2p_ALL_59_fermi_ver2.png"  
    cwd = os.getcwd()
    name = "pdos.dat.pdos_atm#59(F)_wfc#2(p)"
    name_ = "pdos.dat.pdos_atm#56(F)_wfc#2(p)"
    _name = "pdos.dat.pdos_atm#56(O)_wfc#2(p)"
    wd1 = "{cwd}/PF6/".format(cwd=cwd) + name
    wd2 = "{cwd}/AsF6/".format(cwd=cwd) + name
    wd3 = "{cwd}/SbF6/".format(cwd=cwd) + name
    wd4 = "{cwd}/TaF6/".format(cwd=cwd) + name
    wd5 = "{cwd}/BF4/".format(cwd=cwd) + name_
    wd6 = "{cwd}/ClO4/".format(cwd=cwd) + _name
    wd7 = "{cwd}/ReO4/".format(cwd=cwd) + _name
    filename_list = [wd1, wd2, wd3, wd4, wd5, wd6, wd7]
    orb_list = [r"PF$_6$ F 2p$_y$ orbital", r"AsF$_6$ F 2p$_y$ orbital", r"SbF$_6$ F 2p$_y$ orbital", r"TaF$_6$ F 2p$_y$ orbital","","",""]
    count = 0
    plot_dos_log(filename_list, orb_list, outname, fermi_list=fermi_list, range_=[-0.8,0.2])
    return



if __name__ == "__main__":
    #main2()
    main()
    main2_fermi()
