import streamlit as st
st.set_page_config(layout="wide")

import json
import pandas as pd
import requests

FILE_URL='https://raw.githubusercontent.com/cheongqinxue/sector_classifier_results/main/mined_sample_multilang.json'

@st.cache
def downloadjsondata():
    resp = requests.get(FILE_URL)
    return resp.text

if __name__ == '__main__':
    data = downloadjsondata()
    df = pd.DataFrame(json.loads(data))
    lang = st.sidebar.selectbox(label='Filter by language', options=['all','en','es','pt','ar'])
    df.drop_duplicates(subset='title', inplace=True)
    if lang != 'all':
        df = df[df.language==lang]
    template = '<span style="border:1px solid lightgrey; font-family:monospace;font-size:11px;color:grey;padding:3px;margin:3px">{}</span>'
    for i in range(len(df)):
        title = f"SN {df.iloc[i]['index']}: " + df.iloc[i].title
        pred = df.iloc[i].predictions
        st.markdown( 
            f'<span style="font-size:14px; font-weight:bold; margin-right:5px">{title}</span>' + \
            ''.join([template.format(p) for p in pred]), unsafe_allow_html=True)
        with st.expander('Read content'):
            st.markdown(df.iloc[i].content)

