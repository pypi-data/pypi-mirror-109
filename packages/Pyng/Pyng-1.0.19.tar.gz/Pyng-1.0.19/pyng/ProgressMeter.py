# from http://tkinter.unpythonic.net/wiki/ProgressMeter :
'''Michael Lange <klappnase (at) freakmail (dot) de>
The Meter class provides a simple progress bar widget for Tkinter.

INITIALIZATION OPTIONS:
The widget accepts all options of a Tkinter.Frame plus the following:

    fillcolor -- the color that is used to indicate the progress of the
                 corresponding process; default is "orchid1".
    value -- a float value between 0.0 and 1.0 (corresponding to 0% - 100%)
             that represents the current status of the process; values higher
             than 1.0 (lower than 0.0) are automagically set to 1.0 (0.0); default is 0.0 .
    text -- the text that is displayed inside the widget; if set to None the widget
            displays its value as percentage; if you don't want any text, use text="";
            default is None.
    font -- the font to use for the widget's text; the default is system specific.
    textcolor -- the color to use for the widget's text; default is "black".

WIDGET METHODS:
All methods of a Tkinter.Frame can be used; additionally there are two widget specific methods:

    get() -- returns a tuple of the form (value, text)
    set(value, text) -- updates the widget's value and the displayed text;
                        if value is omitted it defaults to 0.0 , text defaults to None .
'''
from __future__ import division

from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
import tkinter

class Meter(tkinter.Frame):
    def __init__(self, master, width=300, height=20, bg='white', fillcolor='orchid1',
                 value=0.0, text=None, font=None, textcolor='black', *args, **kw):
        tkinter.Frame.__init__(self, master, bg=bg, width=width, height=height, *args, **kw)
        self._value = value

        self._canv = tkinter.Canvas(self, bg=self['bg'], width=self['width'], height=self['height'],
                                    highlightthickness=0, relief='flat', bd=0)
        self._canv.pack(fill='both', expand=1)
        self._rect = self._canv.create_rectangle(0, 0, 0, self._canv.winfo_reqheight(), fill=fillcolor,
                                                 width=0)
        self._text = self._canv.create_text(self._canv.winfo_reqwidth()//2, self._canv.winfo_reqheight()//2,
                                            text='', fill=textcolor)
        if font:
            self._canv.itemconfigure(self._text, font=font)

        self.set(value, text)
        self.bind('<Configure>', self._update_coords)

    def _update_coords(self, event):
        '''Updates the position of the text and rectangle inside the canvas when the size of
        the widget gets changed.'''
        # looks like we have to call update_idletasks() twice to make sure
        # to get the results we expect
        self._canv.update_idletasks()
        self._canv.coords(self._text, self._canv.winfo_width()//2, self._canv.winfo_height()//2)
        self._canv.coords(self._rect, 0, 0, self._canv.winfo_width()*self._value, self._canv.winfo_height())
        self._canv.update_idletasks()

    def get(self):
        return self._value, self._canv.itemcget(self._text, 'text')

    def set(self, value=0.0, text=None):
        #make the value failsafe:
        if value < 0.0:
            value = 0.0
        elif value > 1.0:
            value = 1.0
        self._value = value
        if text == None:
            #if no text is specified use the default percentage string:
            text = str(int(round(100 * value))) + ' %'
        self._canv.coords(self._rect, 0, 0, self._canv.winfo_width()*value, self._canv.winfo_height())
        self._canv.itemconfigure(self._text, text=text)
        self._canv.update_idletasks()

##-------------demo code--------------------------------------------##

def _demo(meter, value):
    meter.set(value)
    if value < 1.0:
        value = value + 0.005
        meter.after(50, lambda: _demo(meter, value))
    else:
        meter.set(value, 'Demo successfully finished')

# from http://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
def center(win):
    # do this before retrieving any geometry to ensure accurate values
    win.update_idletasks()
    # width of client area
    width = win.winfo_width()
    # winfo_rootx() is client area's left x; winfo_x() is outer frame's left x
    frm_width = win.winfo_rootx() - win.winfo_x()
    # outer frame overall width is client width plus two frame widths
    win_width =  width + 2 * frm_width
    # height of client area
    height = win.winfo_height()
    # winfo_rooty() is client area's top y; winfo_y() is outer frame's top y
    # y is measured from top, therefore winfo_rooty() > winfo_y()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    # outer frame overall height = client height plus titlebar plus frame width
    win_height = height + titlebar_height + frm_width
    x = (win.winfo_screenwidth() - win_width) // 2
    y = (win.winfo_screenheight() - win_height) // 2
    win.geometry('%sx%s+%s+%s' % (width, height, x, y))
    ## if win.attributes('-alpha') == 0:
    ##     win.attributes('-alpha', 1.0)
    win.deiconify()

if __name__ == '__main__':
    import time
    root = tkinter.Tk(className='meter demo')
    m = Meter(root, relief='ridge', bd=3)
    m.pack(fill='x')
    center(root)
    m.set(0.0, 'Starting demo...')
##    m.after(1000, lambda: _demo(m, 0.0))
##    root.mainloop()
    time.sleep(1)
    total = 200
    for tick in range(total):
        # want 1..total, not 0..(total - 1)
        m.set(float(tick) / total)
        time.sleep(0.05)
    m.set(1, "Demo successfully finished")
    time.sleep(1)
    root.destroy()
