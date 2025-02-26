# Ispmanager integration to Homeassistat
Simple custom integration for ispmanager in Homeassistant.

Based on the API request to the ispmanager server, two sensors are created - CPU usage and RAM usage.
For the integration to work, it is necessary to manually upload it ti custom_components/ispmanager and write in the configuration:
```
sensors:
 - platform: ispmanager
   host: "Server hostname or IP address"
   username: "root"
   password: "xxxxxxxxxxxxxx"
```
After that restart Homeassistant.
