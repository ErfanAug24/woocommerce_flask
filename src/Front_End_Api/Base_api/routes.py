from flask import Blueprint

base_header_urls = Blueprint('base_header_urls', __name__)


@base_header_urls.route('/')
@base_header_urls.route('/home')
def home():
    return {'page': 'home'}


@base_header_urls.route('/about_us')
def about_us():
    return {'page': 'about_us'}


@base_header_urls.route('/contact_us')
def contact_us():
    return {'page': 'contact_us'}


@base_header_urls.route('/privacy')
def privacy_and_policy():
    return {'page': 'privacy_and_policy'}
