# Copyright 2007-2008 One Laptop Per Child
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gtk, gobject
import logging
import json
import math
from gettext import gettext as _
import csv
import time
from telepathy.interfaces import (
    CHANNEL_INTERFACE, CHANNEL_INTERFACE_GROUP, CHANNEL_TYPE_TEXT,
    CONN_INTERFACE_ALIASING)
from telepathy.constants import (
    CHANNEL_GROUP_FLAG_CHANNEL_SPECIFIC_HANDLES,
    CHANNEL_TEXT_MESSAGE_TYPE_NORMAL)
from telepathy.client import Connection, Channel

from sugar.graphics import style
from sugar.graphics.alert import NotifyAlert
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.palette import Palette
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity import activity
from sugar.presence import presenceservice
from sugar.activity.widgets import ActivityButton, TitleEntry
from sugar.activity.widgets import StopButton, ShareButton, RadioMenuButton
from random import randint
from chat import smilies

from chat.box import ChatBox


logger = logging.getLogger('ChatStudioSelf-activity')
steps=0
SMILIES_COLUMNS = 5
snum=0
c1=0
c2=0
score=0

class scoreWindow:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.window.set_size_request(795, 474)
	self.window.set_resizable(False)
	self.window.set_position(gtk.WIN_POS_CENTER)
	white = gtk.gdk.color_parse("white")
	self.window.modify_bg(gtk.STATE_NORMAL, white)
        self.table = gtk.Table(2, 4, True)

        self.table.attach(gtk.Label("1"), 0, 1, 0, 1)
        self.table.attach(gtk.Label("2"), 1, 2, 0, 1)
        self.table.attach(gtk.Label("3"), 2, 3, 0, 1)
        self.table.attach(gtk.Label("4"), 3, 4, 0, 1)
        self.table.attach(gtk.Label("5"), 0, 1, 1, 2)
        self.table.attach(gtk.Label("6"), 1, 2, 1, 2)
        self.table.attach(gtk.Label("7"), 2, 3, 1, 2)
        self.table.attach(gtk.Label("8"), 3, 4, 1, 2)
	self.window.add(self.table)
	self.window.show_all()

class ScoreButton(ToolButton):

    def __init__(self, activity, **kwargs):
        ToolButton.__init__(self, 'dialog-apply', **kwargs)
        self.props.tooltip = _('Score Card')
        self.props.accelerator = '<Ctrl>Q'
        self.connect('clicked', self.__show_score_win, activity)

    def __show_score_win(self, button, activity):
	scoreWindow()

class MathCompEntry1(gtk.ToolItem):
    def __init__(self,activity, **kwargs):
        gtk.ToolItem.__init__(self)
        self.entry1 = gtk.Entry(**kwargs)
	global c1
	c1=randint(2,9)
        self.entry1.set_size_request(int(gtk.gdk.screen_width() / 19),-1)
        self.entry1.set_text(str(c1))
	self.entry1.set_property("editable", False)
        self.entry1.unset_flags(gtk.CAN_FOCUS)
        self.entry1.show()
        self.add(self.entry1)
        
class MathCompEntry2(gtk.ToolItem):
    def __init__(self,activity, **kwargs):
        gtk.ToolItem.__init__(self)
        self.entry1 = gtk.Entry(**kwargs)
	global c2
	c2=randint(2,9)
        self.entry1.set_size_request(int(gtk.gdk.screen_width() / 19),-1)
        self.entry1.set_text(str(c2))
	self.entry1.set_property("editable", False)
        self.entry1.unset_flags(gtk.CAN_FOCUS)
        self.entry1.show()
        self.add(self.entry1)
