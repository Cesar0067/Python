# install any Python package:
# C:/path/to/specific/python.exe -m pip install packagename
# Author's path for install py package: C:\Python310\python.exe

from tkinter import *
import serial.tools.list_ports
import threading
import signal
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# DEFINES
INIT_X_AXIS = -20
END_X_AXIS = 20


def signal_handler(signum, frame):
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)
class Graphics():
    pass

def getADC():
    global serialData, graph, refTime
    if get_ADC_btn["text"] in "Start ADC":
        graph.canvas.grid()
        chart.get_tk_widget().grid()
        root.geometry("1200x500")
        serialData = True
        # if len(xData) == 0:
        #    refTime = time.perf_counter()
        # else:
        #    refTime = time.perf_counter()-xData[len(xData)-1]

        get_ADC_btn["text"] = "Stop ADC"
        print("ADC ON")
        serialData = True
        t1 = threading.Thread(target=readSerial)
        t1.daemon = True
        t1.start()
        update_chart()
    else:
        root.geometry("500x500")
        graph.canvas.grid_remove()
        chart.get_tk_widget().grid_remove()
        print("ADC OFF")
        serialData = False
        get_ADC_btn["text"] = "Start ADC"
        serialData = False
        # graph.canvas.itemconfig(graph.text, text="---")


def update_chart():
    global x, y, fig, chart, ax, serialData, xData, yData
    ax.clear()
    ax.plot(x, y, '-', color="black", dash_capstyle='projecting')
    ax.grid(color='b', linestyle='-', linewidth=0.2)
    ax.set_xlim([INIT_X_AXIS, END_X_AXIS])
    ax.axvline(0, linestyle='--', color='red')
    ax.set_ylim([0, 100])
    ax.set_xlabel("Distance [cm]")
    ax.set_ylabel("Intensity [%]")
    fig.canvas.draw()
    if serialData:
        root.after(10, update_chart)


def connect_menu_init():
    global root, connect_btn, refresh_btn, graph, get_ADC_btn, chart, xData, yData, x, y, ax, fig, line
    root = Tk()
    root.title("Graph from STM32")
    root.geometry("500x500")
    root.config(bg="white")

    port_label = Label(root, text="Available port(s): ", bg="white")  # setting of label
    port_label.grid(column=1, row=2, padx=10, pady=20)  # show label in GUI window

    bd_label = Label(root, text="Baud Rate: ", bg="white")  # setting of label
    bd_label.grid(column=1, row=3, padx=10, pady=20)  # show label in GUI window

    refresh_btn = Button(root, text="Refresh", height=1, width=10, command=update_coms)  # setting of refresh btn
    refresh_btn.grid(column=3, row=2)  # show btn in GUI window

    connect_btn = Button(root, text="Connect", height=2, width=10, state="disabled", command=connection)
    connect_btn.grid(column=3, row=3)

    baud_select()
    update_coms()

    graph = Graphics()

    graph.canvas = Canvas(root, width=300, height=300, bg="white", highlightthickness=0)
    graph.canvas.grid(row=6, columnspan=5)

    graph.canvas.grid_remove()

    # Dynamic update
    # graph.outer = graph.canvas.create_arc(10, 10, 290, 290, start=90, extent=100, outline="#f11", fill="#f11", width=2)
    ## Static update
    # graph.canvas.create_oval(75, 75, 225, 225, outline="#f11", fill="white", width=2)
    ## Dynamic update of text
    # graph.text = graph.canvas.create_text(
    #    150, 150, anchor=E, font=("Helvetiva", "20"), text="---")
    ## Static update of text
    # graph.canvas.create_text(
    #    175, 150, anchor=CENTER, font=("Helvetiva", "20"), text="V")

    # ADC widget
    get_ADC_btn = Button(root, text="Start ADC", height=2, width=10, state="disabled", command=getADC)
    get_ADC_btn.grid(column=3, row=4)
    # get_ADC_btn.grid_remove()

    # Widget for plot
    fig = plt.Figure(figsize=(8, 5), dpi=100)
    ax = fig.add_subplot(111)
    chart = FigureCanvasTkAgg(fig, master=root)
    chart.get_tk_widget().grid(column=6, row=1, columnspan=6, rowspan=6)
    chart.get_tk_widget().grid_remove()

    xData = []
    yData = []
    x = []
    y = []


