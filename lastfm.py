import znc, lxml.etree, urllib.request

class lastfm(znc.Module):
    description = "Last.fm now playing command for ZNC"
    has_args = True
    args_help_text = "Last.fm username"
    module_types = [znc.CModInfo.UserModule]
    username = ""

    def OnLoad(self, args, message):
        self.username = args
        return True

    def OnUserMsg(self, channel, message):
        if message == '.np':
            try:
                nowplaying = now_playing(self.username, 'eba9632ddc908a8fd7ad1200d771beb7')
            except (Exception) as e:
                self.PutModNotice("Could not fetch now playing: {0}".format(str(e)))
                return znc.HALTCORE
            else:
                message.s = "Now Playing: {0}".format(nowplaying)
                self.PutModNotice(message.s)
        return znc.CONTINUE

def now_playing(username, api_key):
    try:
        feed_url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=' + username + '&api_key=' + api_key + '&limit=1'
        feed = lxml.etree.parse(urllib.request.urlopen(feed_url))
        track = feed.xpath('/lfm/recenttracks/track')[0]
        if track.attrib.get('nowplaying'):
            try:
                album = " [" + feed.xpath('/lfm/recenttracks/track/album')[0].text + "]"
            except (TypeError, IndexError):
                album = ""
            return feed.xpath('/lfm/recenttracks/track/artist')[0].text + ' - ' + feed.xpath('/lfm/recenttracks/track/name')[0].text + album
        else:
            raise Exception('Nothing is playing')
    except (TypeError, IndexError):
        raise Exception('No recent tracks found for %s' % username)
    except IOError:
        raise Exception('Couldn\'t reach last.fm')
