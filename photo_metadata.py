import os
import glob
import time
import pandas as pd
import numpy as np
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
if __name__== "__main__":

    #path where the folders with the photos are located
    path="/home/usuario/scraping-instagram/location_scraper"
    folders=[x[0] for x in os.walk(path)]
    df=pd.DataFrame(columns=["title","owner_id","profile","date","url","likes","comments","text","place","latitude","longitude"])
    
    for folder in folders[1:]:
        for file in os.listdir(folder):
            if file.endswith(".txt"):
                f=open(folder+"/"+file,"r")
                metadata=f.read()
                metadata=metadata.split(",")
                df.loc[metadata[0],"title"]=metadata[2]
                df.loc[metadata[0],"owner_id"]=metadata[4]
                df.loc[metadata[0],"date"]=metadata[5]
                df.loc[metadata[0],"url"]=metadata[6]
                df.loc[metadata[0],"likes"]=metadata[7]
                df.loc[metadata[0],"comments"]=metadata[8]
                df.loc[metadata[0],"latitude"]=metadata[-2]
                df.loc[metadata[0],"longitude"]=metadata[-1]
                df.loc[metadata[0],"profile"]=metadata[3]
                df.loc[metadata[0],"place"]=metadata[-4]
                df.loc[metadata[0],"text"]=str(metadata[9:-5])
                

    fix_longitudes= lambda x : x.replace(")\n","").replace("lng=","")
    fix_latitudes= lambda x : x.replace("lat=","")
    fix_place=lambda x : x.replace("slug=","").replace("'","")

    new_lats=np.array(list(map(fix_latitudes,df.latitude)))
    df.latitude=new_lats
    
    new_lons=np.array(list(map(fix_longitudes,df.longitude)))
    df.longitude=new_lons

    new_place=list(map(fix_place,df.place))
    df.place=new_place

    df["id"]=df.index
    df.replace(None,np.nan,inplace=True,regex="None")
    print(df.info())
    df.to_csv("metadata_photos.csv",index=False)
    gdf=gpd.GeoDataFrame(df,crs="EPSG:4326",geometry=gpd.points_from_xy(df.longitude,df.latitude))
 
    fig=plt.figure()
    ax=fig.add_subplot(111)
    gdf.plot(ax=ax)
    ctx.add_basemap(ax=ax, crs=gdf.crs, source= ctx.providers.OpenStreetMap.DE.url)
    plt.show()
    
