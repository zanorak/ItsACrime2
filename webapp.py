from flask import Flask, render_template, request
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

crimeData = json.load( open( "state_crime.json" ) )

# get list of states
stateList = []
currState = ""
for stateYear in crimeData:
    if stateYear["State"] != currState:
        currState = stateYear["State"]
        stateList.append( currState )


@app.route("/")
def render_about():
    return render_template('about.html')


@app.route("/rates", methods=['GET', 'POST'])
def render_rates():
    if request.method == 'GET':
       return render_template('rates.html', stateList = stateList )

    elif request.method == 'POST':
        thisState = request.form.get("stateSelect", "").strip() # sometimes there is a space on the end
        thisCrime = request.form.get("crimeSelect", "").strip()

        if ( thisState == "Choose State" ) or ( thisCrime == "Type of Crime" ):
            return render_template( 'rates.html', stateList = stateList, alert = "Please pick a State and a Crime" )

        else:
            # Property or Violent - first char tells us which one
            pv = thisCrime[:1]

            # get the crime data
            labels = []
            data = []
            for stateYear in crimeData:
                if stateYear["State"] == thisState:
                    labels.append( stateYear["Year"])
                    if pv == 'p':
                        data.append( stateYear["Data"]["Rates"]["Property"][thisCrime[1:]] )
                    else:
                        data.append( stateYear["Data"]["Rates"]["Violent"][thisCrime[1:]] )

            return render_template( 'rates.html', stateList = stateList, thisState = thisState, thisCrime = thisCrime, labels = labels, data = data )



@app.route("/compare", methods=['GET', 'POST'])
def render_compare():
    if request.method == 'POST':
        thisState1 = request.form.get("stateSelect1", "").strip() # sometimes there is a space on the end
        thisState2 = request.form.get("stateSelect2", "").strip()
        thisCrime = request.form.get("crimeSelect", "").strip()

        if ( thisState1 == "Choose State" ) or ( thisState2 == "ChooseState" ) or ( thisCrime == "Type of Crime" ):
            return render_template( 'compare.html', stateList = stateList, alert = "Please pick two States and a Crime" )

        else:
            # Property or Violent - first char tells us which one
            pv = thisCrime[:1]

            # get the crime data
            labels = []
            data1 = []
            data2 = []
            # get the labels and data for the first state
            for stateYear in crimeData:
                if stateYear["State"] == thisState1:
                    labels.append( stateYear["Year"])
                    if pv == 'p':
                        data1.append( stateYear["Data"]["Rates"]["Property"][thisCrime[1:]] )
                    else:
                        data1.append( stateYear["Data"]["Rates"]["Violent"][thisCrime[1:]] )

            # get the data for the second state
            for stateYear in crimeData:
                if stateYear["State"] == thisState2:
                    if pv == 'p':
                        data2.append( stateYear["Data"]["Rates"]["Property"][thisCrime[1:]] )
                    else:
                        data2.append( stateYear["Data"]["Rates"]["Violent"][thisCrime[1:]] )

            return render_template( 'compare.html', stateList = stateList, thisState1 = thisState1, thisState2 = thisState2, thisCrime = thisCrime, labels = labels, data1 = data1, data2 = data2 )

    else:
        return render_template('compare.html', stateList = stateList )
    
if __name__=="__main__":
    app.run(debug=False)