def connect_check(args):
    # Check of select values in COM and Baud Rate boxes
    if "-" in clicked_com.get() or "-" in clicked_bd.get():
        connect_btn["state"] = "disable"
    else:
        connect_btn["state"] = "active"


def baud_select():
    # Setup of select baud rate
    global clicked_bd, drop_bd
    clicked_bd = StringVar()
    bds = ["-",
           "110", "300",
           "600", "1200",
           "2400", "4800",
           "9600", "14400",
           "19200", "38400",
           "57600", "115200",
           "128000", "256000"]
    clicked_bd.set(bds[12])
    drop_bd = OptionMenu(root, clicked_bd, *bds, command=connect_check)
    drop_bd.config(width=10)
    drop_bd.grid(column=2, row=3, padx=50)


def update_coms():
    # Update of active COM ports
    global clicked_com, drop_com
    ports = serial.tools.list_ports.comports()
    coms = [com[0] for com in ports]
    coms.insert(0, "-")
    try:
        drop_com.destroy()
    except:
        pass
    clicked_com = StringVar()
    clicked_com.set(coms[0])
    drop_com = OptionMenu(root, clicked_com, *coms, command=connect_check)
    drop_com.config(width=10)
    drop_com.grid(column=2, row=2, padx=50)
    connect_check(0)


def readSerial():
    global serialData, graph, x, y
    xAxis = INIT_X_AXIS
    printRange = 0

    while serialData:
        data = ser.readline()
        # print(data)
        # if len(data) > 0:
        try:
            if xAxis < (END_X_AXIS + 1):
                sensor = float(data.decode('utf8'))
                voltage = (round(((3300 * sensor) / 4095 / 1000), 2))
                yData.append(round((voltage / 3.3) * 100, 2))
                xData.append(xAxis)
                xAxis += 1
                lenYdata = len(yData)
                lenXdata = len(xData)
                printRange += 1
                # if lenXdata == printRange:
                #    y = [k for k in yData]
                #    x = [k for k in xData]
                # else:
                y = yData[lenYdata - printRange:lenYdata]
                x = xData[lenYdata - printRange:lenXdata]
                # graph.sensor = sensor
                # t2 = threading.Thread(target=graph_control,args=(graph,))
                # t2.daemon = True
                # t2.start()
            else:
                xAxis = INIT_X_AXIS
                printRange = 0
                # for i in range(0, lenYdata):
                #    yData[i] = -1
        except:
            pass


def connection():
    # Set active/inactive buttons
    global ser, serialData
    if connect_btn["text"] in "Disconnect":
        root.geometry("500x500")
        # serialData = False
        connect_btn["text"] = "Connect"
        refresh_btn["state"] = "active"
        drop_bd["state"] = "active"
        drop_com["state"] = "active"
        get_ADC_btn["state"] = "disable"
        # Hide ADC circle
        # graph.canvas.grid_remove()
        # get_ADC_btn.grid_remove()

    else:
        root.geometry("500x500")
        # serialData = True
        connect_btn["text"] = "Disconnect"
        refresh_btn["state"] = "disable"
        drop_bd["state"] = "disable"
        drop_com["state"] = "disable"
        get_ADC_btn["state"] = "active"
        port = clicked_com.get()
        baud = clicked_bd.get()
        # print(port,baud)
        # Start read data from serial
        try:
            ser = serial.Serial(port, baud, timeout=0, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS)
        except:
            pass
        # graph.canvas.grid()
        get_ADC_btn.grid()


def close_window():
    global root, serialData
    serialData = False
    time.sleep(0.25)
    root.destroy()


# def graph_control(graph):
#    graph.canvas.itemconfig(
#        graph.outer, exten=int((330*graph.sensor)/4095))
#    graph.canvas.itemconfig(
#        graph.text, text=f"{float(round((3300*graph.sensor)/4095/1000,2))}")

connect_menu_init()
root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()