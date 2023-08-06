# Metadata proxy

## CLI Arguments
Once pip installed, there will be a `metadata-proxy` script installed into the path, it accepts the following arguments

    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--log-file', type=str, default=None, help='Log file')
    parser.add_argument('--log-level', type=str, default='INFO',
                        choices=logging._levelToName.values(), help='Log level')
                        
                        
## Register API

The `/register` endpoint will instruct the proxy to register with a metadata server and get periodic updates. It only accepts
HTTP POST requests.

It takes a JSON payload like the following:
```json
{
  "key": "INITIAL_REGISTRATION_KEY",
  "server_url": "https://main_metadata_server.example.com"
}
```

If you make a request to `/register?skip_if_registered=1` then if the proxy is already registered, it wont re-register.

You can re-register but if you do, that will reset the host entry in the metadata database and will default back to no IAM role.