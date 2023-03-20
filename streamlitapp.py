# stremlit app to view the videos stocked in videos/ folder

import streamlit as st
import os
import pandas as pd
import datetime

st.sidebar.title('Navigation')

# pages
pages = ["picture Viewer","Video Viewer", "Graph Viewer"]

# select the page
page = st.sidebar.selectbox('Select a page', pages)

# display the page
if page == "picture Viewer":
    st.title('Picture Viewer')
    st.write('Select a picture to view')

    # get the list of pictures
    pictures = os.listdir('pictures')

    # select the picture to view
    picture = st.selectbox('Select a picture', pictures)

    #  get the date of creation of the picture
    st.write('Date of creation of the picture')
    date = os.path.getmtime('pictures/' + picture)
    st.write(datetime.datetime.fromtimestamp(date))

    # read the picture
    st.image('pictures/' + picture)

    #  get all dates of all pictures
    dates = []
    for picture in pictures:
        dates.append(datetime.datetime.fromtimestamp(os.path.getmtime('pictures/' + picture)))
    
    start_date, end_date = st.slider('Select a date range', min_value=min(dates), max_value=max(dates), value=(min(dates), max(dates)), format='ss:mm:HH DD/MM/YYYY')

    # button to make a timelaps
    if st.button('Make a timelaps'):
        #  make a timelaps of the pictures between the dates using ffmpeg
        # build list of pictures to use
        pictures_to_use = []
        for picture in pictures:
            val = datetime.datetime.fromtimestamp(os.path.getmtime('pictures/'+picture))
            if val >= start_date and val <= end_date:
                pictures_to_use.append(picture)
        #  for each chosen picture, rename it to 0%5d.jpg
        new_names= []
        for i, picture in enumerate(pictures_to_use):
            new_names.append(f'{i:05d}.png')
            os.rename('pictures/'+picture, 'pictures/'+f'{i:05d}.png')
        
        # build the name of the video
        vid_name = start_date.strftime('%Y-%m-%d_%H-%M-%S_') + end_date.strftime('%Y-%m-%d_%H-%M-%S')+ '.mp4'
        # build the command
        command = f'ffmpeg -framerate 1 -i pictures/%05d.png -c:v libx264 -r 30 -pix_fmt yuv420p videos/{vid_name}'
        # execute the command
        res = os.system(command)
        if res == 0:
            st.write(f'Timelaps created {vid_name}')
            #  erase the pictures
            for picture in new_names:
                os.remove('pictures/'+picture)

        else:
            st.write('Error creating timelaps') 


if page == "Video Viewer":
    # st.set_page_config(layout="wide")
    st.title('Video Viewer')
    st.write('Select a video to view')

    # get the list of videos
    videos = os.listdir('videos')

    # select the video to view
    video = st.selectbox('Select a video', videos)

    # play the video
    st.video('videos/' + video)

if page == "Graph Viewer":
    st.title('Graph Viewer')
    #  display the csv
    st.write('Display the csv')

    # get the list of csv
    csvs = os.listdir('csvs')

    # select the csv to view
    csv = st.selectbox('Select a csv', csvs)

    # display the csv
    st.write('Display the csv')

    # read the csv
    df = pd.read_csv('csvs/' + csv)

    # display the csv as graph
    st.line_chart(df)


