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
        'Baudrate':  4800,
        'Bytesize':  'serial.EIGHTBITS',
        'Parity':    'serial.PARITY_EVEN',
        'Stopbits':  'serial.STOPBITS_TWO',
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
        'Command_bytes_read':   5,
        'Command_bytes_write':  5,
        #init:              send'Reset_Command' receive'Reset_Command_Response' send'Sync_Command'
        #request:           send('StartByte' 'Länge der Nutzdaten als Anzahl der Bytes zwischen diesem Byte und der Prüfsumme' 'Request' 'Read' 'addr' 'checksum')
        #request_response:  receive('Acknowledge' 'StartByte' 'Länge der Nutzdaten als Anzahl der Bytes zwischen diesem Byte und der Prüfsumme' 'Response' 'Read' 'addr' 'Anzahl der Bytes des Wertes' 'Wert' 'checksum')
    },
    'KW': {
        'StartByte': 0x01,
        'Read': 0xF7,
        'Write': 0xF4,
        'Acknowledge': 0x05,
    },
    
}
    
commandset = {
    'V200KO1B': {
        # Kessel
        'Aussentemperatur':         { 'addr': '0800', 'len': 2, 'unit': 'UT',   'set': False }, #Aussentemperatur
        'Aussentemperatur_TP':      { 'addr': '5525', 'len': 2, 'unit': 'UT',   'set': False }, #Aussentemperatur_tiefpass
        'Aussentemperatur_Dp':      { 'addr': '5527', 'len': 2, 'unit': 'UT',   'set': False }, #Aussentemperatur in Grad C (Gedaempft)
        'Kesseltemperatur':         { 'addr': '0802', 'len': 2, 'unit': 'UT',   'set': False }, #Kesseltemperatur
        'Kesseltemperatur_TP':      { 'addr': '0810', 'len': 2, 'unit': 'UT',   'set': False }, #Kesseltemperatur_tiefpass
        'Kesselsolltemperatur':     { 'addr': '555A', 'len': 2, 'unit': 'UT',   'set': False }, #Kesselsolltemperatur
        'Temp_Speicher_Ladesensor': { 'addr': '0812', 'len': 2, 'unit': 'UT',   'set': False }, #Temperatur Speicher Ladesensor Komfortsensor
        'Auslauftemperatur':        { 'addr': '0814', 'len': 2, 'unit': 'UT',   'set': False }, #Auslauftemperatur
        'Abgastemperatur':          { 'addr': '0816', 'len': 2, 'unit': 'UT',   'set': False }, #Abgastemperatur
        'Gem_Vorlauftemperatur':    { 'addr': '081a', 'len': 2, 'unit': 'UT',   'set': False }, #Gem. Vorlauftemperatur
        'Relais_K12':               { 'addr': '0842', 'len': 1, 'unit': 'BST',  'set': False }, #Relais K12 Interne Anschlußerweiterung
        'Eingang_0-10_V':           { 'addr': '0a86', 'len': 1, 'unit': 'ST',   'set': False }, #Eingang 0-10 V
        'EA1_Kontakt_0':            { 'addr': '0a90', 'len': 1, 'unit': 'BST',  'set': False }, #EA1: Kontakt 0
        'EA1_Kontakt_1':            { 'addr': '0a91', 'len': 1, 'unit': 'BST',  'set': False }, #EA1: Kontakt 1
        'EA1_Kontakt_2':            { 'addr': '0a92', 'len': 1, 'unit': 'BST',  'set': False }, #EA1: Kontakt 2
        'EA1_Externer_Soll_0-10V':  { 'addr': '0a93', 'len': 1, 'unit': 'ST',   'set': False }, #EA1: Externer Sollwert 0-10V
        'EA1_Relais_0':             { 'addr': '0a95', 'len': 1, 'unit': 'BST',  'set': False }, #EA1: Relais 0
        'AM1_Ausgang_1':            { 'addr': '0aa0', 'len': 1, 'unit': 'BST',  'set': False }, #AM1 Ausgang 1
        'AM1_Ausgang_2':            { 'addr': '0aa1', 'len': 1, 'unit': 'BST',  'set': False }, #AM1 Ausgang 2
        'TempKOffset':              { 'addr': '6760', 'len': 1, 'unit': 'UTI',  'set': True,  'min_value': 0, 'max_value': 1193045 }, #Kesseloffset KT ueber WWsoll in Grad C
        'Systemtime':               { 'addr': '088E', 'len': 8, 'unit': 'TI',   'set': True,  'min_value': 0, 'max_value': 1193045 }, #Systemzeit
        
        'KA5_M2':                   { 'addr': '37A5', 'len': 1, 'unit': 'UTI',  'set': True,  'min_value': 0, 'max_value': 1193045 }, #HeizkreispumpenlogikFunktion M2 <!-- A5:0 Ohne Heizkreispumpenlogik-Funktion | Heizkreispumpe aus, wenn A5:1 AT > RTSoll + 5 K A5:2 AT > RTSoll + 4 K A5:3  AT > RTSoll + 3 K A5:4 AT > RTSoll + 2 K A5:5 AT > RTSoll + 1 K A5:6 AT = RTSoll A5:7 AT > RTSoll -1 K bis A5:15 AT > RTSoll -9 K -->
        
        'KA6_M2':                   { 'addr': '37A6', 'len': 1, 'unit': 'UTI',  'set': True,  'min_value': 0, 'max_value': 1193045 }, #AbsolutSommersparschaltung M2 
        
        'KA3_M2':                   { 'addr': '37A3', 'len': 1, 'unit': 'UTI',  'set': True,  'min_value': 0, 'max_value': 1193045 }, #Frostschutzgrenze M2 <!-- Range GradCelsius SByte 1 -9 15 -->
        'Anlagenschema':            { 'addr': '7700', 'len': 2, 'unit': 'SC',   'set': False}, #Anlagenschema
        'DevType':                  { 'addr': '00F8', 'len': 8, 'unit': 'DT',   'set': False}, #Heizungstyp
        'Inventory':                { 'addr': '08E0', 'len': 7, 'unit': 'SN',   'set': False}, #Sachnummer
        'CtrlId':                   { 'addr': '08E0', 'len': 7, 'unit': 'DT',   'set': False}, #Reglerkennung
        #Fehler
        'Sammelstoerung':           { 'addr': '0a82', 'len': 1, 'unit': 'RT', 'set': False }, #Sammelstörung
        'Error0':                   { 'addr': '7507', 'len': 9, 'unit': 'ES', 'set': False }, #Fehlerhistory Eintrag 1
        'Error1':                   { 'addr': '7510', 'len': 9, 'unit': 'ES', 'set': False }, #Fehlerhistory Eintrag 2
        'Error2':                   { 'addr': '7519', 'len': 9, 'unit': 'ES', 'set': False }, #Fehlerhistory Eintrag 3
        'Error3':                   { 'addr': '7522', 'len': 9, 'unit': 'ES', 'set': False }, #Fehlerhistory Eintrag 4
        'Error4':                   { 'addr': '752B', 'len': 9, 'unit': 'ES', 'set': False }, #Fehlerhistory Eintrag 5
        'Error5':                   { 'addr': '7534', 'len': 9, 'unit': 'ES', 'set': False }, #Fehlerhistory Eintrag 6
        'Error6':                   { 'addr': '753D', 'len': 9, 'unit': 'ES', 'set': False }, #Fehlerhistory Eintrag 7
        'Error7':                   { 'addr': '7546', 'len': 9, 'unit': 'ES', 'set': False }, #Fehlerhistory Eintrag 8
        'Error8':                   { 'addr': '754F', 'len': 9, 'unit': 'ES', 'set': False }, #Fehlerhistory Eintrag 9
        'Error9':                   { 'addr': '7558', 'len': 9, 'unit': 'ES', 'set': False }, #Fehlerhistory Eintrag 10
        #Pumpen
        'Speicherladepumpe':        { 'addr': '6513', 'len': 1, 'unit': 'BST', 'set': False }, #Speicherladepumpe
        'Zirkulationspumpe':        { 'addr': '6515', 'len': 1, 'unit': 'BST', 'set': False }, #Zirkulationspumpe
        'Interne_Pumpe':            { 'addr': '7660', 'len': 1, 'unit': 'BST', 'set': False }, #Interne Pumpe
        'Heizkreispumpe_A1M1':      { 'addr': '7663', 'len': 1, 'unit': 'BST', 'set': False }, #Heizkreispumpe A1
        'Heizkreispumpe_A1M1_RPM':  { 'addr': '7663', 'len': 1, 'unit': 'PR2', 'set': False }, #Heizkreispumpe A1M1 Drehzahl
        'Heizkreispumpe_M2_RPM':    { 'addr': '7665', 'len': 1, 'unit': 'PR2', 'set': False }, #Heizkreispumpe Drehzahl
        'Relais_Status_Pumpe_A1M1': { 'addr': 'a152', 'len': 1, 'unit': 'BST', 'set': False }, #Relais-Status Heizkreispumpe 1
        # Brenner
        'Brennerstarts':                { 'addr': '088a', 'len': 4, 'unit': 'CO',  'set': True,  'min_value': 0, 'max_value': 1193045 }, #Brennerstarts
        'Brenner_Betriebsstunden':      { 'addr': '08a7', 'len': 4, 'unit': 'CS',  'set': True,  'min_value': 0, 'max_value': 1193045 }, #Brenner-Betriebsstunden
        'Brennerstatus_1':              { 'addr': '0842', 'len': 1, 'unit': 'BST', 'set': False }, #Brennerstatus Stufe1
        'Brennerstatus_2':              { 'addr': '0849', 'len': 1, 'unit': 'BST', 'set': False }, #Brennerstatus Stufe2
        'Oeldurchsatz':                 { 'addr': '5726', 'len': 4, 'unit': 'CO',  'set': True,  'min_value': 0, 'max_value': 1193045  }, #Oeldurchsatz Brenner in Dezi-Liter pro Stunde
        'Oelverbrauch':                 { 'addr': '7574', 'len': 4, 'unit': 'COL', 'set': False }, #Oelverbrauch kumuliert
        # Heizkreis A1M1
        'Raumtemperatur_A1M1':                     { 'addr': '0896', 'len': 1, 'unit': 'UTI', 'set': False }, #Raumtemperatur A1M1
        'Raumtemperatur_Soll_Normalbetrieb_A1M1':  { 'addr': '2306', 'len': 1, 'unit': 'UTI', 'set': True,  'min_value': 3, 'max_value': 37 }, #Raumtemperatur Soll Normalbetrieb A1M1
        'Raumtemperatur_Soll_Red_Betrieb_A1M1':    { 'addr': '2307', 'len': 1, 'unit': 'UTI', 'set': True,  'min_value': 3, 'max_value': 37 }, #Raumtemperatur Soll Reduzierter Betrieb A1M1
        'Raumtemperatur_Soll_Party_Betrieb_A1M1':  { 'addr': '2308', 'len': 1, 'unit': 'UTI', 'set': True,  'min_value': 3, 'max_value': 37 }, #Raumtemperatur Soll Party Betrieb A1M1
        'Aktuelle_Betriebsart_A1M1':               { 'addr': '2301', 'len': 1, 'unit': 'BA',  'set': False }, #Aktuelle Betriebsart A1M1
        'Betriebsart_A1M1':                        { 'addr': '2323', 'len': 1, 'unit': 'ST',  'set': True,  'min_value': 0, 'max_value': 4 }, #Betriebsart A1M1
        'Sparbetrieb_A1M1':                        { 'addr': '2302', 'len': 1, 'unit': 'BST', 'set': True,  'min_value': 0, 'max_value': 1 }, #Sparbetrieb A1M1
        'Zustand_Sparbetrieb_A1M1':                { 'addr': '2331', 'len': 1, 'unit': 'ST',  'set': False }, #Zustand Sparbetrieb A1M1
        'Partybetrieb_A1M1':                       { 'addr': '2303', 'len': 1, 'unit': 'BST', 'set': True,  'min_value': 0, 'max_value': 1 }, #Partybetrieb A1M1
        'Zustand_Partybetrieb_A1M1':               { 'addr': '2330', 'len': 1, 'unit': 'ST',  'set': False }, #Zustand Partybetrieb A1M1
        'Vorlauftemperatur_A1M1':                  { 'addr': '2900', 'len': 2, 'unit': 'UT',  'set': False }, #Vorlauftemperatur A1M1
        'Vorlauftemperatur_Soll_A1M1':             { 'addr': '2544', 'len': 2, 'unit': 'UT',  'set': False }, #Vorlauftemperatur Soll A1M1
        'StatusFrost_A1M1':                        { 'addr': '2500', 'len': 1, 'unit': 'BST', 'set': False }, #Status Frostwarnung A1M1
        'Neigung_Heizkennlinie_A1M1':              { 'addr': '27D3', 'len': 1, 'unit': 'UN',  'set': True,  'min_value': 0.2, 'max_value': 3.5 }, #Neigung Heizkennlinie A1M1
        'Niveau_Heizkennlinie_A1M1':               { 'addr': '27d4', 'len': 1, 'unit': 'ST',  'set': True,  'min_value': -13, 'max_value': 40 }, #Niveau Heizkennlinie A1M1
        'Heizkreispumpe_A1M1':                     { 'addr': '2906', 'len': 1, 'unit': 'ST',  'set': False }, #Heizkreispumpe A1M1
        'Externe_Raumsolltemperatur_Normal_A1M1':  { 'addr': '2321', 'len': 1, 'unit': 'UTI', 'set': True,  'min_value': 0, 'max_value': 37 }, #Externe Raumsolltemperatur Normal A1M1
        'Externe_Betriebsartenumschaltung_A1M1':   { 'addr': '2549', 'len': 1, 'unit': 'ST',  'set': True,  'min_value': 0, 'max_value': 4 }, #Externe Betriebsartenumschaltung A1M1
        'KA3_A1M1':                                { 'addr': '27A3', 'len': 1, 'unit': 'UTI', 'set': True,  'min_value': 0, 'max_value': 1193045 }, #Frostschutzgrenze A1M1 <!-- Range GradCelsius SByte 1 -9 15 -->
        'KA5_A1M1':                                { 'addr': '27A5', 'len': 1, 'unit': 'UTI', 'set': True,  'min_value': 0, 'max_value': 1193045 }, #HeizkreispumpenlogikFunktion A1M1 <!-- A5:0 Ohne Heizkreispumpenlogik-Funktion | Heizkreispumpe aus, wenn A5:1 AT > RTSoll + 5 K A5:2 AT > RTSoll + 4 K A5:3  AT > RTSoll + 3 K A5:4 AT > RTSoll + 2 K A5:5 AT > RTSoll + 1 K A5:6 AT = RTSoll A5:7 AT > RTSoll -1 K bis A5:15 AT > RTSoll -9 K -->
        'KA6_A1M1':                                { 'addr': '27A6', 'len': 1, 'unit': 'UTI', 'set': True,  'min_value': 0, 'max_value': 1193045 }, #AbsolutSommersparschaltung A1M1
        
        
        
        # Heizkreis M2
        'Raumtemperatur_M2':                       { 'addr': '0898', 'len': 1, 'unit': 'UTI', 'set': False }, #Raumtemperatur M2
        'Raumtemperatur_Soll_Normalbetrieb_M2':    { 'addr': '3306', 'len': 1, 'unit': 'UTI', 'set': True,  'min_value': 3, 'max_value': 37 }, #Raumtemperatur Soll Normalbetrieb M2
        'Raumtemperatur_Soll_Red_Betrieb_M2':      { 'addr': '3307', 'len': 1, 'unit': 'UTI', 'set': True,  'min_value': 3, 'max_value': 37 }, #Raumtemperatur Soll Reduzierter Betrieb M2
        'Raumtemperatur_Soll_Party_Betrieb_M2':    { 'addr': '3308', 'len': 1, 'unit': 'UTI', 'set': True,  'min_value': 3, 'max_value': 37 }, #Raumtemperatur Soll Party Betrieb M2
        'Aktuelle_Betriebsart_M2':                 { 'addr': '3301', 'len': 1, 'unit': 'BA',  'set': False }, #Aktuelle Betriebsart M2
        'Betriebsart_M2':                          { 'addr': '3323', 'len': 1, 'unit': 'ST',  'set': True,  'min_value': 0, 'max_value': 4 }, #Betriebsart M2
        'Sparbetrieb_M2':                          { 'addr': '3302', 'len': 1, 'unit': 'BST', 'set': True,  'min_value': 0, 'max_value': 1 }, #Sparbetrieb M2
        'Zustand_Sparbetrieb_M2':                  { 'addr': '3331', 'len': 1, 'unit': 'ST',  'set': False }, #Zustand Sparbetrieb M2
        'Partybetrieb_M2':                         { 'addr': '3303', 'len': 1, 'unit': 'BST', 'set': True,  'min_value': 0, 'max_value': 1 }, #Partybetrieb M2
        'Zustand_Partybetrieb_M2':                 { 'addr': '3330', 'len': 1, 'unit': 'ST',  'set': False }, #Zustand Partybetrieb M2
        'Vorlauftemperatur_M2':                    { 'addr': '3900', 'len': 2, 'unit': 'UT',  'set': False }, #Vorlauftemperatur M2
        'Vorlauftemperatur_Soll_M2':               { 'addr': '3544', 'len': 2, 'unit': 'UT',  'set': False }, #Vorlauftemperatur Soll M2
        'StatusFrost_M2':                          { 'addr': '3500', 'len': 1, 'unit': 'BST', 'set': False }, #Status Frostwarnung M2
        'Neigung_Heizkennlinie_M2':                { 'addr': '37d3', 'len': 1, 'unit': 'UN',  'set': True,  'min_value': 0.2, 'max_value': 3.5 }, #Neigung Heizkennlinie M2
        'Niveau_Heizkennlinie_M2':                 { 'addr': '37d4', 'len': 1, 'unit': 'ST',  'set': True,  'min_value': -13, 'max_value': 40 }, #Niveau Heizkennlinie M2
        'Heizkreispumpe_M2':                       { 'addr': '3906', 'len': 1, 'unit': 'ST',  'set': False }, #Heizkreispumpe M2
        'Externe_Raumsolltemperatur_Normal_M2':    { 'addr': '3321', 'len': 1, 'unit': 'UTI', 'set': True,  'min_value': 0, 'max_value': 37 }, #Externe Raumsolltemperatur Normal M2
        'Externe_Betriebsartenumschaltung_M2':     { 'addr': '3549', 'len': 1, 'unit': 'ST',  'set': True,  'min_value': 0, 'max_value': 4 }, #Externe Betriebsartenumschaltung M2
         # Warmwasser
        'Warmwasser_Temperatur':     { 'addr': '0804', 'len': 2, 'unit': 'UT', 'set': False }, #Warmwassertemperatur in Grad C
        'Warmwasser_Solltemperatur': { 'addr': '6300', 'len': 1, 'unit': 'UTI',  'set': True,  'min_value': 10, 'max_value': 95 }, #Warmwasser-Solltemperatur
        'Satus_Warmwasserbereitung': { 'addr': '650a', 'len': 1, 'unit': 'BST',  'set': True,  'min_value': 0, 'max_value': 1 }, #Satus Warmwasserbereitung
        'WarmwasserPumpenNachlauf':  { 'addr': '6762', 'len': 2, 'unit': 'CO' ,  'set': True,  'min_value': 0, 'max_value': 1}, #Warmwasserpumpennachlauf
        'Speichervorrang_A1M1':      { 'addr': '27A2', 'len': 1, 'unit': 'ST',   'set': True,  'min_value': 0, 'max_value': 4 }, #Speichervorrang Heizkreis ohne Mischer A1
        'Speichervorrang_M2':        { 'addr': '37A2', 'len': 1, 'unit': 'ST',   'set': True,  'min_value': 0, 'max_value': 4 }, #Speichervorrang Heizkreis M2
        # Ferienprogramm HK_A1M1
        'Ferienprogramm_A1M1':       { 'addr': '2535', 'len': 1, 'unit': 'BST',  'set': True }, #Ferienprogramm A1M1
        'Ferien_Abreisetag_A1M1':    { 'addr': '2309', 'len': 8, 'unit': 'TI',   'set': True }, #Ferien Abreisetag A1M1
        'Ferien_Rückreisetag_A1M1':  { 'addr': '2311', 'len': 8, 'unit': 'TI',   'set': True }, #Ferien Rückreisetag A1M1
        # Ferienprogramm HK_M2
        'Ferienprogramm_M2':         { 'addr': '3535', 'len': 1, 'unit': 'BST',  'set': True }, #Ferienprogramm M2
        'Ferien_Abreisetag_M2':      { 'addr': '3309', 'len': 8, 'unit': 'TI',   'set': True }, #Ferien Abreisetag M2
        'Ferien_Rückreisetag_M2':    { 'addr': '3311', 'len': 8, 'unit': 'TI',   'set': True }, #Ferien Rückreisetag M2
        # Schaltzeiten Warmwasser
        'Timer_Warmwasser_Mo': { 'addr': '2100', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Warmwasserbereitung Montag
        'Timer_Warmwasser_Di': { 'addr': '2108', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Warmwasserbereitung Dienstag
        'Timer_Warmwasser_Mi': { 'addr': '2110', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Warmwasserbereitung Mittwoch
        'Timer_Warmwasser_Do': { 'addr': '2118', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Warmwasserbereitung Donnerstag
        'Timer_Warmwasser_Fr': { 'addr': '2120', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Warmwasserbereitung Freitag
        'Timer_Warmwasser_Sa': { 'addr': '2128', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Warmwasserbereitung Samstag
        'Timer_Warmwasser_So': { 'addr': '2130', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Warmwasserbereitung Sonntag        
        # Schaltzeiten HK_A1M1
        'Timer_A1M1_Mo':       { 'addr': '2000', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Montag
        'Timer_A1M1_Di':       { 'addr': '2008', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Dienstag
        'Timer_A1M1_Mi':       { 'addr': '2010', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Mittwoch
        'Timer_A1M1_Do':       { 'addr': '2018', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Donnerstag
        'Timer_A1M1_Fr':       { 'addr': '2020', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Freitag
        'Timer_A1M1_Sa':       { 'addr': '2028', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Samstag
        'Timer_A1M1_So':       { 'addr': '2030', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Sonntag
        # Schaltzeiten HK_M2
        'Timer_M2_Mo':         { 'addr': '3000', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Montag
        'Timer_M2_Di':         { 'addr': '3008', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Dienstag
        'Timer_M2_Mi':         { 'addr': '3010', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Mittwoch
        'Timer_M2_Do':         { 'addr': '3018', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Donnerstag
        'Timer_M2_Fr':         { 'addr': '3020', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Freitag
        'Timer_M2_Sa':         { 'addr': '3028', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Samstag
        'Timer_M2_So':         { 'addr': '3030', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Heizkreis_A1M1 Sonntag
        # Schaltzeiten Zirkulation
        'Timer_Zirku_Mo':      { 'addr': '2200', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Zirkulationspumpe Montag
        'Timer_Zirku_Di':      { 'addr': '2208', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Zirkulationspumpe Dienstag
        'Timer_Zirku_Mi':      { 'addr': '2210', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Zirkulationspumpe Mittwoch
        'Timer_Zirku_Do':      { 'addr': '2218', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Zirkulationspumpe Donnerstag
        'Timer_Zirku_Fr':      { 'addr': '2220', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Zirkulationspumpe Freitag
        'Timer_Zirku_Sa':      { 'addr': '2228', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Zirkulationspumpe Samstag
        'Timer_Zirku_So':      { 'addr': '2230', 'len': 8, 'unit': 'CT',  'set': True }, #Timer Zirkulationspumpe Sonntag
    },
}

unitset = {
    'P300': {
		'BA':   { 'unit_de': 'Betriebsart',                                 'type': 'list',     'byte': 1, 'signed': False, 'read_value_transform': 'non' },   #if
		'BH':   { 'unit_de': 'Brennerstunden',                              'type': 'integer',  'byte': 4, 'signed': True,  'read_value_transform': 'non' },
		'BST':  { 'unit_de': 'Bitstatus',                                   'type': 'integer',  'byte': 1, 'signed': False, 'read_value_transform': 'bool' },
		'CO':   { 'unit_de': 'Counter',                                     'type': 'integer',  'byte': 4, 'signed': True,  'read_value_transform': 'non' },
		'COL':  { 'unit_de': 'Counter liter',                               'type': 'integer',  'byte': 4, 'signed': True,  'read_value_transform': '1000' },
		'CS':   { 'unit_de': 'CounterS',                                    'type': 'integer',  'byte': 4, 'signed': False, 'read_value_transform': '3600' },
		'CT':   { 'unit_de': 'CycleTime',                                   'type': 'timer',    'byte': 8, 'signed': False, 'read_value_transform': 'non' },    #if
		'DT':   { 'unit_de': 'DeviceType',                                  'type': 'list',     'byte': 8, 'signed': False, 'read_value_transform': 'non' },    #if
		'ES':   { 'unit_de': 'ErrorState',                                  'type': 'list',     'byte': 9, 'signed': False, 'read_value_transform': 'non' },    #if
		#'ESG': { 'unit_de': 'ErrorStateGWG',                               'type': '',         'byte': 4, 'signed': False, 'read_value_transform': 'non' },
		#'HKT': { 'unit_de': 'HKP Pumpentyp',                               'type': '',         'byte': 4, 'signed': False, 'read_value_transform': 'non' },
		'PR':   { 'unit_de': 'Prozent',                                     'type': 'integer',  'byte': 2, 'signed': False, 'read_value_transform': '2' },
		'PR1':  { 'unit_de': 'Prozent 1 Byte ganzzahlig',                   'type': 'integer',  'byte': 1, 'signed': False, 'read_value_transform': 'non' },
		'PR2':  { 'unit_de': 'Prozent zweites Byte ganzzahlig (Pumpe)',     'type': 'integer',  'byte': 1, 'signed': False, 'read_value_transform': 'non' },
		'PR3':  { 'unit_de': 'Prozent erstes Byte',                         'type': 'integer',  'byte': 1, 'signed': False, 'read_value_transform': '2' },
		'RT':   { 'unit_de': 'ReturnStatus',                                'type': 'list',     'byte': 1, 'signed': False, 'read_value_transform': 'non' },    #if
        'SC':   { 'unit_de': 'SystemScheme',                                'type': 'list',     'byte': 1, 'signed': False, 'read_value_transform': 'non' },    #if
		'SN':   { 'unit_de': 'Sachnummer',                                  'type': 'serial',   'byte': 7, 'signed': False, 'read_value_transform': 'non' },    #if
		'SR':   { 'unit_de': 'SetReturnStatus',                             'type': 'list',     'byte': 1, 'signed': False, 'read_value_transform': 'non' },    #if
		'ST':   { 'unit_de': 'Status',                                      'type': 'integer',  'byte': 1, 'signed': False, 'read_value_transform': 'int' },
		'TI':   { 'unit_de': 'SystemTime',                                  'type': 'datetime', 'byte': 8, 'signed': False, 'read_value_transform': 'non' },    #if
		'UN':   { 'unit_de': 'Neigung',                                     'type': 'integer',  'byte': 2, 'signed': False, 'read_value_transform': '10' },
		'USV':  { 'unit_de': 'Umschaltventil Stellung',                     'type': 'integer',  'byte': 4, 'signed': False, 'read_value_transform': 'non' },
		'UT':   { 'unit_de': 'Temperatur',                                  'type': 'integer',  'byte': 2, 'signed': False, 'read_value_transform': '10' },
		'UT1':  { 'unit_de': 'Temperatur 1Byte',                            'type': 'integer',  'byte': 1, 'signed': False, 'read_value_transform': '2' },
		'UT1U': { 'unit_de': 'Temperatur 1Byte unsigned',                   'type': 'integer',  'byte': 1, 'signed': False, 'read_value_transform': '2' },
		'UTH':  { 'unit_de': 'Temperatur100',                               'type': 'integer',  'byte': 2, 'signed': True,  'read_value_transform': '100' },
		'UTI':  { 'unit_de': 'Temperatur 1Byte ganzzahlig',                 'type': 'integer',  'byte': 1, 'signed': False, 'read_value_transform': 'non' },
		'VS':   { 'unit_de': 'Volumenstrom',                                'type': 'integer',  'byte': 2, 'signed': False, 'read_value_transform': 'non' },
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
    'akteulle_Betriebsart': {
        '00':   'Abschaltbetrieb',
        '01':   'Reduzierter Betrieb',
        '02':   'Normalbetrieb',
        '03':   'Dauernd Normalbetrieb',
    },
}

systemschemes	 = {
    'V200KO1B': {
        '01':    'A1',
        '02':    'A1 + WW',
        '04':    'M2',
        '03':    'M2 + WW',
        '05':    'A1 + M2',
		'06':    'A1 + M2 + WW',
     },
}

devicetypes	 = {
    '2098':   'V200KW2, Protokoll: KW2' ,
    '2053':   'GWG_VBEM, Protokoll: GWG' ,
    '20CB':   'VScotHO1, Protokoll: P300' ,
    '2094':   'V200KW1, Protokoll: KW2' ,
    '209F':   'V200KO1B, Protokoll: P300, KW2' ,
    '204D':   'Vitocal200S, Protokoll: ' ,
    '20B8':   'V333MW1, Protokoll: ' ,
    '20A0':   'V100GC1, Protokoll: ' ,
    '20C2':   'VDensHO1, Protokoll: ' ,
    '20A4':   'V200GW1, Protokoll: ' ,
    '20C8':   'VPlusHO1, Protokoll: ' ,
    '2046':   'V200WO1,VBC700, Protokoll: ' ,
    '2047':   'V200WO1,VBC700, Protokoll: ' ,
    '2049':   'V200WO1,VBC700, Protokoll: ' ,
    '2032':   'VBC550, Protokoll: ' ,
    '2033':   'VBC550, Protokoll: ' ,
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
#P300 Protokoll
    # Beispiel
    #
    # Senden        41 5 0 1 55 25 2 82
    # Read Request  -- - - - ----- - --
    #                | | | |   |   |  +------- Prüfsumme (Summe über alley Bytes ohne die 41; [hex]5+0+1+55+25+2 = [dez]5+0+1+(5x16)+5+(2x16)+5+2 = 130dez = 82hex
    #                | | | |   |   +---------- XX Anzahl der Bytes, die in der Antwort erwartet werden
    #                | | | |   +-------------- XX XX 2 byte Adresse der Daten oder Prozedur
    #                | | | +------------------ XX 01 = ReadData, 02 = WriteData, 07 = Function Call
    #                | | +-------------------- XX 00 = Anfrage, 01 = Antwort, 03 = Fehler
    #                | +---------------------- Länge der Nutzdaten (Anzahl der Bytes zwischen dem Telegramm-Start-Byte (0x41) und der Prüfsumme)
    #                +------------------------ Telegramm-Start-Byte
    #
    # Empfangen   :  6 ----------------------- OK (Antwort auf 0x16 0x00 0x00 und auf korrekt empfangene Telegramme)                        
    #                5 ----------------------- Schnittstelle ist aktiv und wartet auf eine Initialisierung
    #               15 ----------------------- Schnittstelle meldet einen Fehler zurück
    #
    #               41 7 1 1 55 25 2 EF 0 74
    #               -- - - - ----- - ---- --
    #                | | | |   |   |   |   +-- Prüfsumme (Summe über alley Bytes ohne die 41; [hex]7+1+1+55+25+2+EF+0 = [dez]7+1+1+(5x16)+5+(2x16)+5+2+(14*16)+(15*16)+0 = [dez]7+1+1+(80)+5+(32)+5+2+(224)+(15)+0 = 372dez = 1.74hex)
    #                | | | |   |   |   +------ Wert
    #                | | | |   |   +---------- XX Anzahl der Bytes, die in der Antwort erwartet werden
    #                | | | |   +-------------- XX XX 2 byte Adresse der Daten oder Prozedur
    #                | | | +------------------ XX 01 = ReadData, 02 = WriteData, 07 = Function Call
    #                | | +-------------------- XX 00 = Anfrage, 01 = Antwort, 03 = Fehler
    #                | +---------------------- Länge der Nutzdaten (Anzahl der Bytes zwischen dem Telegramm-Start-Byte (0x41) und der Prüfsumme)
    #                +------------------------ Telegramm-Start-Byte

# Kommunikationsbeispiele
    # Information Kessel Außentemperatur read 2-Byte -60..60 0x5525
    # DATA TX: 41 5 0 1 55 25 2 82
    # DATA RX: 41 7 1 1 55 25 2 EF 0 74 --> 00EF = 239 --> 23.9°C (Faktor 0.1)
    # --> Senden   41 5 0 1 55 25 2 82
    #              -- - - - ----- - --
    #               | | | |   |   |  +-- Prüfsumme (Summe über alley Bytes ohne die 41; [hex]5+0+1+55+25+2 = [dez]5+0+1+(5x16)+5+(2x16)+5+2 = 130dez = 82hex
    #               | | | |   |   +----- XX Anzahl der Bytes, die in der Antwort erwartet werden
    #               | | | |   +--------- XX XX 2 byte Adresse der Daten oder Prozedur
    #               | | | +------------- XX 01 = ReadData, 02 = WriteData, 07 = Function Call
    #               | | +--------------- XX 00 = Anfrage, 01 = Antwort, 03 = Fehler
    #               | +----------------- Länge der Nutzdaten (Anzahl der Bytes zwischen dem Telegramm-Start-Byte (0x41) und der Prüfsumme)
    #               +------------------- Telegramm-Start-Byte
    #
    # --> Empfangen 6 41 7 1 1 55 25 2 EF 0 74
    #               - -- - - - ----- - ---- --
    #               |  | | | |   |   |   |   +-- Prüfsumme (Summe über alley Bytes ohne die 41; [hex]7+1+1+55+25+2+EF+0 = [dez]7+1+1+(5x16)+5+(2x16)+5+2+(14*16)+(15*16)+0 = [dez]7+1+1+(80)+5+(32)+5+2+(224)+(15)+0 = 372dez = 1.74hex)
    #               |  | | | |   |   |   +------ Wert
    #               |  | | | |   |   +---------- XX Anzahl der Bytes, die in der Antwort erwartet werden
    #               |  | | | |   +-------------- XX XX 2 byte Adresse der Daten oder Prozedur
    #               |  | | | +------------------ XX 01 = ReadData, 02 = WriteData, 07 = Function Call
    #               |  | | +-------------------- XX 00 = Anfrage, 01 = Antwort, 03 = Fehler
    #               |  | +---------------------- Länge der Nutzdaten (Anzahl der Bytes zwischen dem Telegramm-Start-Byte (0x41) und der Prüfsumme)
    #               |  +------------------------ Telegramm-Start-Byte
    #               +--------------------------- OK (Antwort auf 0x16 0x00 0x00 und auf korrekt empfangene Telegramme)
    #
    # --> Antwort: 0x00EF = 239 = 23.9°