#!/usr/bin/python
def main():
    from sonos_extras import SonosExtrasCliHelper
    # import sonos_extras
    
    import argparse
    import os
    
    try:
        default_sonos_ip = os.environ["SONOS_EXTRAS_IP"]
    except:
        default_sonos_ip = ""
    
    #########################################
    ##### defining command line parsers #####
    #########################################
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--speaker-ip', type=str,
        help='IP of the speaker to connect to. Also can be set as SONOS_EXTRAS_IP environment variable', 
        default=default_sonos_ip)
    
    mainSubCommandParser = parser.add_subparsers(title="sub-commands", 
        description="Valid sub-commands. Use -h for each sub-commands to get detailed help.", 
        dest="sub_command")
    
    volume_commandParser = mainSubCommandParser.add_parser("volume", aliases="v", help="Get/set the volume")
    volume_commandParser.add_argument("n", nargs="?", help="Value between 0 and 100 to set/increase/decrease the volume by.")
    volume_group = volume_commandParser.add_mutually_exclusive_group()
    volume_group.add_argument("-u", "--up"  , action="store_const", const="+1"  , dest="action", help="Increase volume by n")
    volume_group.add_argument("-d", "--down", action="store_const", const="-1", dest="action", help="Decrease volume by n")
    
    current_commandParser       = mainSubCommandParser.add_parser("current", aliases="c", help="Print the current status, and playback item, if available.")
    queue_commandParser         = mainSubCommandParser.add_parser("queue", aliases="q", help="Print the current queue.")
    play_commandParser          = mainSubCommandParser.add_parser("play", aliases="p", help="Play.")
    pause_commandParser         = mainSubCommandParser.add_parser("pause", aliases="p", help="Pause.")
    stop_commandParser          = mainSubCommandParser.add_parser("stop", aliases="s", help="Stop.")
    stop_after_commandParser    = mainSubCommandParser.add_parser("stop_after", aliases=["sa"], help="Stop after the current track.")
    
    line_in_commandParser       = mainSubCommandParser.add_parser("line_in", aliases=["li"], help="Select LineIn for playback.")
    line_in_commandParser.add_argument("n", nargs="?", type=int, default=0, help="LineIn number to select.")
    
    resume_queue_commandParser  = mainSubCommandParser.add_parser("resume_queue", aliases=["rq"], help="Resume playback from the given index of the current queue.")
    resume_queue_commandParser.add_argument("n", nargs="?", type=int, default=0, help="Track index in the current queue.")
    
    args = parser.parse_args()
    # print(args)
    
    #########################################
    #####              Main             #####
    #########################################
    client = SonosExtrasCliHelper(args.speaker_ip)
    
    if   args.sub_command in ["current", "c"]:
        client.print_current_status()
    elif args.sub_command in ["queue", "q"]:
        client.print_queue()
    elif args.sub_command in ["volume", "v"]:
        if args.action != None:
            n = int(args.n) if args.n else 3
            client.volume = client.volume + (int(args.action) * n)
        elif args.n:
            client.volume = int(args.n)
        print(client.volume)
    elif args.sub_command == "p":
        if client.get_current_transport_info()['current_transport_state'] in ["STOPPED", "PAUSED_PLAYBACK"]:
            client.play()
        else:
            client.pause()
    elif args.sub_command == "play":
        client.play()
    elif args.sub_command == "pause":
        client.pause()
    elif args.sub_command in ["stop", "s"]:
        client.stop()
    elif args.sub_command in ["stop_after", "sa"]:
        client.stop_after()
    elif args.sub_command in ["line_in", "li"]:
        client.switch_to_line_in(list(client.all_zones)[args.n])
        client.play()
    elif args.sub_command in ["resume_queue", "rq"]:
        client.play_from_queue(args.n)
    elif args.sub_command == "add_uri_to_queue":
        uri ='x-file-cifs:' + args.uArgs[0]
        position = client.add_uri_to_queue(uri, args.uArgs[1] if len(args.uArgs) > 1 else 0)
        print(position, '|', uri)
    elif args.sub_command == "playlists":
        client.playlists()
    elif args.sub_command == "playlist":
        client.playlist(args.uArgs[0] if args.uArgs else "")

if __name__ == "__main__":
    main()