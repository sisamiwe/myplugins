#!/usr/bin/env python
#########################################################################
# Copyright 2020 Michael Wenzel
#########################################################################
#  Viessmann-Plugin for SmartHomeNG.  https://github.com/smarthomeNG//
#
#  This plugin is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This plugin is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this plugin. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import logging
import socket
import time
import serial
import re
import threading
from datetime import datetime
import cherrypy
from jinja2 import Environment, FileSystemLoader

from . import commands

from lib.item import Items
from lib.model.smartplugin import *
from bin.smarthome import VERSION
if '.'.join(VERSION.split('.', 2)[:2]) <= '1.5':
    self.logger = logging.getLogger(__name__)


class Viessmann(SmartPlugin):

    ALLOW_MULTIINSTANCE = False
    PLUGIN_VERSION = '1.7.0'

    def __init__(self, sh, *args, **kwargs):
        # Get plugin parameter
        self._serialport = self.get_parameter_value('serialport')         # /dev/optolink
        self.heating_type = self.get_parameter_value('heating_type')      # V200KO1B
        self.protocol = self.get_parameter_value('protocol')              # P300
        # Set variables
        self._params = {}
        self._init_cmds = []
        self._cyclic_cmds = {}
        self._lock = threading.Lock()
        self._initread = False
        self._connected = False
        self._initialized = False
        self._lastbyte = b''
        self._lastbytetime = 0

        # Load protocol relevant sets
        if self.protocol in commands.controlset and self.protocol in commands.errorset and self.protocol in commands.unitset and self.protocol in commands.returnstatus and self.protocol in commands.setreturnstatus:
            self._controlset = commands.controlset[self.protocol]
            self._errorset = commands.errorset[self.protocol]
            self._unitset = commands.unitset[self.protocol]
            self._devicetypes = commands.devicetypes
            self._returnstatus = commands.returnstatus[self.protocol]
            self._setreturnstatus = commands.setreturnstatus[self.protocol]
            self.log_info('Loaded controlset for Protocol \'{}\''.format(self._controlset))
            self.log_info('Loaded errors for Protocol \'{}\''.format(self._errorset))
            self.log_info('Loaded units for Protocol \'{}\''.format(self._unitset))
            self.log_info('Loaded device types for Protocol \'{}\''.format(self._devicetypes))
            self.log_info('Loaded Return Status for Protocol \'{}\''.format(self._returnstatus))
            self.log_info('Loaded Set Return Status for Protocol \'{}\''.format(self._setreturnstatus))
        else:
            self.log_err('Sets for Protocol {} could not be found!'.format(self.protocol))
            return None

        # Load heating type relevant sets
        if self.heating_type in commands.commandset and self.heating_type in commands.operatingmodes and self.heating_type in commands.systemschemes:
            self._commandset = commands.commandset[self.heating_type]
            self._operatingmodes = commands.operatingmodes[self.heating_type]
            self._systemschemes = commands.systemschemes[self.heating_type]
            self.log_info('Loaded commands for Heating type \'{}\''.format(self._commandset))
            self.log_info('Loaded operating modes for Heating type \'{}\''.format(self._operatingmodes))
            self.log_info('Loaded system schemes for Heating type \'{}\''.format(self._systemschemes))
        else:
            sets = []
            if self.heating_type not in commands.commandset:
                sets += 'command'
            if self.heating_type not in commands.operatingmodes:
                sets += 'operating modes'
            if self.heating_type not in commands.systemschemes:
                sets += 'system schemes'

            self.log_err('Sets {} for Heating type {} could not be found!'.format(", ".join(sets), self.heating_type))
            return None

        # Remember protocol config
        self._bautrate = self._controlset['Baudrate']
        self._bytesize = self._controlset['Bytesize']
        self._parity = self._controlset['Parity']
        self._stopbits = self._controlset['Stopbits']
        self._startbyte = self.int2bytes(self._controlset['StartByte'], 1)
        self._request = self.int2bytes(self._controlset['Request'], 1)
        self._response = self.int2bytes(self._controlset['Response'], 1)
        self._error = self.int2bytes(self._controlset['Error'], 1)
        self._read = self.int2bytes(self._controlset['Read'], 1)
        self._write = self.int2bytes(self._controlset['Write'], 1)
        self._functioncall = self.int2bytes(self._controlset['Function_Call'], 1)
        self._acknowledge = self.int2bytes(self._controlset['Acknowledge'], 1)
        self._notinitiated = self.int2bytes(self._controlset['Not_initiated'], 1)
        self._initerror = self.int2bytes(self._controlset['Init_Error'], 1)
        self._resetcommand = self.int2bytes(self._controlset['Reset_Command'], 1)
        self._resetcommandresponse = self.int2bytes(self._controlset['Reset_Command_Response'], 1)
        self._synccommand = self.int2bytes(self._controlset['Sync_Command'], 3)
        self._synccommandresponse = self.int2bytes((self._controlset['Sync_Command_Response']), 1)
        self._commandbytesread = self._controlset['Command_bytes_read']
        self._commandbyteswrite = self._controlset['Command_bytes_write']

        # Init web interface
        self.init_webinterface()

    def connect(self):
        self._lock.acquire()
        if self._connected and self._serial:
            return True
        try:
            self.log_info('Connecting ...')
            self._serial = serial.Serial()
            self._serial.baudrate = self._bautrate
            self._serial.parity = self._parity
            self._serial.bytesize = self._bytesize
            self._serial.stopbits = self._stopbits
            self._serial.port = self._serialport
            self._serial.timeout = 1
            self._serial.open()
            self._connected = True
            self.log_info('Connected to {}'.format(self._serialport))
            self._connection_attempts = 0
            return True
        except Exception as e:
            self.log_err('Could not connect to {}; Error: {}'.format(self._serialport, e))
            return False
        finally:
            self._lock.release()

    def disconnect(self):
        self._connected = False
        try:
            self._serial.close()
            self._serial = None
            self.log_warn('disconnected')
        except:
            pass

    def initCommunication(self):
        # Merker: Wurde der Initialisierungsstring b'\x16\x00\x00' gesendet. Wird hierauf dann mit b'\x06' geantwortet ist die Komunikation aufgebaut.
        self.log_info('Init Communication....')
        returnvalue = False
        initstringsent = False
        self.send_bytes(self._resetcommand)
        readbyte = self.read_bytes(1)

        for i in range(0, 10):
            if ((initstringsent is True) and (self._lastbyte == self._acknowledge)):
                # Schnittstelle hat auf den Initialisierungsstring mit OK geantwortet. Die Abfrage von Werten kann beginnen. Diese Funktion meldet hierzu True zurück.
                returnvalue = True
                break
            if ((self._lastbyte == self._acknowledge) or (self._lastbyte == self._notinitiated)):
                # Schnittstelle ist zurückgesetzt und wartet auf Daten; Antwort b'\x05' = Warten auf Initialisierungsstring oder Antwort b'\x06' = Schnittstelle initialisiert
                self.send_bytes(self._synccommand)
                self.log_debug('send_bytes: Send sync command {}'.format(self._synccommand))
                initstringsent = True
            elif (self._lastbyte == self._initerror):
                self.log_err('The interface has reported an error (\x15), loop increment {}'.format(i))
                self.send_bytes(self._resetcommand)
                self.log_debug('send_bytes: Send reset command {}'.format(self._resetcommand))
                initstringsent = False
            else:
                self.send_bytes(self._resetcommand)
                self.log_debug('send_bytes: Send reset command {}'.format(self._resetcommand))
                initstringsent = False
            readbyte = self.read_bytes(1)
            self.log_debug('read_bytes: Read {}'.format(readbyte))

        self.log_info('Communication initialized: {}'.format(returnvalue))
        self._initialized = returnvalue
        return returnvalue

    def send_bytes(self, packet):
        if not self._connected:
            return False
        self._serial.write(packet)
        # self.log_debug('send_bytes: Send {}'.format(packet))
        return True

    def read_bytes(self, length):
        totalreadbytes = bytes()
        # self.log_debug('read_bytes: Start read')
        while True:
            readbyte = self._serial.read()
            self._lastbyte = readbyte
            # self.log_debug('read_bytes: Read {}'.format(readbyte))
            if (readbyte != b''):
                self._lastbytetime = time.time()
            else:
                return totalreadbytes
            totalreadbytes += readbyte
            if len(totalreadbytes) >= length:
                return totalreadbytes

    def parse_item(self, item):
        # Process the update config
        if self.has_iattr(item.conf, 'viess_update'):
            self.log_debug("Item for requesting update found: {}".format(item))
            ad = self.get_iattr_value(item.conf, 'viess_update')
            return self.update_item

        # Process the read config
        if self.has_iattr(item.conf, 'viess_read'):
            commandname = self.get_iattr_value(item.conf, 'viess_read')
            if commandname is None or commandname not in self._commandset:
                self.log_err('Item {} contains invalid read command \'{}\'!'.format(item, commandname))
                return None

            # Remember the read config to later update this item if the configured response comes in
            self.log_info('Item {} reads by using command \'{}\'.'.format(item, commandname))
            commandconf = self._commandset[commandname]
            commandcode = (commandconf['addr']).lower()

            # Fill item dict
            self._params[commandcode] = {'item': item, 'commandname': commandname}
            # self.log_debug('Loaded params \'{}\''.format(self._params))  # Loaded params '# Loaded params '{'27A3': {'item': 'viessmann.heizkreis_a1m1.betriebsart.betriebsart', 'commandname': 'Betrierbsart_A1M1'}}'

            # Allow items to be automatically initiated on startup
            if (self.has_iattr(item.conf, 'viess_init') and bool(self.get_iattr_value(item.conf, 'viess_init')) is True):
                self.log_info('Item {} is initialized on startup.'.format(item))
                if commandcode not in self._init_cmds:
                    self._init_cmds.append(commandcode)
                self.log_debug('CommandCodes should be read at init: {}'.format(self._init_cmds))

            # Allow items to be cyclically updated
            if (self.has_iattr(item.conf, 'viess_read_cycle')):
                cycle = int(self.get_iattr_value(item.conf, 'viess_read_cycle'))
                self.log_info('Item {} should read cyclic every {} seconds.'.format(item, cycle))
                nexttime = time.time() + cycle
                if commandcode not in self._cyclic_cmds:
                    self._cyclic_cmds[commandcode] = {'cycle': cycle, 'nexttime': nexttime}
                else:
                    # If another item requested this command already with a longer cycle, use the shorter cycle now
                    if self._cyclic_cmds[commandcode]['cycle'] > cycle:
                        self._cyclic_cmds[commandcode]['cycle'] = cycle
                self.log_debug('CommandCodes should be read cyclic: {}'.format(self._cyclic_cmds))

        # Process the write config
        if self.has_iattr(item.conf, 'viess_send'):
            if bool(self.get_iattr_value(item.conf, 'viess_send')) is True:
                commandname = self.get_iattr_value(item.conf, 'viess_read')
            else:
                commandname = self.get_iattr_value(item.conf, 'viess_send')

            if commandname is None or commandname not in self._commandset:
                self.log_err('Item {} contains invalid write command \'{}\'!'.format(item, commandname))
                return None
            else:
                self.log_info('Item {} to be written by using command \'{}\''.format(item, commandname))
                return self.update_item

    def parse_logic(self, logic):
        pass

    def update_item(self, item, caller=None, source=None, dest=None):
        if self.alive and caller != self.get_shortname():
            self.log_info("Update item: {}, item has been changed outside this plugin".format(item.id()))
            self.log_debug("update_item was called with item '{}' from caller '{}', source '{}' and dest '{}'".format(item, caller, source, dest))

            if self.has_iattr(item.conf, 'viess_send'):
                # Send write command
                if bool(self.get_iattr_value(item.conf, 'viess_send')) is True:
                    commandname = self.get_iattr_value(item.conf, 'viess_read')
                else:
                    commandname = self.get_iattr_value(item.conf, 'viess_send')
                value = item()
                self.log_debug('Got item value to be written: {} on command name {}.'.format(value, commandname))
                self.create_write_command(commandname, value)

                # If a read command should be sent after write
                if self.has_iattr(item.conf, 'viess_read') and self.has_iattr(item.conf, 'viess_read_afterwrite'):
                    readcommandname = self.get_iattr_value(item.conf, 'viess_read')
                    readafterwrite = self.get_iattr_value(item.conf, 'viess_read_afterwrite')
                    self.log_debug('Attempting read after write for item {}, command {}, delay {}'.format(item, readcommandname, readafterwrite))
                    if readcommandname is not None and readafterwrite is not None:
                        aw = float(readafterwrite)
                        time.sleep(aw)
                        self.create_read_command(readcommandname)

                # If commands should be triggered after this write
                if self.has_iattr(item.conf, 'viess_trigger'):
                    trigger = self.get_iattr_value(item.conf, 'viess_trigger')
                    if trigger is None:
                        self.log_err('Item {} contains invalid trigger command list \'{}\'!'.format(item, trigger))
                    else:
                        tdelay = 5  # default delay
                        if self.has_iattr(item.conf, 'viess_trigger_afterwrite'):
                            tdelay = float(self.get_iattr_value(item.conf, 'viess_trigger_afterwrite'))
                        if type(trigger) != list:
                            trigger = [trigger]
                        for triggername in trigger:
                            triggername = triggername.strip()
                            if triggername is not None and readafterwrite is not None:
                                self.log_debug('Triggering command {} after write for item {}'.format(triggername, item))
                                time.sleep(tdelay)
                                self.create_read_command(triggername)

            elif self.has_iattr(item.conf, 'viess_update'):
                value = item()
                if value is True:
                    self.log_debug('Reading of all values/items has been requested')
                    self.update_all_read_items()

    def send_cyclic_cmds(self):
        # Read all cyclic commands
        currenttime = time.time()
        for commandcode in list(self._cyclic_cmds.keys()):
            entry = self._cyclic_cmds[commandcode]
            # Is the command already due?
            if entry['nexttime'] <= currenttime:
                commandname = self.commandname_by_commandcode(commandcode)
                self.log_info('Triggering cyclic read command: {}'.format(commandname))
                self.create_read_command(commandname)
                entry['nexttime'] = currenttime + entry['cycle']

    def create_cyclic_scheduler(self):
        # Find the shortest cycle
        shortestcycle = -1
        for commandname in list(self._cyclic_cmds.keys()):
            entry = self._cyclic_cmds[commandname]
            if shortestcycle == -1 or entry['cycle'] < shortestcycle:
                shortestcycle = entry['cycle']
        # Start the worker thread
        if shortestcycle != -1:
            # Balance unnecessary calls and precision
            workercycle = int(shortestcycle / 2)
            self.scheduler_add('cyclic', self.send_cyclic_cmds, cycle=workercycle, prio=5, offset=0)
            self.log_info('Added cyclic worker thread ({} sec cycle). Shortest item update cycle found: {} sec.'.format(workercycle, shortestcycle))
        return True

    def send_init_commands(self):
        # Do the init read commands
        if self._init_cmds != []:
            self.log_info('Starting initial read commands.')
            for commandcode in self._init_cmds:
                commandname = self.commandname_by_commandcode(commandcode)
                self.log_debug('send_init_commands {}.'.format(commandname))
                self.create_read_command(commandname)
            self._initread = True
            self.log_debug('self._initread = {}.'.format(self._initread))
        return True

    def update_all_read_items(self):
        for commandcode in list(self._params.keys()):
            commandname = self.commandname_by_commandcode(commandcode)
            self.log_debug('Triggering read command: {} for requested value update'.format(commandname))
            self.create_read_command(commandname)

    def create_read_command(self, commandname):
        # A read_request telegram looks like this: ACK (1 byte), startbyte (1 byte), data length in bytes (1 byte), request/response (1 byte), read/write (1 byte), addr (2 byte), amount of value bytes expected in answer (1 byte), checksum (1 byte)
        self.log_info('____________________________________________________________________________________________________________________________________________________________')
        self.log_info('Got a new read job: Command {}'.format(commandname))

        # Get command config
        commandconf = self._commandset[commandname]
        self.log_debug('Command config: {}'.format(commandconf))
        commandcode = (commandconf['addr']).lower()
        commandvaluebytes = commandconf['len']

        # Build packet for read commands
        packet = bytearray()
        packet.extend(self._startbyte)
        packet.extend(self.int2bytes(self._commandbytesread, 1))
        packet.extend(self._request)
        packet.extend(self._read)
        packet.extend(bytes.fromhex(commandcode))
        packet.extend(self.int2bytes(commandvaluebytes, 1))
        packet.extend(self.int2bytes(self.calc_checksum(packet), 1))
        self.log_debug('Preparing command {} with packet to be sent as hexstring: {} and as bytes: {}'.format(commandname, self.bytes2hexstring(packet), packet))
        packetlen_response = int(self._commandbytesread) + 4 + int(commandvaluebytes)

        # hand over built packet to send_command
        self.send_command(packet, packetlen_response)

    def create_write_command(self, commandname, value=None):
        # A write_request telegram looks like this: ACK (1 byte), startbyte (1 byte), data length in bytes (1 byte), request/response (1 byte), read/write (1 byte), addr (2 byte), amount of bytes to be written (1 byte), value (bytes as per last byte), checksum (1 byte)
        self.log_info('____________________________________________________________________________________________________________________________________________________________')
        self.log_info('Got a new write job: Command {} with value {}'.format(commandname, value))

        # Get command config
        commandconf = self._commandset[commandname]
        self.log_debug('Command config: {}'.format(commandconf))
        commandcode = (commandconf['addr']).lower()
        commandvaluebytes = commandconf['len']
        commandunit = commandconf['unit']

        if commandunit == 'BA':

            # try to convert BA string to byte value, setting str values will fail
            # this will not work properly if multiple entries have the same value!
            try:
                value = int(dict(map(reversed, self._operatingmodes.items()))[value])
                commandunit = 'IFNON'
                commandsignage = False
            except KeyError:
                # value doesn't exist in operatingmodes. don't know what to do
                raise Exception('Value {} not defined in operating modes for device {}'.format(value, self.heating_type))

        set_allowed = bool(commandconf['set'])
        unitconf = self._unitset[commandunit]
        self.log_debug('Unit defined to {} with config{}.'.format(commandunit, unitconf))
        commandvalueresult = unitconf['type']
        commandsignage = unitconf['signed']
        commandtransform = unitconf['read_value_transform']
        if 'min_value' in commandconf:
            min_allowed_value = commandconf['min_value']
        else:
            min_allowed_value = None
        if 'max_value' in commandconf:
            max_allowed_value = commandconf['max_value']
        else:
            max_allowed_value = None

        try:
            # check if command is allowed to write
            if set_allowed is True:
                # check, if value has content
                if value is not None and value != '':
                    # check, if values to be written are in allowed range or None
                    if (min_allowed_value is None or min_allowed_value <= value) and (max_allowed_value is None or max_allowed_value >= value):
                        # Create valuebytes
                        if commandvalueresult == 'datetime' or commandvalueresult == 'date':
                            try:
                                datestring = datetime.fromisoformat(value).strftime("%Y%m%d%w%H%M%S")
                                # Viessmann erwartet 2 digits für Wochentag, daher wird hier noch eine 0 eingefügt
                                datestring = datestring[:8] + '0' + datestring[8:]
                                valuebytes = bytes.fromhex(datestring)
                                self.log_debug('Created value bytes for type {} as bytes: {}'.format(commandvalueresult, valuebytes))
                            except Exception as e:
                                raise Exception('Incorrect data format, YYYY-MM-DD expected; Error: {}'.format(e))
                        elif commandvalueresult == 'timer':
                            try:
                                times = ""
                                for switching_time in value:
                                    an = self.encode_timer(switching_time["An"])
                                    aus = self.encode_timer(switching_time["Aus"])
                                    # times += f"{an:02x}{aus:02x}"
                                    times += "{:02x}".format(an) + "{:02x}".format(aus)
                                valuebytes = bytes.fromhex(times)
                                self.log_debug('Created value bytes for type {} as hexstring: {} and as bytes: {}'.format(commandvalueresult, self.bytes2hexstring(valuebytes), valuebytes))
                            except Exception as e:
                                raise Exception('Incorrect data format, (An: hh:mm Aus: hh:mm) expected; Error: {}'.format(e))
                        elif commandvalueresult == 'integer' or commandvalueresult == 'list':
                            if commandtransform == 'int':
                                value = self.value_transform_write(value, commandtransform)
                                self.log_debug('Transformed value using method {} to {}'.format(commandtransform, value))
                            elif commandtransform == 'bool':
                                value = bool(value)
                            else:
                                value = int(value)
                            valuebytes = self.int2bytes(value, commandvaluebytes)
                            self.log_debug('Created value bytes for type {} as hexstring: {} and as bytes: {}'.format(commandvalueresult, self.bytes2hexstring(valuebytes), valuebytes))
                        else:
                            raise Exception('Type not definied for creating write command bytes')

                        # Calculate length of payload (telegram header for write with 5 byte + amount of valuebytes)
                        payloadlength = int(self._commandbyteswrite) + int(commandvaluebytes)
                        self.log_debug('Payload length is: {} bytes.'.format(payloadlength))

                        # Build packet with value bytes for write commands
                        packet = bytearray()
                        packet.extend(self._startbyte)
                        packet.extend(self.int2bytes(payloadlength, 1))
                        packet.extend(self._request)
                        packet.extend(self._write)
                        packet.extend(bytes.fromhex(commandcode))
                        packet.extend(self.int2bytes(commandvaluebytes, 1, commandsignage))
                        packet.extend(valuebytes)
                        packet.extend(self.int2bytes(self.calc_checksum(packet), 1))
                        self.log_debug('Preparing command {} with value {} (transformed to value byte \'{}\') to be sent as packet {}.'.format(commandname, value, self.bytes2hexstring(valuebytes), self.bytes2hexstring(packet)))
                        packetlen_response = int(self._commandbytesread) + 4

                        # hand over built packet to send_command
                        self.send_command(packet, packetlen_response)
                    else:
                        raise Exception('No valid value to be sent')
                else:
                    raise Exception('No value handed over')
            else:
                raise Exception('Command at Heating is not allowed to be sent')

        except Exception as e:
            self.log_debug('create_write_command failed with error: {}.'.format(e))

    def send_command(self, packet, packetlen_response):
        if not self._connected:
            self.log_err('Not connected, trying to reconnect.')
            self.connect()
            # return

        try:
            self._lock.acquire()
            if self._initialized is False or (time.time() - 500) > self._lastbytetime:
                self.initCommunication()

            if self._initialized is True:
                # send query
                try:
                    self.send_bytes(packet)
                    self.log_debug('Successfully sent packet: {}'.format(self.bytes2hexstring(packet)))
                    time.sleep(0.1)
                except IOError as io:
                    raise IOError('IO Error: {}'.format(io))
                except Exception as e:
                    raise Exception('Exception while sending: {}'.format(e))
                # receive response
                response_packet = bytearray()
                try:
                    self.log_debug('Trying to receive {} bytes of the response.'.format(packetlen_response))
                    chunk = self.read_bytes(packetlen_response)
                    time.sleep(0.1)
                    self.log_debug('Received {} bytes chunk of response as hexstring {} and as bytes {}'.format(len(chunk), self.bytes2hexstring(chunk), chunk))
                    if len(chunk) != 0:
                        if chunk[:1] == self._error:
                            self.log_err('Interface returned error! response was: {}'.format(chunk))
                        elif chunk[:1] != self._acknowledge:
                            self.log_err('Received invalid chunk, not starting with ACK! response was: {}'.format(chunk))
                        else:
                            # self.log_info('Received chunk! response was: {}, Hand over to parse_response now.format(chunk))
                            response_packet.extend(chunk)
                            self.parse_response(response_packet)
                    else:
                        self.log_err('Received 0 bytes chunk - ignoring response_packet! chunck was: {}'.format(chunk))
                except socket.timeout:
                    raise Exception('error receiving response: time-out')
                except IOError as io:
                    raise IOError('IO Error: {}'.format(io))
                except Exception as e:
                    raise Exception('error receiving response: {}'.format(e))
            else:
                raise Exception('Interface not initialized!')
        except IOError as io:
            self.log_err('send_command failed with IO error: {}.'.format(io))
            self.log_err('Trying to reconnect (disconnecting, connecting')
            self.disconnect()
        except Exception as e:
            self.log_err('send_command failed with error: {}.'.format(e))
        finally:
            self._lock.release()

    def parse_response(self, response):
        # A read_response telegram looks like this: ACK (1 byte), startbyte (1 byte), data length in bytes (1 byte), request/response (1 byte), read/write (1 byte), addr (2 byte), amount of valuebytes (1 byte), value (bytes as per last byte), checksum (1 byte)
        # A write_response telegram looks like this: ACK (1 byte), startbyte (1 byte), data length in bytes (1 byte), request/response (1 byte), read/write (1 byte), addr (2 byte), amount of bytes written (1 byte), checksum (1 byte)

        # Validate checksum
        checksum = self.calc_checksum(response[1:len(response) - 1])  # first, cut first byte (ACK) and last byte (checksum) and then calculate checksum
        received_checksum = response[len(response) - 1]
        if (received_checksum != checksum):
            self.log_err('Calculated checksum {} does not match received checksum of {}! Ignoring reponse.'.format(checksum, received_checksum))
            return

        # Extract command/address, valuebytes and valuebytecount out of response
        commandcode = response[5:7].hex()
        responsetypecode = response[3]  # 0x00 = Anfrage, 0x01 = Antwort, 0x03 = Fehler
        responsedatacode = response[4]  # 0x01 = ReadData, 0x02 = WriteData, 0x07 = Function Call
        valuebytecount = response[7]
        self.log_debug('Response decoded to: commandcode: {}, responsedatacode: {}, valuebytecount: {}'.format(commandcode, responsedatacode, valuebytecount))

        # Find items using the commandcode if read response and not error
        if commandcode in self._params.keys() and responsedatacode == 1 and responsetypecode != 3:
            # Extract databytes out of response
            rawdatabytes = bytearray()
            rawdatabytes.extend(response[8:8 + (valuebytecount)])
            self.log_debug('Rawdatabytes formated: {} and unformated: {}'.format(self.bytes2hexstring(rawdatabytes), rawdatabytes))

            # Find corresponding item and commandname
            item = self._params[commandcode]['item']
            commandname = self._params[commandcode]['commandname']
            self.log_debug('Corresponding Item: {}; Corresponding commandname: {}'.format(item.id(), commandname))

            # Get command and respective unit config
            commandconf = self._commandset[commandname]
            commandvaluebytes = commandconf['len']
            commandunit = commandconf['unit']
            unitconf = self._unitset[commandunit]
            commandunit_description = unitconf['unit_de']
            commandvalueresult = unitconf['type']
            commandsignage = unitconf['signed']
            valuetransform = unitconf['read_value_transform']
            self.log_debug('Unit defined to {} with config {}.'.format(commandunit, unitconf))

            # start value decode
            if commandunit == 'CT':
                rawdatastring = rawdatabytes.hex()
                timer = self.decode_timer(rawdatastring)
                # fill list
                timer = [{'An': on_time, 'Aus': off_time}
                         for on_time, off_time in zip(timer, timer)]
                value = timer
                self.log_debug('Matched command {} and read transformed timer {} and byte length {}.'.format(commandname, value, commandvaluebytes))
                # Split timer list and put it the child items, which were created by struct.timer in iso time format
                try:
                    for child in item.return_children():
                        child_item = str(child.id())
                        if child_item.endswith('an1'):
                            child(timer[0]['An'], self.get_shortname())
                            # child(datetime.strptime(timer[0]['An'], '%H:%M').time().isoformat())
                        elif child_item.endswith('aus1'):
                            child(timer[0]['Aus'], self.get_shortname())
                        elif child_item.endswith('an2'):
                            child(timer[1]['An'], self.get_shortname())
                        elif child_item.endswith('aus2'):
                            child(timer[1]['Aus'], self.get_shortname())
                        elif child_item.endswith('an3'):
                            child(timer[2]['An'], self.get_shortname())
                        elif child_item.endswith('aus3'):
                            child(timer[2]['Aus'], self.get_shortname())
                        elif child_item.endswith('an4'):
                            child(timer[3]['An'], self.get_shortname())
                        elif child_item.endswith('aus4'):
                            child(timer[3]['Aus'], self.get_shortname())
                except:
                    self.log_debug('No child items for timer found (use timer.structs) or value no valid')
            elif commandunit == 'TI':
                rawdatastring = rawdatabytes.hex()
                rawdata = bytearray()
                rawdata.extend(map(ord, rawdatastring))
                # decode datetime
                value = datetime.strptime(rawdata.decode(), '%Y%m%d%W%H%M%S').isoformat()
                self.log_debug('Matched command {} and read transformed datetime {} and byte length {}.'.format(commandname, value, commandvaluebytes))
            elif commandunit == 'DA':
                rawdatastring = rawdatabytes.hex()
                rawdata = bytearray()
                rawdata.extend(map(ord, rawdatastring))
                # decode date
                value = datetime.strptime(rawdata.decode(), '%Y%m%d%W%H%M%S').date().isoformat()
                self.log_debug('Matched command {} and read transformed datetime {} and byte length {}.'.format(commandname, value, commandvaluebytes))
            elif commandunit == 'ES':
                # erstes Byte = Fehlercode; folgenden 8 Byte = Systemzeit
                errorcode = (rawdatabytes[:1]).hex()
                errorquerytime = (rawdatabytes[1:8]).hex()
                value = self.error_decode(errorcode)
                self.log_debug('Matched command {} and read transformed errorcode {} (raw value was {}) and byte length {}.'.format(commandname, value, errorcode, commandvaluebytes))
            elif commandunit == 'SC':
                # erstes Byte = Anlagenschema
                systemschemescode = (rawdatabytes[:1]).hex()
                value = self.systemscheme_decode(systemschemescode)
                self.log_debug('Matched command {} and read transformed system scheme {} (raw value was {}) and byte length {}.'.format(commandname, value, systemschemescode, commandvaluebytes))
            elif commandunit == 'BA':
                operatingmodecode = (rawdatabytes[:1]).hex()
                value = self.operatingmode_decode(operatingmodecode)
                self.log_debug('Matched command {} and read transformed operating mode {} (raw value was {}) and byte length {}.'.format(commandname, value, operatingmodecode, commandvaluebytes))
            elif commandunit == 'DT':
                # device type has 8 bytes, but first 4 bytes are device type indicator
                devicetypebytes = rawdatabytes[:2].hex()
                value = self.devicetype_decode(devicetypebytes).upper()
                self.log_debug('Matched command {} and read transformed device type {} (raw value was {}) and byte length {}.'.format(commandname, value, devicetypebytes, commandvaluebytes))
            elif commandunit == 'SN':
                # serial number has 7 bytes,
                serialnummerbytes = rawdatabytes[:7]
                value = self.serialnumber_decode(serialnummerbytes)
                self.log_debug('Matched command {} and read transformed serial number {} (raw value was {}) and byte length {}.'.format(commandname, value, serialnummerbytes, commandvaluebytes))
            else:
                rawvalue = self.bytes2int(rawdatabytes, commandsignage)
                value = self.value_transform_read(rawvalue, valuetransform)
                self.log_debug('Matched command {} and read transformed value {} (integer raw value was {}) and byte length {}.'.format(commandname, value, rawvalue, commandvaluebytes))

            # Update item
            item(value, self.get_shortname())

        # Handling of write command response if not error
        elif responsedatacode == 2 and responsetypecode != 3:
            self.log_info('Write request of adress {} successfull writing {} bytes.'.format(commandcode, valuebytecount))
        else:
            self.log_err('Write request of adress {} NOT successfull writing {} bytes.'.format(commandcode, valuebytecount))

    def run(self):
        self.connect()
        self.alive = True
        self.send_init_commands()
        self.create_cyclic_scheduler()

    def stop(self):
        self.scheduler_remove('cyclic')
        self.alive = False
        self.disconnect()

    def calc_checksum(self, packet):
        checksum = 0
        if len(packet) > 0:
            if packet[:1] == b'\x41':
                packet = packet[1:]
                checksum = sum(packet)
                checksum = checksum - int(checksum / 256) * 256
            else:
                self.log_err('bytes to calculate checksum from not starting with start byte')
        else:
            self.log_err('No bytes received to calculate checksum')
        return checksum

    def log_debug(self, text):
        self.logger.debug('{}: {}'.format(self.get_shortname(), text))

    def log_info(self, text):
        self.logger.info('{}: {}'.format(self.get_shortname(), text))

    def log_err(self, text):
        self.logger.error('{}: {}'.format(self.get_shortname(), text))

    def log_warn(self, text):
        self.logger.warning('{}: {}'.format(self.get_shortname(), text))

    def int2bytes(self, value, length, signage=False):
        # Limit value to the passed byte length
        value = value % (2 ** (length * 8))
        return value.to_bytes(length, byteorder='big', signed=bool(signage))

    def bytes2int(self, rawbytes, signage):
        return int.from_bytes(rawbytes, byteorder='little', signed=bool(signage))

    def bytes2hexstring(self, bytesvalue):
        return "".join("{:02x}".format(c) for c in bytesvalue)

    def decode_rawvalue(self, rawdatabytes, commandsignage):
        rawvalue = 0
        for i in range(len(rawdatabytes)):
            leftbyte = rawdatabytes[0]
            value = int(leftbyte * pow(256, i))
            rawvalue += value
            rawdatabytes = rawdatabytes[1:]
        # Signed/Unsigned berücksichtigen
        if commandsignage == 'signed' and rawvalue > int(pow(256, i) / 2 - 1):
            rawvalue = (pow(256, i) - rawvalue) * (-1)
        return rawvalue

    def decode_timer(self, rawdatabytes):
        while rawdatabytes:
            hours, minutes = divmod(int(rawdatabytes[:2], 16), 8)
            if minutes >= 6 or hours >= 24:
                yield "{}".format('00:00')  # f"00:00"  # keine gültiger Zeit-Wert
            else:
                yield "{:02d}:{:02d}".format(hours, minutes * 10)   # f"{hours:02d}:{minutes*10:02d}"
            rawdatabytes = rawdatabytes[2:]
        return None

    def encode_timer(self, switching_time):
        if switching_time == "00:00":
            return 0xff
        clocktime = re.compile(r'(\d\d):(\d\d)')
        mo = clocktime.search(switching_time)
        number = int(mo.group(1)) * 8 + int(mo.group(2)) // 10
        return number

    def value_transform_read(self, value, transform):
        if transform == 'bool':
            return bool(value)
        elif transform.isdigit() is True:
            return round(value / int(transform), 2)
        else:
            return int(value)

    def value_transform_write(self, value, transform):
        return int(value * int(transform))

    def error_decode(self, value):
        if value in self._errorset:
            errorstring = str(self._errorset[value])
        else:
            errorstring = str(value)
        return errorstring

    def systemscheme_decode(self, value):
        if value in self._systemschemes:
            systemscheme = str(self._systemschemes[value])
        else:
            systemscheme = str(value)
        return systemscheme

    def operatingmode_decode(self, value):
        if value in self._operatingmodes:
            operatingmode = str(self._operatingmodes[value])
        else:
            operatingmode = str(value)
        return operatingmode

    def devicetype_decode(self, value):
        if value in self._devicetypes:
            devicetypes = str(self._devicetypes[value])
        else:
            devicetypes = str(value)
        return devicetypes

    def serialnumber_decode(self, serialnummerbytes):
        # serial number = ((((((((((((B0-48)*10)+(B1-48))*10)+(B2-48))*10)+(B3-48))*10)+(B4-48))*10)+(B5-48))*10)+B6-48"/>

