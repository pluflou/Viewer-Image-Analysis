for file in /home/sara/Documents/SECAR/Diagnostics/Viewer-Image-Analysis/images/stability_FP2/*.tiff
do 
	 python ./src/im_analysis.py "$file"
done
