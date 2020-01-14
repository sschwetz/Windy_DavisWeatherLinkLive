This script is designed to be run as a cron job (linux) or a scheduled task (windows)

This script has only been run using python 3.7

## Quick Start

### Variable updates

This script has 3 variables to change

```
bucket_type = 0.2 
local_address = "WLL_IP_ADDRESS"
windy_api_key = "WINDY.COM_API_KEY"
```

#### bucket_type
This is the size of your bucket in cm. If you have a 2mm bucket it will be 0.2 imperial buckets will need to be multiplied by 2.54

#### local_address
This is the local address for your Weatherlink Live. You will need to look up it's mac address (the DID on the bottom of the unit) on the arp table on your router. 

#### windy_api_key
this is the API key from https://stations.windy.com/stations



