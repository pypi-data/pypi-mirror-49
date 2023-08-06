from tkinter import *
from tkinter import filedialog as fd

import pandas

from TSW_IWR import *
from X4_parser import *
from X4_threshold import *
from imu_extract import *
from xyz_calc import *
import webbrowser

window = Tk()
window.title('Lidar Data Extraction Tool')

menubar = Menu(window)
file_menu = Menu(menubar, tearoff=0)
lidar_extract_menu = Menu(menubar, tearoff=0)
IMU_extract_menu = Menu(menubar, tearoff=0)
xyz_cartesian = Menu(menubar, tearoff=0)
X4 = Menu(menubar, tearoff=0)
TSW = Menu(menubar, tearoff=0)

menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Lidar Extract", menu=lidar_extract_menu)
menubar.add_cascade(label="IMU Extract", menu=IMU_extract_menu)
menubar.add_cascade(label="Lidar XYZ Calulator", menu=xyz_cartesian)
menubar.add_cascade(label="Novelda X4", menu=X4)
menubar.add_cascade(label="TSW IWR-1642", menu=TSW)


label_font = ('times', 20, 'bold')
Label(window, text="Welcome to CUDRDC lidar data extraction tool", font=label_font).place(x=50, y=25)


def print_list(lst):
    """
    Takes in an array and prints it to textbox.

    Parameters:

        lst: list
            A list object of the data that will be read to user.
    """
    t.delete('1.0', END)
    t.place(x=75, y=250, height=300, width=200)
    for x in lst:
        t.insert(END, str(x) + '\n')


def command(entry):
    """
    Takes in a number of rows to be read from file and maps to list of ints.

    Paramters:

        entry: int
            The row numbers that will be output.

    Return:

        mapped list of data
    """
    w = (entry.get().split(","))
    return list(map(int, w))


def openfile():
    """
    Opens the csv file for reading lidar and IMU packet parameters.
    """
    filename = fd.askopenfilename(filetypes=(("csv file", "*.csv"), ("All files", "*.*")))
    f = open(filename)
    f.read()
    global data
    data = pandas.read_csv(filename)


