import requests
from bs4 import BeautifulSoup
import pandas
import data_client


class Parser:
    links_to_parse = [
        'https://www.kufar.by/l/mebel',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6Mn0%3D',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6M30%3D',
        'https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6NH0%3D'
    ]


    @staticmethod
    def get_mebel_by_link(link):
        response = requests.get(link)
        mebel_data = response.text

        mebel_items = []
        to_parse = BeautifulSoup(mebel_data, 'html.parser')
        for elem in to_parse.find_all('a', class_='styles_wrapper__5FoK7'):
            try:
                price, desc = elem.text.split('р.')
                mebel_items.append((elem['href'],
                                    int(price.replace(' ', '')),
                                    desc))
            except:
                pass

        return mebel_items

    def save_to_csv(self, mebel_items):
        pandas.DataFrame(mebel_items).to_csv('mebel.csv', index=False)

    def save_data(self, conn, data_client_imp, mebel_items):
        data_client_imp.create_mebel_table(conn)
        for item in mebel_items:
            data_client_imp.insert(conn, item[0], item[1], item[2])


    def run(self, data_client_imp):
        conn = data_client_imp.get_connection()
        mebel_items = []

        for link in self.links_to_parse:
            mebel_items.extend(self.get_mebel_by_link(link))

        self.save_data(conn, data_client_imp, mebel_items)
        items = data_client_imp.get_items(conn, 10, 30)
        data_client_imp.print_items(items)

        if conn is not None:
            conn.close()

parser = Parser()
data_client_imp = data_client.PostgresClient()
print(f'{'=' * 200}\n\tPostgresClient')
parser.run(data_client_imp)
