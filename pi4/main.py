from http import server
import RPi.GPIO as GPIO
import subprocess, os, time

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Powering Status Pin to indicate that control program is up
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, True)

# setting up communication pins for binary fanmode transmission
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.IN)

# setting up control pin for fancontrol
GPIO.setuo(4, GPIO.OUT)

# define default variables -> fan speed will be at max. if someting goes wrong with getting cpu temps
thermal = -99
fanmode = 100
i = 0

file = open("output.txt", 'r+')

cpu_usage = "--"
total_ram = "--.--"
ram_usage = "--.--"
ram_free = "--.--"

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
    thermal = str(round(float(subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True).rstrip())/1000,2))
    if thermal <= 20:
        fanmode = 0
    elif 20 < thermal <= 40:
        fanmode = 25
    elif 40 < thermal <= 60:
        fanmode = 50
    elif 60 < fanmode <= 70:
        fanmode = 75
    elif 70 < fanmode:
        fanmode = 100
    return thermal, fanmode

# function to round values
def display(val):
  return round(float(val),2)

# function to get system informations
def sys_monitor(cpu_usage, total_ram, ram_usage, ram_free):
    cpu_usage = str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2))
    total_ram = str(round(display(subprocess.check_output("free | awk 'FNR == 2 {print $2/1000000}'", shell=True))))
    ram_usage = str(subprocess.check_output("free | awk 'FNR == 2 {print $3/($3+$4)*100}'", shell=True))
    ram_free = str(100 - display(ram_usage))
    return cpu_usage, total_ram, ram_usage, ram_free

# function to get server status if enabled
def mcserver(mc_motd, mc_version, mc_players_max, mc_players_on, mc_version_brand, mc_plugins, mc_player_list):
    if check_mcserver:
        # importing module mcstatus --> must be installed for this in order to work
        from mcstatus import MinecraftServer
        mcserver = MinecraftServer.lookup(mc_ip + ":" + mc_port)
        status = mcserver.status()
        mc_motd = status.description
        mc_version = status.version.name
        mc_players_max = status.players.max
        mc_players_on = status.players.online

        # IMPORTANT!
        # for the following code to work, the query must be enabled in the server config file ('server.properties' --> 'enable-query=True'). 
        # If you don't have access to that file but still want your server status, you can delete the following lines that contain the 'query' argument. 
        # This will provide you with a more limited status: 
        #   the version brand (vanilla, fabric modded, bukkit, etc.), the plugin list (if any) and the list if players won't be visible in that case
        query = mcserver.query()
        mc_version = query.software.version
        mc_version_brand = query.software.brand
        mc_plugins = query.software.plugins
        mc_player_list = query.players.names

        # if no query --> delete 'mc_version_brand', 'mc_plugins' and 'mc_player_list' from the return argument
        # the line below should then look like THIS: return mc_motd, mc_version, mc_players_max, mc_players_on
        return mc_motd, mc_version, mc_players_max, mc_players_on, mc_version_brand, mc_plugins, mc_player_list


while True:
    # eecute temperature function

    temp(thermal, fanmode)
    # determine fanmode of 2nd raspberry PI and guess CPU temps
    if GPIO.input(17) and GPIO.input(18):
        slave_fanmode = 75
        slave_thermal = "60 - 70"
    elif GPIO.input(17) and not GPIO.input(18):
        slave_fanmode = 50
        slave_thermal = "40 - 60"
    elif not GPIO.input(17) and GPIO.input(18):
        slave_fanmode = 25
        slave_thermal = "0 - 40"
    elif not GPIO.input(17) and not GPIO.input(18):
        slave_fanmode = 100
        slave_thermal = "70 - 100"
    else:
        slave_fanmode = 100
        slave_thermal = "-"
    
    # get other system infos and Minecraft Server stats
    sys_monitor(cpu_usage, total_ram, ram_usage, ram_free)
    mcserver(mc_motd, mc_version, mc_players_max, mc_players_on, mc_version_brand, mc_plugins, mc_player_list)

    # write all data to list
    system_infos = [fanmode, slave_fanmode, thermal, slave_thermal, cpu_usage, total_ram, ram_usage, ram_free, mc_motd, mc_version, mc_players_max, mc_players_on, mc_version_brand, mc_plugins, mc_player_list]

    # delete all text in file and write list to file
    file.truncate(0)
    for e in system_infos:
        file.write(e)
        file.write(";")
    
    # determine the PI with higher CPU temperature
    if slave_fanmode > fanmode:
        fanspeed = slave_fanmode
    else:
        fanspeed = fanmode
    if fanmode == 100:
        GPIO.output(4, True)
        time.sleep(5)
    elif fanmode == 75:
        while i < 12:
            GPIO.output(4, True)
            time.sleep(0.3)
            GPIO.outut(4, False)
            time.sleep(0.1)
            i += 1
    elif fanmode == 50:
        while i < 25:
            GPIO.output(4, True)
            time.sleep(0.1)
            GPIO.output(4, False)
            time.sleep(0.1)
            i += 1
    elif fanmode == 25:
        while i < 12:
            GPIO.output(4, True)
            time.sleep(0.1)
            GPIO.outut(4, False)
            time.sleep(0.3)
            i += 1
    else:
        GPIO.output(4, True)
        time.sleep(5)