#!/usr/bin/python

import spotify, getpass, threading, logging

# Start logging.
logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('spotify').setLevel(logging.INFO) # Turn off spotify logger.
logged_in_event = threading.Event()
end_of_track = threading.Event()

def connection_state_listener(session):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        logged_in_event.set()

def end_of_track_listener(self):
    end_of_track.set()

session = spotify.Session()
loop = spotify.EventLoop(session)
loop.start()
session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED,
           connection_state_listener)
session.on(spotify.SessionEvent.END_OF_TRACK, end_of_track_listener)

print "Logging into Spotify..."
session.login(raw_input("Username: "), getpass.getpass(), remember_me=True)
# session.relogin()
logged_in_event.wait()

# Logged in, user session has started.

audio = spotify.PortAudioSink(session)
track = session.get_track('spotify:track:3Eh33UmqyS7PGIfaNQgr0d').load()
session.player.load(track)
session.player.play()

while not end_of_track.wait(0.1):
    pass
