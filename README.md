##To install & run:

```
docker-compose up
```
##Usage
###Sending config
#####Config from device:

```
POST /api/device-config/{device_id} 
```

#####Config from frontend:

```
POST /api/frontend-config/{device_id} 
```

####Retrieving the active config for a device

```
GET /api/frontend-config/{device_id} 
```