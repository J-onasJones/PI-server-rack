from ftplib import FTP
from io import BytesIO
from time import sleep, time
from xml.sax.handler import feature_namespace_prefixes

launch_time = time()

print_stats = True

hostname = "172.24.1.193"
username = "testuser"
password = "uwu"

ftp = FTP(hostname, username, password)
ftp.encoding = "utf-8"

filename = "output.txt"

while True:
    start_time = time()

    with open(filename, "wb") as file:
        # use FTP's RETR command to download the file
        ftp.retrbinary(f"RETR {filename}", file.write)

    file = open(filename, 'r')
    content = file.read()
    content = content.split(";")

    fanmode = content[0]
    slave_fanmode = content[1]
    fanspeed = content[2]
    fanspeed2 = content[3]
    thermal = content[4]
    slave_thermal = content[5]
    cpu_usage = content[6]
    cpu_freq = content[7]
    cpu_up = content[8]
    total_ram = content[9]
    ram_usage = content[10]
    ram_free = content[11]
    ram_percent = content[12]
    swap_percent = content[13]
    disk_percent = content[14]

    mc_motd = content[15]
    mc_version = content[16]
    mc_players_max = content[17]
    mc_players_on = content[18]
    mc_version_brand = content[19]
    mc_plugins = content[20]
    mc_playerlist = content[21]

    sleep(2)

    stop_time = time()

    if print_stats:
        print("---------- Uptime: " + str(cpu_up) + " ----------")
        print("Loop time:\t" + str(round(stop_time - start_time, 2)) + "\ts")
        print("CMD Uptime:\t" + str(round(stop_time - launch_time, 2)) + "\ts")
        print("CPU")
        print("\tusage:\t" + str(cpu_usage) + "\t%")
        print("\tfreq:\t" + str(cpu_freq) + "\tMHz")
        print("\ttemp:\t" + str(thermal) + "\tC")
        print("RAM")
        print("\tusage:\t" + str(ram_percent) + "\t%")
        print("\tswap :\t" + str(swap_percent) + "\t%")
        print("Disks")
        print("\tusage:\t" + str(disk_percent) + "\t%")
        print("FANMODE")
        print("\tmain:\t" + str(fanmode) + "\t%")
        print("\tslave:\t" + str(slave_fanmode) + "\t%")
        print("\tglobal:\t" + str(fanspeed) + "\t%")
        print("\t2ndary:\t" + str(fanspeed2) + "\t%")


# Close the Connection
ftp.quit()