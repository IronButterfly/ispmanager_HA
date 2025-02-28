# Ispmanager integration to Homeassistat
Simple custom integration for ispmanager in Homeassistant.

Based on the API request to the ispmanager server, two sensors are created - CPU usage and RAM usage. Additionally sensors of your actual ispmanager's services with their statuses will be added.
For the integration to work, it is necessary to manually upload it to custom_components/ispmanager and restart Homeassistant. 
Then you cna add and configure Ispmanager integration in Homeassistan's Integration menu. 
On stage of configuration you will. be asked about hostname or IP address of your ispmanager server, username (usually root), password and scan interval in seconds.
