import json
from datetime import datetime, timedelta

import redis
from dataclasses import dataclass

import pickle
from itertools import groupby


@dataclass
class VesselData:
    ais_n: int
    registered: datetime
    lon: float
    lat: float
    SOG: float
    COG: float
    heading: int
    draught: float
    vessel_id: int

    @classmethod
    def from_row(cls, row):
        return cls(
            ais_n=int(row[0]),
            registered=datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f'),
            lon=float(row[2]) / (10000 * 60),
            lat=float(row[3]) / (10000 * 60),
            SOG=float(row[4]),
            COG=float(row[5]),
            heading=row[6],
            draught=float(row[7] or 0),
            vessel_id=int(row[8]),
        )

    def to_json(self, vessel_data):
        return json.dumps({
            'registered': self.registered.isoformat(),
            'lat': self.lat,
            'lon': self.lon,
            'SOG': self.SOG,
            'COG': self.COG,
            'length': vessel_data['length'] if vessel_data else None,
            'width': vessel_data['width'] if vessel_data else None,
            'name': vessel_data['name'] if vessel_data else None
        })

def main():
    r = redis.Redis(host='localhost', port=6379)

    with open('SHIP2_rmp_Vessel_Kerch.csv') as f:
        lines = f.readlines()
    vessels = {}
    for line in lines:
        try:
            _, id_, name, uid, imo, length, width, date = map(str.strip, line.split(','))
            vessel = {
                'id': int(id_ or -1),
                'name': name,
                'uid': uid or -1,
                'imo': int(imo or -1),
                'length': int(length or -1),
                'width': int(width or -1),
                'date': date,
            }
            vessels[int(id_)] = vessel
            r.set(f'vessels:{id_}', json.dumps(vessel))
        except Exception as e:
            print(e)

    with open('SHIP2_rmp_AISData_Kerch.csv') as f:
        lines = f.readlines()


    data = []
    for line in lines:
        s_data = VesselData.from_row(list(map(str.strip, line.split(','))))
        data.append(s_data)

    pickle.dump(data, open('data.pkl', 'wb'))



if __name__ == '__main__':
    with open('SHIP2_rmp_Vessel_Kerch.csv') as f:
        lines = f.readlines()
    vessels = {}
    for line in lines:
        try:
            id_, _, name, uid, imo, length, width, date = map(str.strip, line.split(','))
            vessel = {
                'id': int(id_ or -1),
                'name': name,
                'uid': uid or -1,
                'imo': int(imo or -1),
                'length': int(length or -1),
                'width': int(width or -1),
                'date': date,
            }
            vessels[int(id_)] = vessel
        except Exception as e:
            print(e)


    data = pickle.load(open('data.pkl', 'rb'))
    r = redis.Redis()
    current_date = datetime(2020, 2, 11)
    while True:
        print(current_date)
        for key, group in groupby(sorted(data, key=lambda x: x.vessel_id), key=lambda x: x.vessel_id):
            d = list(sorted(filter(lambda x: x.registered <= current_date, group), key=lambda x: x.registered))
            if not d:
                continue
            d = d[-1]
            r.sadd(f'ship_data:{current_date.isoformat().replace(":", "_")}', d.to_json(vessels.get(d.vessel_id)))
        current_date += timedelta(minutes=30)

        if current_date > datetime(2020, 3, 11):
            break