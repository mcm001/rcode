clc
clear

data = csvread("D:\Documents\GitHub\rcode\eggfinder_gps_stuff\latlong.csv");

data( ~any(data,2), : ) = [];  %rows

lat = data(:,2);
lon = data(:,1);

geoplot(lat, lon,'-*')
%geolimits([45 62],[-149 -123])
geobasemap satellite