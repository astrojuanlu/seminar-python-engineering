# This requires an account on the Copernicus Open Access Hub
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

api = SentinelAPI(os.environ["SENTINEL_USER"], os.environ["SENTINEL_PASS"])
roi_geojson = read_geojson("search_polygon.geojson")
products = api.query(geojson_to_wkt(roi_geojson),
                     producttype='S2MSI2A',
                     orbitdirection='DESCENDING',
                     limit=1)

# And this will take a lot of time to complete!
api.download_all(products, directory_path="./data")