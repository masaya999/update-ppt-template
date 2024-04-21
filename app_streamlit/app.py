import os
import base64
import streamlit as st
import pandas as pd

csv_path = '../data/extracted_data/saved_contents.csv'
pptx_base_path = '../data/pptx/'
pdf_base_path = '../data/pdf/'

df = pd.read_csv(csv_path, encoding='cp932', index_col=0)
file_list = sorted(set(df['file_name']))

def view_pdf(filename):
    pdf_file_path = os.path.join(pdf_base_path, filename+'.pdf')
    with open(pdf_file_path, "rb") as pdf_file:
        
        pdf_bytes = pdf_file.read()
        b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        pdf_url = f"data:application/pdf;base64,{b64_pdf}"
        st.markdown(f'<iframe src="{pdf_url}" width="800" height="450" type="application/pdf"></iframe>', unsafe_allow_html=True)

def load_info(selected_pptx, info_level):
    df_tmp = df[df['file_name'] == selected_pptx]
    df_info_level = df_tmp[df_tmp['info_level'] == info_level]
    updated_contents = {}

    update_bool = st.button('Update '+info_level)
        
    for idx, row in df_info_level.iterrows():
        updated_contents[idx] = st.text_area(label=str(row['page'])+' - '+row['label'], 
        value=row['content'], key=f"content{idx}", height=60)

    if update_bool:
        for idx, content in updated_contents.items():
            if df.loc[idx, 'content'] != content:
                df.loc[idx, 'content'] = content
        #update_csv(df, csv_path)
        st.success('CSVファイルが更新されました。')
    
    # # スクロール可能なコンテナのスタイルを定義
    # st.markdown("""
    # <style>
    # .scrollable-container {
    #     height: 400px;  /* コンテナの高さを400pxに設定 */
    #     overflow-y: auto;  /* 垂直方向のスクロールを有効にする */
    #     overflow-x: hidden;  /* 水平方向のスクロールを無効にする */
    # }
    # </style>
    # """, unsafe_allow_html=True)

    # # スクロール可能なコンテナを作成
    # container = st.container()
    # container.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
    
    # # テキストエリアを動的に生成
    # for idx, row in df_client.iterrows():
    #     container.text_area(label=str(row['page'])+'-'+row['label'], 
    #     value=row['content'], key=f"content{idx}", height=100)
    # container.markdown('</div>', unsafe_allow_html=True)

def main():
    show_home = st.sidebar.checkbox("ホームを表示")
    show_data = st.sidebar.checkbox("データ表示を表示")
    show_settings = st.sidebar.checkbox("設定を表示")
    st.title('PDF Viewer from Local Files')
    selected_pptx = st.selectbox("Select material", [""]+file_list)
    filename, ext = os.path.splitext(selected_pptx)
    
    if selected_pptx != "":
        view_pdf(filename)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('### Client Infomation')
            load_info(selected_pptx, 'client')
        with col2:
            st.markdown('### Proposal Infomation')
            load_info(selected_pptx, 'proposal')
        
if __name__ == "__main__":
    main()