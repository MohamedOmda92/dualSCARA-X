#!/usr/bin/env python3.8

import sys
import os
sys.path.insert(0, '/home/mohamed/catkin_ws/src/parallel_scara_pkg/scripts')

import sv_ttk
import math
import customtkinter
import numpy as np
import tkinter as tk
import tkinter.font as font
import matplotlib.pyplot as plt
from customtkinter import *
from tkinter import ttk
from PIL import ImageTk
from typing import Sequence, Type
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from parallel_scara_pkg.scarabot_controller import scarabotController
from parallel_scara_pkg.trajectory import Trajectory



class ScarabotGUI:

    folderDir = os.getcwd()
    
    def __init__(self) -> None:

        # Root Window (Home)
        self.root = CTk() 
        self.root.title("ScaraBot Controller")
        # >>> Set root dimensions
        rootW = 800
        rootH = 480
        self.root.geometry('%dx%d+%d+%d' % (rootW, rootH, 1, 1))
        self.root.resizable(False, False)
        # >> Set root icon
        iconDir = os.path.join(ScarabotGUI.folderDir, 'gui/IMG/icon.png')
        icon = ImageTk.PhotoImage(file=iconDir)
        self.root.iconphoto(False, icon)
        # >> Set GUI theme
        customtkinter.set_appearance_mode("dark")
        sv_ttk.set_theme("dark")

        # >> Constant Styles
        self.themeColors = ['#F9F9FA','#343638'] # [light_color, dark_color]
        self.tabviewColors = ['gray86', 'gray17'] # [light_color, dark_color]
        self.btnColors = ['#3B8ED0', '#1F6AA5'] # [light_color, dark_color]
        font_title = CTkFont("Serif", size=18)
        font_entry = CTkFont("Arial", size=14)

        #=============================
        #===== Field Variables ======
        #=============================
        self.shapeVar = StringVar()


        #FOR TEST ONLY
        self.controller = scarabotController()


        # == WIDGETS =================================================================================================
        
        # Root grid Configuration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=8)
        self.root.rowconfigure(1, weight=1)



        # ====================
        # == Tabs Frame ======
        # ====================
        tabH = rootH*0.8
        self.tabview = CTkTabview(self.root, height=tabH)
        self.tabview.pack(padx=5, pady=5, side=TOP, fill=X)

        self.tabview.add("Connection")
        self.tabview.add("Manual")
        self.tabview.add("Defined Shape")
        self.tabview.add("Custom Path")
        self.tabview.set("Defined Shape")



        # ===========================
        # == Manual Control Tab =====
        # ===========================
        # Frame Root (4r 2c)
        manual_frame = CTkFrame(self.tabview.tab("Manual"),
                                fg_color="transparent",
                                height=tabH)
        manual_frame.pack(side=LEFT, expand=True, fill=BOTH)
        # >>> Grid Config.
        manual_frame.rowconfigure(0, weight=1, uniform='a')
        manual_frame.rowconfigure(1, weight=1, uniform='a')
        manual_frame.rowconfigure((2,3), weight=4, uniform='a')
        manual_frame.columnconfigure((0,1), weight=1, uniform='a')
    

        # ===== Manual Control WIDGETS ===============
        # [r0c01] Tab Label
        manual_lbl = CTkLabel(manual_frame,
                              text="Manual Control",
                              font=font_title)
        # [r1c0] Resolution Spinbox
        res_spin = ttk.Spinbox(manual_frame,
                               from_=1,
                               to_=10,
                               width=5)
        res_spin.set(1)
        # [r2c0] Keys Frame
        keys_frame = CTkFrame(manual_frame,
                              fg_color="transparent",
                              border_width=3)
        # >>> Grid Config.
        keys_frame.rowconfigure(0, weight=1, uniform='a')
        keys_frame.rowconfigure((1,2,3), weight=4, uniform='a')
        keys_frame.columnconfigure((0,1,2), weight=1, uniform='a')
        # [r2c1] Home Setting Frame
        homeSet_frame = CTkFrame(manual_frame,
                                 fg_color="transparent",
                                 border_width=3)
        # [r3c1] Ptp Frame
        ptp_frame = CTkFrame(manual_frame,
                             fg_color="transparent",
                             border_width=3)
        # >>> Layout
        manual_lbl.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        res_spin.grid(row=1, column=0)
        keys_frame.grid(row=2, column=0, rowspan=2, sticky=NSEW, padx=(10,5), pady=10)
        homeSet_frame.grid(row=2, column=1, sticky=NSEW, padx=(5,10), pady=(10,5))
        ptp_frame.grid(row=3, column=1, sticky=NSEW, padx=(5,10), pady=(5,10))


        # ===== Keys Frame WIDGETS ===============
        # Keys Title
        keys_title = CTkLabel(keys_frame, text="Keyboard Control", font=("Arial",14))
        # Key Frame Keys
        ul_btn = CTkButton(keys_frame,
                            text="UL",
                            width=80,
                            height=40,
                            corner_radius=20,
                            command=lambda: self.controller.movewithKeys('ul', int(res_spin.get())))
        u_btn = CTkButton(keys_frame,
                            text="U",
                            width=80,
                            height=40,
                            corner_radius=20,
                            command=lambda: self.controller.movewithKeys('u', int(res_spin.get())))
        ur_btn = CTkButton(keys_frame,
                            text="UR",
                            width=80,
                            height=40,
                            corner_radius=20,
                            command=lambda: self.controller.movewithKeys('ur', int(res_spin.get())))
        l_btn = CTkButton(keys_frame,
                            text="L",                            
                            width=80,
                            height=40,
                            corner_radius=20,
                            command=lambda: self.controller.movewithKeys('l', int(res_spin.get())))
        home_btn = CTkButton(keys_frame,
                              text="Home",
                              font=("Arial",14),
                              command=lambda: self.controller.goHome())
        r_btn = CTkButton(keys_frame,
                            text="R",
                            width=80,
                            height=40,
                            corner_radius=20,
                            command=lambda: self.controller.movewithKeys('r', int(res_spin.get())))
        dl_btn = CTkButton(keys_frame,
                            text="DL",
                            width=80,
                            height=40,
                            corner_radius=20,
                            command=lambda: self.controller.movewithKeys('dl', int(res_spin.get())))        
        d_btn = CTkButton(keys_frame,
                            text="D",
                            width=80,
                            height=40,
                            corner_radius=20,
                            command=lambda: self.controller.movewithKeys('d', int(res_spin.get())))
        dr_btn = CTkButton(keys_frame,
                            text="DR",
                            width=80,
                            height=40,
                            corner_radius=20,
                            command=lambda: self.controller.movewithKeys('dr', int(res_spin.get())))
        # >>> Keys Layout
        keys_title.grid(row=0, column=0, columnspan=3, sticky=N, pady=(10,0))
        ul_btn.grid(row=1, column=0, sticky=SE)
        u_btn.grid(row=1, column=1, sticky=S)
        ur_btn.grid(row=1, column=2, sticky=SW)
        l_btn.grid(row=2, column=0, sticky=E)
        home_btn.grid(row=2, column=1, sticky=NSEW, padx=20, pady=20)
        r_btn.grid(row=2, column=2, sticky=W)
        dl_btn.grid(row=3, column=0, sticky=NE)
        d_btn.grid(row=3, column=1, sticky=N)
        dr_btn.grid(row=3, column=2, sticky=NW)


        # ===== Home Set WIDGETS ===============
        # Home Set Title
        homeSet_title = CTkLabel(homeSet_frame, text="Set New Home Position", font=("Arial",14))
        # Entry Frame
        xy_frame = CTkFrame(homeSet_frame, fg_color="transparent")
        # Buttons Frame
        setReset_frame = CTkFrame(homeSet_frame, fg_color="transparent")
        # X Coordinate Entry
        self.x_entry = CTkEntry(xy_frame,
                           width=140,
                           height=28,
                           placeholder_text="X Coordinates {Cm}")
        # Y Coordinate Entry
        self.y_entry = CTkEntry(xy_frame,
                           width=140,
                           height=28,
                           placeholder_text="Y Coordinates {Cm}")
        # Set Home Button
        homeSet_btn = CTkButton(setReset_frame,
                                text="Set Home",
                                width=100,
                                height=40,
                                corner_radius=10,
                                command=lambda: self.controller.setHome(self.getHomeSetValues()))
        # Reset Home Button
        homeReset_btn = CTkButton(setReset_frame,
                                text="Reset Home",
                                width=100,
                                height=40,
                                corner_radius=10,
                                command=lambda: self.controller.resetHome())
        # >>> Layout
        homeSet_title.pack(side=TOP, fill=Y, pady=(5,0))
        xy_frame.pack(side=TOP, expand=True, fill=BOTH, padx=5, pady=(20,5))
        setReset_frame.pack(side=TOP, expand=True, fill=BOTH, padx=5, pady=(5,5))
        self.x_entry.pack(side=LEFT, expand= True, padx=10)
        self.y_entry.pack(side=LEFT, expand= True, padx=10)
        homeSet_btn.pack(side=LEFT, pady=20, expand=True)
        homeReset_btn.pack(side=LEFT, pady=20, expand=True)
        

        # ===== Ptp Frame WIDGETS ===============
        # Ptp Title
        ptp_title = CTkLabel(ptp_frame, text="Move to Point", font=("Arial",14))
        # Entry Frame
        xyPtp_frame = CTkFrame(ptp_frame, fg_color="transparent")
        # X Coordinate Entry
        self.xPtp_entry = CTkEntry(xyPtp_frame,
                           width=140,
                           height=28,
                           placeholder_text="X Coordinates {Cm}")
        # Y Coordinate Entry
        self.yPtp_entry = CTkEntry(xyPtp_frame,
                           width=140,
                           height=28,
                           placeholder_text="Y Coordinates {Cm}")
        # Set Home Button
        movePtp_btn = CTkButton(ptp_frame,
                                text="Move",
                                width=100,
                                height=40,
                                corner_radius=10,
                                command=lambda: self.controller.goToPoint(self.getPointValues()))
        # >>> Layout
        ptp_title.pack(side=TOP, fill=Y, pady=(5,0))
        xyPtp_frame.pack(side=TOP, expand=True, fill=BOTH, padx=5, pady=(20,5))
        self.xPtp_entry.pack(side=LEFT, expand= True, padx=10)
        self.yPtp_entry.pack(side=LEFT, expand= True, padx=10)
        movePtp_btn.pack(side=TOP, pady=20, expand=True)



        # ===========================
        # == Defined Shape Tab =====
        # ===========================

        # Frame Root (3r 1c)
        shape_frame = CTkFrame(self.tabview.tab("Defined Shape"),
                                fg_color="transparent",
                                height=tabH)
        shape_frame.pack(side=LEFT, expand=True, fill=BOTH)
        # >>> Grid Config.
        shape_frame.rowconfigure((0,1), weight=1, uniform='a')
        shape_frame.rowconfigure(2, weight=5, uniform='a')
        shape_frame.columnconfigure(0, weight=1, uniform='a')
        # [r0c0] Tab Label
        shape_lbl = CTkLabel(shape_frame,
                              text="Defined Shape Path Tracking",
                              font=font_title)
        # [r1c0] Shape Selection Frame
        shapeSelect_frame = CTkFrame(shape_frame, fg_color="transparent")
        # >>> Grid Config.
        shapeSelect_frame.rowconfigure(0, weight=1, uniform='a')
        shapeSelect_frame.columnconfigure((0,1), weight=1, uniform='a')
        # [r2c0] Shape Properties Frame
        shapeProp_frame = CTkFrame(shape_frame, fg_color="transparent", border_width=3)
        # >>> Grid Config.
        shapeProp_frame.rowconfigure((0,1,2), weight=1, uniform='a')
        shapeProp_frame.columnconfigure((0,1,2), weight=1, uniform='a')
        # >>> Layout
        shape_lbl.grid(row=0, column=0, sticky=NSEW)
        shapeSelect_frame.grid(row=1, column=0, sticky=NSEW, pady=(5,5))
        shapeProp_frame.grid(row=2, column=0, sticky=NSEW, pady=(5,5))


        # ===== Shape Selection WIDGETS ===============
        self.shapeSelect_combo = CTkComboBox(shapeSelect_frame,
                                     width=160,
                                     height=28,
                                     variable=self.shapeVar,
                                     values=['None','Arc','Circle','Ellipse','Rectangle'],
                                     command=self.setShapeProperties)
        self.moveShape_btn = CTkButton(shapeSelect_frame,
                                  text="Move",
                                  width=100,
                                  height=30,
                                  corner_radius=10,
                                  command=self.followShape_command)
        # >>> Layout
        self.shapeSelect_combo.grid(row=0, column=0, sticky=E, padx=(0,20))
        self.moveShape_btn.grid(row=0, column=1, sticky=W, padx=(20,0))   


        # ===== Shape Properties WIDGETS ===============
        propEntryW = 160
        propEntryH = 30
        self.prop_entry1 = CTkEntry(shapeProp_frame,
                               width=propEntryW,
                               height=propEntryH)
        self.prop_entry2 = CTkEntry(shapeProp_frame,
                               width=propEntryW,
                               height=propEntryH)
        self.prop_entry3 = CTkEntry(shapeProp_frame,
                               width=propEntryW,
                               height=propEntryH)
        self.prop_entry4 = CTkEntry(shapeProp_frame,
                               width=propEntryW,
                               height=propEntryH)
        self.prop_entry5 = CTkEntry(shapeProp_frame,
                               width=propEntryW,
                               height=propEntryH)
        self.prop_entry6 = CTkEntry(shapeProp_frame,
                               width=propEntryW,
                               height=propEntryH)
        self.prop_entry7 = CTkEntry(shapeProp_frame,
                               width=propEntryW,
                               height=propEntryH)
        self.prop_combo1 = CTkComboBox(shapeProp_frame,
                                  width=propEntryW,
                                  height=propEntryH)
        self.prop_combo2 = CTkComboBox(shapeProp_frame,
                                  width=propEntryW,
                                  height=propEntryH)
        # >>> Layout
        # Only if need in setShapesProperties() method



        # == WIDGETS END ================================================================================================

        self.root.mainloop()


    
    def getHomeSetValues(self) -> Sequence[float]:

        xVal = float(self.x_entry.get()) / 100
        yVal = float(self.y_entry.get()) / 100

        return [xVal, yVal]
    


    def getPointValues(self) -> Sequence[float]:

        xVal = float(self.xPtp_entry.get()) / 100
        yVal = float(self.yPtp_entry.get()) / 100

        return [xVal, yVal]
    


    def setShapeProperties(self, choice) -> None:
        
        if choice == 'None':
            self.hideShapeProp()


        elif choice == 'Arc':
            texts = ['Radius {Cm}','Center X {Cm}','Center Y {Cm}','Start angle {Deg}','End Angle {Deg}','Draw Time {Seconds}']
            values = []
            
            self.hideShapeProp()
            self.clearShapeProp()

            self.prop_entry1.configure(placeholder_text=texts[0], border_color=self.btnColors[1])
            self.prop_entry2.configure(placeholder_text=texts[1], border_color=self.btnColors[1])
            self.prop_entry3.configure(placeholder_text=texts[2], border_color=self.btnColors[1])
            self.prop_entry4.configure(placeholder_text=texts[3], border_color=self.btnColors[1])
            self.prop_entry5.configure(placeholder_text=texts[4], border_color=self.btnColors[1])
            self.prop_entry6.configure(placeholder_text=texts[5], border_color=self.btnColors[1])

            self.prop_entry1.grid(row=0, column=0)
            self.prop_entry2.grid(row=0, column=1)
            self.prop_entry3.grid(row=0, column=2)
            self.prop_entry4.grid(row=1, column=0)
            self.prop_entry5.grid(row=1, column=1)
            self.prop_entry6.grid(row=1, column=2)

        elif choice == 'Circle':
            
            texts = ['Radius {Cm}','Center X {Cm}','Center Y {Cm}','Draw Time {Seconds}','Start Angle {Deg}']
            values = ['Draw Direction']
            
            self.hideShapeProp()
            self.clearShapeProp()

            self.prop_entry1.configure(placeholder_text=texts[0], border_color=self.btnColors[1])
            self.prop_entry2.configure(placeholder_text=texts[1], border_color=self.btnColors[1])
            self.prop_entry3.configure(placeholder_text=texts[2], border_color=self.btnColors[1])
            self.prop_entry4.configure(placeholder_text=texts[3], border_color=self.btnColors[1])
            self.prop_entry5.configure(placeholder_text=texts[4], border_color='#565B5E')
            self.prop_combo1.configure(values=['cw','ccw'])
            self.prop_combo1.set(values[0])

            self.prop_entry1.grid(row=0, column=0)
            self.prop_entry2.grid(row=0, column=1)
            self.prop_entry3.grid(row=0, column=2)
            self.prop_entry4.grid(row=1, column=0)
            self.prop_entry5.grid(row=1, column=1)
            self.prop_combo1.grid(row=1, column=2)


        elif choice == 'Ellipse':
            
            texts = ["Center X {Cm}","Center Y {Cm}","X amplitude {Cm}","Y amplitude {Cm}","Draw time {Seconds}","Start angle {Deg}>=0","Rotation angle {Deg}>=0"]
            values = ['Draw Direction']
            
            self.hideShapeProp()
            self.clearShapeProp()

            self.prop_entry1.configure(placeholder_text=texts[0], border_color=self.btnColors[1])
            self.prop_entry2.configure(placeholder_text=texts[1], border_color=self.btnColors[1])
            self.prop_entry3.configure(placeholder_text=texts[2], border_color=self.btnColors[1])
            self.prop_entry4.configure(placeholder_text=texts[3], border_color=self.btnColors[1])
            self.prop_entry5.configure(placeholder_text=texts[4], border_color=self.btnColors[1])
            self.prop_entry6.configure(placeholder_text=texts[5], border_color='#565B5E')
            self.prop_entry7.configure(placeholder_text=texts[6], border_color='#565B5E')
            self.prop_combo1.configure(values=['cw','ccw'])
            self.prop_combo1.set(values[0])

            self.prop_entry1.grid(row=0, column=0)
            self.prop_entry2.grid(row=0, column=1)
            self.prop_entry3.grid(row=0, column=2)
            self.prop_entry4.grid(row=1, column=0)
            self.prop_entry5.grid(row=1, column=1)
            self.prop_entry6.grid(row=1, column=2)
            self.prop_entry7.grid(row=2, column=0)
            self.prop_combo1.grid(row=2, column=1)


        elif choice == 'Rectangle':


            texts = ["Height {Cm}","Width {Cm}","Pin point X {Cm}","Pin point Y {Cm}","Draw time {Seconds}"]
            values = ["Anchor location","Draw direction"]    
            
            self.hideShapeProp()
            self.clearShapeProp()

            self.prop_entry1.configure(placeholder_text=texts[0], border_color=self.btnColors[1])
            self.prop_entry2.configure(placeholder_text=texts[1], border_color=self.btnColors[1])
            self.prop_entry3.configure(placeholder_text=texts[2], border_color=self.btnColors[1])
            self.prop_entry4.configure(placeholder_text=texts[3], border_color=self.btnColors[1])
            self.prop_entry5.configure(placeholder_text=texts[4], border_color=self.btnColors[1])
            self.prop_combo1.configure(values=['n','s','e','w','ne','nw','se','sw'])
            self.prop_combo2.configure(values=['cw','ccw'])
            self.prop_combo1.set(values[0])
            self.prop_combo2.set(values[1])

            self.prop_entry1.grid(row=0, column=0)
            self.prop_entry2.grid(row=0, column=1)
            self.prop_entry3.grid(row=0, column=2)
            self.prop_entry4.grid(row=1, column=0)
            self.prop_entry5.grid(row=1, column=1)            
            self.prop_combo1.grid(row=1, column=2)
            self.prop_combo2.grid(row=2, column=0)



    def hideShapeProp(self):
        
        prop_entries = [self.prop_entry1, self.prop_entry2, self.prop_entry3, 
                      self.prop_entry4, self.prop_entry5, self.prop_entry6,self.prop_entry7]
        prop_combos = [self.prop_combo1, self.prop_combo2]

        for i in range(len(prop_entries)):
                prop_entries[i].grid_forget()

        for i in range(len(prop_combos)):
            prop_combos[i].grid_forget()



    def clearShapeProp(self):
        
        prop_entries = [self.prop_entry1, self.prop_entry2, self.prop_entry3, 
                      self.prop_entry4, self.prop_entry5, self.prop_entry6,self.prop_entry7]

        for i in range(len(prop_entries)):
                prop_entries[i].delete(0,END)



    def followShape_command(self):

        prop_entries = [self.prop_entry1, self.prop_entry2, self.prop_entry3, 
                      self.prop_entry4, self.prop_entry5, self.prop_entry6,self.prop_entry7]
        prop_combos = [self.prop_combo1, self.prop_combo2]

        shape = self.shapeSelect_combo.get()

        values = []
        for i in range(len(prop_entries)):
            if prop_entries[i].winfo_ismapped():
                value = prop_entries[i].get()
                if value == '':
                    values.append(None)
                else:
                    values.append(prop_entries[i].get())

        choices = []
        for i in range(len(prop_combos)):
            if prop_combos[i].winfo_ismapped():            
                choice = prop_combos[i].get()
                if choice not in prop_combos[i].cget('values'):
                    choice = None
                choices.append(choice)


        reqParams = []
        optParams = []

        if shape == "Arc":
            reqParams = values
            optParams = None

        elif shape == "Circle":
            reqParams = values[:4]
            optParams.extend([values[4], choices[0]])
        
        elif shape == "Ellipse":
            reqParams = values[:5]
            optParams.extend([values[5], values[6], choices[0]])

        elif shape == "Rectangle":
            reqParams = values
            optParams = choices

        print(f"Required: {reqParams}")
        print(f"Optional: {optParams}")

        shapeObj = self.controller.followShape(shape, reqParams, optParams)

        self._plotTrajectory(shapeObj.trajectory)

        self.controller.start_point_nav(shapeObj)



    def _plotTrajectory(self, trajectory, customEnds=False):
        
        top = tk.Toplevel()
        top.geometry("700x600")
        top.title("toplevel")

        x = np.asarray(trajectory[1])*100
        y = np.asarray(trajectory[2])*100
        
        plt.rcParams["figure.figsize"] = [7, 3.50]
        plt.rcParams["figure.autolayout"] = True

        f = Figure(figsize=[7, 3.50])
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()

        major_ticksX = np.arange(-20, 20, 5)
        minor_ticksX = np.arange(-20, 20, 1)
        major_ticksY = np.arange(-5, 40, 5)
        minor_ticksY = np.arange(-5, 40, 1)

        ax = f.add_subplot(1, 1, 1)
        ax.set_xticks(major_ticksX)
        ax.set_xticks(minor_ticksX, minor=True)
        ax.set_yticks(major_ticksY)
        ax.set_yticks(minor_ticksY, minor=True)
        ax.set_aspect('equal')
        ax.autoscale(False, axis='both')
        
        ax.grid(which='both')
        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)
        
        stepper1 = plt.Rectangle((-15,-3), 6, 6, fc='black',ec="grey")
        stepper2 = plt.Rectangle((8,-3), 6, 6, fc='black',ec="grey")
        plt.gca().add_patch(stepper1)
        plt.gca().add_patch(stepper2)
        
        # Plot trajectory
        ax.plot(x, y)
        
        # Plot trajectory START point indicator
        ax.plot(x[0], y[0], 'or')

        # Plot trajectory END point indicator
        if customEnds == False:
            idx = math.floor(len(x)*0.99 - 1) # point before END by 0.1%
        else:
            idx = -1

        ax.plot(x[idx], y[idx], 'og')
        
        canvas = FigureCanvasTkAgg(f, top)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        canvas.mpl_connect("key_press_event", lambda event: canvas.get_tk_widget().destroy())
        canvas.mpl_connect("key_press_event", lambda event: top.destroy())




if __name__ == '__main__':

    ScarabotGUI()