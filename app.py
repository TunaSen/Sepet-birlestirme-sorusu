from flask import Flask, render_template , jsonify,request
from utils import sepetOlustur, randomOLustur


app = Flask(__name__)
@app.route('/map')
def map():
    n = request.args.get('n')
    kumeSayisi = request.args.get('kumeSayisi')
    randomOLustur(int(n))
    return render_template("map.html",n=n,kumeSayisi=kumeSayisi)


@app.route('/noktalar')
def getNoktalar():
    n = request.args.get('n')
    kumeSayisi= request.args.get('kumeSayisi')

    if n:
        randomOLustur(int(n))

    data = sepetOlustur(int(kumeSayisi))
    return jsonify(data)




if __name__ == '__main__':
    app.run()
