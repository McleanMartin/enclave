# ArcGIS integration

This package provides a minimal integration scaffold for the ArcGIS
Python SDK. It intentionally keeps import-time behaviour lightweight and
fails with a clear error message if the SDK is not installed.

Installation notes
- The ArcGIS Python API is large and may require binary dependencies.
  - Preferred: install with conda: `conda install -c esri arcgis`
  - Pip install may work in many environments: `pip install arcgis`

Environment variables (recommended)
- `ARCGIS_CLIENT_ID` and `ARCGIS_CLIENT_SECRET` — OAuth client credentials
- `ARCGIS_USERNAME` and `ARCGIS_PASSWORD` — username/password login
- `ARCGIS_PORTAL_URL` — portal URL, defaults to `https://www.arcgis.com`

Usage
1. Install the SDK (see notes above).
2. Configure credentials in environment variables or secret manager.
3. Use `enclave.arcgis.services.ArcGISClient` from your code or tasks.

Example
```py
from enclave.arcgis.services import ArcGISClient

client = ArcGISClient()
print(client.info())
```
