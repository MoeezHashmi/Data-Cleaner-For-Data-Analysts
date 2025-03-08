import streamlit as st  
import pandas as pd 
import os
from io import BytesIO


st.set_page_config(page_title="DATA SWEEPER", layout="wide")
st.title("🏐Data Sweeper")
st.write(" Transform your files between CSV and Excel formats with bulit-in data cleaning and visalization!.")

uploaded_file= st.file_uploader("Upload your CSV or Excel Files.", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file :
    for file in uploaded_file :
        file_ext = file.name.split("file.name")[-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext ==".xlsx":
            df=pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue
#display info about the file 
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")


        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

#option for Data Cleaning
        st.subheader("⚙️Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicate from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicate Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Value have been Filled")

        
        st.subheader("📍Select Column to Convert")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]


        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visiualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
            
        #convert the file -> Csv to Excel
        st.subheader("🔁Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:",["CSV","EXCEL"], key=file.name)
        if st.button(f"Convert{file.name}"):
            buffer = BytesIO ()
            if conversion_type == "CSV":
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mim_type = "text/csv"
                
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mim_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            #download Button
            st.download_button(
                label=f"📩 Download {file.name} as {conversion_type}",
                date=buffer,
                file_name=file_name,
                mime=mim_type
            )

st.success("✅ All files Processed!" )



        

