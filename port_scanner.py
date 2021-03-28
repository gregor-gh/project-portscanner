import socket
import common_ports

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)


def get_open_ports(target, port_range, verbose=False):

    # check if target is host or ip
    if target[0].isnumeric() == True:
        targettype = "IP"
        # check if valid ip
        try:
            socket.inet_aton(target)
        except socket.error:
            return "Error: Invalid IP address"
    else:
        targettype = "HOST"
        # check if valid host by looking up in dns
        try:
            socket.gethostbyname(target)
        except socket.gaierror:
            return "Error: Invalid hostname"

    open_ports = []
    for port in range(port_range[0], port_range[1]+1):
        if port in common_ports.ports_and_services:
            if s.connect_ex((target, port)):
                open_ports.append(port)

    # if verbose is false we just return the list
    if verbose == False:
        return (open_ports)

    # otherwise build the return string
    # get the url and hostname
    if targettype == "IP":
        try:
            hostname = socket.gethostbyaddr(target)
            response = "Open ports for " + hostname[0] + " (" + target + ")\n"
        except:
            response = "Open ports for "+target+"\n"
    else:
        ip = socket.gethostbyname(target)
        response = "Open ports for " + target + " (" + ip + ")\n"

    # title and headers
    response += "PORT     SERVICE\n"

    for port in open_ports:
        spaces = 9 - len(str(port))
        spacestring = ""
        for space in range(spaces):
            spacestring += " "

        response += str(port)+spacestring + \
            common_ports.ports_and_services[port]+"\n"

    # remote last newline
    response = response[:-1]
    return response


ports = get_open_ports("scanme.nmap.org", [20, 80], True)
print(ports + '\n')
