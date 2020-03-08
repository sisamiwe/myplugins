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

controlset = {
    'P300': {
        'StartByte': 0x41,
        'Request': 0x00,
        'Response': 0x01,
        'Error': 0x03,
        'Read': 0x01,
        'Write': 0x02,
        'Function_Call': 0x7,
        'Acknowledge': 0x06,
        'Not_initiated': 0x05,
        'Init_Error': 0x15,
        'Reset_Command': 0x04,
        'Reset_Command_Response': 0x05,
        'Sync_Command': 0x160000,
        'Sync_Command_Response': 0x06,
        'Command_bytes_read': 0x05,
        'Command_bytes_write': 0x05,
        'Command_length': 9,
        'Checksum_length': 1,
        #init:              send'Reset_Command' receive'Reset_Command_Response' send'Sync_Command'
        #request:           send('StartByte' 'Länge der Nutzdaten als Anzahl der Bytes zwischen diesem Byte und der Prüfsumme' 'Request' 'Read' 'addr' 'checksum')
        #request_response:  receive('Acknowledge' 'StartByte' 'Länge der Nutzdaten als Anzahl der Bytes zwischen diesem Byte und der Prüfsumme' 'Response' 'Read' 'addr' 'Anzahl der Bytes des Wertes' 'Wert' 'checksum')
    },
}
    
