
import openai
import streamlit as st
from gtts import gTTS
from docx import Document
import PyPDF2


openai.api_key = 'OPENAI_API_KEY'

 
def translate_text(input_text,source_language,target_language):
    response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {
            "role":"system",
            "content":f"translate the given text from {source_language} to {target_language}"
            },
        {
            "role":"user",
            "content":input_text
        }])
    translated_text = response['choices'][0]['message']['content']
    return translated_text.strip()
     
def main():
    st.title("Language translator application")
    st.write('Enter text to be translated')
    input_method = st.radio("Choose input mode ",['Enter text','Upload file'])
    
    if input_method == 'Enter text':
        input_text = st.text_area("Enter the text to translate")
    else:
        uploaded_file = st.file_uploader("upload the file to be translated",type=["txt","docx","pdf"])
        
    if st.button('translate'):
        if input_method == 'Upload file' and uploaded_file is not None:
            file_ext = uploaded_file.name.split('.')[1]
            
            if file_ext== 'docx':
                translated_text = ""
                doc = Document(uploaded_file)
                for paragraph in doc.paragraphs:
                    if paragraph.text.strip():
                       translated_text += translate_text(paragraph.text,'English','Kannada')    
                       if translated_text:
                           paragraph.text = translated_text
                doc.save("output.docx")
                st.write(f"translated document successfully{translated_text}")
                
            if file_ext== 'txt':
               input_text = uploaded_file.read().decode("utf-8")
               translated_text = translate_text(input_text,'English','Kannada')
               with open('output.txt', 'w',encoding='utf-8') as file:
                   file.write(translated_text)
               st.success("translated file saved successfully")
               st.write(f"translated text:\n{translated_text}")
               
            if file_ext== 'pdf':
              translated_text = ""
              pdfreader = PyPDF2.PdfReader(uploaded_file)
              for page in pdfreader.pages:
                  if page.extract_text():
                     translated_text += translate_text(page.extract_text(),"Engligh","Kannada") + "\n"   
                   
              with open('output.pdf','w',encoding='utf-8') as file:
                  file.write(translated_text)
              st.write(f"translated pdf document successfully")
               
        if input_method == 'Enter text':
            translated_text = translate_text(input_text,'English','Kannada')
            st.success("translated successfully")
            st.write(f"translated text:\n{translated_text}")
   
            
if __name__ == "__main__":
    main()
        
        
    