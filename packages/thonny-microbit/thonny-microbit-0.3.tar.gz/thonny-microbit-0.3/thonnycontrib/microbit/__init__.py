import sys
import os.path
from thonny.plugins.micropython import MicroPythonProxy, MicroPythonConfigPage,\
    add_micropython_backend
from thonny import get_workbench, ui_utils
from thonny.ui_utils import FileCopyDialog
from thonny.misc_utils import find_volume_by_name
import shutil
from time import sleep

class MicrobitProxy(MicroPythonProxy):
    def _interrupt_to_prompt(self, clean, timeout=8):
        # NB! Sometimes disconnecting and reconnecting (on macOS?) 
        # too quickly causes anomalies
        # https://github.com/pyserial/pyserial/issues/176
        # In my Sierra, Calliope and micro:bit seemed to soft-reboot
        # when reconnected too quickly.
        
        if clean and sys.platform == "darwin":
            sleep(1.0)
        
        MicroPythonProxy._interrupt_to_prompt(self, clean, timeout=timeout)
        
    def _supports_directories(self):
        return False

class MicrobitConfigPage(MicroPythonConfigPage):
    pass

def flash_the_firmware(hex_path):
    mount_path = find_volume_by_name("MICROBIT",
                                     not_found_msg="Could not find disk '%s'.\n"
                                        + "Make sure you have micro:bit plugged in!\n\n"
                                        + "Do you want to continue and locate the disk yourself?")
    if mount_path is None:
        return
    
    destination_path = os.path.join(mount_path, os.path.basename(hex_path))
    
    dlg = FileCopyDialog(get_workbench(), hex_path, destination_path, 
                   "Uploading %s to %s" % (os.path.basename(hex_path), mount_path))
    ui_utils.show_dialog(dlg)

def load_plugin():
    add_micropython_backend("microbit", MicrobitProxy, 
                            "MicroPython on BBC micro:bit", MicrobitConfigPage)

    firmware_dir = os.path.join(os.path.dirname(__file__), "firmware")
    for name in sorted(os.listdir(firmware_dir)):
        if name.endswith(".hex"):
            
            def action(hex_path=os.path.join(firmware_dir, name)):
                flash_the_firmware(hex_path)
                 
            get_workbench().add_command("InstallMicroPythonMicrobit" + name, "device",
                                    "Install %s to BBC micro:bit" % name[:-4].replace("_", " "),
                                    action, group=40)
