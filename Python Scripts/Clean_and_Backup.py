import os
import shutil
import time

def backup_files():
        
    path  = os.getcwd()
    path = path[:-14] + "\\" + "Source Files"
    print(path)
    print("Current Work Directory: " + path)
    print("Scanning for existing source files...")
    
    file_list = []
    for directory, folders, files in os.walk(path):
        print("\n[Directory]: " + directory )
        for file in files:
            file_dir = directory + "\\" + file
            file_list.append(file_dir)
            print("[  File   ]: " + file)

    
    if len(file_list) == 0:
        print("\nSource folder seems to be empty")
        print("Please check if you've already backed up")
        print("\nThis program will exit in 5 seconds.", end="" )
        for i in range(5,0, -1):
            print(end='.')
            time.sleep(1)
        exit()
    else:
        print()
        
    if file_list[0][-32:-16] == "Confirmed_Corona":
        file_date = file_list[0][-15:-4]
    else:
        file_date = "Date Unknown"
    print("[  Date   ]: " + file_date)

    destination_path = path[:-14] + "\\Backup\\" + "Source files\\" + file_date
    print("\nCreating folder in backup dated: " + file_date )
    
    os.mkdir(destination_path)
    try:   
        print("[ Success ] folder created")
    except:
        print("[ Failed  ] Please check if folder already exists.")


    print("\n Moving files...")
    try:
        for file in file_list:
            shutil.move(file, destination_path)
        print("[Success] files moved")
    except:
          print("[Failed] Something went wrong")

if __name__=="__main__":
    backup_files()