commandset = {
    'V200KO1B': {
        # Kessel
        'get_Aussentemperatur':         { 'addr': '0800', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Aussentemperatur
        'get_Aussentemperatur_TP':      { 'addr': '5525', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Aussentemperatur_tiefpass
        'get_Aussentemperatur_Dp':      { 'addr': '5527', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Aussentemperatur in Grad C (Gedaempft)
        'get_Kesseltemperatur':         { 'addr': '0802', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Kesseltemperatur
        'get_Kesseltemperatur_TP':      { 'addr': '0810', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Kesseltemperatur_tiefpass
        'get_Kesselsolltemperatur':     { 'addr': '555A', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Kesselsolltemperatur
        'get_Temp_Speicher_Ladesensor': { 'addr': '0812', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Temperatur Speicher Ladesensor Komfortsensor
        'get_Auslauftemperatur':        { 'addr': '0814', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Auslauftemperatur
        'get_Abgastemperatur':          { 'addr': '0816', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Abgastemperatur
        'get_Gem_Vorlauftemperatur':    { 'addr': '081a', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Gem. Vorlauftemperatur
        'get_Relais_K12':               { 'addr': '0842', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Relais K12 Interne Anschlußerweiterung
        'get_Eingang_0-10_V':           { 'addr': '0a86', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Eingang 0-10 V
        'get_EA1_Kontakt_0':            { 'addr': '0a90', 'len': 1, 'type': 'read', 'unit': 'BST' }, #EA1: Kontakt 0
        'get_EA1_Kontakt_1':            { 'addr': '0a91', 'len': 1, 'type': 'read', 'unit': 'BST' }, #EA1: Kontakt 1
        'get_EA1_Kontakt_2':            { 'addr': '0a92', 'len': 1, 'type': 'read', 'unit': 'BST' }, #EA1: Kontakt 2
        'get_EA1_Externer_Soll_0-10V':  { 'addr': '0a93', 'len': 1, 'type': 'read', 'unit': 'ST' }, #EA1: Externer Sollwert 0-10V
        'get_EA1_Relais_0':             { 'addr': '0a95', 'len': 1, 'type': 'read', 'unit': 'BST' }, #EA1: Relais 0
        'get_AM1_Ausgang_1':            { 'addr': '0aa0', 'len': 1, 'type': 'read', 'unit': 'BST' }, #AM1 Ausgang 1
        'get_AM1_Ausgang_2':            { 'addr': '0aa1', 'len': 1, 'type': 'read', 'unit': 'BST' }, #AM1 Ausgang 2
        'get_TempKOffset':              { 'addr': '6760', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Kesseloffset KT ueber WWsoll in Grad C
        'set_TempKOffset':              { 'addr': '6760', 'len': 1, 'type': 'write', 'unit': 'UTI' }, #Kesseloffset KT ueber WWsoll in Grad C
        'get_Systemtime':               { 'addr': '088E', 'len': 8, 'type': 'read', 'unit': 'TI' }, #Systemzeit
        'set_Systemtime':               { 'addr': '088E', 'len': 8, 'type': 'write', 'unit': 'TI' }, #Systemzeit
        'get_KA5_A1M1':                 { 'addr': '27A5', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #HeizkreispumpenlogikFunktion A1M1 <!-- A5:0 Ohne Heizkreispumpenlogik-Funktion | Heizkreispumpe aus, wenn A5:1 AT > RTSoll + 5 K A5:2 AT > RTSoll + 4 K A5:3  AT > RTSoll + 3 K A5:4 AT > RTSoll + 2 K A5:5 AT > RTSoll + 1 K A5:6 AT = RTSoll A5:7 AT > RTSoll -1 K bis A5:15 AT > RTSoll -9 K -->
        'set_KA5_A1M1':                 { 'addr': '27A5', 'len': 1, 'type': 'write', 'unit': 'UTI' }, #HeizkreispumpenlogikFunktion A1M1
        'get_KA5_M2':                   { 'addr': '37A5', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #HeizkreispumpenlogikFunktion M2 <!-- A5:0 Ohne Heizkreispumpenlogik-Funktion | Heizkreispumpe aus, wenn A5:1 AT > RTSoll + 5 K A5:2 AT > RTSoll + 4 K A5:3  AT > RTSoll + 3 K A5:4 AT > RTSoll + 2 K A5:5 AT > RTSoll + 1 K A5:6 AT = RTSoll A5:7 AT > RTSoll -1 K bis A5:15 AT > RTSoll -9 K -->
        'set_KA5_M2':                   { 'addr': '37A5', 'len': 1, 'type': 'write', 'unit': 'UTI' }, #HeizkreispumpenlogikFunktion M2
        'get_KA6_A1M1':                 { 'addr': '27A6', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #AbsolutSommersparschaltung A1M1
        'set_KA6_A1M1':                 { 'addr': '27A6', 'len': 1, 'type': 'write', 'unit': 'UTI' }, #AbsolutSommersparschaltung A1M1
        'get_KA6_M2':                   { 'addr': '37A6', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #AbsolutSommersparschaltung M2 
        'set_KA6_M2':                   { 'addr': '37A6', 'len': 1, 'type': 'write', 'unit': 'UTI' }, #AbsolutSommersparschaltung M2
        'get_KA3_A1M1':                 { 'addr': '27A3', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Frostschutzgrenze A1M1 <!-- Range GradCelsius SByte 1 -9 15 -->
        'set_KA3_A1M1':                 { 'addr': '27A3', 'len': 1, 'type': 'write', 'unit': 'UTI' }, #Frostschutzgrenze A1M1
        'get_KA3_M2':                   { 'addr': '37A3', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Frostschutzgrenze M2 <!-- Range GradCelsius SByte 1 -9 15 -->
        'set_KA3_M2':                   { 'addr': '37A3', 'len': 1, 'type': 'write', 'unit': 'UTI' }, #Frostschutzgrenze M2
        'get_Anlagenschema':            { 'addr': '7700', 'len': 2, 'type': 'read', 'unit': 'ST' }, #Anlagenschema  <!-- 7700 1 A1 | 1 2 A1 + WW | 2 3 M2 | 3 4 M2 + WW | 4 5 A1 + M2 | 5 6 A1 + M2 + WW | 6 -->
        #Fehler
        'get_Sammelstoerung':           { 'addr': '0a82', 'len': 1, 'type': 'read', 'unit': 'RT' }, #Sammelstörung
        'get_Error0':                   { 'addr': '7507', 'len': 9, 'type': 'read', 'unit': 'ES' }, #Fehlerhistory Eintrag 1
        'get_Error1':                   { 'addr': '7510', 'len': 9, 'type': 'read', 'unit': 'ES' }, #Fehlerhistory Eintrag 2
        'get_Error2':                   { 'addr': '7519', 'len': 9, 'type': 'read', 'unit': 'ES' }, #Fehlerhistory Eintrag 3
        'get_Error3':                   { 'addr': '7522', 'len': 9, 'type': 'read', 'unit': 'ES' }, #Fehlerhistory Eintrag 4
        'get_Error4':                   { 'addr': '752B', 'len': 9, 'type': 'read', 'unit': 'ES' }, #Fehlerhistory Eintrag 5
        'get_Error5':                   { 'addr': '7534', 'len': 9, 'type': 'read', 'unit': 'ES' }, #Fehlerhistory Eintrag 6
        'get_Error6':                   { 'addr': '753D', 'len': 9, 'type': 'read', 'unit': 'ES' }, #Fehlerhistory Eintrag 7
        'get_Error7':                   { 'addr': '7546', 'len': 9, 'type': 'read', 'unit': 'ES' }, #Fehlerhistory Eintrag 8
        'get_Error8':                   { 'addr': '754F', 'len': 9, 'type': 'read', 'unit': 'ES' }, #Fehlerhistory Eintrag 9
        'get_Error9':                   { 'addr': '7558', 'len': 9, 'type': 'read', 'unit': 'ES' }, #Fehlerhistory Eintrag 10
        #Pumpen
        'get_Speicherladepumpe':        { 'addr': '6513', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Speicherladepumpe
        'get_Zirkulationspumpe':        { 'addr': '6515', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Zirkulationspumpe
        'get_Interne_Pumpe':            { 'addr': '7660', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Interne Pumpe
        'get_Heizkreispumpe_A1M1':      { 'addr': '7663', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Heizkreispumpe A1
        'get_Heizkreispumpe_A1M1_RPM':  { 'addr': '7663', 'len': 1, 'type': 'read', 'unit': 'PR2' }, #Heizkreispumpe A1M1 Drehzahl
        'get_Heizkreispumpe_M2_RPM':    { 'addr': '7665', 'len': 1, 'type': 'read', 'unit': 'PR2' }, #Heizkreispumpe Drehzahl
        'get_Relais_Status_Pumpe_A1M1': { 'addr': 'a152', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Relais-Status Heizkreispumpe 1
        # Brenner
        'get_Brennerstarts':            { 'addr': '088a', 'len': 4, 'type': 'read', 'unit': 'CO' }, #Brennerstarts
        'set_Brennerstarts':            { 'addr': '088a', 'len': 4, 'type': 'write', 'unit': 'CO', 'min_value': 0, 'max_value': 1193045 }, #Brennerstarts
        'get_Brenner_Betriebsstunden':  { 'addr': '08a7', 'len': 4, 'type': 'read', 'unit': 'CS' }, #Brenner-Betriebsstunden
        'set_Brenner_Betriebsstunden':  { 'addr': '08a7', 'len': 4, 'type': 'write', 'unit': 'CS', 'min_value': 0, 'max_value': 1193045 }, #Brenner-Betriebsstunden        
        'get_Brennerstatus_1':          { 'addr': '0842', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Brennerstatus Stufe1
        'get_Brennerstatus_2':          { 'addr': '0849', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Brennerstatus Stufe2
        'get_Oeldurchsatz':             { 'addr': '5726', 'len': 4, 'type': 'read', 'unit': 'CO' }, #Oeldurchsatz Brenner in Dezi-Liter pro Stunde
        'set_Oeldurchsatz':             { 'addr': '5726', 'len': 4, 'type': 'read', 'unit': 'CO' }, #Oeldurchsatz Brenner in Dezi-Liter pro Stunde
        'get_Oelverbrauch':             { 'addr': '7574', 'len': 4, 'type': 'read', 'unit': 'COL' }, #Oelverbrauch kumuliert
        # Heizkreis A1M1
        'get_Raumtemperatur_A1M1':                     { 'addr': '0896', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Raumtemperatur A1M1
        'get_Raumtemperatur_Soll_Normalbetrieb_A1M1':  { 'addr': '2306', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Raumtemperatur Soll Normalbetrieb A1M1
        'set_Raumtemperatur_Soll_Normalbetrieb_A1M1':  { 'addr': '2306', 'len': 1, 'type': 'write', 'unit': 'UTI', 'min_value': 3, 'max_value': 37 }, #Raumtemperatur Soll Normalbetrieb A1M1
        'get_Raumtemperatur_Soll_Red_Betrieb_A1M1':    { 'addr': '2307', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Raumtemperatur Soll Reduzierter Betrieb A1M1
        'set_Raumtemperatur_Soll_Red_Betrieb_A1M1':    { 'addr': '2307', 'len': 1, 'type': 'write', 'unit': 'UTI', 'min_value': 3, 'max_value': 37 }, #Raumtemperatur Soll Reduzierter Betrieb A1M1
        'get_Raumtemperatur_Soll_Party_Betrieb_A1M1':  { 'addr': '2308', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Raumtemperatur Soll Party Betrieb A1M1
        'set_Raumtemperatur_Soll_Party_Betrieb_A1M1':  { 'addr': '2308', 'len': 1, 'type': 'write', 'unit': 'UTI' }, #Raumtemperatur Soll Party Betrieb A1M1
        'get_Aktuelle_Betriebsart_A1M1':               { 'addr': '2301', 'len': 1, 'type': 'read', 'unit': 'BA' }, #Aktuelle Betriebsart A1M1
        'get_Betriebsart_A1M1':                        { 'addr': '2323', 'len': 1, 'type': 'read', 'unit': 'BA' }, #Betriebsart A1M1
        'set_Betriebsart_A1M1':                        { 'addr': '2323', 'len': 1, 'type': 'write', 'unit': 'BA', 'min_value': 0, 'max_value': 4 }, #Betriebsart A1M1
        'get_Sparbetrieb_A1M1':                        { 'addr': '2302', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Sparbetrieb A1M1
        'set_Sparbetrieb_A1M1':                        { 'addr': '2302', 'len': 1, 'type': 'write', 'unit': 'BST', 'min_value': 0, 'max_value': 1 }, #Sparbetrieb A1M1
        'get_Zustand_Sparbetrieb_A1M1':                { 'addr': '2331', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Zustand Sparbetrieb A1M1
        'get_Partybetrieb_A1M1':                       { 'addr': '2303', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Partybetrieb A1M1
        'set_Partybetrieb_A1M1':                       { 'addr': '2303', 'len': 1, 'type': 'write', 'unit': 'BST', 'min_value': 0, 'max_value': 1 }, #Partybetrieb A1M1
        'get_Zustand_Partybetrieb_A1M1':               { 'addr': '2330', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Zustand Partybetrieb A1M1
        'get_Vorlauftemperatur_A1M1':                  { 'addr': '2900', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Vorlauftemperatur A1M1
        'get_Vorlauftemperatur_Soll_A1M1':             { 'addr': '2544', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Vorlauftemperatur Soll A1M1
        'get_StatusFrost_A1M1':                        { 'addr': '2500', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Status Frostwarnung A1M1
        'get_Neigung_Heizkennlinie_A1M1':              { 'addr': '27D3', 'len': 1, 'type': 'read', 'unit': 'UN' }, #Neigung Heizkennlinie A1M1
        'set_Neigung_Heizkennlinie_A1M1':              { 'addr': '27d3', 'len': 1, 'type': 'write', 'unit': 'UN', 'min_value': 0.2, 'max_value': 3.5 }, #Neigung Heizkennlinie A1M1
        'get_Niveau_Heizkennlinie_A1M1':               { 'addr': '27d4', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Niveau Heizkennlinie A1M1
        'set_Niveau_Heizkennlinie_A1M1':               { 'addr': '27d4', 'len': 1, 'type': 'write', 'unit': 'ST', 'min_value': -13, 'max_value': 40 }, #Niveau Heizkennlinie A1M1
        'get_Heizkreispumpe_A1M1':                     { 'addr': '2906', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Heizkreispumpe A1M1
        'get_Externe_Raumsolltemperatur_Normal_A1M1':  { 'addr': '2321', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Externe Raumsolltemperatur Normal A1M1
        'set_Externe_Raumsolltemperatur_Normal_A1M1':  { 'addr': '2321', 'len': 1, 'type': 'write', 'unit': 'UTI', 'min_value': 0, 'max_value': 37 }, #Externe Raumsolltemperatur Normal A1M1
        'get_Externe_Betriebsartenumschaltung_A1M1':   { 'addr': '2549', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Externe Betriebsartenumschaltung A1M1
        'set_Externe_Betriebsartenumschaltung_A1M1':   { 'addr': '2549', 'len': 1, 'type': 'write', 'unit': 'ST', 'min_value': 0, 'max_value': 4 }, #Externe Betriebsartenumschaltung A1M1
        # Heizkreis M2
        'get_Raumtemperatur_M2':                     { 'addr': '0898', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Raumtemperatur M2
        'get_Raumtemperatur_Soll_Normalbetrieb_M2':  { 'addr': '3306', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Raumtemperatur Soll Normalbetrieb M2
        'set_Raumtemperatur_Soll_Normalbetrieb_M2':  { 'addr': '3306', 'len': 1, 'type': 'write', 'unit': 'UTI', 'min_value': 3, 'max_value': 37 }, #Raumtemperatur Soll Normalbetrieb M2
        'get_Raumtemperatur_Soll_Red_Betrieb_M2':    { 'addr': '3307', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Raumtemperatur Soll Reduzierter Betrieb M2
        'set_Raumtemperatur_Soll_Red_Betrieb_M2':    { 'addr': '3307', 'len': 1, 'type': 'write', 'unit': 'UTI', 'min_value': 3, 'max_value': 37 }, #Raumtemperatur Soll Reduzierter Betrieb M2
        'get_Raumtemperatur_Soll_Party_Betrieb_M2':  { 'addr': '3308', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Raumtemperatur Soll Party Betrieb M2
        'set_Raumtemperatur_Soll_Party_Betrieb_M2':  { 'addr': '3308', 'len': 1, 'type': 'write', 'unit': 'UTI' }, #Raumtemperatur Soll Party Betrieb M2
        'get_Aktuelle_Betriebsart_M2':               { 'addr': '3301', 'len': 1, 'type': 'read', 'unit': 'BA' }, #Aktuelle Betriebsart M2
        'get_Betriebsart_M2':                        { 'addr': '3323', 'len': 1, 'type': 'read', 'unit': 'BA' }, #Betriebsart M2
        'set_Betriebsart_M2':                        { 'addr': '3323', 'len': 1, 'type': 'write', 'unit': 'BA', 'min_value': 0, 'max_value': 4 }, #Betriebsart M2
        'get_Sparbetrieb_M2':                        { 'addr': '3302', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Sparbetrieb M2
        'set_Sparbetrieb_M2':                        { 'addr': '3302', 'len': 1, 'type': 'write', 'unit': 'BST', 'min_value': 0, 'max_value': 1 }, #Sparbetrieb M2
        'get_Zustand_Sparbetrieb_M2':                { 'addr': '3331', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Zustand Sparbetrieb M2
        'get_Partybetrieb_M2':                       { 'addr': '3303', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Partybetrieb M2
        'set_Partybetrieb_M2':                       { 'addr': '3303', 'len': 1, 'type': 'write', 'unit': 'BST', 'min_value': 0, 'max_value': 1 }, #Partybetrieb M2
        'get_Zustand_Partybetrieb_M2':               { 'addr': '3330', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Zustand Partybetrieb M2
        'get_Vorlauftemperatur_M2':                  { 'addr': '3900', 'len': 1, 'type': 'read', 'unit': 'UT' }, #Vorlauftemperatur M2
        'get_Vorlauftemperatur_Soll_M2':             { 'addr': '3544', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Vorlauftemperatur Soll M2
        'get_StatusFrost_M2':                        { 'addr': '3500', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Status Frostwarnung M2
        'get_Neigung_Heizkennlinie_M2':              { 'addr': '37d3', 'len': 1, 'type': 'read', 'unit': 'UN' }, #Neigung Heizkennlinie M2
        'set_Neigung_Heizkennlinie_M2':              { 'addr': '37d3', 'len': 1, 'type': 'write', 'unit': 'UN', 'min_value': 0.2, 'max_value': 3.5 }, #Neigung Heizkennlinie M2
        'get_Niveau_Heizkennlinie_M2':               { 'addr': '37d4', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Niveau Heizkennlinie M2
        'set_Niveau_Heizkennlinie_M2':               { 'addr': '37d4', 'len': 1, 'type': 'write', 'unit': 'ST', 'min_value': -13, 'max_value': 40 }, #Niveau Heizkennlinie M2
        'get_Heizkreispumpe_M2':                     { 'addr': '3906', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Heizkreispumpe M2
        'get_Externe_Raumsolltemperatur_Normal_M2':  { 'addr': '3321', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Externe Raumsolltemperatur Normal M2
        'set_Externe_Raumsolltemperatur_Normal_M2':  { 'addr': '3321', 'len': 1, 'type': 'write', 'unit': 'UTI', 'min_value': 0, 'max_value': 37 }, #Externe Raumsolltemperatur Normal M2
        'get_Externe_Betriebsartenumschaltung_M2':   { 'addr': '3549', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Externe Betriebsartenumschaltung M2
        'set_Externe_Betriebsartenumschaltung_M2':   { 'addr': '3549', 'len': 1, 'type': 'write', 'unit': 'ST', 'min_value': 0, 'max_value': 4 }, #Externe Betriebsartenumschaltung M2
        # Warmwasser
        'get_Warmwasser_Temperatur':     { 'addr': '0804', 'len': 2, 'type': 'read', 'unit': 'UT' }, #Warmwassertemperatur in Grad C
        'get_Warmwasser_Solltemperatur': { 'addr': '6300', 'len': 1, 'type': 'read', 'unit': 'UTI' }, #Warmwasser-Solltemperatur
        'set_Warmwasser_Solltemperatur': { 'addr': '6300', 'len': 1, 'type': 'write', 'unit': 'UTI', 'min_value': 10, 'max_value': 95 }, #Warmwasser-Solltemperatur
        'get_Satus_Warmwasserbereitung': { 'addr': '650a', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Satus Warmwasserbereitung
        'set_Satus_Warmwasserbereitung': { 'addr': '650a', 'len': 1, 'type': 'write', 'unit': 'BST', 'min_value': 0, 'max_value': 1 }, #Satus Warmwasserbereitung
        'get_WWUWPNachlauf':             { 'addr': '6762', 'len': 2, 'type': 'read', 'unit': 'CO' }, #Warmwasserpumpennachlauf
        'set_WWUWPNachlauf':             { 'addr': '6762', 'len': 2, 'type': 'write', 'unit': 'CO', 'min_value': 0, 'max_value': 1 }, #Warmwasserpumpennachlauf
        'get_Speichervorrang_A1M1':      { 'addr': '27A2', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Speichervorrang Heizkreis ohne Mischer A1
        'set_Speichervorrang_A1M1':      { 'addr': '27A2', 'len': 1, 'type': 'write', 'unit': 'ST', 'min_value': 10, 'max_value': 95 }, #Speichervorrang Heizkreis ohne Mischer A1
        'get_Speichervorrang_M2':        { 'addr': '37A2', 'len': 1, 'type': 'read', 'unit': 'ST' }, #Speichervorrang Heizkreis M2
        'set_Speichervorrang_M2':        { 'addr': '37A2', 'len': 1, 'type': 'write', 'unit': 'ST', 'min_value': 10, 'max_value': 95 }, #Speichervorrang Heizkreis M2
        # Ferienprogramm HK_A1M1
        'get_Ferienprogramm_A1M1':      { 'addr': '2535', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Ferienprogramm A1M1
		'set_Ferienprogramm_A1M1':      { 'addr': '2535', 'len': 1, 'type': 'write', 'unit': 'BST' }, #Ferienprogramm A1M1
        'get_Ferien_Abreisetag_A1M1':   { 'addr': '2309', 'len': 8, 'type': 'read', 'unit': 'TI' }, #Ferien Abreisetag A1M1
		'set_Ferien_Abreisetag_A1M1':   { 'addr': '2309', 'len': 8, 'type': 'write', 'unit': 'TI' }, #Ferien Abreisetag A1M1
        'get_Ferien_Rückreisetag_A1M1': { 'addr': '2311', 'len': 8, 'type': 'read', 'unit': 'TI' }, #Ferien Rückreisetag A1M1
        'set_Ferien_Rückreisetag_A1M1': { 'addr': '2311', 'len': 8, 'type': 'write', 'unit': 'TI' }, #Ferien Rückreisetag A1M1 
        # Ferienprogramm HK_M2
        'get_Ferienprogramm_M2':      { 'addr': '3535', 'len': 1, 'type': 'read', 'unit': 'BST' }, #Ferienprogramm M2
        'set_Ferienprogramm_M2':      { 'addr': '3535', 'len': 1, 'type': 'write', 'unit': 'BST' }, #Ferienprogramm M2
        'get_Ferien_Abreisetag_M2':   { 'addr': '3309', 'len': 8, 'type': 'read', 'unit': 'TI' }, #Ferien Abreisetag M2
		'set_Ferien_Abreisetag_M2':   { 'addr': '3309', 'len': 8, 'type': 'write', 'unit': 'TI' }, #Ferien Abreisetag M2
        'get_Ferien_Rückreisetag_M2': { 'addr': '3311', 'len': 8, 'type': 'read', 'unit': 'TI' }, #Ferien Rückreisetag M2
        'set_Ferien_Rückreisetag_M2': { 'addr': '3311', 'len': 8, 'type': 'write', 'unit': 'TI' }, #Ferien Rückreisetag M2        
        # Schaltzeiten Warmwasser
        'get_Timer_Warmwasserbereitung_Mo': { 'addr': '2100', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Montag
        'get_Timer_Warmwasserbereitung_Di': { 'addr': '2108', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Dienstag
        'get_Timer_Warmwasserbereitung_Mi': { 'addr': '2110', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Mittwoch
        'get_Timer_Warmwasserbereitung_Do': { 'addr': '2118', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Donnerstag
        'get_Timer_Warmwasserbereitung_Fr': { 'addr': '2120', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Freitag
        'get_Timer_Warmwasserbereitung_Sa': { 'addr': '2128', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Samstag
        'get_Timer_Warmwasserbereitung_So': { 'addr': '2130', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Sonntag        
        'set_Timer_Warmwasserbereitung_Mo': { 'addr': '2100', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Montag
        'set_Timer_Warmwasserbereitung_Di': { 'addr': '2108', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Dienstag
        'set_Timer_Warmwasserbereitung_Mi': { 'addr': '2110', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Mittwoch
        'set_Timer_Warmwasserbereitung_Do': { 'addr': '2118', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Donnerstag
        'set_Timer_Warmwasserbereitung_Fr': { 'addr': '2120', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Freitag
        'set_Timer_Warmwasserbereitung_Sa': { 'addr': '2128', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Samstag
        'set_Timer_Warmwasserbereitung_So': { 'addr': '2130', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Warmwasserbereitung Sonntag    
        # Schaltzeiten HK_A1M1
        'get_Timer_A1M1_Mo': { 'addr': '2000', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Montag
        'get_Timer_A1M1_Di': { 'addr': '2008', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Dienstag
        'get_Timer_A1M1_Mi': { 'addr': '2010', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Mittwoch
        'get_Timer_A1M1_Do': { 'addr': '2018', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Donnerstag
        'get_Timer_A1M1_Fr': { 'addr': '2020', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Freitag
        'get_Timer_A1M1_Sa': { 'addr': '2028', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Samstag
        'get_Timer_A1M1_So': { 'addr': '2030', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Sonntag
        'set_Timer_A1M1_Mo': { 'addr': '2000', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Montag
        'set_Timer_A1M1_Di': { 'addr': '2008', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Dienstag
        'set_Timer_A1M1_Mi': { 'addr': '2010', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Mittwoch
        'set_Timer_A1M1_Do': { 'addr': '2018', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Donnerstag
        'set_Timer_A1M1_Fr': { 'addr': '2020', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Freitag
        'set_Timer_A1M1_Sa': { 'addr': '2028', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Samstag
        'set_Timer_A1M1_So': { 'addr': '2030', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Sonntag
        # Schaltzeiten HK_M2
        'get_Timer_M2_Mo': { 'addr': '3000', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Montag
        'get_Timer_M2_Di': { 'addr': '3008', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Dienstag
        'get_Timer_M2_Mi': { 'addr': '3010', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Mittwoch
        'get_Timer_M2_Do': { 'addr': '3018', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Donnerstag
        'get_Timer_M2_Fr': { 'addr': '3020', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Freitag
        'get_Timer_M2_Sa': { 'addr': '3028', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Samstag
        'get_Timer_M2_So': { 'addr': '3030', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Sonntag
        'set_Timer_M2_Mo': { 'addr': '3000', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Montag
        'set_Timer_M2_Di': { 'addr': '3008', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Dienstag
        'set_Timer_M2_Mi': { 'addr': '3010', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Mittwoch
        'set_Timer_M2_Do': { 'addr': '3018', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Donnerstag
        'set_Timer_M2_Fr': { 'addr': '3020', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Freitag
        'set_Timer_M2_Sa': { 'addr': '3028', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Samstag
        'set_Timer_M2_So': { 'addr': '3030', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Heizkreis_A1M1 Sonntag
        # Schaltzeiten Zirkulation
        'get_Timer_Zirku_Mo': { 'addr': '2200', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Montag
        'get_Timer_Zirku_Di': { 'addr': '2208', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Dienstag
        'get_Timer_Zirku_Mi': { 'addr': '2210', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Mittwoch
        'get_Timer_Zirku_Do': { 'addr': '2218', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Donnerstag
        'get_Timer_Zirku_Fr': { 'addr': '2220', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Freitag
        'get_Timer_Zirku_Sa': { 'addr': '2228', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Samstag
        'get_Timer_Zirku_So': { 'addr': '2230', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Sonntag
        'set_Timer_Zirku_Mo': { 'addr': '2200', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Montag
        'set_Timer_Zirku_Di': { 'addr': '2208', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Dienstag
        'set_Timer_Zirku_Mi': { 'addr': '2210', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Mittwoch
        'set_Timer_Zirku_Do': { 'addr': '2218', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Donnerstag
        'set_Timer_Zirku_Fr': { 'addr': '2220', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Freitag
        'set_Timer_Zirku_Sa': { 'addr': '2228', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Samstag
        'set_Timer_Zirku_So': { 'addr': '2230', 'len': 8, 'type': 'read', 'unit': 'CT' }, #Timer Zirkulationspumpe Sonntag
    },
}

unitset = {
    'P300': {
		'BA': { 'unit_de': 'Betriebsart', 'type': 'list', 'byte': 1, 'signed': False, 'read_value_transform': 'non' },
		'BH': { 'unit_de': 'Brennerstunden', 'type': 'integer', 'byte': 4, 'signed': True, 'read_value_transform': 'non' },
		'BST': { 'unit_de': 'Bitstatus', 'type': 'integer', 'byte': 1, 'signed': False, 'read_value_transform': 'non' },
		'CO': { 'unit_de': 'Counter', 'type': 'integer', 'byte': 4, 'signed': True, 'read_value_transform': 'non' },
		'COL': { 'unit_de': 'Counter liter', 'type': 'integer', 'byte': 4, 'signed': True, 'read_value_transform': '/ 1000' },
		'CS': { 'unit_de': 'CounterS', 'type': 'integer', 'byte': 4, 'signed': False, 'read_value_transform': '/ 3600' },
		'CT': { 'unit_de': 'CycleTime', 'type': 'list', 'byte': , 'signed': False, 'read_value_transform': 'non' },
		'DT': { 'unit_de': 'DeviceType', 'type': 'list', 'byte': , 'signed': False, 'read_value_transform': 'non' },
		'ES': { 'unit_de': 'ErrorState', 'type': 'list', 'byte': 9, 'signed': False, 'read_value_transform': 'non' },
		'ESG': { 'unit_de': 'ErrorStateGWG', 'type': '', 'byte': , 'signed': False, 'read_value_transform': 'non' },
		'HKT': { 'unit_de': 'HKP Pumpentyp', 'type': '', 'byte': , 'signed': False, 'read_value_transform': 'non' },
		'PR': { 'unit_de': 'Prozent', 'type': 'integer', 'byte': 2, 'signed': False, 'read_value_transform': '/ 2' },
		'PR1': { 'unit_de': 'Prozent 1 Byte ganzzahlig', 'type': 'integer', 'byte': 1, 'signed': False, 'read_value_transform': 'non' },
		'PR2': { 'unit_de': 'Prozent zweites Byte ganzzahlig (Pumpe)', 'type': 'integer', 'byte': 1, 'signed': False, 'read_value_transform': 'non' },
		'PR3': { 'unit_de': 'Prozent erstes Byte', 'type': 'integer', 'byte': 1, 'signed': False, 'read_value_transform': '/ 2' },
		'RT': { 'unit_de': 'ReturnStatus', 'type': 'list', 'byte': 1, 'signed': False, 'read_value_transform': 'non' },
		'SN': { 'unit_de': 'Sachnummer', 'type': 'serial', 'byte': , 'signed': False, 'read_value_transform': 'non' },
		'SR': { 'unit_de': 'SetReturnStatus', 'type': 'list', 'byte': 1, 'signed': False, 'read_value_transform': 'non' },
		'ST': { 'unit_de': 'Status', 'type': 'integer', 'byte': 1, 'signed': False, 'read_value_transform': 'bool' },
		'TI': { 'unit_de': 'SystemTime', 'type': 'datetime', 'byte': 8, 'signed': False, 'read_value_transform': 'non' },
		'UN': { 'unit_de': 'Neigung', 'type': 'integer', 'byte': 2, 'signed': False, 'read_value_transform': '/ 10' },
		'USV': { 'unit_de': 'Umschaltventil Stellung', 'type': '', 'byte': , 'signed': False, 'read_value_transform': 'non' },
		'UT': { 'unit_de': 'Temperatur', 'type': 'integer', 'byte': 2, 'signed': False, 'read_value_transform': '/ 10' },
		'UT1': { 'unit_de': 'Temperatur 1Byte', 'type': 'integer', 'byte': 1, 'signed': False, 'read_value_transform': '/ 2' },
		'UT1U': { 'unit_de': 'Temperatur 1Byte unsigned', 'type': 'integer', 'byte': , 'signed': False, 'read_value_transform': '/ 2' },
		'UTH': { 'unit_de': 'Temperatur100', 'type': 'integer', 'byte': 2, 'signed': True, 'read_value_transform': '/ 100' },
		'UTI': { 'unit_de': 'Temperatur 1Byte ganzzahlig', 'type': 'integer', 'byte': 1, 'signed': False, 'read_value_transform': 'non' },
		'VS': { 'unit_de': 'Volumenstrom', 'type': 'integer', 'byte': 2, 'signed': False, 'read_value_transform': 'non' },
    },
}
errorset = {
    'P300': {
        '00':  'Regelbetrieb (kein Fehler)',
        '0F':  'Wartung (fuer Reset Codieradresse 24 auf 0 stellen)',
        '10':  'Kurzschluss Aussentemperatursensor',
        '18':  'Unterbrechung Aussentemperatursensor',
        '20':  'Kurzschluss Vorlauftemperatursensor',
        '21':  'Kurzschluss Ruecklauftemperatursensor',
        '28':  'Unterbrechung Aussentemperatursensor',
        '29':  'Unterbrechung Ruecklauftemperatursensor',
        '30':  'Kurzschluss Kesseltemperatursensor',
        '38':  'Unterbrechung Kesseltemperatursensor',
        '40':  'Kurzschluss Vorlauftemperatursensor M2',
        '42':  'Unterbrechung Vorlauftemperatursensor M2',
        '50':  'Kurzschluss Speichertemperatursensor',
        '58':  'Unterbrechung Speichertemperatursensor',
        '92':  'Solar: Kurzschluss Kollektortemperatursensor',
        '93':  'Solar: Kurzschluss Sensor S3',
        '94':  'Solar: Kurzschluss Speichertemperatursensor',
        '9A':  'Solar: Unterbrechung Kollektortemperatursensor',
        '9B':  'Solar: Unterbrechung Sensor S3',
        '9C':  'Solar: Unterbrechung Speichertemperatursensor',
        '9E':  'Solar: Zu geringer bzw. kein Volumenstrom oder Temperaturwächter ausgeloest',
        '9F':  'Solar: Fehlermeldung Solarteil (siehe Solarregler)',
        'A7':  'Bedienteil defekt',
        'B0':  'Kurzschluss Abgastemperatursensor',
        'B1':  'Kommunikationsfehler Bedieneinheit',
        'B4':  'Interner Fehler (Elektronik)',
        'B5':  'Interner Fehler (Elektronik)',
        'B6':  'Ungueltige Hardwarekennung (Elektronik)',
        'B7':  'Interner Fehler (Kesselkodierstecker)',
        'B8':  'Unterbrechung Abgastemperatursensor',
        'B9':  'Interner Fehler (Dateneingabe wiederholen)',
        'BA':  'Kommunikationsfehler Erweiterungssatz fuer Mischerkreis M2',
        'BC':  'Kommunikationsfehler Fernbedienung Vitorol, Heizkreis M1',
        'BD':  'Kommunikationsfehler Fernbedienung Vitorol, Heizkreis M2',
        'BE':  'Falsche Codierung Fernbedienung Vitorol',
        'C1':  'Externe Sicherheitseinrichtung (Kessel kuehlt aus)',
        'C2':  'Kommunikationsfehler Solarregelung',
        'C5':  'Kommunikationsfehler drehzahlgeregelte Heizkreispumpe, Heizkreis M1',
        'C6':  'Kommunikationsfehler drehzahlgeregelte Heizkreispumpe, Heizkreis M2',
        'C7':  'Falsche Codierung der Heizkreispumpe',
        'C9':  'Stoermeldeeingang am Schaltmodul-V aktiv',
        'CD':  'Kommunikationsfehler Vitocom 100 (KM-BUS)',
        'CE':  'Kommunikationsfehler Schaltmodul-V',
        'CF':  'Kommunikationsfehler LON Modul',
        'D1':  'Brennerstoerung',
        'D4':  'Sicherheitstemperaturbegrenzer hat ausgeloest oder Stoermeldemodul nicht richtig gesteckt',
        'DA':  'Kurzschluss Raumtemperatursensor, Heizkreis M1',
        'DB':  'Kurzschluss Raumtemperatursensor, Heizkreis M2',
        'DD':  'Unterbrechung Raumtemperatursensor, Heizkreis M1',
        'DE':  'Unterbrechung Raumtemperatursensor, Heizkreis M2',
        'E4':  'Fehler Versorgungsspannung',
        'E5':  'Interner Fehler (Ionisationselektrode)',
        'E6':  'Abgas- / Zuluftsystem verstopft',
        'F0':  'Interner Fehler (Regelung tauschen)',
        'F1':  'Abgastemperaturbegrenzer ausgeloest',
        'F2':  'Temperaturbegrenzer ausgeloest',
        'F3':  'Flammensigal beim Brennerstart bereits vorhanden',
        'F4':  'Flammensigal nicht vorhanden',
        'F7':  'Differenzdrucksensor defekt',
        'F8':  'Brennstoffventil schliesst zu spaet',
        'F9':  'Geblaesedrehzahl beim Brennerstart zu niedrig',
        'FA':  'Geblaesestillstand nicht erreicht',
        'FD':  'Fehler Gasfeuerungsautomat',
        'FE':  'Starkes Stoerfeld (EMV) in der Naehe oder Elektronik defekt',
        'FF':  'Starkes Stoerfeld (EMV) in der Naehe oder interner Fehler',
     },
}

operatingmodes = {
    'V200KW2': {
        '0':    'Abschaltbetrieb',
        '1':    'Warmwasserbetrieb',
        '2':    'Heiz- und Warmwasserbetrieb',
        '3':    'Dauerbetrieb, reduziert',
        '4':    'Dauerbetrieb, normal',
	},
    'V200KO1B': {
        '00':    'Warmwasserbetrieb',
        '01':    'Dauerbetrieb, reduziert',
        '02':    'Dauerbetrieb, normal',
        '04':    'H+WW FS',
        '03':    'H+WW',
        '05':    'Abschaltbetrieb',
    },
}

systemschemes	 = {
    'V200KO1B': {
        '1':    'A1',
        '2':    'A1 + WW',
        '4':    'M2',
        '3':    'M2 + WW',
        '5':    'A1 + M2',
		'6':    'A1 + M2 + WW',
     },
}

devicetypes	 = {
    '2053012B': 			'V200WB2 ID=2053 Protokoll:GWG_VBEM',
	'2098':					'V200KW2 ID=2098 Protokoll:KW',
	'20CB034A0000010A':		'VScotHO1 ID=20CB Protokoll:KW,300',
	'2094':					'V200KW1 ID=2094 Protokoll:KW',
}

returnstatus	 = {
    'P300': {
        '00':    '0',
        '01':    '1',
        '03':    '2',
		'AA':	 'NOT OK',
		#At least for device 20CB the heating circuit pump returns status 03 when it's on and the heating runs in in night mode
     },
}

setreturnstatus	 = {
    'P300': {
        '00':    'OK',
        '05':    'SYNC (NOT OK)',
     },
}