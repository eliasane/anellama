import streamlit as st
import replicate
import os


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
    
    st.sidebar.title('Gerador Atividades Nova Escola')
    
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
        response = generate_llama2_response(ane_prompt, system_prompt_ane )
        st.text(response)

if __name__ == "__main__":
    main()
