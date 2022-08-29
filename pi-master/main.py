# Purpose:
# - transmit the following to Arduino using binary:
#   - uptime
#   - cpu usage (core #0 - #3)
#   - cpu frequency
#   - cpu temps (RPI 4)
#   - cpu temps (RPI 1.2)
#   - ram usage
#   - am capacity
#   - swap usuage
#   - disk usage
#   - disk capacity
#   - disk used
#   - mc server motd
#   - mc sever version
#   - mc server version brand
#   - mc server players max
#   - mc server players online
#   - mc server plugins
#   - mc server player_list
#   - amount of connected devices
#   - fan speed 180mm fan
#   - fan speed 40mm fan

# - receive the following from the Arduino:
#   - connected pc (can only be one)
#   - used current of RPI 4
#   - used current of RPI 1.2
#   - requested fan curve

# - bundle all infos together for Network fetches
# - manage Fan speeds based on fan curve and cpu temps of both pi's
# - binary task feedback LED with button on front IO