from get_data import *
from ml_utils import *
import time





# Setup the year and maker I want
car_makers = ["ford" , "vw-volkswagen"]
year_1 = "31" # 2013
year_2 = "36" #2018

#URL
urll= "https://rj.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/{maker}/flex?o={page}&re={year_2}&rs={year_1}"

# User- agent for get response
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}




def update_db(car_maker = car_makers, url = urll, header = headers):
    with open("new_cars.json", 'w+') as output:
        for maker in car_maker:
            for page in range(1,11):
                search_page = download_search_page(maker,page)
                car_list = parse_search_page(search_page, maker = maker)



                for car in car_list:
                    car_page = download_car_page(car['link'])
                    car_json_data = parse_car_page(car_page, car['link'])

                    pred = make_prediction(car_json_data)


                    car_id = car_json_data.get('link','')
                    data_front = {'car':car_json_data['model'], 'score': float(pred), 'car_id':car_id }
                    data_front['update_time'] = time.time_ns()

                    print(car_id, json.dumps(data_front))
                    output.write("{}\n".format(json.dumps(data_front)))

    return True
                    
                    