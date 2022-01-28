''' filetools
    for working with SD card'''

import uos
import sdcard
from machine import SPI, Pin

# ------------------------------------------------------------------------

#     FILE TOOLS

def is_folder(filename):
    # True if folder
    if uos.stat(filename)[0] & 0x4000:
        return True
    else:
        return False
    
def is_file(filename):
    # True if file, not folder
    if uos.stat(filename)[0] & 0x8000:
        return True
    else:
        return False
    
def list_folders(folder):
    # list subfolders of folder
    l = uos.listdir(folder)
    folders = []
    for f in l:
        fi = folder + '/' + f
        if is_folder(fi):
            folders.append(f)
    ##folders = [f for f in l if is_folder(f)]   ## this gives error if no folder there
    
    return folders

def list_files(folder):
    # list files in folder (subfolders excluded)
    l = uos.listdir(folder)
   
    files = []
    for f in l:
        fi = folder + '/' + f
        if is_file(fi):
            files.append(f)
    #files = [f for f in l if is_file(f)]
    return files
# ------------------------------------------------------------------------

# SD TOOLS
# MAIN SD class, needs sdcard.py (driver)

class SD():
    def __init__(self, SPIselect, SD_CS, sdfolder):
        print("Defining SD")
        self.SPIselect = SPIselect
        self.SD_CS = SD_CS
        self.sdfolder = sdfolder
        self.error = ""
        
        # define SD
        try:
            self.sd = sdcard.SDCard(SPI(SPIselect), Pin(SD_CS))
            
            
        except OSError as e:
            self.error = (str(e))
            self.sd = None
        except:
            self.error = "SD card ERROR"
            self.sd = None
    
        # mount SD
        self.mountsdcard()
        
    def mountsdcard(self):
        print("Mounting SD")
        self._create_mountpoint()
        
        try:
            vfs = uos.VfsFat(self.sd)
            uos.mount(vfs, self.sdfolder)
            self.error = ""
        except OSError as e:
            
            if "EPERM" in str(e):
                print("SD card already mounted!")
                self.error = ""
            else:
                self.error += '\t' + "MOUNT ERROR"
        except Exception:
            self.error += '\t' + "MOUNT ERROR"
       
    def _create_mountpoint(self):
        # if sdfolder does not exist, create it (to use as mountpoint)
        if (self.sdfolder in list_folders('/') == False):
            print("Creating SD mountpoint " + sdfolder)
            uos.mkdir(self.sdfolder)      

    def unmount(self):
        print("Unmounting SD card")
        uos.umount(self.sdfolder)
              
    def list_all(self):
        return  uos.listdir(self.sdfolder)
        
    
    def listfolders(self):
        return list_folders(self.sdfolder)
    
    def listfiles(self):
        return list_files(self.sdfolder)

    
    def readfile(self, fname):
        fname = self.sdfolder + '/' + fname
        f = open(fname, 'r')
        t = f.read()
        f.close()
        return t
       

    def _write2file(self, fname, text, mode = 'a', end = '\n'):
        # mode = 'a' (append) or 'w' (write)
        fname = self.sdfolder + '/' + fname
        f = open( fname, mode)
        f.write(text + end)
        f.close()

    def writefile(self, fname, text):
        # writes a new file to SD card
        self._write2file(fname, text, mode = 'w')
        
    def print(self, fname, text, end = '\n'):
        # works like print, but to a file on the SD card
        # appends text to file fname with line feed at the end
        self._write2file(fname, text, mode = 'a', end = end)
        
#-----------------------------------------------------------------------------------
if __name__ == "__main__":
    
    
    sdfolder = "/SD"
    SPIselect = 0                  # 0/1 for SPI0 or SPI1
    SD_CS = 5                      # Chip select for SD  (may be any GP pin)
    
    sd = SD(SPIselect, SD_CS, sdfolder)
    
    if sd.error:
        print(sd.error)
    else:

        print("SD folder: ", sd.sdfolder)
        
        l = sd.list_all()
        print("Files and folders on SD: ", l)
        
        
        l = sd.listfolders()
        print("Folders on SD: ", l)
        
        l = sd.listfiles()
        print("Files on SD: ", l)
        
        t = 'Blahblah ghjghg pi'
        sd.writefile('blah.txt', t)
        
        t = "This is appended to the file"
        sd.print('blah.txt', t)
        sd.print('blah.txt', t)
        
        t = sd.readfile('blah.txt')
        print(t)
        
        sd.unmount()
