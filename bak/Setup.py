# setup.py
# python setup.py py2exe 
from distutils.core import setup  
import py2exe  
  
setup( 
#      console=["Sacs_Input_Zip.py"],    # for Dos Console
      windows=["Sacs_Input_Zip.pyw"],   # for Window with GUI
)  
