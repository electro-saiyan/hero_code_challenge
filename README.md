<h2>To install & run:</h2>

```
docker-compose up
```
<h2>Usage</h2>
<h3>Auth</h3>
<p>The application uses django built-in users for basic auth. To create superuser inside a running contianer run:</p>

```
docker exec -it <container-id> bash
```
<p>Inside the container shell run:</p>

```
python manage.py createsuperuser
```
<h3>Sending config</h3>
Note: If no config exists for device_id, config will be created
<br><br>
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