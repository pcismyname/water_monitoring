import math
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import time
import pymongo

st.set_page_config(page_title="Vertiz Dashboard",
                    page_icon=":bar_chart:",
                    layout="wide")

MONGO_DETAILS = "mongodb://tesarally:contestor@mongoDB:27017"

def init_connection():
    return pymongo.MongoClient(MONGO_DETAILS)

client = init_connection()

def get_data():
    db = client.mockupdata
    items = db.waterdata.find()
    items = list(items)  # make hashable for st.cache_data
    return items
def get_height_s1():
    db = client.water_data
    height_s1 = db.height_s1_collection.find()
    height_s1 = list(height_s1)
    return height_s1
def get_height_s3():
    db = client.water_data
    height_s3= db.height_s3_collection.find()
    height_s3 = list(height_s3)
    return height_s3

def get_prediction():
    db = client.water_data
    prediction = db.predict_data.find()
    prediction = list(prediction)
    return prediction

height_s1 = get_height_s1()
height_s1_frame = pd.DataFrame(height_s1)
height_s1_frame = height_s1_frame.drop(columns=['_id'])
height_s1_frame = height_s1_frame.rename_axis('Day')
height_s1_frame = height_s1_frame.rename(columns={'height': 'Height S1 (m)'})
day_s1 = height_s1_frame.index.astype(int) + 1

height_s3 = get_height_s3()
height_s3_frame = pd.DataFrame(height_s3)
height_s3_frame = height_s3_frame.drop(columns=['_id'])
height_s3_frame = height_s3_frame.rename_axis('Day')
height_s3_frame = height_s3_frame.rename(columns={'height': 'Height S3 (m)'})
day_s3 = height_s3_frame.index.astype(int) + 1

pred = get_prediction()
pred_frame = pd.DataFrame(pred)
#get 5 last prediction
last_pred = pred_frame.iloc[-5:]
#drop index
last_pred = last_pred.drop(columns=['_id'])



st.title('Data Monitoring System 🌊')
st.sidebar.image("https://tu.ac.th/uploads//main-logo.svg", use_column_width=True)
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Go to", ('Home', 'Charts', 'Download here'))
# st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/6/6b/Seal_of_Ubon_Ratchathani.png")

if page == 'Home':  
        st.title("station 1 water level prediction in next 5 days")
        col = st.columns(5)
        for i in range(5):
            col[i].metric(label=f"Day {i+1}", value=(f"{last_pred.iloc[i, 0]:.4f} m"))
        st.warning('สภาวะน้ำใกล้ตลิ่งชันโปรดระวังน้ำท่วม', icon="⚠️")
        #show map in ubon
        data = {
            'lat': [15.223,15.1334],
            'lon': [104.8580,104.7033],
            'city': ['Station 1', 'Station 2']
        }   
        df = pd.DataFrame(data)
        st.map(df)
elif page == "Download here":
    tab1, tab2 = st.tabs(["Station1", "Station3"])
    with tab1:
        st.title("station 1")
        st.dataframe(height_s1_frame)
    with tab2:
        st.title("station 3")
        st.dataframe(height_s3_frame)
else:
    tab1, tab2 = st.tabs(["Station1", "Station3"])
    with tab1:
        st.title("station 1 water level")
        height_s1_frame = height_s1_frame.iloc[-30:,:]
        st.bar_chart(height_s1_frame.iloc[-30:,:])

    with tab2:
        st.title("station 3 water level")
        #last 30 days
        height_s3_frame = height_s3_frame.iloc[-30:,:]
        st.bar_chart(height_s3_frame.iloc[-30:,:])

time.sleep(3)
st.rerun()



