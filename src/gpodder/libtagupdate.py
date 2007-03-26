

#
# gPodder (a media aggregator / podcast client)
# Copyright (C) 2005-2007 Thomas Perl <thp at perli.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
# MA  02110-1301, USA.
#


#
#  libtagupdate.py -- tag updating/writing library
#  thomas perl <thp@perli.net>   20070315
#
#


# for ogg/vorbis (vorbiscomment utility)
import popen2

# for logging
from liblogger import log

# for mp3 files
has_eyed3 = True
try:
    import eyeD3
except:
    log('(tagupdate) eyed3 not found -- tag update disabled')
    has_eyed3 = False

# do we provide tagging functions to the user?
def tagging_supported():
    global has_eyed3
    return has_eyed3


tag_update_methods = {}

def update_metadata_on_file( filename, **metadata):
    global tag_update_methods

    ext = filename[-3:]
    if ext in tag_update_methods:
        log('Updating tag for %s', filename)
        return tag_update_methods[ext]( filename, **metadata)

    log('Do not know how to update file extension %s :/', ext)


def update_tag_ogg( filename, **metadata):
    data = '\n'.join( [ '%s=%s' % ( i.upper(), metadata[i] ) for i in metadata ] + [''])

    p = popen2.Popen3('vorbiscomment -w "%s"' % filename)

    writer = p.tochild
    writer.write(data)
    writer.close()

    result = p.wait() == 0

    if not result:
        log('Error while running vorbiscomment. Is it installed?! (vorbis-tools)')

    return result

tag_update_methods['ogg'] = update_tag_ogg


def update_tag_mp3( filename, **metadata):
    if not has_eyed3:
        log('eyeD3 not found -> please install. no tags have been updated.')
        return False

    tag = eyeD3.tag.Tag( fileName = filename)
    tag.remove( eyeD3.tag.ID3_ANY_VERSION)
    tag.setVersion( eyeD3.tag.ID3_ANY_VERSION)

    for key in metadata:
        if key.lower() == 'artist':
            tag.setArtist( metadata[key])
        elif key.lower() == 'title':
            tag.setTitle( metadata[key])
        elif key.lower() == 'album':
            tag.setAlbum( metadata[key])

    return tag.update( eyeD3.tag.ID3_V2) == 1 and tag.update( eyeD3.tag.ID3_V1) == 1

tag_update_methods['mp3'] = update_tag_mp3

