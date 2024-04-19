import streamlit as st
import pandas as pd

csv_path = '../data/extracted_data/saved_contents.csv'
pptx_base_path = '../data/pptx/'
pdf_base_path = '../data/pdf/'

df = pd.read_csv(csv_path, encoding='cp932', index_col=0)
file_list = sorted(set(df['file_name']))

import os
import base64

def main():
    st.title('PDF Viewer from Local Files')
    selected_pptx = st.selectbox("Select material", file_list)
    filename, ext = os.path.splitext(selected_pptx)
    
    # 選択されたPDFファイルを表示
    if selected_pptx:
        pdf_file_path = os.path.join(pdf_base_path, filename+'.pdf')
        with open(pdf_file_path, "rb") as pdf_file:
            
            #base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
            #pdf_display = f"data:application/pdf;base64,{base64_pdf}"
            #pdf_height = 600
            #html_string = f"""
            #<iframe src="{pdf_display}" width="100%" height="{pdf_height}px" type="application/pdf">
            #"""
            #st.components.v1.html(html_string, height=pdf_height+20)
            

            pdf_bytes = pdf_file.read()
            b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            pdf_url = f"data:application/pdf;base64,{b64_pdf}"
            st.markdown(f'<iframe src="{pdf_url}" width="700" height="500" type="application/pdf"></iframe>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()