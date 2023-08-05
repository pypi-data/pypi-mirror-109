import json
from pathlib import Path
from traitlets import Any
from urllib.request import urlretrieve

import pandas as pd
import geopandas as gpd
from ipyleaflet import GeoJSON
import geemap
import ee

from sepal_ui.frontend.styles import AOI_STYLE
from sepal_ui.scripts import utils as su
from sepal_ui.scripts import gee
from sepal_ui.message import ms
from sepal_ui.model import Model


class AoiModel(Model):
    """
    an Model object dedicated to the sorage and the manipulation of aoi. 
    It is meant to be used with the AoiView object (embeded in the AoiTile). 
    By using this you will be able to provide your application with aoi as an ee_object or a gdf, depending if you activated the ee binding or not.
    The class also provide insight on your aoi geometry.
    
    Args: 
        gee (bool, optional): wether or not the aoi selector should be using the EarthEngine binding
        vector (str|pathlib.Path, optional): the path to the default vector object
        admin (int, optional): the administrative code of the default selection. Need to be GADM if ee==False and GAUL 2015 if ee==True.
        asset (str, optional): the default asset. Can only work if ee==True
        folder(str, optional): the init GEE asset folder where the asset selector should start looking (debugging purpose)
        
    Attributes:
        method (traitlet, str): the method to use in the aoi selection. Need to be one of the AoiView.
        
        default_vector (str|pathlib.Path): the default vector file 
        default asset (str): the default asset path
        default_admin (int): the default admin code in GADM if ee==False else GAUL 2015
        
        point_json (traitlet, dict): information that will be use to transform the csv into a gdf (pathname, lat, long, id)
        vector_json (trailtet, dict): information that will be use to transform the vector file into a gdf
        geo_json (traitlet, GeoJson): the drawn geojson featureCollection
        admin (traitlet, int): the administrative code. Need to be GADM if ee==False and GAUL 2015 if ee==True. 
        asset_name (traitlet, str): the asset name (only for GEE model)
        name (traitlet, str): the name of the asset (manually set only in drawn shaped, automatic for all the others)
        
        feature_collection (ee.FeatureCollection): the featurecollection of the aoi (only in ee model)
        gdf (geopandas.GeoDataFrame): the geopandas representation of the aoi
        ipygeojson (GeoJson layer): the ipyleaflet representation of the selected aoi
    """
    
    # const params
    FILE = [Path(__file__).parents[1]/'scripts'/'gadm_database.csv', Path(__file__).parents[1]/'scripts'/'gaul_database.csv']
    CODE = ['GID_{}', 'ADM{}_CODE']
    NAME = ['NAME_{}', 'ADM{}_NAME']
    ISO = ['GID_0', 'ISO 3166-1 alpha-3']
    GADM_BASE_URL = "https://biogeo.ucdavis.edu/data/gadm3.6/gpkg/gadm36_{}_gpkg.zip" # the base url to download gadm maps
    GADM_ZIP_DIR = Path('~', 'tmp', 'GADM_zip').expanduser() # the zip dir where we download the zips
    GADM_ZIP_DIR.mkdir(parents=True, exist_ok=True)
    GAUL_ASSET = "FAO/GAUL/2015/level{}"
    ASSET_SUFFIX = 'aoi_' # the suffix to identify the asset in GEE
    
    # const methods 
    CUSTOM = ms.aoi_sel.custom
    ADMIN = ms.aoi_sel.administrative
    METHODS = {
        'ADMIN0': {'name': ms.aoi_sel.adm[0], 'type': ADMIN},
        'ADMIN1': {'name': ms.aoi_sel.adm[1], 'type': ADMIN},
        'ADMIN2': {'name': ms.aoi_sel.adm[2], 'type': ADMIN},
        'SHAPE': {'name': ms.aoi_sel.vector, 'type': CUSTOM},
        'DRAW': {'name': ms.aoi_sel.draw, 'type': CUSTOM},
        'POINTS': {'name': ms.aoi_sel.points, 'type': CUSTOM},
        'ASSET': {'name': ms.aoi_sel.asset, 'type': CUSTOM}
    }
    
    # widget related traitlets
    method = Any(None).tag(sync=True)
    
    point_json = Any(None).tag(sync=True) # information that will be use to transform the csv into a gdf
    vector_json = Any(None).tag(sync=True) # information that will be use to transform the vector file into a gdf
    geo_json = Any(None).tag(sync=True) # the drawn geojson featureCollection
    admin = Any(None).tag(sync=True)
    asset_name = Any(None).tag(sync=True) # the asset name (only for GEE model)
    name = Any(None).tag(sync=True) # the name of the file (use only in drawn shaped)

    def __init__(self, alert, gee=True, vector=None, admin=None, asset=None, folder=None):

        super().__init__()
        
        # the ee retated informations
        self.ee = gee 
        if gee:
            su.init_ee()
            self.folder = folder if folder else ee.data.getAssetRoots()[0]['id']
        
        # outputs of the selection
        self.gdf = None
        self.feature_collection = None
        self.ipygeojson = None
        
        # the Alert used to display information
        self.alert = alert
        
        # set default values
        self.set_default(vector, admin, asset)
        
        
    def set_default(self, vector=None, admin=None, asset=None):
        """
        Set the default value of the object and create a gdf/feature_collection out of it
        
        Params:
            vector (str|pathlib.path, optional): the default vector file that 
                will be used to produce the gdf. need to be readable by fiona and/or GDAL/OGR
            admin (str, optional): the default administrative area in GADM or GAUL norm
            asset (str, optional): the default asset name, need to point to a readable FeatureCollection
            
        Return:
            self
        """
        
        # save the default values
        self.default_vector = vector
        self.default_asset = self.asset_name = asset
        self.default_admin = self.admin = admin
        
        # cast the vector to json
        self.vector_json = {
            'pathname': str(vector), 
            'column': 'ALL', 
            'value': None
        } if vector else None
        
        # set the default gdf in possible 
        if self.vector_json != None:
            self.set_object('SHAPE')
        elif self.admin != None:
            self.set_object('ADMIN0') # any level will work
        elif self.asset_name != None:
            self.set_object('ASSET')
            
        return self
    
    def set_object(self, method=None):
        """
        set the object (gdf/featurecollection) based on the model inputs. The method can be manually overwrite
        
        Args:
            method (str, optional): a model loading method
        
        Return:
            self
        """
        
        # overwrite self.method
        self.method = method or self.method
        
        if self.method in ['ADMIN0', 'ADMIN1', 'ADMIN2']:
            self._from_admin(self.admin)
        elif self.method == 'POINTS':
            self._from_points(self.point_json)
        elif self.method == 'SHAPE':
            self._from_vector(self.vector_json)
        elif self.method == 'DRAW':
            self._from_geo_json(self.geo_json)
        elif self.method == 'ASSET':
            self._from_asset(self.asset_name)
        else:
            raise Exception(ms.aoi_sel.no_inputs)
            
        self.alert.add_msg(ms.aoi_sel.complete, "success")
        
        return self
    
    def _from_asset(self, asset_name):
        """set the ee.FeatureCollection output from an existing asset"""
        
        # check that I have access to the asset 
        ee_col = ee.FeatureCollection(asset_name)
        ee_col.geometry().bounds().coordinates().get(0).getInfo() # it will raise and error if we cannot access the asset
        
        # set the feature collection 
        self.feature_collection = ee_col 
        
        # create a gdf form te feature_collection
        # cannot be used before geemap 0.8.17 (not released)
        #self.gdf = geemap.ee_to_geopandas(self.feature_collection)
        self.gdf = gpd.GeoDataFrame.from_features(self.feature_collection.getInfo()['features'])
        
        
        # set the name 
        self.name = Path(asset_name).stem.replace(self.ASSET_SUFFIX, '')
        
        return self

    def _from_points(self, point_json):
        """set the object output from a csv json"""
        
        if not all(point_json.values()):
            raise Exception('All fields are required, please fill them.')
            
        # cast the pathname to pathlib Path
        point_file = Path(point_json['pathname'])
    
        # check that the columns are well set 
        values = [v for v in point_json.values()]
        if not len(values) == len(set(values)):
            raise Exception(ms.aoi_sel.duplicate_key)
    
        # create the gdf
        df = pd.read_csv(point_file, sep=None, engine='python')
        self.gdf = gpd.GeoDataFrame(
            df, 
            crs='EPSG:4326', 
            geometry = gpd.points_from_xy(
                df[point_json['lng_column']], 
                df[point_json['lat_column']])
        )
        
        # set the name
        self.name = point_file.stem
        
        if self.ee:
            # transform the gdf to ee.FeatureCollection 
            self.feature_collection = geemap.geojson_to_ee(self.gdf.__geo_interface__)

            # export as a GEE asset
            self.export_to_asset()
            
        return self
    
    def _from_vector(self, vector_json):
        """set the object output from a vector json"""
        
        if not (vector_json['pathname']):
            raise Exception('Please select a file.')
        
        if vector_json['column'] != 'ALL':
            if vector_json['value'] is None:
                raise Exception('Please select a value.')
            
        # cast the pathname to pathlib Path
        vector_file = Path(vector_json['pathname'])
        
        # create the gdf
        self.gdf = gpd.read_file(vector_file).to_crs("EPSG:4326")
        
        # set the name using the file stem
        self.name = vector_file.stem
        
        # filter it if necessary
        if vector_json['value']:
            self.gdf = self.gdf[self.gdf[vector_json['column']] == vector_json['value']]
            self.name = f"{self.name}_{vector_json['column']}_{vector_json['value']}"
        
        if self.ee:
            # transform the gdf to ee.FeatureCollection 
            self.feature_collection = geemap.geojson_to_ee(self.gdf.__geo_interface__)

            # export as a GEE asset
            self.export_to_asset()
        
        return self
    
    def _from_geo_json(self, geo_json):
        """set the gdf output from a geo_json"""
        
        if not geo_json:
            raise Exception('Please draw a shape in the map')
        
        # remove the style property from geojson as it's not recognize by geopandas and gee
        for feat in geo_json['features']:
            del feat['properties']['style']
        
        # create the gdf
        self.gdf = gpd.GeoDataFrame.from_features(geo_json)
        
        # normalize the name
        self.name =su.normalize_str(self.name)
        
        if self.ee:
            # transform the gdf to ee.FeatureCollection 
            self.feature_collection = geemap.geojson_to_ee(self.gdf.__geo_interface__)

            # export as a GEE asset
            self.export_to_asset()
        else:
            # save the geojson in downloads 
            path = Path('~', 'downloads', 'aoi').expanduser()
            path.mkdir(exist_ok=True, parents=True) # if nothing have been run the downloads folder doesn't exist
            self.gdf.to_file(path/f'{self.name}.geojson', driver='GeoJSON')
        
        return self
            
    def _from_admin(self, admin):
        """Set the object according to given an administrative number in the GADM norm. The object will be projected in EPSG:4326"""
        
        if not admin:
            raise Exception('Select an administrative layer')
        
        # get the admin level corresponding to the given admin code
        df = pd.read_csv(self.FILE[self.ee])
        
        # extract the first element that include this administrative code and set the level accordingly 
        is_in = df.filter([self.CODE[self.ee].format(i) for i in range(3)]).isin([admin])
        
        if not is_in.any().any():
            raise Exception("The code is not in the database")
        else:
            index = 3 if self.ee else -1
            level = is_in[~((~is_in).all(axis=1))].idxmax(1).iloc[0][index] # the character that contains the index
            
        if self.ee:
            
            # get the feature_collection
            self.feature_collection = ee.FeatureCollection(self.GAUL_ASSET.format(level)) \
                .filter(ee.Filter.eq(f'ADM{level}_CODE', admin))
            
            # transform it into gdf
            # cannot be used before geemap 0.8.17 (not released)
            #self.gdf = geemap.ee_to_geopandas(self.feature_collection)
            self.gdf = gpd.GeoDataFrame.from_features(self.feature_collection.getInfo()['features'])
            
        else:     
            # save the country iso_code 
            iso_3 = admin[:3]
        
            # download the geopackage in tmp 
            zip_file = self.GADM_ZIP_DIR/f'{iso_3}.zip'
        
            if not zip_file.is_file():
            
                # get the zip from GADM server only the ISO_3 code need to be used
                urlretrieve(self.GADM_BASE_URL.format(iso_3), zip_file)
            
            # read the geopackage 
            layer_name = f"gadm36_{iso_3}_{level}"
            level_gdf = gpd.read_file(f'{zip_file}!gadm36_{iso_3}.gpkg', layer=layer_name)
        
            # get the exact admin from this layer 
            self.gdf = level_gdf[level_gdf[self.CODE[self.ee].format(level)] == admin]
        
        # set the name using the layer 
        r = df[df[self.CODE[self.ee].format(level)] == admin].iloc[0]
        names = [su.normalize_str(r[self.NAME[self.ee].format(i)]) if i else r[self.ISO[self.ee]] for i in range(int(level)+1)]
        self.name = '_'.join(names)
        
        return self
    
    def clear_attributes(self):
        """
        Return all attributes to their default state.
        Set the default setting as current object.

        Return: 
            self
        """

        # keep the default 
        admin = self.default_admin
        vector = self.default_vector 
        asset = self.default_asset

        # delete all the traits
        [setattr(self, attr, None) for attr in self.trait_names()]
        
        # reset the outputs
        self.gdf = None
        self.feature_collection = None
        self.ipygeojson = None
        self.selected_feature = None

        # reset the default 
        self.set_default(vector, admin, asset)

        return self

    def get_columns(self):
        """ 
        Retrieve the columns or variables from self excluding geometries and gee index.

        Return: 
            ([str]): sorted list of column names
        """
        
        if type(self.gdf) == type(None):
            raise Exception("You must set the gdf before interacting with it")
        
        if self.ee: 
            aoi_ee = ee.Feature(self.feature_collection.first())
            columns = aoi_ee.propertyNames().getInfo()
            list_ = [col for col in columns if col not in ['system:index', 'Shape_Area']]
        else:
            list_ = list(set(['geometry'])^set(self.gdf.columns.to_list()))
            
        return sorted(list_)
        
    def get_fields(self, column):
        """" 
        Retrieve the fields from a column
        
        Args:
            column (str): A column name to query over the asset
        
        Return: 
            ([str]): sorted list of fields value

        """
        
        if type(self.gdf) == type(None):
            raise Exception("You must set the gdf before interacting with it")
        
        if self.ee: 
            fields = self.feature_collection.distinct(column).aggregate_array(column)
            list_ = fields.getInfo()
        else:
            list_ = self.gdf[column].to_list()
            
        return sorted(list_)
    
    def get_selected(self, column, field):
        """ 
        Select an ee object based on selected column and field.

        Return:
            (ee.Feature|GoeSeries): the Feature associated with the query
        """
        
        if type(self.gdf) == type(None):
            raise Exception("You must set the gdf before interacting with it") 
        
        if self.ee:
            selected_feature = self.feature_collection.filterMetadata(column, 'equals', field)
        else:
            selected_feature = self.gdf[self.gdf[column] == field]
            
        return selected_feature
    
    def total_bounds(self):
        """
        Reproduce the behaviour of the total_bounds method from geopandas
        
        Return: 
            (tuple): minxx, miny, maxx, maxy
        """
        
        if self.ee:
            ee_bounds = self.feature_collection.geometry().bounds().coordinates()
            coords = ee_bounds.get(0).getInfo()
            ll, ur = coords[0], coords[2]
            bounds = ll[0], ll[1], ur[0], ur[1]
        else: 
            bounds = self.gdf.total_bounds
        
        return bounds
    
    def export_to_asset(self):
        """
        Export the feature_collection as an asset (only for ee model)
        
        Return: 
            self
        """
        
        asset_name = self.ASSET_SUFFIX + self.name
        asset_id = str(Path(self.folder, asset_name))
        
        # set the asset name 
        self.asset_name = asset_id
        
        # check if the table already exist
        if asset_id in [a['name'] for a in gee.get_assets(self.folder)]:
            return self
        
        # check if the task is running 
        if gee.is_running(asset_name):
            return self
        
        # run the task
        task_config = {
            'collection': self.feature_collection,
            'description': asset_name,
            'assetId': asset_id
        }
        
        task = ee.batch.Export.table.toAsset(**task_config)
        task.start()
        
        return self
    
    def get_ipygeojson(self):
        """ 
        Converts current geopandas object into ipyleaflet GeoJSON
        
        Return: 
            (GeoJSON): the geojson layer of the aoi gdf
        """
        
        if type(self.gdf) == type(None):
            raise Exception("You must set the gdf before converting it into GeoJSON")
    
        data = json.loads(self.gdf.to_json())
        self.ipygeojson = GeoJSON(data=data, style=AOI_STYLE, name='aoi')
        
        return self.ipygeojson
        