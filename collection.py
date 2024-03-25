import numpy as np
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from pandas import ExcelFile
import xlrd
import datetime

# make 3 overlapping ones and change the boarders
location1 = "C:\\Users\\Dell\\Desktop\\Academic\\Comp_Sci\\SRP\\data\\dataset_gen2.0.xlsx"
location2 = "C:\\Users\\Dell\\Desktop\\Academic\\Comp_Sci\\SRP\\data\\dataset_gen2.1.xlsx"
location3 = "C:\\Users\\Dell\\Desktop\\Academic\\Comp_Sci\\SRP\\data\\dataset_gen2.2.xlsx"


def y_axis(loc):
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell(0, 0)
    data_points = []
    length = int(sheet.cell_value(0, 4))
    for line in range(1, length, int(length / 100)):
        ratios = sheet.cell_value(line, 0)[1:-1].split(', ')
        ratio = int(ratios[-1]) / sum([int(ratios[0]), int(ratios[1]), int(ratios[2])])
        data_points.append(ratio*100)
    final = sheet.cell_value(int(sheet.cell_value(0, 4)), 0)[1:-1].split(', ')
    ratio = int(final[-1]) / sum([int(final[0]), int(final[1]), int(final[2])])
    data_points.append(ratio*100)
    return data_points


def x_axis(location):
    wb = xlrd.open_workbook(location)
    sheet = wb.sheet_by_index(0)
    sheet.cell(0, 0)
    length = int(sheet.cell_value(0, 4))
    x = np.arange(1, length + int(length / 100) + 1, int(length / 100))
    return x


def plotting_gen(l1, l2, l3):
    fig = plt.figure()
    plt.plot(x_axis(l1), y_axis(l1), 'b')
    plt.plot(x_axis(l2), y_axis(l2), 'b')
    plt.plot(x_axis(l3), y_axis(l3), 'b')
    plt.axis([0, 10000, 25, 55])
    plt.ylabel('Tying Percentage')
    plt.xlabel('Runs')
    plt.show()
    time = str(datetime.datetime.now()).replace(':', '').replace(' ', '_').split('.')[0]
    fig.savefig(f'data_{time}', bbox_inches='tight')  # how to set a name for every point?


# dangerous: do not open unless u wanna fix this
# def dont_mind_this_crudeness():
#     l1 = [0.38888888888888884, 0.1908175456562553, 0.193167701863354, 0.13716890264877882, 0.1497543461829176,
#           0.1313352826510721, 0.12004298495526565, 0.11225455276088186, 0.1089110354885756, 0.1162819896196111,
#           0.12188973033028618, 0.10697528278173439, 0.07839412915279968, 0.07060794044665013, 0.05794245142351162,
#           0.050461687772787304]
#     l2 = [0.24603174603174602, 0.16436251920122888, 0.13368983957219252, 0.1302542867760259, 0.09882437823614294, 0.08900226757369616, 0.09279367421569257, 0.0964306514685082, 0.08059942782658744, 0.08282840442464856, 0.08041085840058694, 0.07487296445976464, 0.07667247400071828, 0.07006022717298313, 0.06043809195931901, 0.05331937292207173]
#     l3 = [0.2253968253968254, 0.21093285799168152, 0.17779933481152996, 0.17616161616161619, 0.13744588744588745, 0.11282550814987986, 0.0925275582869964, 0.09789321789321788, 0.10422820467106436, 0.08746221337462212, 0.09383243100269478, 0.08942061094958903, 0.08664883834809402, 0.0879884399409232, 0.06650140958904009, 0.05241747218111862]
#     x_ax = np.arange(0, 10000, 100)
#     l_1 = []
#     l_2 = []
#     l_3 = []
#     for rate in l1:
#         for appended in range(int(100/len(l1))):
#             l_1.append(rate)
#     l_1.append(l1[-1])
#     l_1.append(l1[-1])
#     l_1.append(l1[-1])
#     l_1.append(l1[-1])
#     for rate in l2:
#         for appended in range(int(100/len(l2))):
#             l_2.append(rate)
#     l_2.append(l2[-1])
#     l_2.append(l2[-1])
#     l_2.append(l2[-1])
#     l_2.append(l2[-1])
#     for rate in l3:
#         for appended in range(int(100/len(l3))):
#             l_3.append(rate)
#     l_3.append(l3[-1])
#     l_3.append(l3[-1])
#     l_3.append(l3[-1])
#     l_3.append(l3[-1])
#     fig = plt.figure()
#     plt.plot(x_ax, l_1, 'g')
#     plt.plot(x_ax, l_2, 'g')
#     plt.plot(x_ax, l_3, 'g')
#     plt.axis([0, 10000, 0, 1])
#     plt.ylabel('Tying Percentage')
#     plt.xlabel('Runs')
#     plt.show()
#     time = str(datetime.datetime.now()).replace(':', '').replace(' ', '_').split('.')[0]
#     fig.savefig(f'data_{time}', bbox_inches='tight')  #


loc1 = input('loc 1: ')
loc2 = input('loc 2: ')
loc3 = input('loc 3: ')
plotting_gen(loc1, loc2, loc3)
# plotting_gen(location1, location2, location3)