def lidar_single_row():
    """
    GUI window for reading lidar data in a single row

    Return:

        A textbox of the parameter data user wanted to read.
    """
    newwin = Toplevel(window)
    newwin.geometry("500x600")

    global t
    t = Text(newwin)
    t.place(x=75, y=250, height=300, width=200)

    row_num = IntVar(newwin)
    row_choice = ['Choose Row']
    for i in range(0, data.shape[0]):
        row_choice.append(i)

    row_num.set('Choose Row')
    popupMenu = OptionMenu(newwin, row_num, *row_choice).place(x=0, y=0, width=150)

    azimuth_block_num = IntVar(newwin)
    azimuth_choices = ['Choose Azimuth Block', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    azimuth_block_num.set('Choose Azimuth Block')
    popupMenu = OptionMenu(newwin, azimuth_block_num, *azimuth_choices).place(x=175, y=0, width=200)

    Label(newwin, text="Datablock parameter:").place(x=175, y=75)

    timestamp = Button(newwin, text='Get Timestamp', fg="red", command=lambda: print_list(get_timestamp(data, row_num.get(), single_row=True))).place(x=0, y=100, width=150)
    frame_id = Button(newwin, text='Get Frame Id', fg="red", command=lambda: print_list(get_frame_id(data, row_num.get(), single_row=True))).place(x=0, y=125, width=150)
    measurement_id = Button(newwin, text='Get Measurement Id', fg="red", command=lambda: print_list(get_measurement_id(data, row_num.get(), single_row=True))).place(x=0, y=150, width=150)
    encoder_count = Button(newwin, text='Get Encoder Count', fg="red", command=lambda: print_list(get_encoder_count(data, row_num.get(), single_row=True))).place(x=0, y=175, width=150)
    signal_photon = Button(newwin, text='Get Signal Photons', fg="red", command=lambda: print_list(get_signal_photons(data, row_num.get(), single_row=True, azimuth_block=azimuth_block_num.get()))).place(x=175, y=100, width=150)
    range_mm = Button(newwin, text='Get Range', fg="red", command=lambda: print_list(get_range(data, row_num.get(), single_row=True, azimuth_block=azimuth_block_num.get()))).place(x=175, y=125, width=150)
    reflectivity = Button(newwin, text='Get Reflectivity', fg="red", command=lambda: print_list(get_reflectivity(data, row_num.get(), single_row=True, azimuth_block=azimuth_block_num.get()))).place(x=175, y=150, width=150)
    noise_photon = Button(newwin, text='Get Noise Photons', fg="red", command=lambda: print_list(get_noise_photons(data, row_num.get(), single_row=True, azimuth_block=azimuth_block_num.get()))).place(x=175, y=175, width=150)


def lidar_multiple_row():
    """
    GUI window for reading lidar data of multiple rows

    Return:

        A textbox of the parameter data user wanted to read.
    """
    newwin = Toplevel(window)
    newwin.geometry("500x600")

    global t
    t = Text(newwin)
    t.place(x=75, y=250, height=300, width=200)

    Label(newwin, text="Enter Rows").place(x=0,y=0)
    entry1 = Entry(newwin)
    entry1.place(x=0,y=25,width=50)

    Label(newwin, text="Azimuth Block").place(x=100, y=0)
    azimuth_block_num = IntVar(newwin)
    azimuth_choices = ['Choose Azimuth Block', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    azimuth_block_num.set(0)
    popupMenu = OptionMenu(newwin, azimuth_block_num, *azimuth_choices).place(x=100,y=25, width=50)

    Label(newwin, text="Datablock parameter:").place(x=175, y=75)

    timestamp = Button(newwin, text='Get Timestamp', fg="red", command=lambda:print_list(get_timestamp(data, command(entry1), multiple_row=True))).place(x=0, y=100, width=150)
    frame_id = Button(newwin, text='Get Frame Id', fg="red", command=lambda: print_list(get_frame_id(data, command(entry1), multiple_row=True))).place(x=0, y=125, width=150)
    measurement_id = Button(newwin, text='Get Measurement Id', fg="red", command=lambda: print_list(get_measurement_id(data, command(entry1), multiple_row=True))).place(x=0, y=150, width=150)
    encoder_count = Button(newwin, text='Get Encoder Count', fg="red", command=lambda: print_list(get_encoder_count(data, command(entry1), multiple_row=True))).place(x=0, y=175, width=150)
    signal_photon = Button(newwin, text='Get Signal Photons', fg="red", command=lambda: print_list(get_signal_photons(data, command(entry1), multiple_row=True, azimuth_block=azimuth_block_num.get()))).place(x=175, y=100, width=150)
    range_mm = Button(newwin, text='Get Range', fg="red", command=lambda: print_list(get_range(data, command(entry1), multiple_row=True, azimuth_block=azimuth_block_num.get()))).place(x=175, y=125, width=150)
    reflectivity = Button(newwin, text='Get Reflectivity', fg="red", command=lambda: print_list(get_signal_photons(data, command(entry1), multiple_row=True, azimuth_block=azimuth_block_num.get()))).place(x=175, y=150, width=150)
    noise_photon = Button(newwin, text='Get Noise Photons', fg="red", command=lambda: print_list(get_signal_photons(data, command(entry1), multiple_row=True, azimuth_block=azimuth_block_num.get()))).place(x=175, y=175, width=150)


def lidar_row_section():
    """
    GUI window for reading lidar data of the row section

    Return:

        A textbox of the parameter data user wanted to read.
    """
    newwin = Toplevel(window)
    newwin.geometry("500x600")

    global t
    t = Text(newwin)
    t.place(x=75, y=250, height=300, width=200)

    Label(newwin, text="Enter rows").place(x=0, y=0)
    entry1 = Entry(newwin)
    entry1.place(x=0, y=25, width=50)

    Label(newwin, text="Azimuth Block").place(x=100, y=0)
    azimuth_block_num = IntVar(newwin)
    azimuth_choices = ['Choose Azimuth Block', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    azimuth_block_num.set(0)
    popupMenu = OptionMenu(newwin, azimuth_block_num, *azimuth_choices).place(x=100, y=25, width=50)

    Label(newwin, text="Datablock parameter:").place(x=175, y=75)

    timestamp = Button(newwin, text='Get Timestamp', fg="red", command=lambda: print_list(get_timestamp(data, command(entry1), row_section=True))).place(x=0, y=100, width=150)
    frame_id = Button(newwin, text='Get Frame Id', fg="red", command=lambda: print_list(get_frame_id(data, command(entry1), row_section=True))).place(x=0, y=125, width=150)
    measurement_id = Button(newwin, text='Get Measurement Id', fg="red", command=lambda: print_list(get_measurement_id(data, command(entry1), row_section=True))).place(x=0, y=150, width=150)
    encoder_count = Button(newwin, text='Get Encoder Count', fg="red", command=lambda: print_list(get_encoder_count(data, command(entry1), row_section=True))).place(x=0, y=175, width=150)
    signal_photon = Button(newwin, text='Get Signal Photons', fg="red", command=lambda: print_list(get_signal_photons(data, command(entry1), row_section=True, azimuth_block=azimuth_block_num.get()))).place(x=175, y=100, width=150)
    range_mm = Button(newwin, text='Get Range', fg="red", command=lambda: print_list(get_range(data, command(entry1), row_section=True, azimuth_block=azimuth_block_num.get()))).place(x=175, y=125, width=150)
    reflectivity = Button(newwin, text='Get Reflectivity', fg="red", command=lambda: print_list(get_signal_photons(data, command(entry1), row_section=True, azimuth_block=azimuth_block_num.get()))).place(x=175, y=150, width=150)
    noise_photon = Button(newwin, text='Get Noise Photons', fg="red", command=lambda: print_list(get_signal_photons(data, command(entry1), row_section=True, azimuth_block=azimuth_block_num.get()))).place(x=175, y=175, width=150)


def imu_single_row():
    """
    GUI window for reading IMU data of the single row

    Return:

        A textbox of the parameter data user wanted to read.
    """
    newwin = Toplevel(window)
    newwin.geometry("500x600")

    global t
    t = Text(newwin)
    t.place(x=75, y=250, height=300, width=200)

    row_num = IntVar(newwin)
    row_choice = ['Choose Row']
    for i in range(0, data.shape[0]):
        row_choice.append(i)

    row_num.set('Choose Row')
    popupMenu = OptionMenu(newwin, row_num, *row_choice).place(x=0, y=0, width=150)

    imu_time = Button(newwin, text="Get IMU Timestamp", fg="red", command=lambda: print_list(get_IMU_time(data, row_num.get(), single_row=True))).place(x=0, y=50, width=150)
    accel_time = Button(newwin, text="Get Accelerometer Timestamp", fg="red", command=lambda: print_list(get_accel_time(data, row_num.get(), single_row=True))).place(x=0, y=75, width=150)
    gyro_time = Button(newwin, text="Get Gyroscope Timestamp", fg="red", command=lambda: print_list(get_gyro_time(data, row_num.get(), single_row=True))).place(x=0, y=100, width=150)
    x_accel = Button(newwin, text="Get x acceleration", fg="red", command=lambda: print_list(get_x_accel(data, row_num.get(), single_row=True))).place(x=0, y=125, width=150)
    y_accel = Button(newwin, text="Get y acceleration", fg="red", command=lambda: print_list(get_y_accel(data, row_num.get(), single_row=True))).place(x=175, y=50, width=150)
    z_accel = Button(newwin, text="Get z acceleration", fg="red", command=lambda: print_list(get_z_accel(data, row_num.get(), single_row=True))).place(x=175, y=75, width=150)
    x_ang_vel = Button(newwin, text="Get x angular velocity", fg="red", command=lambda: print_list(get_x_ang_vel(data, row_num.get(), single_row=True))).place(x=175, y=100, width=150)
    y_ang_vel = Button(newwin, text="Get y angular velocity", fg="red", command=lambda: print_list(get_y_ang_vel(data, row_num.get(), single_row=True))).place(x=175, y=125, width=150)
    z_ang_vel = Button(newwin, text="Get z angular velocity", fg="red", command=lambda: print_list(get_z_ang_vel(data, row_num.get(), single_row=True))).place(x=175, y=150, width=150)


def imu_multiple_row():
    """
    GUI window for reading IMU data of multiple rows

    Return:

        A textbox of the parameter data user wanted to read.
    """
    newwin = Toplevel(window)
    newwin.geometry("500x600")

    global t
    t = Text(newwin)
    t.place(x=75, y=250, height=300, width=200)

    Label(newwin, text="Enter Rows").place(x=0, y=0)
    entry1 = Entry(newwin)
    entry1.place(x=0, y=25, width=50)

    imu_time = Button(newwin, text="Get IMU Timestamp", fg="red", command=lambda: print_list(get_IMU_time(data, command(entry1), multiple_row=True))).place(x=0, y=50, width=150)
    accel_time = Button(newwin, text="Get Accelerometer Timestamp", fg="red", command=lambda: print_list(get_accel_time(data, command(entry1), multiple_row=True))).place(x=0, y=75, width=150)
    gyro_time = Button(newwin, text="Get Gyroscope Timestamp", fg="red", command=lambda: print_list(get_gyro_time(data, command(entry1), multiple_row=True))).place(x=0, y=100, width=150)
    x_accel = Button(newwin, text="Get x acceleration", fg="red", command=lambda: print_list(get_x_accel(data, command(entry1), multiple_row=True))).place(x=0, y=125, width=150)
    y_accel = Button(newwin, text="Get y acceleration", fg="red", command=lambda: print_list(get_y_accel(data, command(entry1), multiple_row=True))).place(x=175, y=50, width=150)
    z_accel = Button(newwin, text="Get z acceleration", fg="red", command=lambda: print_list(get_z_accel(data, command(entry1), multiple_row=True))).place(x=175, y=75, width=150)
    x_ang_vel = Button(newwin, text="Get x angular velocity", fg="red", command=lambda: print_list(get_x_ang_vel(data, command(entry1), multiple_row=True))).place(x=175, y=100, width=150)
    y_ang_vel = Button(newwin, text="Get y angular velocity", fg="red", command=lambda: print_list(get_y_ang_vel(data, command(entry1), multiple_row=True))).place(x=175, y=125, width=150)
    z_ang_vel = Button(newwin, text="Get z angular velocity", fg="red", command=lambda: print_list(get_z_ang_vel(data, command(entry1), multiple_row=True))).place(x=175, y=150, width=150)


def imu_row_section():
    """
    GUI window for reading IMU data of the row section

    Return:

        A textbox of the parameter data user wanted to read.
    """
    newwin = Toplevel(window)
    newwin.geometry("500x600")

    global t
    t = Text(newwin)
    t.place(x=75, y=250, height=300, width=200)

    Label(newwin, text="Enter Rows").place(x=0, y=0)
    entry1 = Entry(newwin)
    entry1.place(x=0, y=25, width=50)

    imu_time = Button(newwin, text="Get IMU Timestamp", fg="red", command=lambda: print_list(get_IMU_time(data, command(entry1), row_section=True))).place(x=0, y=50, width=150)
    accel_time = Button(newwin, text="Get Accelerometer Timestamp", fg="red", command=lambda: print_list(get_accel_time(data, command(entry1), row_section=True))).place(x=0, y=75, width=150)
    gyro_time = Button(newwin, text="Get Gyroscope Timestamp", fg="red", command=lambda: print_list(get_gyro_time(data, command(entry1), row_section=True))).place(x=0, y=100, width=150)
    x_accel = Button(newwin, text="Get x acceleration", fg="red", command=lambda: print_list(get_x_accel(data, command(entry1), row_section=True))).place(x=0, y=125, width=150)
    y_accel = Button(newwin, text="Get y acceleration", fg="red", command=lambda: print_list(get_y_accel(data, command(entry1), row_section=True))).place(x=175, y=50, width=150)
    z_accel = Button(newwin, text="Get z acceleration", fg="red", command=lambda: print_list(get_z_accel(data, command(entry1), row_section=True))).place(x=175, y=75, width=150)
    x_ang_vel = Button(newwin, text="Get x angular velocity", fg="red", command=lambda: print_list(get_x_ang_vel(data, command(entry1), row_section=True))).place(x=175, y=100, width=150)
    y_ang_vel = Button(newwin, text="Get y angular velocity", fg="red", command=lambda: print_list(get_y_ang_vel(data, command(entry1), row_section=True))).place(x=175, y=125, width=150)
    z_ang_vel = Button(newwin, text="Get z angular velocity", fg="red", command=lambda: print_list(get_z_ang_vel(data, command(entry1), row_section=True))).place(x=175, y=150, width=150)


def xyz_calc():
    """
    GUI window for reading the xyz coordinates gotten from lines of the lidar csv file.

    Return:

        A textbox of the xyz coordinates from rows of the lidar csv file.
    """
    newwin = Toplevel(window)
    newwin.geometry("500x600")

    global t
    t = Text(newwin)
    t.place(x=75, y=250, height=300, width=200)

    row_num = IntVar(newwin)
    row_choice = ['Choose Row']
    for i in range(0, data.shape[0]):
        row_choice.append(i)

    row_num.set('Choose Row')
    popupMenu = OptionMenu(newwin, row_num, *row_choice).place(x=0, y=0, width=175)

    azimuth_block_num = IntVar(newwin)
    azimuth_choice = ['Choose Azimuth Block']
    for i in range(0, 16):
        azimuth_choice.append(i)

    azimuth_block_num.set('Choose Azimuth Block')
    popupMenu = OptionMenu(newwin, azimuth_block_num, *azimuth_choice).place(x=175, y=0, width=175)

    channel_num = IntVar(newwin)
    channel_choice = ['Choose Channel']
    for i in range(0, 64):
        channel_choice.append(i)

    channel_num.set('Choose Channel')
    popupMenu = OptionMenu(newwin, channel_num, *channel_choice).place(x=325, y=0, width=175)

    xyz = Button(newwin, text="Get lidar XYZ coordinates", fg='red', command=lambda: print_list(get_xyz(data, row_num.get(), azimuth_block_num.get(), channel_num.get()))).place(x=175, y=100)


def open_x4_bin():
    """
    Opens the Novelda X4 binary file for reading.
    """
    global X4_file
    X4_file = fd.askopenfilename(filetypes=(("binary file", "*.dat"), ("All files", "*.*")))


def open_x4_csv():
    """
    Opens the Novelda X4 csv file for use in threshold functions.
    """
    global X4_csv
    X4_csv = fd.askopenfilename(filetypes=(("csv file", "*.csv"), ("All files", "*.*")))


def convert_x4():
    """
    GUI window with button to allow conversion of X4 binary file to csv file.

    Return:

        Readable X4 csv file.
    """
    newwin = Toplevel(window)
    newwin.geometry("200x200")

    Label(newwin, text="Enter desired csv file name").place(x=0, y=0)
    entry1 = Entry(newwin)
    entry1.place(x=0, y=25, width=100)

    convert = Button(newwin, text="Convert binary file to csv file", command=lambda: iq_data(X4_file, entry1.get())).place(x=0, y=50)


def x4_threshold():
    """
    GUI window to run X4 threshold functions

    Returns:

        Radar threshold, noise and range estimates
    """
    newwin = Toplevel(window)
    newwin.geometry("800x600")

    global t
    t = Text(newwin)
    t.place(x=75, y=250, height=300, width=200)

    Label(newwin, text="Enter an estimated threshold").place(x=0, y=0)
    entry1 = Entry(newwin)
    entry1.place(x=0, y=25, width=100)

    range_bin = Button(newwin, text="Get range bin(s) above threshold", command=lambda: print_list(range_finder(X4_csv, float(entry1.get())))).place(x=0, y=50)
    noise = Button(newwin, text="Get noise estimate", command=lambda: print_list(noise_power_estimate(X4_csv, float(entry1.get())))).place(x=200, y=50)
    distance = Button(newwin, text="Get target distance", command=lambda: print_list(distance_finder(X4_csv, float(entry1.get())))).place(x=325, y=50)
    plot = Button(newwin, text="Plot data for range vs. amplitude", command=lambda: plot_data(X4_csv)).place(x=450, y=50)


def open_TSW_bin():
    """
    Opens the TSW binary file.
    """
    global TSW_file
    TSW_file = fd.askopenfilename(filetypes=(("binary file", "*.bin"), ("All files", "*.*")))


def convert_TSW():
    """
    Converts the TSW binary file to a readable csv file.
    """
    newwin = Toplevel(window)
    newwin.geometry("200x200")

    Label(newwin, text="Enter desired csv file name").place(x=0, y=0)
    entry1 = Entry(newwin)
    entry1.place(x=0, y=25, width=100)

    convert = Button(newwin, text="Convert binary file to csv file", command=lambda: readTSWdata(TSW_file, entry1.get())).place(x=0, y=50)


def instruction():
    """
    A set of instructions on how to use the program
    """
    webbrowser.open_new('https://docs.google.com/drawings/d/13fMRdlxXYuzx3p6o0sGeW2jcWu4JypsdJ_sgtaB_t_s/edit?usp=sharing')


""" Options for the file menu """
file_menu.add_command(label="Open", command=openfile)
file_menu.add_command(label="Instructions", command=instruction)
file_menu.add_command(label="Quit", command=quit)

""" Options for the extract menu """
lidar_extract_menu.add_command(label="Single row", command=lidar_single_row)
lidar_extract_menu.add_command(label="Multiple row", command=lidar_multiple_row)
lidar_extract_menu.add_command(label="Row section", command=lidar_row_section)

IMU_extract_menu.add_command(label="Single row", command=imu_single_row)
IMU_extract_menu.add_command(label="Multiple row", command=imu_multiple_row)
IMU_extract_menu.add_command(label="Row section", command=imu_row_section)

xyz_cartesian.add_command(label="Get point", command=xyz_calc)

X4.add_command(label="Open binary file", command=open_x4_bin)
X4.add_command(label="Open converted csv file", command=open_x4_csv)
X4.add_command(label="Convert binary file", command=convert_x4)
X4.add_command(label="Threshold functions", command=x4_threshold)

TSW.add_command(label="Open binary file", command=open_TSW_bin)
TSW.add_command(label="Convert binary file", command=convert_TSW)

window.geometry("700x100")
window.config(menu=menubar)
window.mainloop()


