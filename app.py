# app.py
from flask import Flask, request, render_template, jsonify
app = Flask(__name__)

# Импортируем функцию проверки заявки
def проверка_заявки(заявка):
    ошибки = []
    обязательные_параметры = ["тип_промо", "период", "код_товара", "скидка", "география", "частота_участия", "пересечение_периодов"]
    for параметр in обязательные_параметры:
        if параметр not in заявка:
            ошибки.append(f"Параметр {параметр} отсутствует.")
    тип_промо = заявка["тип_промо"]
    скидка = заявка["скидка"]
    if тип_промо == "недельное" and скидка < 20:
        ошибки.append(f"Скидка недостаточна: указано {скидка}%, требуется минимум 20%.")
    elif тип_промо == "сезонное" and скидка < 30:
        ошибки.append(f"Скидка недостаточна: указано {скидка}%, требуется минимум 30%.")
    if ошибки:
        return {"статус": "ошибка", "сообщение": ошибки}
    else:
        return {"статус": "успех", "сообщение": "Заявка соответствует требованиям."}

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    заявка = request.form.to_dict()
    заявка["скидка"] = float(заявка["скидка"])
    заявка["пересечение_периодов"] = заявка["пересечение_периодов"] == 'true'
    заявка["география"] = заявка["география"].split(",")
    заявка["период"] = int(заявка["период"])
    заявка["частота_участия"] = int(заявка["частота_участия"])
    результат = проверка_заявки(заявка)
    return jsonify(результат)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)