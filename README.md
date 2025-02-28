# Ispmanager integration to Homeassistat

Simple custom integration for [ispmanager](https://ispmanager.com) in Home Assistant.

This integration retrieves data from the ispmanager server using API requests to create two sensors: CPU load and RAM usage. Additionally, it adds sensors to monitor the status of your services in ispmanager and their current states.

To use this integration, manually upload it to the custom_components/ispmanager directory and restart Home Assistant.

After restarting, you can configure the ispmanager integration from the **Integrations** menu in Home Assistant.
During the setup, you will need to specify the hostname or IP address of your ispmanager server, the username (usually "root"), the password, and the scan interval in seconds.
