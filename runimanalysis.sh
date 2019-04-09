for file in /mnt/daqtesting/secar_camera/new_captures/April_5/D1542/*
do 
	 python ./src/im_analysis.py "$file"
done
