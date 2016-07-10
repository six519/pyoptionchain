from Tkinter import *
from ttk import *
from google_api import GoogleFinanceOption
import tkMessageBox
import tkSimpleDialog, tkFileDialog
from pandas_utility import pickColumns, writeToExcel, EXCEL_INITIAL_FILENAME

class TkOptionGUILoadDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        Label(master, text="Exchange:").grid(row=0)
        Label(master, text="Exchange Symbol:").grid(row=1)

        self.exchange = Entry(master)
        self.exchangeSymbol = Entry(master)

        self.exchange.grid(row=0, column=1)
        self.exchangeSymbol.grid(row=1, column=1)

        self.exchange.delete(0, END)
        self.exchange.insert(0, GoogleFinanceOption.DEFAULT_EXCHANGE)

        self.exchangeSymbol.delete(0, END)
        self.exchangeSymbol.insert(0, GoogleFinanceOption.DEFAULT_EXCHANGE_SYMBOL)

        self.resizable(height=FALSE, width=FALSE)
        return self.exchange

    def apply(self):
        exchange = self.exchange.get()
        exchangeSymbol = self.exchangeSymbol.get()
        self.result = exchange, exchangeSymbol

    def validate(self):

        if self.exchange.get() not in GoogleFinanceOption.DEFAULT_VALID_EXCHANGE:
            tkMessageBox.showerror(TkOptionGUI.DEFAULT_GUI_TITLE, "Invalid Exchange Value")
            return False

        if self.exchangeSymbol.get() not in GoogleFinanceOption.DEFAULT_VALID_EXCHANGE_SYMBOL:
            tkMessageBox.showerror(TkOptionGUI.DEFAULT_GUI_TITLE, "Invalid Exchange Symbol Value")
            return False

        return True

class TkOptionGUIExpirationDialog(tkSimpleDialog.Dialog):

    expiration_options = []

    """
    def __init__(self,parent, **kwargs):
        expiration_options = kwargs.pop("expiration_options", [])
        #super(TkOptionGUIExpirationDialog, self).__init__(parent, **kwargs)
        tkSimpleDialog.Dialog.__init__(self, parent, **kwargs)
        self.__expiration_options = expiration_options
    """

    def body(self, master):
        tkSimpleDialog.Dialog.body(self, master)
        Label(master, text="Expiration:").grid(row=0)

        #"%s/%s/%s" % (expi["m"], expi["d"], expi["y"]) for expi in self.expiration_options
        #print TkOptionGUIExpirationDialog.expiration_options
        init_val = ["%s/%s/%s" % (expi["m"], expi["d"], expi["y"]) for expi in TkOptionGUIExpirationDialog.expiration_options]
        self.expiration = Combobox(master, values=init_val)
        self.expiration.grid(row=0, column=1)

        self.resizable(height=FALSE, width=FALSE)
        return self.expiration

    def apply(self):
        expiration = self.expiration.get()
        self.result = expiration

    def validate(self):

        expiration = self.expiration.get()

        if len(expiration.split("/")) == 3:
            return True

        return False

