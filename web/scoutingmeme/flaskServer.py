from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/scout', methods = ['POST', 'GET'])
def scoutAMatch():
   if request.method == 'POST':
      # Handle POST requests from hitting submit
      result = request.form
      print(result)

   #Point back to the main form page
   return render_template('matchData.html')

if __name__ == '__main__':
   app.run(debug = True)