# alternativ (schöner? :-) )
# serial = 0
# serialnummerbytes.reverse()
# for byte in range(0, len(serialnummerbytes)):
#   serial += (serialnummerbytes[byte] - 48) * 10 ** byte

        B0 = (serialnummerbytes[0])
        B1 = (serialnummerbytes[1])
        B2 = (serialnummerbytes[2])
        B3 = (serialnummerbytes[3])
        B4 = (serialnummerbytes[4])
        B5 = (serialnummerbytes[5])
        B6 = (serialnummerbytes[6])
        serialnumber = hex(((((((((((((B0 - 48) * 10) + (B1 - 48)) * 10) + (B2 - 48)) * 10) + (B3 - 48)) * 10) + (B4 - 48)) * 10) + (B5 - 48)) * 10) + B6 - 48).upper()
        return serialnumber

    def commandname_by_commandcode(self, commandcode):
        for commandname in self._commandset.keys():
            if (self._commandset[commandname]['addr']).lower() == commandcode:
                return commandname
        return None

    def init_webinterface(self):
        """"
        Initialize the web interface for this plugin

        This method is only needed if the plugin is implementing a web interface
        """
        try:
            self.mod_http = Modules.get_instance().get_module(
                'http')  # try/except to handle running in a core version that does not support modules
        except:
            self.mod_http = None
        if self.mod_http is None:
            self.logger.error("Not initializing the web interface")
            return False

        import sys
        if "SmartPluginWebIf" not in list(sys.modules['lib.model.smartplugin'].__dict__):
            self.logger.warning("Web interface needs SmartHomeNG v1.5 and up. Not initializing the web interface")
            return False

        # set application configuration for cherrypy
        webif_dir = self.path_join(self.get_plugin_dir(), 'webif')
        config = {
            '/': {
                'tools.staticdir.root': webif_dir,
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'static'
            }
        }

        # Register the web interface as a cherrypy app
        self.mod_http.register_webif(WebInterface(webif_dir, self),
                                     self.get_shortname(),
                                     config,
                                     self.get_classname(), self.get_instance_name(),
                                     description='')

        return True


