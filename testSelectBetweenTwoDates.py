import PySQL
# import ProjectPublicVariable as PPV

from flask import Flask, jsonify

# dateFormat=PPV.dateFormat[int(PySQL.selectSQL_Reg(4, 1))][1] # ISO

startDate = '2024-06-25'
endDate = '2024-07-10'

# print(PySQL.selectR3XDates(startDate, endDate))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
    return jsonify(PySQL.selectR3XDates(startDate, endDate))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = 5000)