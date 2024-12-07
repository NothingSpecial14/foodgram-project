import csv
from recipes.models import Ingredient


def save_csv_to_db(csv_file):
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader=csv.reader(file, delimiter=',')
            ingredients=[           
                Ingredient(
                    name=row[0],
                    unit=row[1]                
                ) 
                for row in reader
            ]          
            Ingredient.objects.bulk_create(ingredients)
            
            print(f'Данные из {csv_file} успешно импортированы!')
    except FileNotFoundError:
        print(f'Файл {csv_file} не найден!')
    except csv.Error as e:
        print(f'Ошибка при обработке CSV-файла: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')

save_csv_to_db('ingredients.csv')