# ------------------------------------------
#    Webinterface of the plugin
# ------------------------------------------


class WebInterface(SmartPluginWebIf):

    def __init__(self, webif_dir, plugin):
        """
        Initialization of instance of class WebInterface

        :param webif_dir: directory where the webinterface of the plugin resides
        :param plugin: instance of the plugin
        :type webif_dir: str
        :type plugin: object
        """
        self.logger = logging.getLogger(__name__)
        self.webif_dir = webif_dir
        self.plugin = plugin
        self.tplenv = self.init_template_environment()

        self.items = Items.get_instance()

    @cherrypy.expose
    def index(self, reload=None):
        """
        Build index.html for cherrypy

        Render the template and return the html file to be delivered to the browser

        :return: contents of the template after beeing rendered
        """
        tmpl = self.tplenv.get_template('index.html')
        # add values to be passed to the Jinja2 template eg: tmpl.render(p=self.plugin, interface=interface, ...)
        return tmpl.render(p=self.plugin, items=sorted(self.items.return_items(), key=lambda k: str.lower(k['_path'])))

    @cherrypy.expose
    def get_data_html(self, dataSet=None):
        """
        Return data to update the webpage

        For the standard update mechanism of the web interface, the dataSet to return the data for is None

        :param dataSet: Dataset for which the data should be returned (standard: None)
        :return: dict with the data needed to update the web page.
        """
        if dataSet is None:
            # get the new data
            data = {}

            # data['item'] = {}
            # for i in self.plugin.items:
            #     data['item'][i]['value'] = self.plugin.getitemvalue(i)
            #
            # return it as json the the web page
            # try:
            #     return json.dumps(data)
            # except Exception as e:
            #     self.logger.error("get_data_html exception: {}".format(e))
        return {}
