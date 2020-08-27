from datetime import datetime
from flask import render_template, redirect, url_for, request, abort
from . import main
from flask_login import login_user, login_required, logout_user, current_user
import smartcar
# from ..db import db_session, Car, User
from .. import db
from ..models import User, Car, load_user
from flask import current_app
from flask_cors import CORS
from flask_googlemaps import GoogleMaps, Map

COMPATIBLE_MAKES = [
    'AUDI', 'BMW', 'BUICK', 'CADILLAC', 'CHEVROLET', 'CHRYSLER', 'DODGE', 'FORD', 'GMC', 'HYUNDAI',
    'JAGUAR', 'JEEP', 'LAND ROVER', 'LEXUS', 'LINCOLN', 'NISSAN', 'RAM', 'TESLA', 'VOLKSWAGEN',
]

CORS(current_app)
GoogleMaps(current_app)

smartcar_client = smartcar.AuthClient(
    client_id=current_app.config['CLIENT_ID'],
    client_secret=current_app.config['CLIENT_SECRET'],
    redirect_uri=current_app.config['REDIRECT_URI'],
    scope=['required:read_vehicle_info', 'read_vin', 'required:read_location', 'read_odometer', 'read_fuel',
           'read_battery', 'read_engine_oil'],
    test_mode=True,
)


@main.route('/', methods=['GET', 'POST'])
def index():
    cars = None
    user_id = current_user.get_id()
    if user_id is not None:
        user = load_user(user_id)
        user_cars = db.session.query(Car).filter(Car.user == user).all()
        cars = [CarData(check_update_car(user_car)) for user_car in user_cars]

    return render_template('index.html', cars=cars)


@main.route('/car/<car_id>')
@login_required
def car(car_id):
    user_car = Car.query.filter_by(u_id=car_id).first()
    user_id = current_user.get_id()
    user = load_user(user_id)
    if user_car is None or user_car.user != user:
        abort(404)

    car = CarData(check_update_car(user_car))

    return render_template('car.html', car=car)


@main.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    auth_url = smartcar_client.get_auth_url()
    return redirect(auth_url)


@main.route('/exchange', methods=('GET', 'POST'))
@login_required
def exchange():
    # global access
    code = request.args.get('code')
    access = smartcar_client.exchange_code(code)
    cars_params = get_cars_params(access)
    for car_params in cars_params:
        car = Car(**car_params)
        db.session.add(car)
    db.session.commit()
    return redirect(url_for('main.index'))


def get_cars_params(access):
    # global access
    params = []
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    user = User.query.get(current_user.get_id())
    for vehicle_id in vehicle_ids:
        dct = {'u_id': vehicle_id}
        vehicle = smartcar.Vehicle(vehicle_id, access['access_token'])
        dct['make'] = vehicle.info()['make']
        for key in access.keys():
            if key in ['access_token', 'refresh_token', 'expiration', 'refresh_expiration']:
                dct[key] = access[key]
        dct['user'] = user
        params.append(dct)
    return params


def check_update_car(car):
    if smartcar.is_expired(car.expiration):
        new_access = smartcar_client.exchange_refresh_token(car.refresh_token)
        car.access_token = new_access['access_token']
        car.expiration = new_access['expiration']
        car.refresh_token = new_access['refresh_token']
        car.refresh_expiration = new_access['refresh_expiration']
    return car


class CarData:
    def __init__(self, car):
        self.id = car.u_id
        self.access_token = car.access_token
        self.make = car.make

        connected_car = smartcar.Vehicle(self.id, self.access_token)
        location = connected_car.location()['data']
        info = connected_car.info()

        self.model = info['model']
        self.year = info['year']
        self.full_name = '{} {} {}'.format(self.make, self.model, self.year)
        self.lat = location['latitude']
        self.lng = location['longitude']

        self.map = Map(identifier='{}'.format(self.id), lat=self.lat, lng=self.lng)
