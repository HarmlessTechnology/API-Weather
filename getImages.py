# API Weather support file
#V0.5
import os
import urllib.request

d_image = ['01d.png', '02d.png', '03d.png', '04d.png', '09d.png', '10d.png', '11d.png', '13d.png', '50d.png']
n_image = ['01n.png', '02n.png', '03n.png', '04n.png', '09n.png', '10n.png', '11n.png', '13n.png', '50n.png']
link = 'https://openweathermap.org/img/w/'
folder = './image/'

if not os.path.exists(folder):
    os.makedirs(folder)

# Get daytime weather icons
for stock_image in d_image:
    local_image = folder + stock_image
    if not os.path.exists(local_image):
        urllib.request.urlretrieve(link + stock_image, local_image)

# Get nighttime weather icons
for stock_image in n_image:
    local_image = folder + stock_image
    if not os.path.exists(local_image):
        urllib.request.urlretrieve(link + stock_image, local_image)
