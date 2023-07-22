import keyUEFI_finder
import time
import tkinter
import tkinter.ttk
from tkinter import filedialog
import tkinter.font
import os
import threading
import webbrowser

#DebugWall-Software
#Created by ZombiDebugWall


EOA = 36 * "\x00" + "\x2B" + "\x00"


dmi_vars_size = {"DmiVar0100010800": 0,
                 "DmiVar0100010500": 15,
                 "DmiVar0100010700": 9,
                 "DmiVar0100010600": 15,
                 "DmiVar0100011a00": 15,
                 "DmiArray": 0,
                 "DmiVar0200020700": 9,
                 "DmiVar0300030800": 0,
                 "DmiVar0200020600": 29,
                 
                 "SerialNum": 29,
                 
                 "RomHoleReplaceOA3Var": 41,
                 "WinKeySize": 29}

global _TIME_CONST
_TIME_CONST = int(str(time.time())[0:10])


_SECURE_BOOT_KEYS_PATH_AND_FIRMWARE = "./finished/"
_DONATE_URL = "https://debugwall-software.com/?cat=7"



def run_tkinter_interface(name_art):
    
    def get_Area_EOA(start_pos, offset_start_pos, file_content_old, stop_running):
        string_cache = ""
        
        end_found = False
        
        index_cache = 0
        
        
        
        for character_index_end in range(start_pos + offset_start_pos, len(file_content_old), 1):
            
            if stop_running.is_set():
                return
            
            
            
            if file_content_old[character_index_end] == EOA[index_cache]:
                string_cache += file_content_old[character_index_end]
                index_cache += 1
                
                if string_cache == EOA:
                    end_pos = character_index_end - len(EOA) - 4
                    end_found = True
                    break
                            
            else:
                string_cache = ""
                index_cache = 0
                
            
                    
            if end_found:
                break

        
        return end_pos



    def getSecureBootKeys(file_content_old, file_old, stop_running):
        
        #dbx
        if stop_running.is_set():
            return
        print("Extracting secure boot keys...")
        output_window_log("Extracting secure boot keys...\n")
        
        area_names_old, dbx_positions = keyUEFI_finder.keyUEFIFinderMain("dbx", len("dbx") - 1, file_name = file_old, stop_running = stop_running)
        if stop_running.is_set():
            return
        
        
        
        if not area_names_old and not dbx_positions:
            print("No valid secure boot area start address could be found. Stopping...\n")
            output_window_log("\nNo valid secure boot area start address could be found. Stopping...\n")
            return
        else:
            pass
        
        start_dbx_area = dbx_positions[0]
        real_start_data_offset_dbx = 4
        
        
        end_dbx_area = get_Area_EOA(start_dbx_area, real_start_data_offset_dbx, file_content_old, stop_running)
        if stop_running.is_set():
            return

        
        dbx_file = open(_SECURE_BOOT_KEYS_PATH_AND_FIRMWARE + "dbx_" + str(_TIME_CONST), "wb")
        
        dbx_file.write(bytes(file_content_old[start_dbx_area + real_start_data_offset_dbx:end_dbx_area], "ANSI"))
        dbx_file.close()
        
        print("Saved DBX key!")
        output_window_log("Saved DBX key!\n")
        
        if stop_running.is_set():
            return
        
        
        #db
        
        db_start_pos = end_dbx_area + len(EOA) + 16
        
        
        if file_content_old[db_start_pos:db_start_pos + 2] != "db":
            print("DB not found. Stopping...")
            output_window_log("\nDB not found. Stopping...\n")
            return
            
        
        
        
        real_start_data_offset_db = 3
        
        db_end_pos = get_Area_EOA(db_start_pos, real_start_data_offset_db, file_content_old, stop_running)
        if stop_running.is_set():
            return
        
        
        file_db = open(_SECURE_BOOT_KEYS_PATH_AND_FIRMWARE + "db_" + str(_TIME_CONST), "wb")
        
        file_db.write(bytes(file_content_old[db_start_pos + real_start_data_offset_db:db_end_pos], "ANSI"))
        
        file_db.close()
        
        print("Saved DB key!")
        output_window_log("Saved DB key!\n")
        
        if stop_running.is_set():
            return
        
        
        #KEK
        
        KEK_start_pos = db_end_pos + 16 + len(EOA)
        
        
        if file_content_old[KEK_start_pos:KEK_start_pos + 3] != "KEK":
            print("KEK not found. Stopping...")
            output_window_log("\nKEK not found. Stopping...\n")
            exit()
        
        
        real_start_data_offset_KEK = 4
        
        
        KEK_end_pos = get_Area_EOA(KEK_start_pos, real_start_data_offset_KEK, file_content_old, stop_running)
        if stop_running.is_set():
            return

        file_KEK = open(_SECURE_BOOT_KEYS_PATH_AND_FIRMWARE + "KEK_" + str(_TIME_CONST), "wb")
        
        file_KEK.write(bytes(file_content_old[KEK_start_pos + real_start_data_offset_KEK:KEK_end_pos], encoding="ANSI"))
        
        file_KEK.close()
        
        print("Saved KEK!")
        output_window_log("Saved KEK!\n")
        
        if stop_running.is_set():
            return
        
        
        
        #PK
        
        PK_start_pos = KEK_end_pos + 16 + len(EOA)
        
        
        
        if file_content_old[PK_start_pos:PK_start_pos + 2] != "PK":
            print("PK not found. Stopping...")
            output_window_log("\nPK not found. Stopping...\n")
            return
            


        real_start_data_offset_PK = 3
        
        
        PK_end_pos = get_Area_EOA(PK_start_pos, real_start_data_offset_PK, file_content_old, stop_running)
        if stop_running.is_set():
            return
        
        file_PK = open(_SECURE_BOOT_KEYS_PATH_AND_FIRMWARE + "PK_" + str(_TIME_CONST), "wb")
        
        file_PK.write(bytes(file_content_old[PK_start_pos + real_start_data_offset_PK:PK_end_pos], encoding="ANSI"))
        
        file_PK.close()
        
        print("Saved PK!")
        output_window_log("Saved PK!\n")

        print("Job is done. Stopping...")
        output_window_log("Job is done. Stopping...\n")




    def WinKeyReplace(file_content_new, file_content_old, file_old, file_new, stop_running):
        
        
        print("Searching for Windows keys...")
        output_window_log("Searching for Windows keys...\n")
        
        if stop_running.is_set():
            return
        
        
        
        area_names_old, old_positions = keyUEFI_finder.keyUEFIFinderMain("RomHoleReplaceOA3Var", len("RomHoleReplaceOA3Var") - 1, file_name = file_old, stop_running = stop_running)
        if stop_running.is_set():
            return
        
        
        
        if not area_names_old and not old_positions:
            print("No valid Windows key area (old file) addresses could be found. Skipping...")
            output_window_log("\nNo valid Windows key area (old file) addresses could be found. Skipping...\n")
            getSecureBootKeys(file_content_old, file_old)
        else:
            pass
        
        area_names_new, new_positions = keyUEFI_finder.keyUEFIFinderMain("RomHoleReplaceOA3Var", len("RomHoleReplaceOA3Var") - 1, file_name = file_new, stop_running = stop_running)
        
        if stop_running.is_set():
            return
        
        
        if area_names_new == [] and new_positions == []:
            print("No valid Windows key area (new file) addresses could be found. Skipping...")
            output_window_log("\nNo valid Windows key area (new file) addresses could be found. Skipping...\n")
            getSecureBootKeys(file_content_old, file_old)
        else:
            pass
        
        
        
        key_list = []
        
        byte_offset = dmi_vars_size["RomHoleReplaceOA3Var"]
        
        for winkey in range(0, len(old_positions), 1):
            if stop_running.is_set():
                return
            area_pos = old_positions[winkey]
            string_key_cache = ""
            
            for key_char in range(area_pos + byte_offset, area_pos + byte_offset + dmi_vars_size["WinKeySize"], 1):
                if stop_running.is_set():
                    return
                string_key_cache += file_content_old[key_char]
                
            key_list.append(string_key_cache)
        
        key_found = True
        
        
        if '-' not in key_list[0] and '-' not in key_list[1]:
            key_found = False
            
        else:
            print("")
            print("###################################################")
            print("Key found:", key_list[0])
            print("###################################################")      
            print("")
            print("Replacing Windows keys...")

            output_window_log("\n")
            output_window_log("###################################################\n")
            output_window_log("Key found: {key}".format(key = key_list[0]))
            output_window_log("\n###################################################\n")      
            output_window_log("\n")
            output_window_log("Replacing Windows keys...\n")



        for old_key in range(0, len(new_positions), 1):
            
            if stop_running.is_set():
                return
            
            area_pos = new_positions[old_key]
            key = key_list[old_key]
            for key_char in range(area_pos + byte_offset, area_pos + byte_offset + dmi_vars_size["WinKeySize"], 1):
                if stop_running.is_set():
                    return
            
                file_content_new[key_char] = key[key_char - area_pos - byte_offset]
                
        
        finished_file_instance = open(_SECURE_BOOT_KEYS_PATH_AND_FIRMWARE + "finished_bios_" + str(_TIME_CONST)+ ".bin", "wb")
        finished_file_instance.write(bytes(''.join(file_content_new), "ANSI"))
        finished_file_instance.close()

        if not key_found:
            print("No valid Windows keys could be found.")
            output_window_log("\nNo valid Windows keys could be found.\n")
            
        else:
            print("Windows key replace successful!")
            output_window_log("Windows key replace successful!\n")


        getSecureBootKeys(file_content_old, file_old, stop_running)




    def dmi_data_replace(file_old, file_new, stop_running):
        
        if stop_running.is_set():
            return
        
        time.sleep(0.1)
        
        print("Loading and analyzing provided binary image...this can take some time")
        
        output_window_log("Loading and analyzing provided binary image...this can take some time\n")
        
        try:
            image_old = open(file_old, "rb")
        
        except FileNotFoundError:
            print("File \"" + file_old + "\" not found.")
            output_window_log("File \"" + file_old + "\" not found.\n")
            return
        
        
        
        try:
            image_new = open(file_new, "rb")
        except FileNotFoundError:
            print("File \"" + file_new + "\" not found.")
            output_window_log("File \"" + file_new + "\" not found.\n")
            return
        
        
        
        image_content_old = image_old.read().decode("ANSI")
        image_old.close()
        
        result_list_data_old, result_list_bytes_old = keyUEFI_finder.keyUEFIFinderMain("Dmi", len("Dmi") - 1, file_name = file_old, stop_running = stop_running)
        if stop_running.is_set():
            return
        
        if not result_list_bytes_old and not result_list_data_old:
            print("No valid DMI data could be found. Check inputfile. Stopping...")
            output_window_log("\nNo valid DMI data could be found. Check old image file. Stopping...\n")
            return
        
        else:
            pass
        
        
        image_content_new = list(image_new.read().decode("ANSI"))
        image_new.close()
        if stop_running.is_set():
            return
        
        
        
        result_list_data, result_list_bytes = keyUEFI_finder.keyUEFIFinderMain("Dmi", len("Dmi") - 1, file_name = file_new, stop_running = stop_running)
        if stop_running.is_set():
            return
        
        if not result_list_bytes and not result_list_data:
            print("No valid DMI data addresses could be found. Check templatefile. Stopping...")
            output_window_log("\nNo valid DMI data addresses could be found. Check new image file. Stopping...\n")
            return
            
        else:
            pass
            

        
        dmi_data_old = []
        dmi_data_old_cache = ""
        

        
        
        for byte_adress_index in range (0, len(result_list_bytes), 1):
            
            if stop_running.is_set():
                return
            
            
            
            dmi_area_name_old = result_list_data_old[byte_adress_index]
            dmi_area_position_old = result_list_bytes_old[byte_adress_index]
            
            if dmi_area_name_old[-1] == '2':
                dmi_area_size = dmi_vars_size[dmi_area_name_old[0:len(dmi_area_name_old) - 1]]
            
            else:
                dmi_area_size = dmi_vars_size[dmi_area_name_old]
            
            dmi_area_offset = len(dmi_area_name_old)
            
            for byte_index in range (dmi_area_position_old + dmi_area_offset, dmi_area_position_old + dmi_area_offset + dmi_area_size, 1):
                dmi_data_old_cache += image_content_old[byte_index]
                
                if stop_running.is_set():
                    return
                
            
            dmi_data_old.append(dmi_data_old_cache)
            
            dmi_data_old_cache = ""
        
        
    ############################################################################
        machine_model = "N/A"
        serial_number = "N/A"
        brand_id = "N/A"
        license_OS = "N/A"
        
        for dmivarindex, dmivarname in enumerate(result_list_data_old):
            
            if stop_running.is_set():
                return
            
            
            if dmivarname == "DmiVar0100010500":
                machine_model = dmi_data_old[dmivarindex][1:11]

            if dmivarname == "DmiVar0100010700":
                serial_number = dmi_data_old[dmivarindex][1:len(dmi_data_old[3])]
        
            if dmivarname == "DmiVar0100010600":
                brand_id = dmi_data_old[dmivarindex][1:len(dmi_data_old[4])]
                
            if dmivarname == "DmiVar0200020600":
                license_OS = dmi_data_old[dmivarindex][1:len(dmi_data_old[-1]) - 1]
        
        print("")
        print("###################################################")
        print("Found UEFI image \"{filename}\" DMI data: ".format(filename = file_old))

        print("Machine Model:", machine_model)
        print("Brand ID:", brand_id)
        print("Serial number:", serial_number)
        print("OS license:", license_OS)
        print("###################################################")
        print("")
        
        output_window_log("\n")
        output_window_log("###################################################\n")
        output_window_log("Found UEFI image DMI data:")

        output_window_log("\nMachine Model: {machine_model}".format(machine_model = machine_model))
        output_window_log("\nBrand ID: {brand_id}".format(brand_id = brand_id))
        output_window_log("\nSerial number: {serial_number}".format(serial_number = serial_number))
        
        output_window_log("\nOS license: {license_OS}".format(license_OS = license_OS))
        output_window_log("\n###################################################\n")
        output_window_log("\n")
        
        
    ############################################################################


        output_window_log("Replacing DMI data...\n")
        print("Replacing DMI data...")
        
        
        for byte_adress_index_new in range (0, len(result_list_bytes), 1):
            
            if stop_running.is_set():
                return
            
            
            dmi_area_name_old = result_list_data_old[byte_adress_index_new]
            #print(dmi_area_name_old)
            dmi_area_position_new = result_list_bytes[result_list_data.index(dmi_area_name_old)]
            
            if dmi_area_name_old[-1] == '2':
                dmi_area_size = dmi_vars_size[dmi_area_name_old[0:len(dmi_area_name_old) - 1]]
            
            else:
                dmi_area_size = dmi_vars_size[dmi_area_name_old]
            
            
            if dmi_area_size != False:
                
                dmi_area_offset = len(dmi_area_name_old)
                dmi_area_content = dmi_data_old[byte_adress_index_new]
                
                
                for byte_index in range(0, dmi_area_size):
                    if stop_running.is_set():
                        return
                    image_content_new[byte_index + dmi_area_position_new + dmi_area_offset] = dmi_area_content[byte_index]
            
        
        result_list_data_old_serial, result_list_bytes_old_serial = keyUEFI_finder.keyUEFIFinderMain("SerialNUM", len("SerialNUM") - 1, file_name = file_old, stop_running = stop_running)
        if stop_running.is_set():
            return
        result_list_data_serial, result_list_bytes_serial = keyUEFI_finder.keyUEFIFinderMain("SerialNUM", len("SerialNUM") - 1, file_name = file_new, stop_running = stop_running)
        if stop_running.is_set():
            return
        
        old_serial_data_pos = result_list_bytes_old_serial[0]
        new_serial_data_pos = result_list_bytes_serial[0]
        dmi_area_offset = len("SerialNum")
        dmi_area_size = dmi_vars_size["SerialNum"]
        
        for byte_index in range(0, dmi_area_size, 1):
            if stop_running.is_set():
                return
            image_content_new[new_serial_data_pos + dmi_area_offset + byte_index] = image_content_old[old_serial_data_pos + dmi_area_offset + byte_index]
        
        print("DMI data replace finished!")
        output_window_log("DMI data replace finished!\n")
        
        
        WinKeyReplace(image_content_new, image_content_old, file_old, file_new, stop_running)
    
    
    
    

    
    inputfile = ""
    templatefile = os.path.abspath(os.getcwd()) + "\\templates\\bios_template.bin"
    

    global cancel_button_clicked
    cancel_button_clicked = False

    
    def browseFiles_template():
        filename = tkinter.filedialog.askopenfilename(initialdir = os.path.abspath(os.getcwd()),
                                            title = "Select a File",
                                            filetypes = (("Bin files",
                                                            "*.bin*"),
                                                         ("Rom files",
                                                            "*.rom"),
                                                        ("All files",
                                                            "*.*")))
        
        
        # Correction
        if filename != "":
            templatefile = ""
            
            for char in filename:
                if char != '/':
                    templatefile += char
                else:
                    templatefile += "\\"
            
            # Change label contents
            
            path_templatefile.delete('0', tkinter.END)
            path_templatefile.insert(tkinter.END, templatefile)

        
    
    def browseFiles_inputfile():
        filename = tkinter.filedialog.askopenfilename(initialdir = os.path.abspath(os.getcwd()),
                                            title = "Select a File",
                                            filetypes = (("Bin files",
                                                            "*.bin*"),
                                                         ("Rom files",
                                                            "*.rom"),
                                                        ("All files",
                                                            "*.*")))
        

        # Correction
        if filename != "":
            inputfile = ""
            
            for char in filename:
                if char != '/':
                    inputfile += char
                else:
                    inputfile += "\\"
            
            # Change label contents
            
            path_inputfile.delete('0', tkinter.END)
            path_inputfile.insert(tkinter.END,inputfile)


    def output_window_log(string_to_output):
        output_textwidget["state"] = tkinter.NORMAL
        output_textwidget.insert(tkinter.END, string_to_output)
        output_textwidget.see("end")
        output_textwidget["state"] = tkinter.DISABLED


    def set_buttons_on(on):
        if on:
            start_button["state"] = tkinter.NORMAL
            exit_button["state"] = tkinter.NORMAL
            path_inputfile["state"] = tkinter.NORMAL
            chooseinputfile["state"] = tkinter.NORMAL
            checkbox_enable_change["state"] = tkinter.NORMAL
            donate_button["state"] = tkinter.NORMAL
        if not on:
            start_button["state"] = tkinter.DISABLED
            exit_button["state"] = tkinter.DISABLED
            path_inputfile["state"] = tkinter.DISABLED
            chooseinputfile["state"] = tkinter.DISABLED
            choosetemplatefile["state"] = tkinter.DISABLED
            checkbox_enable_change["state"] = tkinter.DISABLED
            donate_button["state"] = tkinter.DISABLED
    
        
    def choosetemplatefile_control():
        if enabled_var.get():
            path_templatefile["state"] = tkinter.NORMAL
            choosetemplatefile["state"] = tkinter.NORMAL
            
            
        if not enabled_var.get():
            path_templatefile.delete('0', tkinter.END)
            path_templatefile.insert(tkinter.END, templatefile)
            path_templatefile["state"] = tkinter.DISABLED
            choosetemplatefile["state"] = tkinter.DISABLED

            
    
    def cancel_button_callback():
        global cancel_button_clicked
        if not cancel_button_clicked:
            cancel_button_clicked = True
    
    
    def change_activitylabel(state):
        if state == "running":
            label_activity.config(fg="#32CD32")
            label_activity.config(text="Status: Active")
            
        if state == "stopped":
            label_activity.config(fg="#FF0000")
            label_activity.config(text="Status: Inactive")
        
        if state == "stopping":
            label_activity.config(fg="#FF0000")
            label_activity.config(text="Status: Stopping...")
            

    
    def watchDog(event_instance, thread_instance):
        print("Starting WatchDog...")
        change_activitylabel("running")
        
        checkpoint_time = time.time()
        time_warning_call = False
        
        while True:
            if cancel_button_clicked:
                change_activitylabel("stopping")
                output_window_log("\nCancelling...\n")
                print("Cancelling...")
                event_instance.set()
                thread_instance.join()
                change_activitylabel("stopped")
                set_buttons_on(True)
                print("WatchDog stopped")
                break
            
            if not thread_instance.is_alive():
                output_window_log("\nOperation completed in {:.1f}s\n".format(time.time() - checkpoint_time))
                set_buttons_on(True)
                change_activitylabel("stopped")
                print("WatchDog stopped")
                break
            
            if time.time() - checkpoint_time > 100 and not time_warning_call:
                output_window_log("\nWATCHDOG_WARNING: Replace thread is running for 100s already. That's unusual.")
                time_warning_call = True
            
            
            time.sleep(0.5)
            
  
  
    def run():
        
        global _TIME_CONST
        _TIME_CONST = int(str(time.time())[0:10])
        
        set_buttons_on(False)
        
        stop_running = threading.Event()
        stop_running.clear()
        
        global cancel_button_clicked
        cancel_button_clicked = False
        
        input_file = path_inputfile.get()
        template = path_templatefile.get()

        thread_main = threading.Thread(target=dmi_data_replace, args=(input_file, template, stop_running))
        thread_main.start()

        thread_watchDog = threading.Thread(target=watchDog, args=(stop_running, thread_main, ))
        thread_watchDog.start()
                

    
    def start_donate_window():
        donate_window = tkinter.Toplevel(main_window)
        donate_window.title("Donate")
        donate_window.geometry("390x200" + "+" + str(int(x)) + "+" + str(int(y)))
        donate_window.iconbitmap("icon.ico")
        
        expla_label = tkinter.Label(donate_window, text = "There went a lot of work into creating this software.\n I'd be happy if you support me through a donation.")
        expla_label.place(x = 50, y = 20)
        
        
        donate_link = tkinter.Label(donate_window, text = "Click me", fg = "blue", cursor = "hand2")
        underline_font = tkinter.font.Font(donate_link, donate_link.cget("font"))
        underline_font.configure(underline = True)
        donate_link.configure(font = underline_font)
        donate_link.bind("<Button-1>", lambda e: browser_callback())
        donate_link.place(x = 163, y = 80)
        
        thank_label = tkinter.Label(donate_window, text = "Thank you!❤️")
        thank_label.place(x = 157, y = 130)
        
        donate_window.transient(main_window)
        donate_window.grab_set()
        style_donate_window = tkinter.ttk.Style(donate_window)
        
        main_window.wait_window(donate_window)
    
    
    def browser_callback():
        webbrowser.open(_DONATE_URL)
    
    
    
    window_width = 700
    window_height = 300




    main_window = tkinter.Tk()
    main_window.title("UEFI-DDWKR V1.0")
    
    sw = main_window.winfo_screenwidth()
    sh = main_window.winfo_screenheight()
    
    x = (sw/2) - (window_width/2)
    y = (sh/2) - (window_height/2)
    
    
    main_window.geometry(str(window_width) + "x" + str(window_height) + "+" + str(int(x)) + "+" + str(int(y)))
    main_window.minsize(window_width, window_height)
    main_window.maxsize(window_width, window_height)
    main_window.iconbitmap("icon.ico")
    style = tkinter.ttk.Style(main_window)
    
    
    output_textwidget = tkinter.Text(main_window, height = 10, width = 84)
    output_textwidget.place(x = 10, y = 10)
    output_window_log("UEFI-DDWKR V1.0 by Zombi3000\n")
    
    start_button = tkinter.ttk.Button(main_window, text = "Start", width = 10, command = run)
    start_button.place(x = 610, y = 262)
    
    cancel_button = tkinter.ttk.Button(main_window, text = "Cancel", width = 10, command = cancel_button_callback)
    cancel_button.place(x = 530, y = 262)
    
    
    exit_button = tkinter.ttk.Button(main_window, text = "Exit", width = 10, command = exit)
    exit_button.place(x = 450, y = 262)
    



    donate_button = tkinter.ttk.Button(main_window, text="Donate", width = 10, command=start_donate_window)
    donate_button.place(x = 370, y = 262)
    
    label_activity = tkinter.Label(main_window, text="Status: Inactive")
    label_activity.config(fg="#FF0000")    
    label_activity.place(x = 200, y = 264)

    
    inputfile_pos_y = 188
    label_inputfile = tkinter.Label(main_window, text="Input file:")
    label_inputfile.place(x = 10, y = inputfile_pos_y)
    path_inputfile = tkinter.ttk.Entry(main_window, width = 83)
    path_inputfile.insert(tkinter.END, inputfile)
    path_inputfile.place(x = 90, y = inputfile_pos_y)
    chooseinputfile = tkinter.ttk.Button(main_window, text = "Change File", width = 11, command = browseFiles_inputfile)
    chooseinputfile.place(x = 605, y = inputfile_pos_y - 2)
    
    
    
    
    templatefile_pos_y = 220
    label_templatefile = tkinter.Label(main_window, text="Template file:")
    label_templatefile.place(x = 10, y = templatefile_pos_y)
    path_templatefile = tkinter.ttk.Entry(main_window, width = 83)
    #path_inputfile.config(wrap='none')
    path_templatefile.insert(tkinter.END, templatefile)
    path_templatefile.place(x = 90, y = templatefile_pos_y)
    enabled_var = tkinter.IntVar()
    checkbox_enable_change = tkinter.ttk.Checkbutton(main_window, variable = enabled_var, text = "Change template file", onvalue=1, offvalue=0, command=choosetemplatefile_control)
    enabled_var.set(0)
    checkbox_enable_change.place(x = 13, y = 264)
    choosetemplatefile = tkinter.ttk.Button(main_window, text = "Change File", width = 11, command = browseFiles_template)
    choosetemplatefile.place(x = 605, y = templatefile_pos_y - 2)
    path_templatefile["state"] = tkinter.DISABLED
    choosetemplatefile["state"] = tkinter.DISABLED
    
    
    
    
    main_window.mainloop()


def initialize():
    version = 1.0
    
    name_art = ("   __  __________________     ____  ____ _       ____ __ ____\n"
    "  / / / / ____/ ____/  _/    / __ \/ __ \ |     / / //_// __ \\\n"
    " / / / / __/ / /_   / /_____/ / / / / / / | /| / / ,<  / /_/ /\n"
    "/ /_/ / /___/ __/ _/ /_____/ /_/ / /_/ /| |/ |/ / /| |/ _, _/\n" 
    "\____/_____/_/   /___/    /_____/_____/ |__/|__/_/ |_/_/ |_|\n")
    
    print(name_art)
    print("UEFI-ddwkr V{version_num} by ZombiDebugWall".format(version_num = version))
    
    #dmi_data_replace(old_file, new_file)
    run_tkinter_interface(name_art)
    
    
    
    
if __name__ == "__main__":
    initialize()