from cx_Freeze import setup, Executable 
  
setup(name = "AutoAnswerMachine" , 
      version = "0.1" , 
      description = "An autoanswer machine" , 
      executables = [Executable("gui_version.py"), Executable("update.py")]) 