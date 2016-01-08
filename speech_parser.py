#!/usr/bin/env python
import pygst
import urllib2
import os
pygst.require('0.10')
import gst

class SpeechParser():

  def __init__(self, name, audiosrc, partial_cb, final_cb, lm_path=None, dict_path=None):
    """ Sets up the gstreamer pipeline and registers callbacks.
        Partial and full callbacks must take arguments (name, uttid, text)
    """
    self.name = name
    self.partial_cb = partial_cb
    self.final_cb = final_cb
    self.pipe = gst.Pipeline()
    
    conv = gst.element_factory_make("audioconvert", "audioconv")
    res = gst.element_factory_make("audioresample", "audioresamp")
    
    # Vader controls when sphinx listens for spoken text
    vader = gst.element_factory_make("vader", "vad")
    vader.set_property("auto-threshold", True)
    
    asr = gst.element_factory_make("pocketsphinx", "asr")
    asr.connect('partial_result', self.asr_partial_result)
    asr.connect('result', self.asr_result)
    if lm_path and dict_path:
      asr.set_property('lm', lm_path)
      asr.set_property('dict', dict_path)
    asr.set_property('configured', True)
    
    # we don't do anything with the actual audio data after transcription,
    # but you could e.g. write the audio to a file here instead.
    sink = gst.element_factory_make("fakesink", "fs")
    
    self.pipe.add(audiosrc, conv, res, vader, asr, sink)
    gst.element_link_many(audiosrc, conv, res, vader, asr, sink)
    self.pipe.set_state(gst.STATE_PLAYING)
   
  def pause(self):
    self.pipe.set_state(gst.STATE_PAUSED)

  def play(self):
    self.pipe.set_state(gst.STATE_PLAYING)

  def asr_partial_result(self, asr, text, uttid):
    """ This function is called when pocketsphinx gets a partial
        transcription of spoken audio. 
    """
    self.partial_cb(self.name, uttid, text)
    
  def asr_result(self, asr, text, uttid):
    """ This function is called when pocketsphinx gets a 
        full result (spoken command with a pause)
    """
    if text == "MOFRERE" :
    	os.system('aplay ~/Documents/voiceRecoTest/audio/moussa/yeahMan.wav')
    	print "\n\n\n\nMON FREEEEEEEEEEEEEEEEEEEEEEEEEEEEERE  !!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n\n"
    if text == "LIGHT ON":
    	urllib2.urlopen("http://192.168.200.102:8080/controller/light/17613/ON")
    	urllib2.urlopen("http://192.168.200.102:8080/controller/light/1/ON")
    	print "\n\n\n\nLIGHT ON IS DONE\n\n\n\n"
    	os.system('aplay ~/Documents/voiceRecoTest/audio/moussa/lightON.wav')
    
    if text == "LIGHT OFF":
    	urllib2.urlopen("http://192.168.200.102:8080/controller/light/17613/OFF")
    	urllib2.urlopen("http://192.168.200.102:8080/controller/light/1/OFF")
    	os.system('aplay ~/Documents/voiceRecoTest/audio/moussa/lightOFF.wav')
    	print "\n\n\n\nLIGHT OFF IS DONE\n\n\n\n"
    	
    self.final_cb(self.name, uttid, text)

if __name__ == "__main__":
  import threading
  import gobject 
  gobject.threads_init()

  def print_cb(name, uttid, text):
    print "(%s) %s: %s" % (uttid, name, text)

  src = gst.element_factory_make("autoaudiosrc") # Grab a random source
  parser = SpeechParser("parser", src, print_cb, print_cb)

  # This loops the program until Ctrl+C is pressed
  g_loop = threading.Thread(target=gobject.MainLoop().run)
  g_loop.daemon = False
  g_loop.start()
