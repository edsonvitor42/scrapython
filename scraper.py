import scrapy
import os
from fpdf import FPDF
import pdfkit 

class BrickSetSpider(scrapy.Spider):
    name = 'redacao_online_spider'
    start_urls = ['url_que_deseja_fazer_o_scrape']

    def parse(self, response):
        SET_SELECTOR = '#main'

        for thema_redacao in response.css(SET_SELECTOR):

            NAME_SELECTOR_HEADER = '.post-header h1'
            NAME_SELECTOR_BODY = '.post-content'

            # yield 
            html_header = thema_redacao.css(NAME_SELECTOR_HEADER).extract()
            html_body = thema_redacao.css(NAME_SELECTOR_BODY).extract()

            pdf_header = thema_redacao.css(NAME_SELECTOR_HEADER + ' ::text').extract()
            pdf_body = thema_redacao.css(NAME_SELECTOR_BODY + ' ::text').extract()

        self.generete_html(html_header, html_body)
        self.generete_pdf(pdf_header, pdf_body)

        return

    def generete_pdf(self, pdf_header, pdf_body):
        pdf_header = self.return_essay_themes_of_header(''.join(pdf_header))

        pdf_body = ''.join(pdf_body)[0:''.join(pdf_body).find('QUERO USAR ESSE TEMA!')]

        pdf_bundled = pdf_header + pdf_body

        # Abre o arquivo pdf que sera utilizado apra salvar os dados.
        pdf_file = open('index.text', 'w')
        # Altera o conteúdo do html pelo tema do site da redação online.
        pdf_file.write(pdf_bundled)
        # Fecha o arquivo pdf
        pdf_file.close()
        return

    def generete_html(self, html_header, html_body):
        html_header = self.return_essay_themes_of_header(''.join(html_header))

        html_body = html_body[0][0:html_body[0].find('QUERO USAR ESSE TEMA!')] + '</div>'

        html = html_header + html_body

        # Remove os css da página.
        html = self.remove_css_of_html(html)

        # Remove os anuncios da página (BETA).
        html_bundled = self.remove_banner_of_html(html)

        # Abre o arquivo html que sera utilizado apra salvar os dados.
        html_file = open('index.html', 'w')
        # Altera o conteúdo do html pelo tema do site da redação online.
        html_file.write(html_bundled)
        # Fecha o arquivo html
        html_file.close()

        # Abre o arquivo html no google chrome.
        os.system('open -a "Google Chrome" index.html')

        return

    def remove_css_of_html(self, string):
        tags = ['class=', 'style=', 'id=']

        for tag in tags:
            while True:
                first_class_index = string.find(tag)

                if first_class_index == -1:
                    break

                last_class_index = string[first_class_index + 7:].find('"')

                string = string[0 : first_class_index : ] + string[(first_class_index + 7) + (last_class_index + 1) : :]

        return string

    def return_essay_themes_of_header(self, string):
        index = string.lower().find('tema de redação: ')

        if index != -1:
            last_index = string.find(': ')
            string = string[0: index :] + string[last_index + 2: :]

        return string

    def remove_banner_of_html(self, string):
        return string