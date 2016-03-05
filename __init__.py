import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"python-verisure")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import eg
import verisure
eg.RegisterPlugin(
    name = "VerisureGhost",
    author = "datagutten",
    version = "0.0.1",
    kind = "other",
    description = "Verisure alarm and lock"
)

class VerisureGhost(eg.PluginBase):
    def __init__(self):
        self.AddAction(GetAll)
        self.AddAction(SetLockState)
    def __start__(self, username,password,code):
        self.username = username
        self.password = password
        self.code = code
        self.myPages = verisure.MyPages(username, password)
        print "Logging in"
        self.myPages.login()
    def __stop__(self):
        self.myPages.logout()

    def Configure(self, username="",password="",code=""):
        panel = eg.ConfigPanel()

        usernameCtrl = panel.TextCtrl(username)
        passwordCtrl = panel.TextCtrl(password, style=wx.TE_PASSWORD)
        codeCtrl = panel.TextCtrl(code)
        st1 = panel.StaticText("Username")
        st2 = panel.StaticText("Password")
        st3 = panel.StaticText("Code")
        eg.EqualizeWidths((st1, st2, st3))
        settingsBox = panel.BoxedGroup(
            "Settings",
            (st1, usernameCtrl),
            (st2, passwordCtrl),
            (st3, codeCtrl),
        )
        panel.sizer.Add(settingsBox, 0, wx.EXPAND)

        #panel.sizer.AddMany([
        #    (usernameCtrl, 0, wx.EXPAND),
        #    (passwordCtrl, 0, wx.EXPAND|wx.TOP, 10),
        #    (codeCtrl, 0, wx.EXPAND|wx.TOP, 10),
        #])

        while panel.Affirmed():
            panel.SetResult(
                usernameCtrl.GetValue(),
                passwordCtrl.GetValue(),
                codeCtrl.GetValue()
            )
            #panel.SetResult(textControl.GetValue())
    def GetAll(self):
        return self.myPages.get_overviews()
    def SetState(self,serialNumber,state):
        print "Set state of " + serialNumber + " to " + state
        return self.myPages.lock.set(self.code, serialNumber, state)


class GetAll(eg.ActionBase):

    def __call__(self):
        print self.plugin.GetAll


class SetLockState(eg.ActionBase):
    def __call__(self, serialNumber, state):
        print self.plugin.SetState(serialNumber,state)
    def Configure(self, serialNumber="", state=""):
        print "Serial: "+serialNumber
        print "State: "+state
        panel = eg.ConfigPanel()
        serialCtrl = panel.TextCtrl(serialNumber)
        stateCtrl = panel.TextCtrl(state)
        #stateCtrl = wx.Choice(panel, -1, choices=['UNLOCKED':'Unlock','LOCKED':'Lock'])
        #stateCtrl = wx.Choice(panel, choices=['UNLOCKED','LOCKED'])


        st1 = panel.StaticText("Serial number")
        st2 = panel.StaticText("Lock state")
        eg.EqualizeWidths((st1, st2))

        settingsBox = panel.BoxedGroup(
            "Lock settings",
            (st1, serialCtrl),
            (st2, stateCtrl),
        )
        panel.sizer.Add(settingsBox, 0, wx.EXPAND)
        while panel.Affirmed():
            #panel.SetResult(serialCtrl.GetValue(),stateCtrl.GetSelection())
            panel.SetResult(serialCtrl.GetValue(),stateCtrl.GetValue())
