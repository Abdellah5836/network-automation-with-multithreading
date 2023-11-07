from netmiko import Netmiko
import re
import pandas as pd
import concurrent.futures



def device_processin():
    prompt = "[+] This script merely understand Excel extension files, "
    prompt += "\nplease enter the excel file that contains the devices you want to make connections to"
    print(prompt)

    filepath01 = input("File name: ")
    if filepath01:
        extension = 'xlsx'
        pattern = r'[\w\.-_]+\.' + extension + '$'
        try:
            if re.match(pattern, filepath01):
                df = pd.read_excel(filepath01)
                df.drop(columns=['Unnamed: 0'], inplace=True)
                devicesList = df.to_dict(orient='records')
            else:
                return "[!] The script could not understand the file extension."
        except Exception as e:
            print(e)
        else:
            return devicesList
    else:
        print("[!] FIle name must not be empty.")



def command_processin():
    prompt = "\n[+] please enter the excel file that contains the configuration commands that will be executed"
    print(prompt)

    filepath02 = input("File name: ")
    if filepath02:
        extension02 = 'xlsx'
        pattern02 = r'[\w\.-_]+\.' + extension02 + '$'
        try:
            if re.match(pattern02, filepath02):
                df = pd.read_excel(filepath02)
                # df.drop(columns=['Unnamed: 0'], inplace=True)
                len_columns = len(df.columns)
                list_lists = [[] for i in range(len_columns)]

                for i, column_name in enumerate(df.columns):
                    list_lists[i] = df[column_name].tolist()
            else:
                return "[!] The script could not understand the file extension."
        except Exception as e:
            print(e)
        else:
            return list_lists
    else:
        print("[!] File name must not be empty.")


def main_config(host, cmd):
    # deviceList = device_processin()
    # listLists = command_processin()


    # for host, cmd in zip(deviceList, listLists):
        try:
            print(f"\n**** Connecting to {host['host']} ****")
            net_connect = Netmiko(**host)
            net_connect.enable()

            output = net_connect.send_config_set(cmd)
        except:
            print(f"\n**** Can not login to {host['host']} ****")
        else:
            print(output)



def ssh_threadin():
        deviceList = device_processin()
        listLists = command_processin()
        results = []
        
        if deviceList is not None and listLists is not None:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(main_config, host, cmd) for host, cmd in zip(deviceList, listLists)]
            
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        results.append(result)
            
            print(results)
            




ssh_threadin()