class TkOptionGUI(object):

    DEFAULT_GUI_TITLE = "Google Option Chain"
    DEFAULT_TOP_WIDTH = 500
    DEFAULT_TOP_HEIGHT = 500
    DEFAULT_LOAD_TYPE = "puts"

    def __init__(self, *args, **kwargs):
        self.__root = Tk()
        self.__google_api = GoogleFinanceOption()
        self.__currentLoadType = TkOptionGUI.DEFAULT_LOAD_TYPE
        self.__currentExchange = GoogleFinanceOption.DEFAULT_EXCHANGE
        self.__currentExchangeSymbol = GoogleFinanceOption.DEFAULT_EXCHANGE_SYMBOL
        self.__itemId = []

        #make the window maximized
        try:
            self.__root.attributes("-zoomed", True)
        except:
            self.__root.attributes("-fullscreen", True)
        #set window title
        self.__root.title(TkOptionGUI.DEFAULT_GUI_TITLE)

        #set up menu bar
        self.__menuBar = Menu(self.__root)

        #file menu
        self.__fileMenu = Menu(self.__menuBar, tearoff=0)
        self.__fileMenu.add_command(label="Load Option Chain Calls", command=lambda : self.__showLoadOption("calls"))
        self.__fileMenu.add_command(label="Load Option Chain Puts", command=lambda : self.__showLoadOption("puts"))
        self.__fileMenu.add_command(label="Dump To MS Excel File", command=self.__saveToExcel)
        self.__fileMenu.add_separator()
        self.__fileMenu.add_command(label="Exit", command=self.__root.quit)
        self.__menuBar.add_cascade(label="File", menu=self.__fileMenu)

        #edit menu
        self.__editMenu = Menu(self.__menuBar, tearoff=0)
        self.__editMenu.add_command(label="Set Expiration", command=self.__showExpirationOption)
        self.__menuBar.add_cascade(label="Edit", menu=self.__editMenu)

        #help menu
        self.__helpMenu = Menu(self.__menuBar, tearoff=0)
        self.__helpMenu.add_command(label="About", command=self.__showAbout)
        self.__menuBar.add_cascade(label="Help", menu=self.__helpMenu)

        self.__root.config(menu=self.__menuBar)

        #config treeview
        self.__root.grid_rowconfigure(0,weight=1)
        self.__root.grid_columnconfigure(0,weight=1)
        self.__cols = ("Strike", "Price", "Change", "Bid", "Ask", "Volume", "Open Int")
        self.__treeview = Treeview(self.__root, columns=self.__cols, show="headings")
        #setup columns
        for col in self.__cols:
            self.__treeview.heading(col, text=col)
        self.__treeview.grid(sticky=N+E+S+W)
        #set scrollbars
        self.__hScrollbar = Scrollbar(self.__treeview, orient=HORIZONTAL)
        self.__hScrollbar.pack(side=BOTTOM, fill=X)
        self.__hScrollbar.config(command=self.__treeview.xview)

        self.__vScrollbar = Scrollbar(self.__treeview, orient=VERTICAL)
        self.__vScrollbar.pack(side=RIGHT, fill=Y)
        self.__vScrollbar.config(command=self.__treeview.yview)

        self.__treeview.config(xscrollcommand=self.__hScrollbar.set, yscrollcommand=self.__vScrollbar.set)

    def __showAbout(self):
        tkMessageBox.showinfo(TkOptionGUI.DEFAULT_GUI_TITLE, "Created by: Ferdinand Silva")

    def __showExpirationOption(self):
        if len(self.__itemId) > 0:
            expirations = self.__google_api.getExpirations()

            if len(expirations) > 0:
                TkOptionGUIExpirationDialog.expiration_options = expirations
                expirationDialog = TkOptionGUIExpirationDialog(self.__root)

                if expirationDialog.result:

                    splittedInput = expirationDialog.result.split("/")
                    self.__google_api = GoogleFinanceOption()
                    self.__google_api.setParameters({
                        "q" : "%s:%s" % (self.__currentExchange, self.__currentExchangeSymbol),
                        "expm" : splittedInput[0],
                        "expd" : splittedInput[1],
                        "expy" : splittedInput[2]
                    })

                    self.__loader(self.__currentLoadType)

    def __showLoadOption(self, loadType="puts"):
        loadDialog = TkOptionGUILoadDialog(self.__root)

        if loadDialog.result:
            self.__google_api = GoogleFinanceOption()
            self.__google_api.setParameters({
                "q": "%s:%s" % loadDialog.result
            })

            self.__currentExchange = loadDialog.result[0]
            self.__currentExchangeSymbol = loadDialog.result[1]

            self.__loader(loadType)

    def __loader(self, loadType):

        if self.__google_api.fetchData():
            #pass
            #tkMessageBox.showinfo(TkOptionGUI.DEFAULT_GUI_TITLE, "Option Chain Successfully Loaded")
            self.__currentLoadType = loadType
            self.__clearTreeView()

            if loadType == "puts":
                data = self.__google_api.getPuts()
            else:
                data = self.__google_api.getCalls()

            finalData = pickColumns(data)

            for ind, fData in enumerate(finalData):
                self.__itemId.append(self.__treeview.insert('',ind, '', values=tuple(fData)))

            expiry = self.__google_api.getExpiry()
            self.__root.title("%s (%s/%s/%s)" % (TkOptionGUI.DEFAULT_GUI_TITLE, expiry['m'], expiry['d'], expiry['y']))

        else:
            self.__currentLoadType = TkOptionGUI.DEFAULT_LOAD_TYPE
            tkMessageBox.showerror(TkOptionGUI.DEFAULT_GUI_TITLE, "Cannot Fetch Option Chain Data")
    
    def __clearTreeView(self):

        tempIDs = self.__itemId
        idCount = len(tempIDs)
        self.__itemId = []

        for tempID in range(idCount):
            iid = tempIDs.pop()
            self.__treeview.delete(iid)

    def __saveToExcel(self):

        if len(self.__itemId) > 0:

            if self.__currentLoadType == "puts":
                data = self.__google_api.getPuts()
            else:
                data = self.__google_api.getCalls()

            finalData = []
            finalData.append(list(self.__cols))

            pickCol = pickColumns(data)
            for ind, fData in enumerate(pickCol):
                finalData.append(fData)

            dialogOption = {
                "filetypes" : [("All Files", ".*"), ("Excel File", ".xls")],
                "parent" : self.__root,
                "initialfile" : EXCEL_INITIAL_FILENAME
            }

            fname = tkFileDialog.asksaveasfilename(**dialogOption)

            if fname:
                writeToExcel(finalData, fname)


    def run(self):
        self.__root.mainloop()