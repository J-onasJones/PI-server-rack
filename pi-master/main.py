VERSION = "0.1.1"

from http import server
import RPi.GPIO as GPIO
import subprocess, os, time, psutil

launch_time = time.time()

# Wether or not to print system essential stats into the console (This can have a small to medium performance impact.)
print_stats = True
# Wehter or not to ignore the slave PI. This can be useful if no second PI is connected.
ignore_slave = True

# Starting Messages
print("Starting PI-MC-WATCHER v" + VERSION + " for RPi")
print("Processing first loop. Each loop takes 5 seconds...")
print("\n")
if print_stats:
    print("The system essential stats will be printed into the console. (This can be disabled at line 8 in the program file)")
else:
    print("The system essential stats will NOT be printed into the console. (This can be enabled at line 8 in the program file)")

print("\n")

if ignore_slave:
    print("Slave will be ignored. (This can be configured at line 10 in the program file)")
else:
    print("Slave will NOT be ignored. (This can be configured at line 10 in the program file)")

# Program Delay to allow reading the above printed messages
time.sleep(5)
print("\nStarting process MAIN")

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Powering Status Pin to indicate that control program is up
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, True)

# setting up communication pins for binary fanmode transmission
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# setting up control pin for fancontrol
GPIO.setup(4, GPIO.OUT)

# setting up power pin for second fancontrol
GPIO.setup(25, GPIO.OUT)

# define default variables -> fan speed will be at max. if someting goes wrong with getting cpu temps
global thermal, fanmode, slave_fanmode, slave_thermal, i, file, cpu_usage, cpu_freq, cpu_up, total_ram, ram_usage, ram_free, ram_percent, swap_percent, disk_percent, mc_motd, mc_version, mc_players_max, mc_players_on, mc_version_brand, mc_plugins, mc_player_list
thermal = -99
fanmode = 100
i = 0

file_path = "/home/testuser/output.txt"

file = open(file_path, 'w')
file.close()

cpu_usage = 0
cpu_freq = 0
cpu_up = 0
total_ram = 0
ram_usage = 0
ram_free = 0
ram_percent = 0
swap_percent = 0
disk_percent = 0

# check mc server status too. Set to False to disable Minecraft server module
check_mcserver = True
mc_ip = "127.0.0.1"
mc_port = "25565"

mc_motd = "-"
mc_version = 0
mc_players_max = 0
mc_players_on = 0
mc_version_brand = "-"
mc_plugins = []
mc_player_list = []

# function to get cpu temperature on linux and macOS and decide on fan speed.
def temp(thermal, fanmode):
    thermal = int(round(float(subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True).rstrip())/1000,2))
    thermal = int(thermal)
    if thermal <= 20:
        fanmode = 0
    elif 20 < thermal <= 35:
        fanmode = 25
    elif 35 < thermal <= 50:
        fanmode = 50
    elif 50 < thermal <= 65:
        fanmode = 75
    elif 65 < thermal:
        fanmode = 100
    return thermal, fanmode

# function to round values
def display(val):
  return round(float(val),2)

# function to get system informations
def sys_monitor(cpu_usage, cpu_freq, cpu_up, total_ram, ram_usage, ram_free, ram_percent, swap_percent, disk_percent):
    #cpu_usage = str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2))
    cpu_usage = psutil.cpu_percent(interval=None)
    cpu_freq = psutil.cpu_freq(percpu=False)
    cpu_freq = cpu_freq.current
    cpu_up = psutil.cpu_times()
    cpu_up = cpu_up.user

    ram = psutil.virtual_memory()
    #total_ram = str(round(display(subprocess.check_output("free | awk 'FNR == 2 {print $2/1000000}'", shell=True))))
    total_ram = ram.total
    #ram_usage = int(subprocess.check_output("free | awk 'FNR == 2 {print $3/($3+$4)*100}'", shell=True))
    ram_usage = ram.used
    #ram_free = str(100 - display(ram_usage))
    ram_free = ram.free
    ram_percent = ram.percent

    swap = psutil.swap_memory()
    swap_percent = swap.percent

    disk = psutil.disk_usage('/')
    disk_percent = disk.percent


    return cpu_usage, cpu_freq, cpu_up, total_ram, ram_usage, ram_free, ram_percent, swap_percent, disk_percent

