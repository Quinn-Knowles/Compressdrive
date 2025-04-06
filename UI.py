import wx
import subprocess


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Compress Drive", size=(750, 350))
        panel = wx.Panel(self)

        # Create "Compress" button
        self.compress_button = wx.Button(panel, label="Compress", pos=(550, 250))
        self.compress_button.Bind(wx.EVT_BUTTON, self.on_compress)
        
        # Create "Pre-Check"  button
        self.compress_button = wx.Button(panel, label="Run Pre-Check", pos=(450, 250))
        self.compress_button.Bind(wx.EVT_BUTTON, self.on_pre_check)
        
        # Create "Select Directory" button
        self.select_button = wx.Button(panel, label="Select Directory", pos=(150, 50))
        self.select_button.Bind(wx.EVT_BUTTON, self.on_select_directory)

        # Create a text control for displaying selected directory
        self.text_ctrl = wx.TextCtrl(panel, pos=(270, 55), size=(350, -1), style=wx.TE_READONLY)

        # Create a text control for user input (custom argument)
        self.instruction_static_text_1 = wx.StaticText(panel, pos=(75, 100), label="Enter target percentage as # 0-99")
        self.custom_text_ctrl = wx.TextCtrl(panel, pos=(270, 100), size=(350, -1), style=wx.TE_PROCESS_ENTER)
        self.custom_text_ctrl.SetHint("Enter a custom argument")

        # Create four radio buttons
        self.radio1 = wx.RadioButton(panel, label="Individual", pos=(50, 150), style=wx.RB_GROUP)
        self.radio2 = wx.RadioButton(panel, label="Top level", pos=(150, 150))
        self.radio3 = wx.RadioButton(panel, label="Try all", pos=(250, 150))
        self.radio4 = wx.RadioButton(panel, label="Test Bench", pos=(350, 150))

        self.Show()

    def on_select_directory(self, event):
        """Opens a directory selection dialog and displays the chosen directory."""
        with wx.DirDialog(self, "Choose a directory", style=wx.DD_DEFAULT_STYLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                selected_path = dialog.GetPath()
                self.text_ctrl.SetValue(selected_path)  # Display selected path next to the button

    def on_compress(self, event):
        """Calls the appropriate Python script based on the selected radio button."""
        selected_directory = self.text_ctrl.GetValue()
        ratio_target = self.custom_text_ctrl.GetValue()  # Get the custom argument text

        if not selected_directory:
            wx.MessageBox("Please select a directory first.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Determine which radio button is selected and set the script path
        if self.radio1.GetValue():
            script_name = "control/individual.py"
        elif self.radio2.GetValue():
            script_name = "control/toplevel.py"
        elif self.radio3.GetValue():
            script_name = "control/tryall.py"
        elif self.radio4.GetValue():
            script_name = "control/testbench.py"
        else:
            wx.MessageBox("Please select an option.", "Error", wx.OK | wx.ICON_ERROR)
            return
        command = ["python", script_name, selected_directory]
        if ratio_target:
            command.append(ratio_target)  

        try:
            subprocess.run(command, check=True)
            wx.MessageBox(f"{script_name} started successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(f"Error running {script_name}:\n{e}", "Error", wx.OK | wx.ICON_ERROR)
        except FileNotFoundError:
            wx.MessageBox(f"{script_name} not found!", "Error", wx.OK | wx.ICON_ERROR)

    def on_pre_check(self, event):
        """Calls the appropriate Python script based on the selected radio button."""
        selected_directory = self.text_ctrl.GetValue()
        ratio_target = self.custom_text_ctrl.GetValue()  
        
        
        if not ratio_target:
            wx.MessageBox("Please select a target first.", "Error", wx.OK | wx.ICON_ERROR)
            return
        if not selected_directory:
            wx.MessageBox("Please select a directory first.", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        script_name = "control/precheck.py"

        command = ["python", script_name, selected_directory, ratio_target]
        try:
            info = subprocess.run(command, check=True, encoding='utf-8', stdout=subprocess.PIPE)
            for line in info.stdout.split('\n'):
                print(line)
            wx.MessageBox(f"{script_name} started successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(f"Error running {script_name}:\n{e}", "Error", wx.OK | wx.ICON_ERROR)
        except FileNotFoundError:
            wx.MessageBox(f"{script_name} not found!", "Error", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
