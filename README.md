Python Web Framework with Django @ SoftUni

This repo was created for the 'Python Web Framework' course at SoftUni. It contains a Django project with a web app for the final exam.

The main idea behind the project is to create an operational web application which allows users to register, create/edit profiles, create/edit tasks, create/edit and manage vacations also the app offers a simple news board with comments on the homepage.

The project consists of main app called 'TaskManager', staticfiles folder, templates folder, mediafiles folder.

The project app uses Postgresql as a DBMS.

The app can send automatic emails via AWS SES.

The project app uses environment variables to hide sensitive information.

DISCLAIMER: This app is not a fully operational product, it's not intended for commercial use and has many features that haven't been properly tested or developed.

HOW TO BUILD:

In a new vnv:

1. pip install requirements.txt

setup your .env file:
DEBUG=on
SECRET_KEY='YOUR_SECRET'
CLOUDINARY_CLOUD_NAME='YOUR_CLOUDINARY_CLOUD_NAME'
CLOUDINARY_API_KEY='YOUR_CLOUDINARY_API_KEY'
CLOUDINARY_API_SECRET='YOUR_CLOUDINARY_API_SECRET'

HOW TO USE:

In "mango_product_data" folder run:

scrapy crawl single_site_product_scraper_loc -o mango_data_loc.json
