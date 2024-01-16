import configparser
from string import Template

def read_language_file(file_path, lang_code):
    config = configparser.ConfigParser()
    config.read(file_path,encoding='utf-8')
    return config[lang_code]

def generate_html(template, language_data):
    html = Template(template)
    return html.substitute(language_data)

def create_html_page(language_file_path, lang_code, output_file):
    with open('template.html', 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    language_data = read_language_file(language_file_path, lang_code)
    generated_html = generate_html(template_content, language_data)

    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(generated_html)

if __name__ == "__main__":
    language_file_path = 'nazvy.txt'
    lang_code = 'SK'  # Change this to the desired language code
    output_file = f'../templates/{lang_code}.html'

    create_html_page(language_file_path, lang_code, output_file)
    print(f'HTML stránka pre jazyk {lang_code} bola úspešne vytvorená do súboru {output_file}.')