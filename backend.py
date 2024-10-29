"""
Programmed by Victor Jimenez & Matthew Tujague
"""

from flask import Flask, jsonify, render_template, request, url_for
from flask_cors import CORS
from pprint import pprint
from hFunctions import *

from firebase import addTestToFirebase, retrieveAllTests, formatTestsToModel, trainModelToNewData


tableData = [
        [8103, 83727895, 769158, 31678925, 3294059, 73914, 3512407, 8089170, 1992939, 2120],
        [4567, 8092573, 45013, 29758, 530345, 618475, 12445683, 30127987, 366305, 297539],
        [139723, 45298716, 3295870, 3980, 253970, 579340, 6138, 432063, 81924982, 6583],
        [9813, 32145678, 84673, 139475, 58145469, 13820, 37428981, 63017980, 45607, 13925647],
        [34602458, 3643, 83921, 4512693, 4698723, 836438, 5801, 89063, 23972165, 3263],
        [42915, 5853, 72631, 34670654, 36135, 4626071, 83959, 4959398, 68130, 6301],
        [987302, 9672, 4286158, 7807347, 675246, 946053, 2002193, 6004745, 35671, 1061],
        [5732186, 45013, 84203, 56239, 671302, 3004, 38672168, 80873, 4108, 371903],
        [6837, 183820, 43612063, 90542145, 784352, 3956, 23781, 198378, 187123, 6004216],
        [3407, 1792635, 4067903, 98103, 5624, 780523, 56792604, 37801, 6356791, 93956467],
        [431025, 4297589, 83961, 56465421, 6138940, 4295901, 6476023, 97654985, 13283, 21243],
        [613947, 43169857, 4302, 3251673, 70765583, 760536, 37821245, 4623, 1308418, 9212494],
        [8077, 3824510, 53906, 4389, 80610972, 3120, 760530, 3940, 8405737, 89203],
        [579103, 970943, 42057, 87652143, 3048, 497538, 1230, 93745125, 19081257, 23456]
    ]

# flask app
app = Flask(__name__)
CORS(app)


#app route
@app.route('/')
def home():
    return render_template('home.html'); #make dynamic later

@app.route('/regular')
def regular():
    return render_template('regular.html')

@app.route('/TimeSeriesResults')
def timeseries_results():
    return render_template('timeseries_results.html')

@app.route('/FinalResults')
def final_results():
    return render_template('final_results.html')

@app.route("/api/submitTest", methods=["POST"])
def submit_test():
    print("hello")

    data = request.get_json()
    click_data = data.get('clickData', [])

# Calculate answers for each question using functions and store in JSON format
    scoring_data = {
        "R": {
            "left_column_crossed_3s": number_of_crossed_3s_column_left_side(click_data, column=0),  # example for column
            "right_column_crossed_3s": number_of_crossed_3s_column_right_side(click_data, column=0)  # example for column
        },
        "S": {
            "quadrant_crossed_3s": number_of_crossed_3s_column_quads(click_data, 0, 7, 0, 5)  # example for quadrant dimensions
        },
        "T": {
            "total_crossed_3s": total_crossed_3s(click_data)
        },
        "U": {
            "total_omissions": total_omissions(click_data)
        },
        "V": {
            "left_side_crossed_3s": ol_count_crossed_threes(click_data)
        },
        "W": {
            "left_side_missed_3s": ol_count_missed_threes(click_data)
        },
        "X": {
            "right_side_crossed_3s": or_count_crossed_threes(click_data)
        },
        "Y": {
            "right_side_missed_3s": or_count_missed_threes(click_data)
        },
        "Z": {
            "page_centered_omissions": page_centered_omission(click_data)
        },
        "AA": {
            "left_column_crossed_3s_repeat": number_of_crossed_3s_column_left_side(click_data, column=0)
        },
        "BB": {
            "missed_threes_left_half": count_missed_threes_left_half_all_rows(click_data)
        },
        "CC": {
            "right_column_crossed_3s_repeat": number_of_crossed_3s_column_right_side(click_data, column=0)
        },
        "DD": {
            "missed_threes_right_half": count_missed_threes_right_half_all_rows(click_data)
        },
        "EE": {
            "string_centered_omissions": string_centered_omissions(click_data)
        }

    }

    aiModel = {"cognitivelyImpaired" : (1 if trainModelToNewData() else 0)}
    scoring_data.update(aiModel)

    # Send JSON response
    return jsonify(scoring_data)

if __name__ == '__main__':
    app.run(debug=True)
