znc-lastfm
==========

A ZNC python plugin that displays your currently playing music via last.fm

Usage
-----
Place `lastfm.py` in `<znc user>/.znc/modules/`

The `modpython` plugin must be loaded aswell. Requires the `lxml` package for python3.

Load the module with `/znc LoadMod lastfm <lastfm username>`

In any channel or PM, send `.np` as a message, and the channel will receive your currently playing song.
