# nhdplusextractor.py
#
# Mitchell Sawtelle (mitchell.sawtelle@okstate.edu)
#
# last updated: 06/25/2018
#
# contains the NHDPlus Extractor class, which can be used to retrieve source
# data from the NHDPlus V2 dataset online, and then extract the data from
# the larger source files for a given 8-digit Hydrologic Unit Code (HUC8).


import subprocess, time, os, numpy, struct, datetime, shutil
from osgeo import gdal
from osgeo import osr
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from gdalconst import GA_ReadOnly
from matplotlib import pyplot, path, ticker
from matplotlib import patches, colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from .flowline import Flowline
from .vectorutils import merge_shapes
from shapefile import Reader, Writer
import pickle
import xml.etree.ElementTree as ET


class NHDPlusExtractor(object):
    """class which holds various methods to manipulate, gather, and unpack the NHDPlus Dataset
       updated email list
       destination argument of the init method denotes the working directory for all ndhplus work
     """

    def __init__(self, destination):
        '''
        init method for NHDPlusExtractor class

        arguments:
            destination is the path to where the user would like the nhdplus data to be stored
            if no argument is given the location of this file is used
        '''
        if destination is None: #if no destination given in init method set destination to current directory
            self. destination = os.path.dirname(__file__)
        if not os.path.isdir(destination): os.mkdir(destination)
        #base_url to EPA's hosting of the NHDPlusV21 Dataset on amazon servers
        self.base_url = 'https://s3.amazonaws.com/nhdplus/'
        self.destination = destination #set destination
        self.currentpath = os.path.dirname(__file__) #currentpath variable
        self.path_to_7zip = r'C:\Program Files\7-Zip\7z.exe' #path to 7zip will vary per User


        #names of the Drainage areas with respective abbreviations
        self.DD = {'AMERICAN SAMOA': 'PI',
              'ARK-RED-WHITE': 'MS',
              'CALIFORNIA': 'CA',
              'GREAT BASIN': 'GB',
              'GREAT LAKES': 'GL',
              'GUAM': 'PI',
              'HAWAII': 'HI',
              'LOWER COLORADO': 'CO',
              'LOWER MISSISSIPPI': 'MS',
              'LOWER MISSOURI': 'MS',
              'MID-ATLANTIC': 'MA',
              'NORTHEAST': 'NE',
              'NORTHERN MARIANA ISLANDS': 'PI',
              'OHIO': 'MS',
              'PACIFIC NORTHWEST': 'PN',
              'PUERTO RICO/U.S. VIRGIN ISLANDS': 'CI',
              'RIO GRANDE': 'RG',
              'SOURIS-RED-RAINY': 'SR',
              'SOUTH ATLANTIC NORTH': 'SA',
              'SOUTH ATLANTIC SOUTH': 'SA',
              'SOUTH ATLANTIC WEST': 'SA',
              'TENNESSEE': 'MS',
              'TEXAS': 'TX',
              'UPPER COLORADO': 'CO',
              'UPPER MISSISSIPPI': 'MS',
              'UPPER MISSOURI': 'MS',
              }
        # VPU in each drainage area
        self.DA_to_VPU = {'PN': ['17'],
                     'CA': ['18'],
                     'GB': ['16'],
                     'CO': ['14', '15'],
                     'MS': ['05', '06', '07', '08', '10U', '10L', '11'],
                     'TX': ['12'],
                     'RG': ['13'],
                     'SR': ['09'],
                     'SA': ['03N', '03S', '03W'],
                     'GL': ['04'],
                     'MA': ['02'],
                     'NE': ['01'],
                     'PI': ['22AS', '22GU', '22MP'],
                     'HI': ['20'],
                     'CI': ['21'],
                     }
        #VPU numbers to Drainage Area abbreviations
        self.VPU_to_DA = {'01': 'NE',
                     '02': 'MA',
                     '03N': 'SA',
                     '03S': 'SA',
                     '03W': 'SA',
                     '04': 'GL',
                     '05': 'MS',
                     '06': 'MS',
                     '07': 'MS',
                     '08': 'MS',
                     '09': 'SR',
                     '10U': 'MS',
                     '10L': 'MS',
                     '11': 'MS',
                     '12': 'TX',
                     '13': 'RG',
                     '14': 'CO',
                     '15': 'CO',
                     '16': 'GB',
                     '17': 'PN',
                     '18': 'CA',
                     '20': 'HI',
                     '21': 'CI',
                     '22AS': 'PI',
                     '22GU': 'PI',
                     '22MP': 'PI',
                     }
        #VPU numbers to Drainage Area name
        self.VPU_names = {'01': 'NORTHEAST',
                     '02': 'MID-ATLANTIC',
                     '03N': 'SOUTH ATLANTIC NORTH',
                     '03S': 'SOUTH ATLANTIC SOUTH',
                     '03W': 'SOUTH ATLANTIC WEST',
                     '04': 'GREAT LAKES',
                     '05': 'OHIO',
                     '06': 'TENNESSEE',
                     '07': 'UPPER MISSISSIPPI',
                     '08': 'LOWER MISSISSIPPI',
                     '09': 'SOURIS-RED-RAINY',
                     '10U': 'UPPER MISSOURI',
                     '10L': 'LOWER MISSOURI',
                     '11': 'ARK-RED-WHITE',
                     '12': 'TEXAS',
                     '13': 'RIO GRANDE',
                     '14': 'UPPER COLORADO',
                     '15': 'LOWER COLORADO',
                     '16': 'GREAT BASIN',
                     '17': 'PACIFIC NORTHWEST',
                     '18': 'CALIFORNIA',
                     '20': 'HAWAII',
                     '21': 'PUERTO RICO/U.S. VIRGIN ISLANDS',
                     '22AS': 'AMERICAN SAMOA',
                     '22GU': 'GUAM',
                     '22MP': 'NORTHERN MARIANA ISLANDS',}
        #VPU number to RPU numbers
        self.VPU_to_RPU = {'01': ['01a'],
                      '02': ['02a', '02b'],
                      '03N': ['03a', '03b'],
                      '03S': ['03c', '03d'],
                      '03W': ['03e', '03f'],
                      '04': ['04a', '04b', '04c', '04d'],
                      '05': ['05a', '05b', '05c', '05d'],
                      '06': ['06a'],
                      '07': ['07a', '07b', '07c'],
                      '08': ['08a', '08b', '03g'],
                      '09': ['09a'],
                      '10U': ['10e', '10f', '10g', '10h', '10i'],
                      '10L': ['10a', '10b', '10c', '10d'],
                      '11': ['11a', '11b', '11c', '11d'],
                      '12': ['12a', '12b', '12c', '12d'],
                      '13': ['13a', '13b', '13c', '13d'],
                      '14': ['14a', '14b'],
                      '15': ['15a', '15b'],
                      '16': ['16a', '16b'],
                      '17': ['17a', '17b', '17c', '17d'],
                      '18': ['18a', '18b', '18c'],
                      '20': ['20a', '20b', '20c', '20d', '20e', '20f', '20g', '20h'],
                      '21': ['21a', '21b', '21c'],
                      '22AS': ['22c'],
                      '22GU': ['22a'],
                      '22MP': ['22b'],
                      }

        #RPU numbers to VPU numbers
        self.RPU_to_VPU = {'01a': '01',
                      '02a': '02',
                      '02b': '02',
                      '03a': '03N',
                      '03b': '03N',
                      '03c': '03S',
                      '03d': '03S',
                      '03e': '03W',
                      '03f': '03W',
                      '03g': '08',
                      '04a': '04',
                      '04b': '04',
                      '04c': '04',
                      '04d': '04',
                      '05a': '05',
                      '05b': '05',
                      '05c': '05',
                      '05d': '05',
                      '06a': '06',
                      '07a': '07',
                      '07b': '07',
                      '07c': '07',
                      '08a': '08',
                      '08b': '08',
                      '09a': '09',
                      '10a': '10L',
                      '10b': '10L',
                      '10c': '10L',
                      '10d': '10L',
                      '10e': '10U',
                      '10f': '10U',
                      '10g': '10U',
                      '10h': '10U',
                      '10i': '10U',
                      '11a': '11',
                      '11b': '11',
                      '11c': '11',
                      '11d': '11',
                      '12a': '12',
                      '12b': '12',
                      '12c': '12',
                      '12d': '12',
                      '13a': '13',
                      '13b': '13',
                      '13c': '13',
                      '13d': '13',
                      '14a': '14',
                      '14b': '14',
                      '15a': '15',
                      '15b': '15',
                      '16a': '16',
                      '16b': '16',
                      '17a': '17',
                      '17b': '17',
                      '17c': '17',
                      '17d': '17',
                      '18a': '18',
                      '18b': '18',
                      '18c': '18',
                      '20a': '20',
                      '20b': '20',
                      '20c': '20',
                      '20d': '20',
                      '20e': '20',
                      '20f': '20',
                      '20g': '20',
                      '20h': '20',
                      '21a': '21',
                      '21b': '21',
                      '21c': '21',
                      '22a': '22GU',
                      '22b': '22MP',
                      '22c': '22AS',
                    }
        #files needed
        self.files = ('NHDPlusCatchment',
                      'NHDSnapshot',
                      'NHDPlusAttributes',
                      'EROMExtension',
                      'NEDSnapshot',
                      )


        #headers to use when pinging the amazon servers
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
        self.vpu_links = {'01': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusNE/',
                          '02': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusMA/',
                          '03N': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusSA/NHDPlus03N/',
                          '03S': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusSA/NHDPlus03S/',
                          '03W': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusSA/NHDPlus03W/',
                          '04': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusGL/',
                          '05': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusMS/NHDPlus05/',
                          '06': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusMS/NHDPlus06/',
                          '07': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusMS/NHDPlus07/',
                          '08': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusMS/NHDPlus08/',
                          '09': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusSR/',
                          '10U':'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusMS/NHDPlus10U/',
                          '10L':'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusMS/NHDPlus10L/',
                          '11': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusMS/NHDPlus11/',
                          '12': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusTX/',
                          '13': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusRG/',
                          '14': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusCO/NHDPlus14/',
                          '15': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusCO/NHDPlus15/',
                          '16': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusGB/',
                          '17': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusPN/',
                          '18': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusCA/',
                          '20': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusHI/',
                          '21': 'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusCI/',
                          '22AS':'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusPI/NHDPlus22AS/',
                          '22GU':'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusPI/NHDPlus22GU/',
                          '22MP':'https://s3.amazonaws.com/nhdplus?delimiter=/&prefix=NHDPlusV21/Data/NHDPlusPI/NHDPlus22MP/'
                         }

    def get_links(self,vpu):
        '''
        grab the download links for self.files from the amazon xml pages
        '''
        xml = self.vpu_links[vpu]
        req = Request(xml, data = None, headers = self.headers)
        response = urlopen(req).read().decode('ascii')
        tree = ET.ElementTree(ET.fromstring(response))
        root = tree.getroot()
        links = []
        for i,child in enumerate(root.iter(r'{http://s3.amazonaws.com/doc/2006-03-01/}Contents')):
            if i == 0 or i ==1:
                continue
            link = child.find(r'{http://s3.amazonaws.com/doc/2006-03-01/}Key').text
            for files in self.files:
                if files.lower() in link.lower():
                    dwn_link = self.base_url + link
                    links.append(dwn_link)
        return links

    def decompress(self,filename):

        '''
        identifies operating system and decompresses with the appropriate method
        filename takes full path to file to be decompressed
        '''

        if os.name == 'posix':
            self.decompress_linux(filename)
        elif os.name == 'nt':
            self.decompress_windows(filename)
        else:
            print('unknown operating system')
            raise


    def decompress_windows(self,
                           filename,
                           ):
        """
        Spawns a subprocess to use 7zip to decompress the file.
        filename takes fullpath of file to be decompressed
        """



        if not os.path.isfile(self.path_to_7zip):
            print('error: specified path to 7zip ' +
                  '{} does not exist!\n'.format(self.path_to_7zip))
            raise

        args = [self.path_to_7zip, 'x', '-o{}'.format(self.destination),
                filename]

        try:

            with subprocess.Popen(args) as p: pass

        except:

            print('error: unable to decompress files')
            print('is 7zip installed?')

    def decompress_linux(self, filename):
        """
        Unzips the archive on linux.
        filename takes fullpath of file of be decompressed
        """

        args = ['7z', 'x', '-o{}'.format(self.destination), filename]

        try:

            with subprocess.Popen(args) as p: pass

        except:

            print('error: unable to decompress files')
            print('is 7zip installed?')

    def download_decompress(self,vpu,decompress=True):
        '''
        function to download and decompress the data from the NHDPlus DataSet
        this function will download all of the raster and vector data for a specified Drainage area
        **kwargs
        vpu: string, the VPU corresponding to the Drainage Area ID to be downloaded ie DA = 'MA' vpu = '02'
        decomrpess: if True decompress files with 7zip
        '''
        assert vpu in self.VPU_to_RPU.keys(), 'VPU must be in ' + str(sorted(self.VPU_to_RPU.keys()))
        links = self.get_links(vpu)
        local_files = [f for f in os.listdir(self.destination)]
        for f in self.files:
            dwn_link = None
            if any([f in localfile for localfile in local_files]):
                print(f,'for vpu:',vpu,'exists')
            else:
                print(f,'for vpu:',vpu,'does not exist starting download')
                for link in links:
                    if f.lower() in link.lower():
                        dwn_link = link
            if dwn_link is not None:
                filename = os.path.basename(dwn_link)
                req = Request(dwn_link, data = None, headers = self.headers)
                response = urlopen(req)
                CHUNK = 1024 * 1024
                with open(os.path.join(self.destination, filename), 'wb') as f:
                    while True:
                        chunk = response.read(CHUNK)
                        if not chunk:
                            break
                        f.write(chunk)
                print(filename,'for vpu:',vpu,'downloaded')
            del(dwn_link)

        if decompress == True:
            local_files = [os.path.join(self.destination,f) for f in os.listdir(self.destination) if f.endswith('.7z')]
            print(local_files)
            for file in local_files:
                self.decompress(file)

    def get_degree_transform(self, dataset):
        """
        Gets a GDAL transform to convert coordinate latitudes and longitudes
        to northings and eastings associated with the NAD 1983 projection.
        """

        # get the old coordinate system

        old = osr.SpatialReference()
        old.ImportFromWkt(dataset.GetProjection())

        # create the new coordinate system

        nad83_wkt = (
            """
            GEOGCS["NAD83",
            DATUM["North_American_Datum_1983",
            SPHEROID["GRS 1980",6378137,298.257222101,
            AUTHORITY["EPSG","7019"]],
            AUTHORITY["EPSG","6269"]],
            PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
            UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9108"]],
            AUTHORITY["EPSG","4269"]]
            """
            )

        new = osr.SpatialReference()
        new.ImportFromWkt(nad83_wkt)

        # create a transform object to convert between coordinate systems

        transform = osr.CoordinateTransformation(old, new)

        return transform

    def get_raster(self, filename, points, quiet = False):
        """
        Reads the value of attributes in a raster file at a list of points.
        """

        if quiet: gdal.PushErrorHandler('CPLQuietErrorHandler')

        # register all of the drivers

        gdal.AllRegister()

        # open the image

        dataset = gdal.Open(filename, GA_ReadOnly)

        # get the coordinate transformation

        transform = self.get_NAD1983_transform(dataset)

        # get image size

        rows  = dataset.RasterYSize
        cols  = dataset.RasterXSize
        bands = dataset.RasterCount

        # get georeference info

        x0, width, x_rotation, y0, y_rotation, height = dataset.GetGeoTransform()

        # loop through the points and get the raster values

        values = []
        for point in points:

            # get x,y

            x, y, z = transform.TransformPoint(point[0], point[1])

            # transform the easting and northing to pixel space

            pixel_x = int((x - x0) / width)
            pixel_y = int((y - y0) / height)

            # loop through the bands and find the values

            for i in range(1, bands + 1):

                band = dataset.GetRasterBand(i)

                # read data and add the value to the string

                value = band.ReadRaster(pixel_x, pixel_y, 1, 1)
                if value is None: value = -1
                else: value = int.from_bytes(value, byteorder = 'little')

            values.append(value)

        return values

    def get_NAD1983_transform(self,dataset):
        """
        Gets a GDAL transform to convert coordinate northings and eastings
        associated with the NAD 1983 projection to latitudes and longitudes.
        """

        # get the old coordinate system

        old = osr.SpatialReference()
        old.ImportFromWkt(dataset.GetProjection())

        # create the new coordinate system

        nad83_wkt = (
            """
            GEOGCS["NAD83",
            DATUM["North_American_Datum_1983",
            SPHEROID["GRS 1980",6378137,298.257222101,
            AUTHORITY["EPSG","7019"]],
            AUTHORITY["EPSG","6269"]],
            PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
            UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9108"]],
            AUTHORITY["EPSG","4269"]]
            """
            )

        new = osr.SpatialReference()
        new.ImportFromWkt(nad83_wkt)

        # create a transform object to convert between coordinate systems

        transform = osr.CoordinateTransformation(new, old)

        return transform

    def get_raster_table(self,
                         filename,
                         extent,
                         dtype,
                         locations = False,
                         quiet = False,
                         ):
        """
        Gets the values of a DEM raster over a rectangular plot with corners
        located at longmin, latmin, longmin, and latmax as specified by extents.
        Returns a matrix of values and the corresponding latitude and longitude.
        """

        start = time.time()

        longmin, latmin, longmax, latmax = extent

        if quiet: gdal.PushErrorHandler('CPLQuietErrorHandler')

        # register all of the drivers

        gdal.AllRegister()

        # open the image

        dataset = gdal.Open(filename, GA_ReadOnly)

        # get image size

        rows  = dataset.RasterYSize
        cols  = dataset.RasterXSize
        bands = dataset.RasterCount

        # get georeference info

        x0, w, x_rotation, y0, y_rotation, h = dataset.GetGeoTransform()

        # transform the to/from NAD 1983 and latitudes/longitudes

        NAD1983_transform = self.get_NAD1983_transform(dataset)
        degree_transform  = self.get_degree_transform(dataset)

        # transform the corner points to NAD 1983

        points = zip([longmin] * 2 + [longmax] * 2, [latmin, latmax] * 2)

        xs, ys, zs = zip(*[NAD1983_transform.TransformPoint(*point)
                           for point in points])

        # get the pixel values of the min longitudes and latitudes and the number
        # of pixels in each direction

        pxmin  = min([self.get_pixel(x, x0, w) for x in xs])
        pymin  = min([self.get_pixel(y, y0, h) for y in ys])
        width  = max([self.get_pixel(x, x0, w) for x in xs]) - pxmin
        height = max([self.get_pixel(y, y0, h) for y in ys]) - pymin

        # find the location of the origin (pixels are integers, degrees are reals)

        rx = self.get_remainder(min(xs), x0, w)
        ry = self.get_remainder(min(ys), y0, h)

        origin = [min(xs), min(ys)]

        # pre-allocate some space to store the lat/long of each pixel and the value

        latitudes  = numpy.empty((height, width), dtype = 'float')
        longitudes = numpy.empty((height, width), dtype = 'float')

        # read the band

        band = dataset.GetRasterBand(1)

        # iterate through the file, noting that pixels start at top left and move
        # down and right, and the y values move up

        values = numpy.empty((height, width), dtype = dtype)

        if locations:

            # need to return the latitudes and longitudes, which takes time

            for row in range(height):
                values[height - row - 1] = band.ReadAsArray(pxmin, pymin + row,
                                                            width, 1)
                for column in range(width):
                    x, y, z = degree_transform.TransformPoint(origin[0] + w *column,
                                                              origin[1] + h * row)
                    latitudes[height - row - 1,  column] = y
                    longitudes[height - row - 1, column] = x

            return longitudes, latitudes, values

        else:

            # just return the location of the origin

            try:

                for row in range(height):
                    b = band.ReadAsArray(pxmin, pymin + row, width, 1)
                    values[height - row - 1] = b

            except:

                if not quiet: print('warning: unable to read data\n')
                values = None

            return values, [origin[0] - rx, origin[1] - ry]

    def read_dbf(self, source, comids, attributes = None,verbose=True):
        '''
        function to read database files, .dbf,
        arguments:
            source: dbf file to be read
            comids: comids of flowlines to  from source
        kwargs:
            attributes: attributes of flowline to be extracted from source if None
                        all attributes are returned
            verbose: verbosity of function
        '''
        record=[] #empty list to hold singular record
        records=[] #empty list to hold multiple record
        temp = {} #dictionary mapping values to fields example temp['COMID'] = [7621376,24557283]
        index=[] #index of the requested attributes in the dbf
        mydbf = open(source,'rb')#open dbf file
        sf = Reader(dbf=mydbf)#use PyShp to read dbf
        fields = sf.fields[1:]#list of the fields from the dbf excluding the DeletionFlag
        fields = [item[0].upper() for item in fields]#capitalize the names of the fields and remove the other qualitites of the fields


        #iterate over the dbf file accessing the records using attributes as a fields
        ##query. if attributes is none return all the records for all the fields
        if attributes is None: attributes = fields

        #find comid index in the dbf file
        for attribute in attributes:
            if attribute == ['COMID', 'N', 9, 0]:
                comid_index = [pos for pos,j in enumerate(fields) if attribute[0] == j]
                if verbose is True:
                    print('the comid_index is ' + str(comid_index[0]))

            index.append([pos for pos,j in enumerate(fields) if attribute[0] == j][0])

        if verbose is True:
            print('iterating over records finding matching comids from list given')
        #iterate over records finding matching comids
        for pos,rec in enumerate(sf.records()):

            if rec[comid_index[0]] in comids:
                for indice in index:
                    record.append(rec[indice])
                if verbose is True:
                    print('data for {} has been collected'.format(rec[comid_index[0]]))
                records.append(record)
                record = []
        #write records to dictionary linking the attributes to all their respective records
        for field in attributes:
            y = attributes.index(field)
            field = field[0]
            temp[field]=[]
            for record in records:
                temp[field].append(record[y])

        return temp


    def get_comids(self, flowlinefile):
        """
        Finds the comids from the flowline file.
        """

        # open the file

        shapefile = Reader(flowlinefile)

        # find the index of the comids
        try:
            comid_index = shapefile.fields.index(['COMID', 'N', 9,  0]) - 1
        except:
            comid_index = shapefile.fields.index(['ComID', 'N', 9, 0]) - 1

        # make a list of the comids

        comids = [r[comid_index] for r in shapefile.records()]

        return comids

    def extract_flowlines(self,
                          source,
                          destination,
                          HUC8,
                          verbose = True,
                          ):
        """
        Extracts flowlines from the source datafile to the destination using
        the HUC8 for the query.
        """

        # open the flowline file

        if verbose: print('reading the flowline file\n')

        shapefile = Reader(source, shapeType = 3)
        records   = shapefile.records()

        # figure out which field codes are the Reach code and comid

        fields = shapefile.fields[1:]
        fields = [item[0].upper() for item in fields]

        for pos, j in enumerate(fields):
            if j == 'REACHCODE':
                reach_index = pos

        # go through the reach indices, add add them to the list of flowlines
        # if in the watershed; also make a list of the corresponding comids

        if verbose: print('searching for flowlines in the watershed\n')

        indices = []

        i = 0
        for record in records:
            if record[reach_index][:8] == HUC8: indices.append(i)
            i+=1

        if len(indices) == 0:
            if verbose: print('error: query returned no values')
            raise

        # write the data from the HUC8 to a new shapefile

        w = Writer(shapeType = 3)

        for field in shapefile.fields:  w.field(*field)

        for i in indices:
            shape = shapefile.shape(i)
            w.poly(shapeType = 3, parts = [shape.points])

            record = records[i]

            #little work around for blank GNIS_ID and GNIS_NAME values

            if isinstance(record[3], bytes):
                record[3] = record[3].decode('cp1252')
            if isinstance(record[4], bytes):
                record[4] = record[4].decode('cp1252')

            w.record(*record)

        w.save(destination)

        if verbose:
            l = len(indices)
            print('queried {} flowlines from original shapefile\n'.format(l))

    def extract_catchments(self,
                           source,
                           destination,
                           flowlinefile,
                           verbose = True,
                           ):
        """
        Extracts the catchments from the source data file to the destination
        using the list of comids for the query.
        """

        # make a list of the comids

        comids = self.get_comids(flowlinefile)

        # open the catchment shapefile

        if verbose: print('reading the catchment shapefile\n')

        shapefile = Reader(source)

        # get the index of the feature id, which links to the flowline comid
        print(shapefile.fields)
        featureid_index = shapefile.fields.index(['FEATUREID', 'N', 9, 0]) - 1

        # go through the comids from the flowlines and add the corresponding
        # catchment to the catchment list

        if verbose: print('searching the catchments in the watershed\n')

        records = shapefile.records()
        indices = []

        i = 0
        for record in records:
            if record[featureid_index] in comids: indices.append(i)
            i+=1

        if len(indices) == 0:
            print('query returned no values, returning\n')
            raise

        # create the new shapefile

        if verbose: print('writing the new catchment shapefile\n')

        w = Writer()

        for field in shapefile.fields:  w.field(*field)

        for i in indices:
            shape = shapefile.shape(i)
            w.poly(shapeType = 5, parts = [shape.points])
            w.record(*records[i])

        w.save(destination)

    def combine_NED(self, nedfiles, VPU):
        '''
        combines all NED files in the RPU regions for specified VPU into one big file for simplicity

        arguments:
            nedfiles: list of nedfiles for specified region
            VPU Vector Proecessing Unit specified
        '''
        DA = self.VPU_to_DA[VPU]


        destination = '{}/NHDPlus{}'.format(self.destination, DA)
        NHDPlus = '{}/NHDPlus{}'.format(destination, VPU)

        inmosaic = 'mosaic_{}.vrt'.format(DA)
        vrtcommand = 'gdalbuildvrt {}'.format(inmosaic)
        outmosaic = 'mosaic_{}.tif'.format(DA)

        #path to combined NED file
        nedfilepath = '{}/NEDSnapshot/Combined_NED'.format(NHDPlus)
        if not os.path.exists(nedfilepath):
            os.makedirs(nedfilepath)
        newfile = '{}/{}'.format(nedfilepath, outmosaic)
        for f in nedfiles:
            vrtcommand = vrtcommand + ' ' + f

        print('making combined file this might take awhile')
        os.system(vrtcommand)
        warpcommand = 'gdalwarp {} -co BIGTIFF=YES --config GDAL_CACHEMAX 6000 -wm 1500 {}'.format(inmosaic, newfile)
        os.system(warpcommand)
        raster = gdal.Open(newfile, GA_ReadOnly)
        band = raster.GetRasterBand(1)
        band.ComputeStatistics(False)
        newfile = None #save changes to file
        os.remove(inmosaic) #delete vrt
        combinednedfile = newfile = '{}/{}'.format(nedfilepath, outmosaic)


    def get_pixel(self, x, x0, width):
        """returns the pixel number for a coordinate value."""

        return int((x - x0) // width)

    def extract_NED(self,
                    nedfile,
                    catchmentfile,
                    destination,
                    zmin = -100000,
                    space = 0.05,
                    verbose = True,
                    quiet = True,
                    ):
        """
        Extracts elevation data as a raster file from the National Elevation
        Dataset located in the NHDPlus directory.
        """

        if verbose: print('copying the elevation data from NED\n')

        # get the coordinates for the bounding box from the flowline shapefile

        shapefile = Reader(catchmentfile)

        xmin, ymin, xmax, ymax = shapefile.bbox

        if quiet: gdal.PushErrorHandler('CPLQuietErrorHandler')

        # adjust to make the map just larger than the extents

        xmin = xmin - space * (xmax - xmin)
        ymin = ymin - space * (ymax - ymin)
        xmax = xmax + space * (xmax - xmin)
        ymax = ymax + space * (ymax - ymin)

        # get data for each file and store the values

        values = None


        if verbose: print('reading data from {}'.format(nedfile))



            # get the values of the DEM raster as an array and origin

        array, corner = self.get_raster_table(nedfile, [xmin, ymin, xmax, ymax], dtype = 'float')

        if values is None: values = array



        # find the indices of the missing data

        missing = numpy.where(values < zmin)

        # fill in the values

        values[missing] = array[missing]

        # open the file

        source = gdal.Open(nedfile)

        # set the transform to the new origin

        transform = source.GetGeoTransform()
        transform = (corner[0], transform[1], transform[2],
                     corner[1], transform[4], transform[1])

        # get the source band

        band = source.GetRasterBand(1)



        if verbose: print('')

        # get a driver and make the new file

        driver = gdal.GetDriverByName('GTiff')

        dest = driver.Create(destination, len(values[0]), len(values), 1,
                             gdal.GDT_UInt16)

        dest.SetProjection(source.GetProjection())
        dest.SetMetadata(source.GetMetadata())
        dest.SetGeoTransform(transform)

        dest.GetRasterBand(1).WriteArray(values, 0, 0)
        dest.GetRasterBand(1).SetNoDataValue(band.GetNoDataValue())
        #dest.GetRasterBand(1).SetStatistics(*band.GetStatistics(0,1))

        # close the files

        source = None
        dest   = None

        if verbose: print('successfully extracted elevation data to new file\n')

    def extract_HUC8(self,
                     VPU,
                     HUC8,                             # HUC8
                     output,                           # output directory
                     flowlinefile  = 'flowlines',      # flowline shapefile
                     catchmentfile = 'catchments',     # catchment shapefile
                     boundaryfile  = 'boundary',       # merged catchment file
                     VAAfile       = 'flowlineVAAs',   # VAA file
                     elevfile      = 'elevations.tif', # NED raster file
                     plotfile      = 'watershed',      # plot of the results
                     verbose       = True,             # print verbosity
                     vverbose      = True,            # print verbosity
                     ):
        """
        Creates shapefiles for the NHDPlus flowlines and catchments for an
        8-digit hydrologic unit code from the NHDPlus Version 2 source data.
        Output shapefiles are written to the optional "output" directory.
        """

        #getting proper files for vpu and huc8 selected
        start = time.time()
        DA = self.VPU_to_DA[VPU]

        destination = '{}/NHDPlus{}'.format(self.destination, DA)
        NHDPlus = '{}/NHDPlus{}'.format(destination, VPU)

        #catchment shapefile
        its = NHDPlus, 'Catchment'
        sourececatchmentfile = '{0}/NHDPlus{1}/{1}'.format(*its)

        #flowline shapefile
        its = NHDPlus, 'NHDSnapshot', 'Hydrography', 'NHDFlowline'
        sourceflowlinefile = '{}/{}/{}/{}'.format(*its)
        projection   = '{}/{}/{}/{}.prj'.format(*its)

        #NHDPlus attribute databases
        its = NHDPlus, 'NHDPlusAttributes'
        elevslopefile       = '{}/{}/elevslope.dbf'.format(*its)
        PlusFlowlineVAAfile = '{}/{}/PlusFlowlineVAA.dbf'.format(*its)

        #EROM database
        eromfile = '{}/EROMExtension/EROM_MA0001.dbf'.format(NHDPlus)

        # NED rasters -- there is more than one per VPU
        nedfiles = ['{}/NEDSnapshot/Ned{}/elev_cm'.format(NHDPlus,RPU)
                         for RPU in self.VPU_to_RPU[VPU]]

        newnedfile = '{}/NEDSnapshot/Combined_NED/mosaic_{}.tif'.format(NHDPlus,DA)
        if not os.path.isfile(newnedfile):
            self.combine_NED(nedfiles, VPU) #combine all the NED files into one big one

        # if the destination folder for the HUC8 does not exist, make it

        if not os.path.isdir(output): os.mkdir(output)

        # start by copying the projection files

        if vverbose: print('\ncopying the projections from NHDPlus\n')

        p = '{}/{}.prj'.format(output, flowlinefile)
        if not os.path.isfile(p): shutil.copy(projection, p)

        p = '{}/{}.prj'.format(output, catchmentfile)
        if not os.path.isfile(p): shutil.copy(projection, p)

        # extract the flowlines and get the NHDPlus comids

        p = '{}/{}'.format(output, flowlinefile)
        if not os.path.isfile(p + '.shp'):
            if verbose:
                print('extracting flowline shapefile for {}\n'.format(HUC8))
            self.extract_flowlines(sourceflowlinefile, p, HUC8,
                                   verbose = vverbose)

        # extract the different files from the sources sequentially

        p = '{}/{}'.format(output, catchmentfile)
        if not os.path.isfile(p + '.shp'):

            if verbose:
                print('extracting catchment shapefile for {}\n'.format(HUC8))
            self.extract_catchments(sourececatchmentfile, p, '{}/{}'.format(output, flowlinefile),
                                    verbose = vverbose)

        p = '{}/{}'.format(output, VAAfile)
        if not os.path.isfile(p):

        # get the comids using the flowline shapefile
            ffile = '{}/{}'.format(output, flowlinefile)
            comids = self.get_comids(ffile)

        # read hydrologic sequence and drainage attributes from the database
            if verbose:
                print('reading flowline value added attributes for ' + '{}\n'.format(HUC8))

            flowattributes = [['COMID', 'N', 9, 0], ['HYDROSEQ', 'N', 11, 0], ['UPHYDROSEQ','N', 11, 0],
                              ['DNHYDROSEQ','N', 11, 0], ['REACHCODE', 'C', 14, 0],['AREASQKM', 'N', 15, 6],
                              ['TOTDASQKM','N', 15, 6], ['DIVDASQKM','N', 15, 6]]
            flowvalues = self.read_dbf(PlusFlowlineVAAfile,
                                      attributes = flowattributes,
                                      comids = comids,
                                      verbose = vverbose)

            # read the slope data from the database
            if verbose:
                print('reading slope and elevation attributes for ' +
                          '{}\n'.format(HUC8))

            slopeattributes = [['COMID', 'N',9, 0], ['MAXELEVSMO', 'N', 12, 3], ['MINELEVSMO', 'N', 12, 3],['SLOPELENKM', 'N', 8, 3]]
            slopevalues = self.read_dbf(elevslopefile,
                                       attributes = slopeattributes,
                                       comids = comids,
                                       verbose = vverbose)

            # get the flow and velocity data
            eromattributes = [['COMID', 'N', 9, 0],  ['Q0001E', 'N', 15, 3], ['V0001E', 'N', 14, 5], ['SMGAGEID', 'C', 16, 0]]

            if verbose: print('reading EROM model attributes for ' +
                                  '{}\n'.format(HUC8))
            eromvalues = self.read_dbf(eromfile,
                                      attributes = eromattributes,
                                      comids = comids,
                                      verbose = vverbose)

            # store the flowline data in a dictionary using hydroseqs as keys
            # and make a dictionary linking the comids to hydroseqs

            flowlines = {}

            if verbose: print('making flowline dictionary')

            for flowlineVAAs in zip(*(flowvalues[a[0]] for a in flowattributes)):
                flowlines[flowlineVAAs[1]] = Flowline(*flowlineVAAs)

            for f in flowlines:

                if flowlines[f].comid in slopevalues['COMID']:
                    i = slopevalues['COMID'].index(flowlines[f].comid)

                    flowlines[f].add_slope(slopevalues['MAXELEVSMO'][i],
                                           slopevalues['MINELEVSMO'][i],
                                           slopevalues['SLOPELENKM'][i])

                if flowlines[f].comid in eromvalues['COMID']:
                    i = eromvalues['COMID'].index(flowlines[f].comid)
                    flowlines[f].add_flow(eromvalues['Q0001E'][i],
                                          eromvalues['V0001E'][i],
                                          eromvalues['SMGAGEID'][i])

                #catch for missing elevslope data points
                try:
                    flowlines[f].estimate_traveltime()
                except AttributeError:
                    pass

                # save the data in a dictionary for future use


            with open(p, 'wb') as f: pickle.dump(flowlines, f)

        # find the right NED DEM and extract the elevation raster

        p = '{}/{}'.format(output, elevfile)
        if not os.path.isfile(p):
            if verbose:
                print('extracting the NED raster file for {}\n'.format(HUC8))
            cfile = '{}/{}'.format(output, catchmentfile)
            self.extract_NED(newnedfile, cfile, p, verbose = verbose)

        end = time.time()
        t = end - start

        if verbose:
            print('successfully queried NHDPlus data for {} '.format(HUC8) +
                  'in {:.1f} seconds\n'.format(t))

        # merge the shapes into a watershed

        bfile = '{}/{}'.format(output, boundaryfile)
        if not os.path.exists(bfile + '.shp'):

            cfile = '{}/{}'.format(output, catchmentfile)
            merge_shapes(cfile, outputfile = bfile)

        # plot the results

        if plotfile is not None:

            flowfile = '{}/{}'.format(output, flowlinefile)
            cfile    = '{}/{}'.format(output, catchmentfile)
            bfile    = '{}/{}'.format(output, boundaryfile)
            VAAfile  = '{}/{}'.format(output, VAAfile)
            elevfile = '{}/{}'.format(output, elevfile)
            plotfiledestination = '{}/{}'.format(output, plotfile)

            if not os.path.isfile(plotfiledestination + '.png'):

                self.plot_HUC8(flowfile, cfile, bfile, VAAfile, elevfile,
                               output = plotfiledestination)

    def get_distance(self, p1, p2):
        """Approximates the distance in kilometers between two points on the
        Earth's surface designated in decimal degrees using an ellipsoidal
        projection. per CFR 73.208 it is applicable for up to 475 kilometers.
        p1 and p2 are listed as (longitude, latitude).
        """

        deg_rad = numpy.pi / 180

        dphi = p1[1] - p2[1]
        phim = 0.5 * (p1[1] + p2[1])
        dlam = p1[0] - p2[0]

        k1 = (111.13209 - 0.56605 * numpy.cos(2 * phim * deg_rad) + 0.00120 *
              numpy.cos(4 * phim * deg_rad))
        k2 = (111.41513 * numpy.cos(phim * deg_rad) - 0.09455 *
              numpy.cos(3 * phim * deg_rad) + 0.0012 *
              numpy.cos(5 * phim * deg_rad))

        return numpy.sqrt(k1**2 * dphi**2 + k2**2 * dlam**2)

    def get_boundaries(self, shapes, space = 0.1):
        """
        Gets the boundaries for the plot.
        """

        boundaries = shapes[0].bbox
        for shape in shapes[0:]:
            b = shape.bbox
            if b[0] < boundaries[0]: boundaries[0] = b[0]
            if b[1] < boundaries[1]: boundaries[1] = b[1]
            if b[2] > boundaries[2]: boundaries[2] = b[2]
            if b[3] > boundaries[3]: boundaries[3] = b[3]

        xmin = boundaries[0] - (boundaries[2] - boundaries[0]) * space
        ymin = boundaries[1] - (boundaries[3] - boundaries[1]) * space
        xmax = boundaries[2] + (boundaries[2] - boundaries[0]) * space
        ymax = boundaries[3] + (boundaries[3] - boundaries[1]) * space

        return xmin, ymin, xmax, ymax

    def get_remainder(self, x, x0, width):
        """
        returns the remainder for the pixel.
        """

        return (x - x0) % width

    def make_patch(self,
                   points,
                   facecolor,
                   edgecolor = 'Black',
                   width = 1,
                   alpha = None,
                   hatch = None,
                   label = None,
                   ):
        """Uses a list or array of points to generate a matplotlib patch."""

        vertices = [(point[0], point[1]) for point in points]
        vertices.append((points[0][0], points[0][1]))

        codes     = [path.Path.LINETO for i in range(len(points) + 1)]
        codes[0]  = path.Path.MOVETO

        patch = patches.PathPatch(path.Path(vertices, codes),
                                  facecolor = facecolor,
                                  edgecolor = edgecolor,
                                  lw = width,
                                  hatch = hatch,
                                  alpha = alpha,
                                  label = label)
        return patch

    def add_raster(self,
                   fig,
                   filename,
                   resolution,
                   extent,
                   colormap,
                   scale,
                   ):
        """
        adds a rectangular raster image with corners located at the extents
        to a plot.
        """

        # flatten the arrays and set up an array for the raster

        xmin, ymin, xmax, ymax = extent

        xs = numpy.array([xmin + (xmax - xmin) / resolution * i
                          for i in range(resolution + 1)])
        ys = numpy.array([ymax  - (ymax  - ymin)  / resolution * i
                          for i in range(resolution + 1)])

        zs = numpy.zeros((resolution + 1, resolution + 1))

        # iterate through the grid and fill the array

        for i in range(len(ys)):
            zs[i, :] = self.get_raster(filename, zip(xs, [ys[i]] * (resolution + 1)),
                                  quiet = True)

        # scale the values

        zs = zs / scale
        space = 0.1

        # deal with missing values

        mi = numpy.min(zs[numpy.where(zs > 0)])
        ma = zs.max()

        mi, ma = mi - space * (ma - mi), ma + space * (ma - mi)
        norm = colors.Normalize(vmin = mi, vmax = ma)

        # plot the grid

        return fig.imshow(zs, extent = [xmin, xmax, ymin, ymax], norm = norm,
                          cmap = colormap)

    def plot_HUC8(self,
                  flowfile,
                  cfile,
                  bfile,
                  VAAfile,
                  elevfile,
                  vmin = 0.1,
                  patchcolor = None,
                  resolution = 400,
                  colormap = 'gist_earth',
                  grid = False,
                  title = None,
                  verbose = True,
                  output = None,
                  show = False,
                  ):
        """
        Makes a plot of the raw NHDPlus data.
        """

        if verbose: print('generating plot of the watershed\n')

        fig = pyplot.figure()
        subplot = fig.add_subplot(111, aspect = 'equal')
        subplot.tick_params(axis = 'both', which = 'major', labelsize = 10)

        # add the title

        if title is not None: subplot.set_title(title, fontsize = 14)

        if patchcolor is None: facecolor = (1,0,0,0.)
        else:                  facecolor = patchcolor

        # open up and show the boundary

        b = Reader(bfile, shapeType = 5)

        boundary = b.shape(0)
        points = numpy.array(boundary.points)
        subplot.add_patch(self.make_patch(points, facecolor, width = 0.5))

        # open up and show the catchments

        c = Reader(cfile, shapeType = 5)

        extent = self.get_boundaries(c.shapes(), space = 0.02)

        xmin, ymin, xmax, ymax = extent

        # figure out how far one foot is on the map

        points_per_width = 72 * 8
        ft_per_km = 3280.84
        scale_factor = (points_per_width /
                        self.get_distance([xmin, ymin], [xmax, ymin]) /
                        ft_per_km)

        # make patches of the catchment area

        for i in range(len(c.records())):
            catchment = c.shape(i)
            points = numpy.array(catchment.points)
            subplot.add_patch(self.make_patch(points, facecolor, width = 0.1))

        # get the flowline attributes, make an "updown" dictionary to follow
        # flow, and change the keys to comids

        with open(VAAfile, 'rb') as f: flowlineVAAs = pickle.load(f)

        updown = {}
        for f in flowlineVAAs:
            if flowlineVAAs[f].down in flowlineVAAs:
                updown[flowlineVAAs[f].comid] = \
                    flowlineVAAs[flowlineVAAs[f].down].comid

        flowlineVAAs = {flowlineVAAs[f].comid:flowlineVAAs[f]
                        for f in flowlineVAAs}

        # open up and show the flowfiles

        f = Reader(flowfile, shapeType = 3)
        comid_index = f.fields.index(['COMID', 'N',  9, 0]) - 1

        all_comids = [r[comid_index] for r in f.records()]

        # get the flows and velocities from the dictionary

        widths = []
        comids = []
        for comid in all_comids:
            if comid in flowlineVAAs:
                flow = flowlineVAAs[comid].flow
                velocity = flowlineVAAs[comid].velocity

                # estimate flow width (ft) assuming triangular 90 d channel

                comids.append(comid)

                if velocity < 0: widths.append(numpy.sqrt(4 * flow / vmin))
                else:            widths.append(numpy.sqrt(4 * flow / velocity))

        # convert widths in feet to points on the figure; exaggerated by 10

        widths = [w * scale_factor * 20 for w in widths]

        # get the flowline and the corresponding catchment

        for comid, w in zip(comids, widths):

            i = all_comids.index(comid)
            flowline = numpy.array(f.shape(i).points)

            # plot it

            subplot.plot(flowline[:, 0], flowline[:, 1], 'b', lw = w)

        subplot.set_xlabel('Longitude, Decimal Degrees', size = 13)
        subplot.set_ylabel('Latitude, Decimal Degrees',  size = 13)

        # add the NED raster

        im = self.add_raster(subplot, elevfile, resolution, extent,
                             colormap, 100)

        divider = make_axes_locatable(subplot)
        cax = divider.append_axes('right', size = 0.16, pad = 0.16)
        colorbar = fig.colorbar(im, cax = cax, orientation = 'vertical')
        colorbar.set_label('Elevation, m', size = 12)
        cbax = pyplot.axes(colorbar.ax)

        for t in cbax.get_yaxis().get_majorticklabels(): t.set_fontsize(10)

        subplot.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
        subplot.yaxis.set_major_locator(ticker.MultipleLocator(0.2))

        if grid:

            subplot.xaxis.grid(True, 'minor', linestyle = '-', linewidth = 0.5)
            subplot.yaxis.grid(True, 'minor', linestyle = '-', linewidth = 0.5)

        # show it

        pyplot.tight_layout()

        if output is not None:  pyplot.savefig(output)

        if show: pyplot.show()

        pyplot.close()
        pyplot.clf()
