<h2>To install & run:</h2>

```
docker-compose up
```
<h2>Usage</h2>
<h3>Sending config</h3>
<p>Config from device:</p>

```
POST /api/device-config/{device_id} 
```

<h4>Config from frontend:</h4>

```
POST /api/frontend-config/{device_id} 
```

<h4>Retrieving the active config for a device</h4>

```
GET /api/frontend-config/{device_id} 
```