VERSION = "0.1.1"

from ftplib import FTP
from io import BytesIO
from time import sleep, time

launch_time = time()

print("Starting PI-MC-WATCHER v" + VERSION + " for PC and Mac")
print("Initializing...")

# wehther or not to print the stats to the console
print_stats = True

# The credentials for the ftp server. These must be tweaked.
hostname = "172.24.1.193"
username = "testuser"
password = "uwu"

# defining the name of the file the stats are saved to
filename = "output.txt"

print("Connecting to FTP server...")

ftp = FTP(hostname, username, password)
ftp.encoding = "utf-8"

print("Connected!")

start_time = time()

print("All setup!")

# permits user to read console logs from above. Can be removed to accelerate start.
sleep(3)

while True:

    with open(filename, "wb") as file:
        # use FTP's RETR command to download the file
        ftp.retrbinary(f"RETR {filename}", file.write)

    file = open(filename, 'r')
    content = file.read()
    content = content.split(";")
    # it is possible for the program to fetch the output text file right inbetween when the program on the Master PI cleared it and before it writes the stats.
    # This sends an error message in the rare case of this occuring.
    try:
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
    except:
        # The error message to display if the above explained happens
        print("WARNING: Couldn't read the file's data. If this doesn't happen a lot, just ignore this warning.")


    if print_stats:
        print("---------- Uptime: " + str(cpu_up) + " ----------")
        # loop_time and stop_time won't be available on the first run as they haven't been measured yet. Therefore this fallback is needed.
        try:
            print("Loop time:\t" + str(round(loop_time, 2)) + "\ts")
            print("CMD Uptime:\t" + str(round(stop_time - launch_time, 2)) + "\ts")
        except:
            print("Loop time:\t--.--\ts")
            print("CMD Uptime:\t--.--\ts")
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

    sleep(2)

    stop_time = time()
    loop_time = stop_time - start_time
    start_time = time()