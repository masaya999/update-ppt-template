import re
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



def completion_with_llm(df: pd.DataFrame) -> pd.DataFrame:

    input_template = """
    # requirements
    Update the contents of "Output" based on the information in "Input".
    "Input" and "Output" are written in the form <description>: <content>.
    The <content> of "Output" are examples.
    Answer only "Output" in the form <description>: <content> in Japanese.

    # Input
    {}

    # Output
    {}
    """
    llm = ChatOpenAI()
    input_contents = ""
    output_contents = ""
    for idx, row in df.iterrows():
        if row['info_level'] == 'client':
            input_contents += str(row['label'])+': '+str(row['content'])+'\n'
        elif row['info_level']=='proposal':
            output_contents +=  str(row['label'])+': ex)'+str(row['content'])+'\n'

    input_prompt = input_template.format(input_contents, output_contents)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are world class sales exective. Please answer the following requirements."),
        ("user", "{input}")
    ])

    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    result = chain.invoke({"input": f"{input_prompt}"})

    for idx, row in df.iterrows():
        if row['info_level']=='proposal':
            match_s = re.search(row['label']+'.*', result).group()
            df.loc[idx, 'content'] = match_s[len(row['label'])+2:]

    return df