# pylint: disable-msg=W0223
class ChatStudioSelf(activity.Activity):

    global score
    score = time.time()
    
    def __init__(self, handle):
        smilies.init()
	
        self.chatbox = ChatBox()

        super(ChatStudioSelf, self).__init__(handle)

        self.entry = None
	self.no_of_mistake=0
        root = self.make_root()
        self.set_canvas(root)

        root.show_all()
        self.entry.grab_focus()
	self.score1=0
	self.accuracy=0.0

        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.toolbar.insert(ActivityButton(self), -1)
        toolbar_box.toolbar.insert(TitleEntry(self), -1)
	try:
            from sugar.activity.widgets import DescriptionItem
        except ImportError:
            logger.debug('DescriptionItem button is not available, ' \
                   'toolkit version < 0.96')
        else:
            description_item = DescriptionItem(self)
            toolbar_box.toolbar.insert(description_item, -1)
            description_item.show()
	
	StartLabel = gtk.Label(_("START: "))
      	StartLabel.show()
       	tool_item_StartLabel = gtk.ToolItem()
       	tool_item_StartLabel.add(StartLabel)
        toolbar_box.toolbar.insert(tool_item_StartLabel, -1)
       	tool_item_StartLabel.show()
	mc1=MathCompEntry1(self)
	toolbar_box.toolbar.insert(mc1,-1)

	AddLabel = gtk.Label(_("  ADD: "))
      	AddLabel.show()
       	tool_item_AddLabel = gtk.ToolItem()
       	tool_item_AddLabel.add(AddLabel)
        toolbar_box.toolbar.insert(tool_item_AddLabel, -1)
       	tool_item_AddLabel.show()
	mc2=MathCompEntry2(self)
	toolbar_box.toolbar.insert(mc2,-1)
        separator = gtk.SeparatorToolItem()
        toolbar_box.toolbar.insert(separator, -1)
        separator = gtk.SeparatorToolItem()
        toolbar_box.toolbar.insert(separator, -1)
        self._smiley = RadioMenuButton(icon_name='smilies')
        self._smiley.palette = Palette(_('Insert smiley'))
        self._smiley.props.sensitive = True
        #toolbar_box.toolbar.insert(self._smiley, -1)


        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(False)
        toolbar_box.toolbar.insert(separator, -1)
	scoreButton=ScoreButton(self)
	toolbar_box.toolbar.insert(scoreButton,-1)
	stopButton=StopButton(self)
	toolbar_box.toolbar.insert(stopButton,-1)
        toolbar_box.show_all()
	self.a1=c1
	self.a2=c2
	self.sum1=self.a1+self.a2
        pservice = presenceservice.get_instance()
        self.owner = pservice.get_owner()
        # Chat is room or one to one:
        self._chat_is_room = False
        self.text_channel = None

        if self.shared_activity:
            # we are joining the activity
            self.connect('joined', self._joined_cb)
            if self.get_shared():
                # we have already joined
                self._joined_cb(self)
        elif handle.uri:
            # XMPP non-Sugar incoming chat, not sharable
            share_button.props.visible = False
            self._one_to_one_connection(handle.uri)
        else:
            # we are creating the activity
            #if not self.metadata or self.metadata.get('share-scope',activity.SCOPE_PRIVATE) == activity.SCOPE_PRIVATE:
                # if we are in private session
                #self._alert(_('Off-line'), _('Share, or invite someone.'))
            self.connect('shared', self._shared_cb)

    def _shared_cb(self, sender):
        logger.debug('Chat was shared')
        self._setup()

    def _one_to_one_connection(self, tp_channel):
        """Handle a private invite from a non-Sugar XMPP client."""
        if self.shared_activity or self.text_channel:
            return
        bus_name, connection, channel = json.loads(tp_channel)
        logger.debug('GOT XMPP: %s %s %s', bus_name, connection,
                     channel)
        Connection(
            bus_name, connection, ready_handler=lambda conn: \
            self._one_to_one_connection_ready_cb(bus_name, channel, conn))

    def _one_to_one_connection_ready_cb(self, bus_name, channel, conn):
        """Callback for Connection for one to one connection"""
        text_channel = Channel(bus_name, channel)
        self.text_channel = TextChannelWrapper(text_channel, conn)
        self.text_channel.set_received_callback(self._received_cb)
        self.text_channel.handle_pending_messages()
        self.text_channel.set_closed_callback(
            self._one_to_one_connection_closed_cb)
        self._chat_is_room = False
        self._alert(_('On-line'), _('Private Chat'))

        # XXX How do we detect the sender going offline?
        self.entry.set_sensitive(True)
        self.entry.grab_focus()

    def _one_to_one_connection_closed_cb(self):
        """Callback for when the text channel closes."""
        self._alert(_('Off-line'), _('left the chat'))

    def _setup(self):
        self.text_channel = TextChannelWrapper(self.shared_activity.telepathy_text_chan,self.shared_activity.telepathy_conn)
        self.text_channel.set_received_callback(self._received_cb)
        self._alert(_('On-line'), _('Connected'))
        self.shared_activity.connect('buddy-joined', self._buddy_joined_cb)
        self.shared_activity.connect('buddy-left', self._buddy_left_cb)
        self._chat_is_room = True
        self.entry.set_sensitive(True)
        self.entry.grab_focus()

    def _joined_cb(self, sender):
        """Joined a shared activity."""
        if not self.shared_activity:
            return
        logger.debug('Joined a shared chat')
        for buddy in self.shared_activity.get_joined_buddies():
            self._buddy_already_exists(buddy)
        self._setup()

    def _received_cb(self, buddy, text):
        """Show message that was received."""
        if buddy:
            if type(buddy) is dict:
                nick = buddy['nick']
            else:
                nick = buddy.props.nick
        else:
            nick = '???'
        logger.debug('Received message from %s: %s', nick, text)
        self.chatbox.add_text(buddy, text)

    def _alert(self, title, text=None):
        alert = NotifyAlert(timeout=5)
        alert.props.title = title
        alert.props.msg = text
        self.add_alert(alert)
        alert.connect('response', self._alert_cancel_cb)
        alert.show()

    def _alert_cancel_cb(self, alert, response_id):
        self.remove_alert(alert)

    def _buddy_joined_cb(self, sender, buddy):
        """Show a buddy who joined"""
        if buddy == self.owner:
            return
        self.chatbox.add_text(buddy,
                buddy.props.nick + ' ' + _('joined the chat'),
                status_message=True)

    def _buddy_left_cb(self, sender, buddy):
        """Show a buddy who joined"""
        if buddy == self.owner:
            return
        self.chatbox.add_text(buddy,
                buddy.props.nick + ' ' + _('left the chat'),
                status_message=True)

    def _buddy_already_exists(self, buddy):
        """Show a buddy already in the chat."""
        if buddy == self.owner:
            return
        self.chatbox.add_text(buddy, buddy.props.nick + ' ' + _('is here'),
                status_message=True)

    def can_close(self):
        """Perform cleanup before closing. Close text channel of a one to one XMPP chat."""
	""" Create or Open csv file score_log """

     	l= [[c1,c2,self.no_of_mistake,steps,self.accuracy]]

	with open('/home/labadmin/Activities/score_log.csv', 'a+') as f:
	 for row in l:
	    for column in row:
	        f.write('%d\t\t ' % column)
	    f.write('\n')
	 f.close()
	
        if self._chat_is_room is False:
            if self.text_channel is not None:
                self.text_channel.close()
        return True

    def make_root(self):
        entry = gtk.Entry()
        entry.modify_bg(gtk.STATE_INSENSITIVE,style.COLOR_WHITE.get_gdk_color())
        entry.modify_base(gtk.STATE_INSENSITIVE, style.COLOR_WHITE.get_gdk_color())
        entry.set_sensitive(True)
        entry.connect('activate', self.entry_activate_cb)
        entry.connect('key-press-event', self.entry_key_press_cb)
        self.entry = entry
        hbox = gtk.HBox()
        hbox.add(entry)
        box = gtk.VBox(homogeneous=False)
        box.pack_start(self.chatbox)
        box.pack_start(hbox, expand=False)
        return box

    def entry_key_press_cb(self, widget, event):
        """Check for scrolling keys.

        Check if the user pressed Page Up, Page Down, Home or End and
        scroll the window according the pressed key.
        """
        vadj = self.chatbox.get_vadjustment()
        if event.keyval == gtk.keysyms.Page_Down:
            value = vadj.get_value() + vadj.page_size
            if value > vadj.upper - vadj.page_size:
                value = vadj.upper - vadj.page_size
            vadj.set_value(value)
        elif event.keyval == gtk.keysyms.Page_Up:
            vadj.set_value(vadj.get_value() - vadj.page_size)
        elif event.keyval == gtk.keysyms.Home and \
             event.state & gtk.gdk.CONTROL_MASK:
            vadj.set_value(vadj.lower)
        elif event.keyval == gtk.keysyms.End and \
             event.state & gtk.gdk.CONTROL_MASK:
            vadj.set_value(vadj.upper - vadj.page_size)
	    


    def entry_activate_cb(self, entry):
	strr="Please enter a number."
	self.chatbox._scroll_auto = True
        text = entry.props.text
	logger.debug('Entry: %s' % text)
	while (self.sum1<50):
	 if text.isdigit():
	  self.chatbox.add_text(self.owner, "Your ans")	
   	  self.chatbox.add_text(self.owner, text)
       	  entry.props.text = ''
   	  self.connect(self.entry_ans_check_auto(text))
	 else:
	    self.chatbox.add_text(self.owner, strr)
	 entry.props.text = ''
	self.chatbox.add_text(self.owner,"Game Over")
	global score
	self.chatbox.add_text(self.owner, '%.2f' % (time.time()-score))
	entry.props.text = ''
	
	

    #to evaluate the entered answer
    def entry_ans_check_auto(self,ans):
	 global steps
	 steps+=1
	 self.chatbox.add_text(self.owner, "My ans")
	 self.chatbox.add_text(self.owner,str(self.sum1))
	 if (self.sum1==int(ans)):
	 	self.accuracy+=10
	 else:	 
	  self.no_of_mistake+=1
	  self.chatbox.add_text(self.owner,"No of steps"+ str(steps))
  	 self.sum1=self.sum1+self.a2
	 self.connect(self.entry_ans_check_auto(self.connect(self.entry_activate_cb())))    

	
	
	

    

    def write_file(self, file_path):
        """Store chat log in Journal.

        Handling the Journal is provided by Activity - we only need
        to define this method.
        """
        logger.debug('write_file: writing %s' % file_path)
        self.chatbox.add_log_timestamp()
        f = open(file_path, 'w')
        try:
            f.write(self.chatbox.get_log())
        finally:
            f.close()
        self.metadata['mime_type'] = 'text/plain'

    def read_file(self, file_path):
        """Load a chat log from the Journal.

        Handling the Journal is provided by Activity - we only need
        to define this method.
        """
        logger.debug('read_file: reading %s' % file_path)
        log = open(file_path).readlines()
        last_line_was_timestamp = False
        for line in log:
            if line.endswith('\t\t\n'):
                if last_line_was_timestamp is False:
                    timestamp = line.strip().split('\t')[0]
                    self.chatbox.add_separator(timestamp)
                    last_line_was_timestamp = True
            else:
                timestamp, nick, color, status, text = line.strip().split('\t')
                status_message = bool(int(status))
                self.chatbox.add_text({'nick': nick, 'color': color},
                              text, status_message)
                last_line_was_timestamp = False


