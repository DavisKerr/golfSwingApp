from tkinter import *
from tkinter.ttk import *



class Double_Slider(Frame):

    # Global slider attributes
    LINE_COLOR = "#476b6b"
    LINE_WIDTH = 3
    BAR_COLOR_INNER = "#5c8a8a"
    BAR_COLOR_OUTTER = "#c2d6d6"
    BAR_RADIUS = 10
    BAR_RADIUS_INNER = BAR_RADIUS-5
    DIGIT_PRECISION = '.1f' # for showing in the canvas

    def __init__(self, master, on_change, width = 400, height = 80, min_val = 0, max_val = 1, show_value = True, num_bars=2):

        Frame.__init__(self, master, height = height, width = width) # Create a new frame in Tkinter
        self.master = master

        init_lis = [min_val, max_val]
        self.using_slider = False
        self.on_change = on_change
        self.init_lis = init_lis
        self.max_val = max_val
        self.min_val = min_val
        self.show_value = show_value
        self.H = height
        self.W = width
        self.canv_H = self.H
        self.canv_W = self.W
        if not show_value:
            self.slider_y = self.canv_H/2 # y pos of the slider
        else:
            self.slider_y = self.canv_H*2/5
        self.slider_x = Double_Slider.BAR_RADIUS # x pos of the slider (left side)

        self.bars = []
        self.selected_idx = None # current selection bar index
        for value in self.init_lis[0:num_bars]:
            pos = (value-min_val)//(max_val-min_val)
            ids = []
            bar = {"Pos":pos, "Ids":ids, "Value":value}
            self.bars.append(bar)


        self.canv = Canvas(self, height = self.canv_H, width = self.canv_W) # Canvas used for drawing the widget.
        self.canv.pack()
        self.canv.bind("<Motion>", self._mouseMotion)
        self.canv.bind("<B1-Motion>", self._moveBar)
        self.canv.bind("<ButtonRelease-1>", self.resume)

        self.__addTrack(self.slider_x, self.slider_y, self.canv_W-self.slider_x, self.slider_y)
        for bar in self.bars:
            bar["Ids"] = self.__addBar(bar["Pos"])

    def resume(self, pos):
        self.on_change(self.getValues())
        self.using_slider = False


    def advance_slider(self, number):
        if not number > self.max_val and not self.using_slider:
            pos = number / self.max_val
            self.__moveBar(0, pos)

    def getValues(self):
        values = [round(bar["Value"]) for bar in self.bars]
        return sorted(values)

    def _mouseMotion(self, event):
        x = event.x
        y = event.y
        selection = self.__checkSelection(x,y)
        if selection[0]:
            self.canv.config(cursor = "hand2")
            self.selected_idx = selection[1]
        else:
            self.canv.config(cursor = "")
            self.selected_idx = None

    def _moveBar(self, event):
        self.using_slider = True
        x = event.x
        y = event.y
        if self.selected_idx == None:
            return False
        pos = self.__calcPos(x)
        idx = self.selected_idx
        self.__moveBar(idx,pos)

    def __addTrack(self, startx, starty, endx, endy):
        id1 = self.canv.create_line(startx, starty, endx, endy, fill = Double_Slider.LINE_COLOR, width = Double_Slider.LINE_WIDTH)
        return id

    def __addBar(self, pos):
        """@ pos: position of the bar, ranged from (0,1)"""
        if pos <0 or pos >1:
            raise Exception("Pos error - Pos: "+str(pos))
        R = Double_Slider.BAR_RADIUS
        r = Double_Slider.BAR_RADIUS_INNER
        L = self.canv_W - 2*self.slider_x
        y = self.slider_y
        x = self.slider_x+pos*L
        id_outer = self.canv.create_oval(x-R,y-R,x+R,y+R, fill = Double_Slider.BAR_COLOR_OUTTER, width = 2, outline = "")
        id_inner = self.canv.create_oval(x-r,y-r,x+r,y+r, fill = Double_Slider.BAR_COLOR_INNER, outline = "")
        if self.show_value:
            y_value = y+Double_Slider.BAR_RADIUS+8
            value = pos*(self.max_val - self.min_val)+self.min_val
            id_value = self.canv.create_text(x,y_value, text = round(value))
            return [id_outer, id_inner, id_value]
        else:
            return [id_outer, id_inner]

    def __moveBar(self, idx, pos):
        ids = self.bars[idx]["Ids"]
        for id in ids:
            self.canv.delete(id)
        self.bars[idx]["Ids"] = self.__addBar(pos)
        self.bars[idx]["Pos"] = pos
        self.bars[idx]["Value"] = pos*(self.max_val - self.min_val)+self.min_val
        

    def __calcPos(self, x):
        """calculate position from x coordinate"""
        pos = (x - self.slider_x)/(self.canv_W-2*self.slider_x)
        if pos<0:
            return 0
        elif pos>1:
            return 1
        else:
            return pos

    def __getValue(self, idx):
        """#######Not used function#####"""
        bar = self.bars[idx]
        ids = bar["Ids"]
        x = self.canv.coords(ids[0])[0] + Double_Slider.BAR_RADIUS
        pos = self.__calcPos(x)
        return pos*(self.max_val - self.min_val)+self.min_val

    def __checkSelection(self, x, y):
        """
        To check if the position is inside the bounding rectangle of a Bar
        Return [True, bar_index] or [False, None]
        """
        if self.bars:
            for idx in range(len(self.bars)):
                id = self.bars[idx]["Ids"][0]
                bbox = self.canv.bbox(id)
                if bbox[0] < x and bbox[2] > x and bbox[1] < y and bbox[3] > y:
                    return [True, idx]
            return [False, None]