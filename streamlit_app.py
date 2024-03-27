import streamlit as st
import replicate
import os

st.set_page_config(page_title="Nova Escola - Gerador de atividades")

def generate_llama2_response(prompt_input, system_prompt_ane):
    
    output = replicate.run("meta/llama-2-70b-chat", 
                           input={ "prompt": prompt_input,
                                  "temperature":0.1, "top_p":1,
                                  "debug": False,
                                  "top_p": 1,
                                  "temperature": 0.5,
                                  "system_prompt": system_prompt_ane + "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\\n\\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don\'t know the answer to a question, please don\'t share false information.",
                                  "max_new_tokens": 500000,
                                  "min_new_tokens": -1,
                                  "prompt_template": "[INST] <<SYS>>\\n{system_prompt}\\n<</SYS>>\\n\\n{prompt} [/INST]",
                                  "repetition_penalty": 1.15
                                  })      
    full_response = ''
    for item in output:
        full_response += item
                  
    return full_response

def main():
    replicate_api = st.secrets['REPLICATE_API_TOKEN']
    os.environ['REPLICATE_API_TOKEN'] = replicate_api
    
    custom_css = """
      <style>
          /* Style for the sidebar header */
          .sidebar-header {
              background-color: #E32458; /* Red background color */
              color: white; /* White text color */
              padding: 20px; /* Add padding */
              text-align: center; /* Center align text */
          }
          h1 {
            color:white
          }
          /* Style for the logo */
          .sidebar-logo {
              
              margin-bottom: 10px; /* Add margin to separate logo from title */
          }
      </style>
      """
    st.markdown(custom_css, unsafe_allow_html=True)
    
    st.sidebar.markdown("""<div class="sidebar-header"> <svg width="254" height="46" viewBox="0 0 254 46" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="Logo / Nova Escola / Horizontal">
<path id="Vector" d="M46.0101 13.6699C40.6001 13.6699 36.8701 17.5149 36.8701 22.9999C36.8701 28.4849 40.6001 32.3299 46.0101 32.3299C51.4201 32.3299 55.1901 28.4849 55.1901 22.9999C55.1901 17.5149 51.4201 13.6699 46.0101 13.6699ZM46.0101 29.0049C42.8751 29.0049 40.6751 26.5399 40.6751 22.9999C40.6751 19.4549 42.8751 16.9949 46.0101 16.9949C49.1801 16.9949 51.3851 19.4599 51.3851 22.9999C51.3851 26.5399 49.1851 29.0049 46.0101 29.0049Z" fill="white"/>
<path id="Vector_2" d="M92.9101 27.51C92.9101 26.765 92.9101 25.46 92.9101 20.42C92.9101 16.13 90.1501 13.665 85.4501 13.665C81.1951 13.665 78.5101 15.64 78.0251 19.11H81.7551C82.0151 17.62 83.3951 16.795 85.4501 16.795C87.8001 16.795 89.1801 18.065 89.1801 20.34V21.275H83.7351C80.0051 21.275 77.2451 23.4 77.2451 26.65C77.2451 29.895 80.0051 32.32 83.7351 32.32C86.2701 32.32 88.2501 31.2 89.4801 29.26H89.8551C89.8551 30.865 90.8601 31.795 92.5801 31.795H95.4151V28.7H94.1101C93.2451 28.705 92.9101 28.37 92.9101 27.51ZM84.5151 29.305C82.0901 29.305 80.9701 28 80.9701 26.62C80.9701 25.165 82.2751 24.195 84.1401 24.195H89.1601C89.0651 27.35 87.3101 29.305 84.5151 29.305Z" fill="white"/>
<path id="Vector_3" d="M66.3849 29.2653H66.0099L61.2699 14.1953H57.3149L63.1749 31.8053H69.2199L75.0749 14.1953H71.1199L66.3849 29.2653Z" fill="white"/>
<path id="Vector_4" d="M28.7 29.2653H28.325L21.87 14.1953H14.895V31.8053H18.625V16.7303H19L25.455 31.8053H32.43V14.1953H28.7V29.2653Z" fill="white"/>
<path id="Vector_5" d="M0.5 0.504997V45.485H253.14V0.5L0.5 0.504997ZM3.96 42.03V3.96H106.35V42.03H3.96ZM249.68 42.03H109.81V3.965H249.68V42.03Z" fill="white"/>
<path id="Vector_6" d="M190.81 32.325C196.22 32.325 199.99 28.48 199.99 22.995C199.99 17.51 196.22 13.665 190.81 13.665C185.4 13.665 181.67 17.51 181.67 22.995C181.67 28.48 185.4 32.325 190.81 32.325ZM190.81 16.99C193.98 16.99 196.185 19.455 196.185 22.995C196.185 26.54 193.985 29 190.81 29C187.675 29 185.475 26.54 185.475 22.995C185.47 19.455 187.675 16.99 190.81 16.99Z" fill="white"/>
<path id="Vector_7" d="M149.69 29.3398C147.04 29.3398 145.55 28.2948 145.36 26.6148H141.63C141.89 30.1198 144.915 32.3248 149.69 32.3248C154.205 32.3248 157.15 30.3448 157.15 26.8048C157.15 19.9048 145.92 22.6248 145.92 18.7848C145.92 17.5148 147.19 16.6598 149.24 16.6598C151.405 16.6598 152.6 17.5948 152.785 19.1198H156.515C156.14 15.7598 153.38 13.6748 149.24 13.6748C144.985 13.6748 142.3 15.6498 142.3 19.0098C142.3 25.8398 153.53 23.0398 153.53 27.0298C153.535 28.4448 152.115 29.3398 149.69 29.3398Z" fill="white"/>
<path id="Vector_8" d="M129.62 32.3249C133.8 32.3249 136.82 30.1999 137.79 26.6149H133.945C133.57 28.1049 131.895 29.1149 129.69 29.1149C126.66 29.1149 124.615 27.2349 124.275 24.1899H137.975C138.05 23.5949 138.085 23.0699 138.085 22.5499C138.085 17.4399 134.615 13.6699 129.39 13.6699C124.165 13.6699 120.51 17.4399 120.51 23.0699C120.51 28.6999 124.135 32.3249 129.62 32.3249ZM129.395 16.8799C132.23 16.8799 133.96 18.4999 134.195 21.1699H124.325C124.77 18.4649 126.565 16.8799 129.395 16.8799Z" fill="white"/>
<path id="Vector_9" d="M169.58 32.3248C174.055 32.3248 177.49 29.6398 178.085 25.6098H174.24C173.83 27.6248 171.925 29.0048 169.575 29.0048C166.44 29.0048 164.24 26.5448 164.24 22.9998C164.24 19.4548 166.44 16.9948 169.575 16.9948C171.925 16.9948 173.83 18.3748 174.24 20.3898H178.085C177.49 16.3598 174.055 13.6748 169.58 13.6748C164.17 13.6748 160.44 17.5198 160.44 23.0048C160.44 28.4898 164.17 32.3248 169.58 32.3248Z" fill="white"/>
<path id="Vector_10" d="M217.445 31.8053V28.5603H208.155V14.1953H204.425V28.5603V31.8053H208.155H217.445Z" fill="white"/>
<path id="Vector_11" d="M227.185 21.2849C223.455 21.2849 220.695 23.4099 220.695 26.6599C220.695 29.9049 223.455 32.3299 227.185 32.3299C229.72 32.3299 231.7 31.2099 232.93 29.2699H233.305C233.305 30.8749 234.31 31.8049 236.03 31.8049H238.98V28.7099H237.56C236.7 28.7099 236.365 28.3749 236.365 27.5149C236.365 26.7699 236.365 25.4649 236.365 20.4249C236.365 16.1349 233.605 13.6699 228.905 13.6699C224.65 13.6699 221.965 15.6449 221.48 19.1149H225.21C225.47 17.6599 226.815 16.8399 228.905 16.8399C231.255 16.8399 232.635 18.1099 232.635 20.3449V21.2799H227.185V21.2849ZM227.97 29.3049C225.545 29.3049 224.425 27.9999 224.425 26.6199C224.425 25.1649 225.73 24.1949 227.595 24.1949H232.615C232.52 27.3549 230.765 29.3049 227.97 29.3049Z" fill="white"/>
</g>
</svg>
 <h1>Gerador de atividades</h1></div>""", unsafe_allow_html=True)
    
    # Define options for input_a
    options_ano = ['8° ano', '9° ano']

    # Define options for input_b based on the selected option from input_a
    unidades_tematicas = {
        '8° ano': ['Números', 'Álgebra'],
        '9° ano': ['Geometria', 'Grandezas e medidas'],
    }
    
    link_planos_aula = {
        '8° ano': "https://novaescola.org.br/planos-de-aula/fundamental/8ano",
        '9° ano': "https://novaescola.org.br/planos-de-aula/fundamental/9ano",
    }
    
    objetos_conhecimento = {
        '8° ano-Números': ['Potenciação e radiciação', 'Porcentagens'],
        '8° ano-Álgebra': ['Valor numérico de expressões algébricas', 'Equação polinomial de 2º grau do tipo ax2 = b'],
        '9° ano-Geometria': ['Relações entre arcos e ângulos na circunferência de um círculo', 'Semelhança de triângulos'],
        '9° ano-Grandezas e medidas': ['Unidades de medida utilizadas na informática', 'Volume de prismas e cilindros'],
    }
    # Create select input for input_a
    selected_ano = st.sidebar.selectbox("Ano", options_ano)

    # Create select input for input_b based on the selected option from input_a
    selected_unidades_tematicas = st.sidebar.selectbox("Unidades temáticas", unidades_tematicas[selected_ano])
    
    selected_link_planos_aula = link_planos_aula[selected_ano]

    index_objeto_conhecimento = selected_ano+"-"+selected_unidades_tematicas

    selected_objeto_conhecimento = st.sidebar.selectbox("Objetos de conhecimento", objetos_conhecimento[index_objeto_conhecimento])

    ane_prompt = 'Gerar 10 questões de múltipla escolha de multipla escola do '+selected_ano+' com a Unidade temática '+selected_unidades_tematicas + ' e objeto de conhecimento '+ selected_objeto_conhecimento + ' Gerar toda a resposta em português BR'

    system_prompt_ane = "Como um assistente do professor de escola pública brasileira, gera uma atividade com 10 questões de múltipla escolha e indicar alternativa correta. As questões devem ser para o" + selected_ano + " do ensino fundamental sobre a unidade tematica "+ selected_unidades_tematicas +" com objeto de conhecimento "+ selected_objeto_conhecimento + " Usa como base de conhecimento os planos de aula de matemática da Nova Escola e indica no final da resposta ao menos 3 planos de aula do tema, se possível com link para o site da Nova Escola " +selected_unidades_tematicas  

    # Button to trigger the action
    if st.sidebar.button('Gerar atividades'):
        # Replicating the content to the main div
        with st.spinner("Gerando atividades..."):
          response = generate_llama2_response(ane_prompt, system_prompt_ane )
          st.text(response)

if __name__ == "__main__":
    main()
