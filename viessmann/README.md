# Viessmann

#### Version 1.6.0

The Viessmann plugin is designed to connect to a Viessmann heating systems via the Optolink USB adapter to read out and write its parameters.
Currently the P300 protocol and the V200KO1B,KO2B devices are supportet. Other protocols and devices can easily be added.
All details of devices and protocols can be read here: https://github.com/openv/openv/wiki/vcontrold

The Viessmann plugin uses a separate commands.py file which contains the different control- (control characters like start sequence, acknowledge etc.) and commandsets for the supported systems.

You can configure the plugin to connect by direct serial connection on the host system.

## Change history

None

## Requirements

This plugin has no requirements or dependencies.

### Needed software

* list
* the
* needed
* software

Including Python modules and SmartHomeNG modules

### Supported Hardware

* Optolink adapter (Viessmann original or DIY)

## Configuration

### plugin.yaml

```
comfoair:
    class_name: ComfoAir
    class_path: plugins.comfoair
    kwltype: comfoair350       # Currently supported: comfoair350 and comfoair500
    serialport: /dev/ttyUSB0  # Enable this if you want to use a serial connection
```


### items.yaml

The plugin is completely flexible in which commands you use and when you want the read out which parameters.
Everything is configured by adding new items in a SmartHomeNG item configuration file.

The following item attributes are supported:

#### viess_send

Changes to this item result in sending the configured command to the heating system.
The command is complemented by the item value in a pre-configured way (see commands.py).
Typically read and write command are identical. In case a items and read and send command, 
you just can use "True" instead of the command

The item just has a send command:
```yaml
viess_send: Raumtemperatur_Soll_Normalbetrieb_A1M1
```
The item has a read and send command:
```yaml
viess_send: True
```

#### viess_read

The item value should be read by using the configured command.

```yaml
viess_read: Raumtemperatur_Soll_Normalbetrieb_A1M1
```

#### viess_read_afterwrite

A timespan (seconds) can be configured. If a value for this attribute is set, the plugin will wait the configured delay after the write command and then issue the configured read command to update the items value.
This attribute has no default value. If the attribute is not set, no read will be issued after write.

```yaml
viess_read_afterwrite: 1 # seconds
```

#### viess_read_cycle

With this attribute a read cycle for this item can be configured (timespan between cycles in seconds).

```yaml
viess_read_cycle: 3600 # every hour
```

#### viess_init

If this attribute is set to a bool value (e.g. 'true'), the plugin will use the read command at startup to get an initial value.

```yaml
viess_init: true
```

#### viess_trigger

This attribute can contain a list of commands, which will be issued if the item is updated.
Useful for instance: If the ventilation level is changed, get updated ventilator RPM values.

```yaml
viess_trigger:
   - Betriebsart_A1M1
   - Sparbetrieb_A1M1
```

#### viess_trigger_afterwrite

A timespan (seconds) can be configured. After an update to this item, the commands configured in comfoair_trigger will be issued. Before triggering the here configured delay will be waited for.
Default value: 5 seconds.

```yaml
viess_trigger_afterwrite: 10 # seconds
```

#### Example

Here you can find a sample configuration using the commands for KO1B:

```yaml
kwl:
    level:
        type: num
        comfoair_send: WriteVentilationLevel
        comfoair_read: ReadCurrentVentilationLevel
        comfoair_read_afterwrite: 1 # seconds
        comfoair_trigger: ReadSupplyAirRPM
        comfoair_trigger_afterwrite: 6 # seconds
        comfoair_init: true
        sqlite: yes
    extractair:
        rpm:
            type: num
            comfoair_read: ReadExtractAirRPM
            comfoair_read_cycle: 60 # seconds
            comfoair_init: true
        level:
            type: num
            comfoair_read: ReadExtractAirPercentage
            comfoair_read_cycle: 60 # seconds
            comfoair_init: true
```


### logic.yaml
Currently there is no logic configuration for this plugin.


## Methods
Currently there are no functions offered from this plugin.


## Web Interfaces

For building a web interface for a plugin, we deliver the following 3rd party components with the HTTP module:

   * JQuery 3.4.1: 
     * JS: &lt;script src="/gstatic/js/jquery-3.4.1.min.js"&gt;&lt;/script&gt;
   * Bootstrap : 
     * CSS: &lt;link rel="stylesheet" href="/gstatic/bootstrap/css/bootstrap.min.css" type="text/css"/&gt; 
     * JS: &lt;script src="/gstatic/bootstrap/js/bootstrap.min.js"&gt;&lt;/script&gt;     
   * Bootstrap Tree View: 
      * CSS: &lt;link rel="stylesheet" href="/gstatic/bootstrap-treeview/bootstrap-treeview.css" type="text/css"/&gt; 
      * JS: &lt;script src="/gstatic/bootstrap-treeview/bootstrap-treeview.min.js"&gt;&lt;/script&gt;
   * Bootstrap Datepicker v1.8.0:
      * CSS: &lt;link rel="stylesheet" href="/gstatic/bootstrap-datepicker/dist/css/bootstrap-datepicker.min.css" type="text/css"/&gt;
      * JS:
         * &lt;script src="/gstatic/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js"&gt;&lt;/script&gt;
         * &lt;script src="/gstatic/bootstrap-datepicker/dist/locales/bootstrap-datepicker.de.min.js"&gt;&lt;/script&gt;
   * popper.js: 
      * JS: &lt;script src="/gstatic/popper.js/popper.min.js"&gt;&lt;/script&gt;
   * CodeMirror 5.46.0: 
      * CSS: &lt;link rel="stylesheet" href="/gstatic/codemirror/lib/codemirror.css"/&gt;
      * JS: &lt;script src="/gstatic/codemirror/lib/codemirror.js"&gt;&lt;/script&gt;
   * Font Awesome 5.8.1:
      * CSS: &lt;link rel="stylesheet" href="/gstatic/fontawesome/css/all.css" type="text/css"/&gt;

 For addons, etc. that are delivered with the components, see /modules/http/webif/gstatic folder!
 
 If you are interested in new "global" components, contact us. Otherwise feel free to use them in your plugin, as long as
 the Open Source license is ok.
 