
*********************************************************************************************************
**************************************
1. Event Script:
**************************************

-> Event script je volan pri dosle event z librespot (Spotify), zajisti dostuonost souboru
CONFIG: /opt/spotify/event.sh -> script volany z librespot
CONFIG: /opt/spotify/event.py -> script volany z event.sh, ktery ovlada LARA prehravac
CMD: sudo chmod 777 /opt/spotify/event.sh /opt/spotify/event.py

*********************************************************************************************************
**************************************
2. Instalace Raspotify:
**************************************

-> Vytvori z CS Spotify Connect zarizeni
URL: https://github.com/dtcooper/raspotify
CMD: curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
CONFIG: /etc/default/raspotify -> doplnit cestu ke scriptu:

    OPTIONS="--onevent /opt/spotify/event.sh"

*********************************************************************************************************
**************************************
3. Pridani uzivatele imm do skupiny audio
**************************************

CMD: sudo adduser imm audio

*********************************************************************************************************
**************************************
4. ALSA Loopback
**************************************

-> Vytvori virtualni nahravaci zarizeni Loopback
CMD: sudo modprobe snd-aloop
CONFIG: /etc/modules -> doplnit moduly pro zajisteni aktivace pri Boot:

    snd_bcm2835
    snd-aloop

*********************************************************************************************************
**************************************
5. Povoleni Audio modulu
**************************************

CONFIG: /boot/config.txt -> zkontrolovat, ze je povoleno:

    dtparam=audio=on

*********************************************************************************************************
**************************************
6. ALSA Default soudcard
**************************************

-> Nastaveni default karty
CONFIG: /usr/share/alsa/alsa.conf -> nastavit default kartu:

    defaults.ctl.card 1
    defaults.pcm.card 1

*********************************************************************************************************
**************************************
7. Reboot
**************************************

CMD: sudo reboot

*********************************************************************************************************
**************************************
8. Kontrola
**************************************

-> Pokud je vse spravne nastaveno, zobrazi se dostupna zarizeni pro prehravani a zaznam
CMD: aplay -l
CMD: arecord -l

*********************************************************************************************************
**************************************
9. Instalace DarkIce a IceCast:
**************************************

-> Vytvoreni premosteni streamu
URL: https://gist.github.com/bmweiner/f80e7aaeca5bcee1db46e56914b415fa
URL: https://stmllr.net/blog/live-mp3-streaming-from-audio-in-with-darkice-and-icecast2-on-raspberry-pi/

**************************************
9.1. IceCast
**************************************

-> Distribuuje audio stream
CMD: sudo apt-get update
CMD: sudo apt-get install icecast2
CONFIG: /etc/icecast2/icecast.xml -> upravit pro snizeni latence a zmenu portu:

    <limits>
        <burst-on-connect>0</burst-on-connect>
        <burst-size>0</burst-size>
    </limits>

    <listen-socket>
        <port>50000</port>
    </listen-socket>

CONFIG: /etc/init.d/icecast2 -> vytvoreni slozky pro Logging z duvodu mazani adresare pri Boot:

    LOG_PATH=/var/log/icecast2
    sudo mkdir $LOG_PATH
    sudo touch $LOG_PATH/access.log
    sudo touch $LOG_PATH/error.log
    sudo chown -R 777 $LOG_PATH
    sudo chown -R icecast2 $LOG_PATH

CONFIG: /etc/default/icecast2 -> povoleni sluzby (nemusi byt vzdy):
    ENABLE=true

CMD: sudo systemctl start icecast2
CMD: sudo systemctl enable icecast2

**************************************
9.2. DarkIce
**************************************

-> Zachytava audio ze vstupu a posila do IceCast
CMD: sudo apt-get install darkice
CONFIG: /etc/darkice.cfg -> vytvorit soubor a pridat:

    # see the darkice.cfg man page for details

    # this section describes general aspects of the live streaming session
    [general]
    duration        = 0                # duration of encoding, in seconds. 0 means forever
    bufferSecs      = 1                # size of internal slip buffer, in seconds
    reconnect       = yes              # reconnect to the server(s) if disconnected
    realtime        = yes
    rtprio          = 3

    # this section describes the audio input that will be streamed
    [input]
    device          = hw:Loopback,1,0  # Alsa soundcard device for the audio input
    sampleRate      = 44100            # sample rate in Hz. try 11025, 22050 or 44100
    bitsPerSample   = 16               # bits per sample. try 16
    channel         = 2                # channels. 1 = mono, 2 = stereo

    # this section describes a streaming connection to an IceCast2 server
    # there may be up to 8 of these sections, named [icecast2-0] ... [icecast2-7]
    # these can be mixed with [icecast-x] and [shoutcast-x] sections
    [icecast2-0]
    bitrateMode     = vbr              # variable bit rate
    format          = mp3              # format of the stream: mp3
    quality         = 1.0              # quality of the stream sent to the server
    server          = localhost        # host name of the server
    port            = 50000            # port of the IceCast2 server
    password        = hackme           # source password to the IceCast2 server
    mountPoint      = spotify          # mount point of this stream on the IceCast2 server
    name            = Spotify          # name of the stream
    description     = CS Spotify       # description of the stream
    genre           = Custom           # genre of the stream
    #public          = no               # advertise this stream?
    #localDumpFile   = recording.mp3    # Record also to a file

CONFIG: /etc/systemd/system/darkice.service -> vytvorit soubor a pridat:

    [Unit]
    Description=DarkIce Live audio streamer
    After=icecast2.service

    [Service]
    ExecStart=/usr/bin/darkice

    [Install]
    WantedBy=multi-user.target
                
CMD: sudo chmod 777 /etc/systemd/system/darkice.service

CMD: sudo systemctl daemon-reload
CMD: sudo systemctl start darkice.service
CMD: sudo systemctl enable darkice.service

*********************************************************************************************************
**************************************
10. Reboot
**************************************

CMD: sudo reboot

*********************************************************************************************************
