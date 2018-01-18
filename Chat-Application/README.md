# Name
        Chat - Simple p2p Threaded Java Chat Application

# Compiling Instruction
        javac Chat.java

# Execute Instruction
        java Chat [listener port]

# Synopsis
        Chat [listener port]

# Description
        Starts a p2p chat application able to connect to other chat peer processes via a network.

# Arguments
        help
            Returns all possible commands available
        
        myip
            Returns current ip address
        
        myport
            Returns the listening port for this process
        
        connect [destination ip address] [listening port]
            Establishes a connection to a peer process with the given IP address and listening port
        
        terminate [connection id]
            Terminates the connection with a peer based on connection id

        send [connection id] [message]
            Sends contents of message to given connection id

        exit
            Exits the process