class TextChannelWrapper(object):
    """Wrap a telepathy Text Channel to make usage simpler."""

    def __init__(self, text_chan, conn):
        """Connect to the text channel"""
        self._activity_cb = None
        self._activity_close_cb = None
        self._text_chan = text_chan
        self._conn = conn
        self._logger = logging.getLogger(
            'chat-activity.TextChannelWrapper')
        self._signal_matches = []
        m = self._text_chan[CHANNEL_INTERFACE].connect_to_signal(
            'Closed', self._closed_cb)
        self._signal_matches.append(m)

    def send(self, text):
        """Send text over the Telepathy text channel."""
        # XXX Implement CHANNEL_TEXT_MESSAGE_TYPE_ACTION
        if self._text_chan is not None:
            self._text_chan[CHANNEL_TYPE_TEXT].Send(
                CHANNEL_TEXT_MESSAGE_TYPE_NORMAL, text)

    def close(self):
        """Close the text channel."""
        self._logger.debug('Closing text channel')
        try:
            self._text_chan[CHANNEL_INTERFACE].Close()
        except Exception:
            self._logger.debug('Channel disappeared!')
            self._closed_cb()

    def _closed_cb(self):
        """Clean up text channel."""
        self._logger.debug('Text channel closed.')
        for match in self._signal_matches:
            match.remove()
        self._signal_matches = []
        self._text_chan = None
        if self._activity_close_cb is not None:
            self._activity_close_cb()

    def set_received_callback(self, callback):
        """Connect the function callback to the signal.

        callback -- callback function taking buddy and text args
        """
        if self._text_chan is None:
            return
        self._activity_cb = callback
        m = self._text_chan[CHANNEL_TYPE_TEXT].connect_to_signal('Received',
            self._received_cb)
        self._signal_matches.append(m)

    def handle_pending_messages(self):
        """Get pending messages and show them as received."""
        for identity, timestamp, sender, type_, flags, text in \
            self._text_chan[
                CHANNEL_TYPE_TEXT].ListPendingMessages(False):
            self._received_cb(identity, timestamp, sender, type_, flags, text)

    def _received_cb(self, identity, timestamp, sender, type_, flags, text):
        """Handle received text from the text channel.

        Converts sender to a Buddy.
        Calls self._activity_cb which is a callback to the activity.
        """
        if type_ != 0:
            # Exclude any auxiliary messages
            return

        if self._activity_cb:
            try:
                self._text_chan[CHANNEL_INTERFACE_GROUP]
            except Exception:
                # One to one XMPP chat
                nick = self._conn[
                    CONN_INTERFACE_ALIASING].RequestAliases([sender])[0]
                buddy = {'nick': nick, 'color': '#000000,#808080'}
            else:
                # Normal sugar MUC chat
                # XXX: cache these
                buddy = self._get_buddy(sender)
            self._activity_cb(buddy, text)
            self._text_chan[
                CHANNEL_TYPE_TEXT].AcknowledgePendingMessages([identity])
        else:
            self._logger.debug('Throwing received message on the floor'
                ' since there is no callback connected. See '
                'set_received_callback')

    def set_closed_callback(self, callback):
        """Connect a callback for when the text channel is closed.

        callback -- callback function taking no args

        """
        self._activity_close_cb = callback

    def _get_buddy(self, cs_handle):
        """Get a Buddy from a (possibly channel-specific) handle."""
        # XXX This will be made redundant once Presence Service
        # provides buddy resolution
        # Get the Presence Service
        pservice = presenceservice.get_instance()
        # Get the Telepathy Connection
        tp_name, tp_path = pservice.get_preferred_connection()
        conn = Connection(tp_name, tp_path)
        group = self._text_chan[CHANNEL_INTERFACE_GROUP]
        my_csh = group.GetSelfHandle()
        if my_csh == cs_handle:
            handle = conn.GetSelfHandle()
        elif group.GetGroupFlags() & \
            CHANNEL_GROUP_FLAG_CHANNEL_SPECIFIC_HANDLES:
            handle = group.GetHandleOwners([cs_handle])[0]
        else:
            handle = cs_handle

            # XXX: deal with failure to get the handle owner
            assert handle != 0

        return pservice.get_buddy_by_telepathy_handle(tp_name, tp_path, handle)
