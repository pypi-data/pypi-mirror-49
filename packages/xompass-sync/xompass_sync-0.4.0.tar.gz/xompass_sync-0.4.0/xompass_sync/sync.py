import requests
from shapely.geometry.polygon import Polygon


class InvalidResponse(Exception):
    def __init__(self, res):
        super().__init__(f'Invalid response: {res.status_code}')
        self.res = res


class InvalidSensorData(Exception):
    def __init__(self, msg):
        super().__init__(f'Invalid sensor data: {msg}')


class Sensor:
    def __init__(self, sensor_datum):
        self.id = sensor_datum['id']
        self.name = sensor_datum['name']
        self.type = sensor_datum['type']
        self.parameters = sensor_datum['parameters']


class ConcentrationAlert(Sensor):
    def __init__(self, sensor_datum):
        super().__init__(sensor_datum)

        def tpoint(point):
            return (point['x'], point['y'])
        self.polygon = Polygon([tpoint(p) for p in self.parameters['points']])

    def __repr__(self):
        return f'ConcentrationAlert({self.polygon})'


class ObjectRecognition(Sensor):
    def __init__(self, sensor_datum):
        super().__init__(sensor_datum)

    def __repr__(self):
        return f'ObjectRecognition({self.id})'


class CrossLineMultiRecognition(Sensor):
    def __init__(self, sensor_datum):
        super().__init__(sensor_datum)

        if not 'points' in self.parameters:
            raise InvalidSensorData('Expecting "points" in CLMR')
        if not type(self.parameters['points']) is list:
            raise InvalidSensorData('Expecting "points" to be list in CLMR')
        if len(self.parameters['points']) < 2:
            raise InvalidSensorData(
                'Expecting len("points") to be at least 2 in CLMR')

    def clr(self):
        return {
            'id': self.id,
            'x1': self.parameters['points'][0]['x'],
            'y1': self.parameters['points'][0]['y'],
            'x2': self.parameters['points'][1]['x'],
            'y2': self.parameters['points'][0]['y'],
            'multi': True
        }

    def __repr__(self):
        return f'CLMR({self.clr()})'


class QueueSize(Sensor):
    def __init__(self, sensor_datum):
        super().__init__(sensor_datum)

        def tpoint(point):
            return (point['x'], point['y'])
        self.polygon = Polygon([tpoint(p) for p in self.parameters['points']])

    def __repr__(self):
        return f'QueueSize({self.polygon})'


class CrossedBarriersDetection(Sensor):
    def __init__(self, sensor_datum):
        super().__init__(sensor_datum)

        if type(self.parameters) is not dict:
            raise InvalidSensorData(
                'Expecting root.parameters dict')
        if not 'barriers' in self.parameters:
            raise InvalidSensorData(
                'Expecting root.parameters.barriers to exist')
        barriers = self.parameters['barriers']
        if type(barriers) is not list:
            raise InvalidSensorData(
                'Expecting root.parameters.barriers list')
        if len(barriers) < 2:
            raise InvalidSensorData('Expecting at least 2 barriers')
        for i, barrier in enumerate(barriers[:2]):
            if type(barrier) is not dict:
                raise InvalidSensorData(
                    f'Expecting root.parameters.barriers[{i}] dict')
            if not 'barrier' in barrier:
                raise InvalidSensorData(
                    f'Expecting root.parameters.barriers[{i}].barrier to exist')
            lines = barrier['barrier']
            if type(lines) is not list:
                raise InvalidSensorData(
                    f'Expecting root.parameters.barriers[{i}].barrier list')
            for j, line in enumerate(lines):
                if type(line) is not dict:
                    raise InvalidSensorData(
                        f'Expecting root.parameters.barriers[{i}].barrier[{j}] dict')
                if not 'points' in line:
                    raise InvalidSensorData(
                        f'Expecting root.parameters.barriers[{i}].barrier[{j}].points to exist')
                points = line['points']
                if type(points) is not list:
                    raise InvalidSensorData(
                        f'Expecting root.parameters.barriers[{i}].barrier[{j}].points list')
                if len(points) < 2:
                    raise InvalidSensorData('Expecting at least 2 points')
                for k, point in enumerate(points[:2]):
                    if type(point) is not dict:
                        raise InvalidSensorData(
                            f'Expecting root.parameters.barriers[{i}].barrier[{j}].points[{k}] dict')
                    if not 'x' in point:
                        raise InvalidSensorData(
                            f'Expecting root.parameters.barriers[{i}].barrier[{j}].points[{k}].x to exist')
                    if not 'y' in point:
                        raise InvalidSensorData(
                            f'Expecting root.parameters.barriers[{i}].barrier[{j}].points[{k}].y to exist')

        barriers = self.parameters['barriers']
        a, b = barriers[0]['barrier'], barriers[1]['barrier']

        def seg(i):
            x1 = i['points'][0]['x']
            y1 = i['points'][0]['y']
            x2 = i['points'][1]['x']
            y2 = i['points'][1]['y']
            return x1, y1, x2, y2

        self.segment_a = [seg(i) for i in a]
        self.segment_b = [seg(i) for i in b]

        self.segments_a = [seg(i) for i in a]
        self.segments_b = [seg(i) for i in b]

    def __repr__(self):
        return f'CrossedBarriersDetection({self.id})'


class Asset:
    def __init__(self, asset_id, sensors_data):
        self.id = asset_id

        def mksensor(datum):
            if datum['type'] == 'ConcentrationAlert':
                return ConcentrationAlert(datum)
            elif datum['type'] == 'ObjectRecognition':
                return ObjectRecognition(datum)
            elif datum['type'] == 'CrossLineMultiRecognition':
                return CrossLineMultiRecognition(datum)
            elif datum['type'] == 'QueueSize':
                return QueueSize(datum)
            elif datum['type'] == 'CrossedBarriersDetection':
                return CrossedBarriersDetection(datum)
        self.sensors = [mksensor(s) for s in sensors_data if s['enabled']]

    def __repr__(self):
        return f'Asset(sensors={[s.type for s in self.sensors if s is not None]})'


def download_asset(asset_id, api_key):
    url = f'https://bridge-staging.xompass.com/api/Assets/{asset_id}/Sensors?api_key={api_key}'
    res = requests.get(url)
    if res.status_code != 200:
        raise InvalidResponse(res)
    return Asset(asset_id, res.json())


def download_sensor(asset_id, sensor_id, api_key):
    url = f'https://bridge-staging.xompass.com/api/Assets/{asset_id}/Sensors/{sensor_id}?api_key={api_key}'
    res = requests.get(url)
    if res.status_code != 200:
        raise InvalidResponse(res)
    asset = Asset(asset_id, [res.json()])
    return asset.sensors[0]
