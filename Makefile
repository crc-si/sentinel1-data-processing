

get-sample:
	wget http://ec2-52-201-154-0.compute-1.amazonaws.com/datacube/ui_results/static_files/s1_swiss_cube_2017.tif  -O data/s1_swiss_cube_2017.tif
	wget http://ec2-52-201-154-0.compute-1.amazonaws.com/datacube/ui_results/static_files/s1_swiss_cube.csv  -O data/s1_swiss_cube.csv 

get-config:
	wget http://ec2-52-201-154-0.compute-1.amazonaws.com/datacube/ui_results/static_files/ingestS1GEE.tar
	tar -xzvf ingestS1GEE.tar