# function to get server status if enabled
def mcserver(mc_motd, mc_version, mc_players_max, mc_players_on, mc_version_brand, mc_plugins, mc_player_list):
    if check_mcserver:
        # importing module mcstatus --> must be installed for this in order to work
        from mcstatus import MinecraftServer
        mcserver = MinecraftServer.lookup(mc_ip + ":" + mc_port)
        try:
            status = mcserver.status()
            mc_motd = status.description
            mc_version = status.version.name
            mc_players_max = status.players.max
            mc_players_on = status.players.online
        except:
            status = "offline"
            mc_motd = "-"
            mc_version = "-"
            mc_players_max = "-"
            mc_players_on = "-"

        # IMPORTANT!
        # for the following code to work, the query must be enabled in the server config file ('server.properties' --> 'enable-query=True'). 
        # If you don't have access to that file but still want your server status, you can delete the following lines that contain the 'query' argument. 
        # This will provide you with a more limited status: 
        #   the version brand (vanilla, fabric modded, bukkit, etc.), the plugin list (if any) and the list if players won't be visible in that case
        try:
            query = mcserver.query()
            mc_version = query.software.version
            mc_version_brand = query.software.brand
            mc_plugins = query.software.plugins
            mc_player_list = query.players.names
        except:
            query = "unreachable"
            mc_version = "-"
            mc_version_brand = "-"
            mc_plugins = "-"
            mc_player_list = "-"

        # if no query --> delete 'mc_version_brand', 'mc_plugins' and 'mc_player_list' from the return argument
        # the line below should then look like THIS: return mc_motd, mc_version, mc_players_max, mc_players_on
        return mc_motd, mc_version, mc_players_max, mc_players_on, mc_version_brand, mc_plugins, mc_player_list


while True:
    start_time = time.time()
    # execute temperature function

    thermal, fanmode = temp(thermal, fanmode)
    # determine fanmode of 2nd raspberry PI and guess CPU temps
    if GPIO.input(17) == GPIO.HIGH and GPIO.input(18)  == GPIO.HIGH:
        slave_fanmode = 75
        slave_thermal = "60 - 70"
    elif GPIO.input(17) == GPIO.HIGH and not GPIO.input(18) == GPIO.HIGH:
        slave_fanmode = 50
        slave_thermal = "40 - 60"
    elif not GPIO.input(17) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
        slave_fanmode = 25
        slave_thermal = "0 - 40"
    elif not GPIO.input(17) == GPIO.HIGH and not GPIO.input(18) == GPIO.HIGH:
        slave_fanmode = 100
        slave_thermal = "70 - 100"
    else:
        slave_fanmode = 100
        slave_thermal = "-"
    
    # get other system infos and Minecraft Server stats
    cpu_usage, cpu_freq, cpu_up, total_ram, ram_usage, ram_free, ram_percent, swap_percent, disk_percent = sys_monitor(cpu_usage, cpu_freq, cpu_up, total_ram, ram_usage, ram_free, ram_percent, swap_percent, disk_percent)
    mc_motd, mc_version, mc_players_max, mc_players_on, mc_version_brand, mc_plugins, mc_player_list = mcserver(mc_motd, mc_version, mc_players_max, mc_players_on, mc_version_brand, mc_plugins, mc_player_list)
    
    # determine the PI with higher CPU temperature
    if ignore_slave:
        fanspeed = fanmode
    else:
        if slave_fanmode > fanmode:
            fanspeed = slave_fanmode
        else:
            fanspeed = fanmode
    
    if fanmode < 50:
        fanspeed2 = 0
        GPIO.output(25, False)
    elif fanmode >= 50:
        fanspeed2 = 100
        GPIO.output(25, True)
    elif thermal >= 85:
        os.system("sudo poweroff")

    i = 0
    

    if fanmode == 100:
        GPIO.output(4, True)
        time.sleep(2)
    elif fanmode == 75:
        while i < 6:
            GPIO.output(4, True)
            time.sleep(0.3)
            GPIO.output(4, False)
            time.sleep(0.1)
            i = i + 1
    elif fanmode == 50:
        while i < 6:
            GPIO.output(4, True)
            time.sleep(0.2)
            GPIO.output(4, False)
            time.sleep(0.2)
            i = i + 1
    elif fanmode == 25:
        while i < 6:
            GPIO.output(4, True)
            time.sleep(0.1)
            GPIO.output(4, False)
            time.sleep(0.3)
            i = i + 1
    else:
        GPIO.output(4, True)
        time.sleep(2)

    # write all data to list
    system_infos = [fanmode, slave_fanmode, fanspeed, fanspeed2, thermal, slave_thermal, cpu_usage, cpu_freq, cpu_up, total_ram, ram_usage, ram_free, ram_percent, swap_percent, disk_percent, mc_motd, mc_version, mc_players_max, mc_players_on, mc_version_brand, mc_plugins, mc_player_list]

    # delete all text in file and write list to file
    file = open(file_path, 'r+')
    file.truncate(0)
    file.close()
    file = open(file_path, 'w')
    for e in system_infos:
        file.write(str(e))
        file.write(";")
    file.close()

    stop_time = time.time()

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
    