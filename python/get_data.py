import fitbit
import json
from json_handler import set_token_client_id, set_debug_state, print_json, read_tokens, write_tokens
from platform import python_version
import select
import argparse
from datetime import date, timedelta


##############################################
# All output must be printed in JSON format, #
# as it is read in by node_helper.js         #
##############################################

#TODO: make more loops instead of calling the same method several times in a row

def print_data(resource, data, goals, weekdays, debug=False):
    if debug is True and not debug_mode:
        return

    print(json.dumps({"type": "data", "resource": resource,
                      "values": {"day1": {"weekday": weekdays[0], "data": data[0], "goal": goals[0]}, 
                                 "day2": {"weekday": weekdays[1], "data": data[1], "goal": goals[1]}, 
                                 "day3": {"weekday": weekdays[2], "data": data[2], "goal": goals[2]}, 
                                 "day4": {"weekday": weekdays[3], "data": data[3], "goal": goals[3]}, 
                                 "day5": {"weekday": weekdays[4], "data": data[4], "goal": goals[4]}, 
                                 "day6": {"weekday": weekdays[5], "data": data[5], "goal": goals[5]}, 
                                 "day7": {"weekday": weekdays[6], "data": data[6], "goal": goals[6]}}}))


def print_empty_resource(resource):
    # Print out resource value anyway. This will show as empty
    # in the module and allows other data to be fetched
    print_data(
        resource=resource,
        data=[0,0,0,0,0,0,0],
        goals=[1,1,1,1,1,1,1],
        weekdays=["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    )


def handle_key_error(key_error, resource=None):
    print_json("error", str(key_error))
    if resource is not None:
        print_empty_resource(resource)


if __name__ == "__main__":

    print_json("debug", "Python Version", python_version())

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--debug', action='store_true', default=False)
    # TODO: print dummy data if this is called
    parser.add_argument('-t', '--test', action='store_true', default=False)

    parser.add_argument("client_id", type=str)
    parser.add_argument("client_secret", type=str)

    parser.add_argument('-r', '--resources', nargs='+')

    args = parser.parse_args()

    debug_mode = args.debug

    client_id = args.client_id
    client_secret = args.client_secret

    resource_list = args.resources

    set_debug_state(debug_mode)
    print_json("status", "Debug Mode", str(debug_mode))

    set_token_client_id(client_id)
    print_json("status", "Client ID", str(client_id))

    print_json("debug", "Client Secret", str(client_secret))

    resource_list_str = ", ".join(resource_list) \
        if len(resource_list) > 0 else "All"
    print_json("status", "Resources to get", resource_list_str)

    access_token, refresh_token, expires_at = read_tokens()
    print_json("debug", "access_token", access_token)
    print_json("debug", "refresh_token", refresh_token)
    print_json("debug", "expires_at", expires_at)

    def WriteTokenWrapper(token):
        print_json("status", "Access token expired - refreshing tokens")
        print_data(
            resource=token,
            data=0,
            goal=1,
            debug=True
        )
        acc_tok = token["access_token"]
        ref_tok = token["refresh_token"]
        expires_at = token["expires_at"]
        write_tokens(acc_tok, ref_tok, expires_at)

    print_json("debug", "Creating authorised client")
    authd_client = fitbit.Fitbit(client_id,
                                 client_secret,
                                 system="METRIC",
                                 oauth2=True,
                                 access_token=access_token,
                                 refresh_token=refresh_token,
                                 expires_at=expires_at,
                                 refresh_cb=WriteTokenWrapper,
                                 redirect_uri="http://127.0.0.1:8888/"
                                 )
    
    #####################################################
    print_json("debug", "Polling API for data")
    #####################################################

    # Determine the last 7 days (not including today)
    today = date.today()
    day7 = today - timedelta(days=1)
    day6 = today - timedelta(days=2)
    day5 = today - timedelta(days=3)
    day4 = today - timedelta(days=4)
    day3 = today - timedelta(days=5)
    day2 = today - timedelta(days=6)
    day1 = today - timedelta(days=7)

    # Get the weekday for these days
    week = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    weekdays = [week[day1.weekday()], 
                week[day2.weekday()],
                week[day3.weekday()],
                week[day4.weekday()],
                week[day5.weekday()],
                week[day6.weekday()],
                week[day7.weekday()]]
    
    #####################################################
    print_json("status", "API polling stage", "Activity")
    #####################################################
    activity_resources_all = [
        "steps", "caloriesOut", "distance", "activeMinutes"]
    activity_resources_easy_parse = ["steps", "caloriesOut"]

    if len(resource_list) == 0 or \
            any(item in activity_resources_all for item in resource_list):


        # Get Activities for Day 1
        activity_list1 = authd_client.activities(day1)
        activity_summary1 = activity_list1["summary"]
        activity_goals1 = activity_list1["goals"]

        # Get Activities for Day 2
        activity_list2 = authd_client.activities(day2)
        activity_summary2 = activity_list2["summary"]
        activity_goals2 = activity_list2["goals"]     

        # Get Activities for Day 3
        activity_list3 = authd_client.activities(day3)
        activity_summary3 = activity_list3["summary"]
        activity_goals3 = activity_list3["goals"] 

        # Get Activities for Day 4
        activity_list4 = authd_client.activities(day4)
        activity_summary4 = activity_list4["summary"]
        activity_goals4 = activity_list4["goals"] 

        # Get Activities for Day 5
        activity_list5 = authd_client.activities(day5)
        activity_summary5 = activity_list5["summary"]
        activity_goals5 = activity_list5["goals"] 

        # Get Activities for Day 6
        activity_list6 = authd_client.activities(day6)
        activity_summary6 = activity_list6["summary"]
        activity_goals6 = activity_list6["goals"] 

        # Get Activities for Day 2
        activity_list7 = authd_client.activities(day7)
        activity_summary7 = activity_list7["summary"]
        activity_goals7 = activity_list7["goals"] 


        ### Print the data for all days
        if len(resource_list) == 0:
            activity_resources_selected = activity_resources_easy_parse
        else:
            activity_resources_selected = set(resource_list) & \
                set(activity_resources_easy_parse)

        # Get resources that are easy to parse
        for resource in activity_resources_selected:
            try:
                currentData = [activity_summary1[resource],
                               activity_summary2[resource],
                               activity_summary3[resource],
                               activity_summary4[resource],
                               activity_summary5[resource],
                               activity_summary6[resource],
                               activity_summary7[resource]]
                
                currentGoals = [activity_goals1[resource],
                                activity_goals2[resource],
                                activity_goals3[resource],
                                activity_goals4[resource],
                                activity_goals5[resource],
                                activity_goals6[resource],
                                activity_goals7[resource]]

                print_data(
                    resource=resource,
                    data=currentData,
                    goal=currentGoals,
                    weekdays=weekdays
                )
            except KeyError as err:
                handle_key_error(err, resource)

        # These require more complicated parsing
        if len(resource_list) == 0 or "activeMinutes" in resource_list:
            try:
                currentData = [activity_summary1["fairlyActiveMinutes"] + activity_summary1["veryActiveMinutes"],
                               activity_summary2["fairlyActiveMinutes"] + activity_summary2["veryActiveMinutes"],
                               activity_summary3["fairlyActiveMinutes"] + activity_summary3["veryActiveMinutes"],
                               activity_summary4["fairlyActiveMinutes"] + activity_summary4["veryActiveMinutes"],
                               activity_summary5["fairlyActiveMinutes"] + activity_summary5["veryActiveMinutes"],
                               activity_summary6["fairlyActiveMinutes"] + activity_summary6["veryActiveMinutes"],
                               activity_summary7["fairlyActiveMinutes"] + activity_summary7["veryActiveMinutes"]]

                currentGoals = [activity_goals1["activeMinutes"],
                                activity_goals2["activeMinutes"],
                                activity_goals3["activeMinutes"],
                                activity_goals4["activeMinutes"],
                                activity_goals5["activeMinutes"],
                                activity_goals6["activeMinutes"],
                                activity_goals7["activeMinutes"]]

                print_data(
                    resource="activeMinutes",
                    data=currentData,
                    goal=currentGoals,
                    weekdays=weekdays
                )
            except KeyError as err:
                handle_key_error(err, "activeMinutes")

        if len(resource_list) == 0 or "distance" in resource_list:
            try:

                allDistances1 = activity_summary1["distances"]
                dailyDistance1 = None
                for x in allDistances1:
                    if x["activity"] == "total":
                        dailyDistance1 = x["distance"]
                        break
                if dailyDistance1 is None:
                    dailyDistance1 = 0
                
                allDistances2 = activity_summary2["distances"]
                dailyDistance2 = None
                for x in allDistances2:
                    if x["activity"] == "total":
                        dailyDistance2 = x["distance"]
                        break
                if dailyDistance2 is None:
                    dailyDistance2 = 0

                allDistances3 = activity_summary3["distances"]
                dailyDistance3 = None
                for x in allDistances3:
                    if x["activity"] == "total":
                        dailyDistance3 = x["distance"]
                        break
                if dailyDistance3 is None:
                    dailyDistance3 = 0

                allDistances4 = activity_summary4["distances"]
                dailyDistance4 = None
                for x in allDistances4:
                    if x["activity"] == "total":
                        dailyDistance4 = x["distance"]
                        break
                if dailyDistance4 is None:
                    dailyDistance4 = 0
                
                allDistances5 = activity_summary5["distances"]
                dailyDistance5 = None
                for x in allDistances5:
                    if x["activity"] == "total":
                        dailyDistance5 = x["distance"]
                        break
                if dailyDistance5 is None:
                    dailyDistance5 = 0

                allDistances6 = activity_summary6["distances"]
                dailyDistance6 = None
                for x in allDistances6:
                    if x["activity"] == "total":
                        dailyDistance6= x["distance"]
                        break
                if dailyDistance6 is None:
                    dailyDistance6 = 0

                allDistances7 = activity_summary7["distances"]
                dailyDistance7 = None
                for x in allDistances7:
                    if x["activity"] == "total":
                        dailyDistance7 = x["distance"]
                        break
                if dailyDistance7 is None:
                    dailyDistance7 = 0

                currentData = [dailyDistance1,
                               dailyDistance2,
                               dailyDistance3,
                               dailyDistance4,
                               dailyDistance5,
                               dailyDistance6,
                               dailyDistance7]
                
                currentGoals = [activity_goals1["distance"],
                                activity_goals2["distance"],
                                activity_goals3["distance"],
                                activity_goals4["distance"],
                                activity_goals5["distance"],
                                activity_goals6["distance"],
                                activity_goals7["distance"]]
                
                print_data(
                    resource="distance",
                    data=currentData,
                    goal=currentGoals,
                    weekdays=weekdays
                )
            except KeyError as err:
                handle_key_error(err, "distance")

    ##################################################
    print_json("status", "API polling stage", "Sleep")
    ##################################################
    if len(resource_list) == 0 or "sleep" in resource_list:
        try:

            # get sleep data for all days
            sleep_data1 = authd_client.sleep(day1)
            sleep_summary1 = sleep_data1["summary"]
            total_minutes_asleep1 = sleep_summary1["totalMinutesAsleep"]

            sleep_data2 = authd_client.sleep(day2)
            sleep_summary2 = sleep_data2["summary"]
            total_minutes_asleep2 = sleep_summary2["totalMinutesAsleep"]

            sleep_data3 = authd_client.sleep(day3)
            sleep_summary3 = sleep_data3["summary"]
            total_minutes_asleep3 = sleep_summary3["totalMinutesAsleep"]

            sleep_data4 = authd_client.sleep(day4)
            sleep_summary4 = sleep_data4["summary"]
            total_minutes_asleep4 = sleep_summary4["totalMinutesAsleep"]

            sleep_data5 = authd_client.sleep(day5)
            sleep_summary5 = sleep_data5["summary"]
            total_minutes_asleep5 = sleep_summary5["totalMinutesAsleep"]

            sleep_data6 = authd_client.sleep(day6)
            sleep_summary6 = sleep_data6["summary"]
            total_minutes_asleep6 = sleep_summary6["totalMinutesAsleep"]

            sleep_data7 = authd_client.sleep(day7)
            sleep_summary7 = sleep_data7["summary"]
            total_minutes_asleep7 = sleep_summary7["totalMinutesAsleep"]

            currentData = [total_minutes_asleep1,
                           total_minutes_asleep2,
                           total_minutes_asleep3,
                           total_minutes_asleep4,
                           total_minutes_asleep5,
                           total_minutes_asleep6,
                           total_minutes_asleep7]

            # python-fitbit does not have this function
            # so we make it ourselves
            def get_sleep_goal(fitbit_client):
                """
                https://dev.fitbit.com/build/reference/web-api/sleep/#sleep-goals
                """
                url = "{0}/{1}/user/-/sleep/goal.json".format(
                    *fitbit_client._get_common_args()
                )
                return fitbit_client.make_request(url)

            # There is only one sleep goal for all days
            sleep_goal_data = get_sleep_goal(authd_client)
            currentGoals = [sleep_goal_data["goal"]["minDuration"],
                            sleep_goal_data["goal"]["minDuration"],
                            sleep_goal_data["goal"]["minDuration"],
                            sleep_goal_data["goal"]["minDuration"],
                            sleep_goal_data["goal"]["minDuration"],
                            sleep_goal_data["goal"]["minDuration"],
                            sleep_goal_data["goal"]["minDuration"]]

            # --------------
            print_data(
                resource="sleep",
                data=currentData,
                goal=currentGoals,
                weekdays=weekdays
            )
        except KeyError as err:
            handle_key_error(err, "sleep")

    ##################################################
    print_json("status", "API polling stage", "Heart")
    ##################################################
    if len(resource_list) == 0 or "restingHeart" in resource_list:
        try:
            # get data for all days
            heart_time_series_data1 = authd_client.time_series(resource="activities/heart", base_date=day1, period="1d")
            heart_summary_time_series1 = heart_time_series_data1["activities-heart"]
            heart_summary_day1 = heart_summary_time_series1[0]["value"]

            heart_time_series_data2 = authd_client.time_series(resource="activities/heart", base_date=day2, period="1d")
            heart_summary_time_series2 = heart_time_series_data2["activities-heart"]
            heart_summary_day2 = heart_summary_time_series2[0]["value"]

            heart_time_series_data3 = authd_client.time_series(resource="activities/heart", base_date=day3, period="1d")
            heart_summary_time_series3 = heart_time_series_data3["activities-heart"]
            heart_summary_day3 = heart_summary_time_series3[0]["value"]

            heart_time_series_data4 = authd_client.time_series(resource="activities/heart", base_date=day4, period="1d")
            heart_summary_time_series4 = heart_time_series_data4["activities-heart"]
            heart_summary_day4 = heart_summary_time_series4[0]["value"]

            heart_time_series_data5 = authd_client.time_series(resource="activities/heart", base_date=day5, period="1d")
            heart_summary_time_series5 = heart_time_series_data5["activities-heart"]
            heart_summary_day5 = heart_summary_time_series5[0]["value"]

            heart_time_series_data6 = authd_client.time_series(resource="activities/heart", base_date=day6, period="1d")
            heart_summary_time_series6 = heart_time_series_data6["activities-heart"]
            heart_summary_day6 = heart_summary_time_series6[0]["value"]

            heart_time_series_data7 = authd_client.time_series(resource="activities/heart", base_date=day7, period="1d")
            heart_summary_time_series7 = heart_time_series_data7["activities-heart"]
            heart_summary_day7 = heart_summary_time_series7[0]["value"]

            currentData = [heart_summary_day1["restingHeartRate"],
                           heart_summary_day2["restingHeartRate"],
                           heart_summary_day3["restingHeartRate"],
                           heart_summary_day4["restingHeartRate"],
                           heart_summary_day5["restingHeartRate"],
                           heart_summary_day6["restingHeartRate"],
                           heart_summary_day7["restingHeartRate"]]
            
            goalData = [0,0,0,0,0,0,0]
            # --------------
            print_data(
                resource="restingHeart",
                data=currentData,
                goal=goalData,
                weekdays=weekdays
            )
        except KeyError as err:
            handle_key_error(err, "restingHeart")

    #################################################
    print_json("status", "API polling stage", "Food")
    #################################################
    if len(resource_list) == 0 or "caloriesIn" in resource_list:
        try:

            # get data for all days
            calories_in_time_series_data1 = authd_client.time_series(resource="foods/log/caloriesIn", base_date=day1, period="1d")
            calories_in_day1 = sum(float(c["value"]) for c in calories_in_time_series_data1["foods-log-caloriesIn"])

            calories_in_time_series_data2 = authd_client.time_series(resource="foods/log/caloriesIn", base_date=day2, period="1d")
            calories_in_day2 = sum(float(c["value"]) for c in calories_in_time_series_data2["foods-log-caloriesIn"])

            calories_in_time_series_data3 = authd_client.time_series(resource="foods/log/caloriesIn", base_date=day3, period="1d")
            calories_in_day3 = sum(float(c["value"]) for c in calories_in_time_series_data3["foods-log-caloriesIn"])

            calories_in_time_series_data4 = authd_client.time_series(resource="foods/log/caloriesIn", base_date=day4, period="1d")
            calories_in_day4 = sum(float(c["value"]) for c in calories_in_time_series_data4["foods-log-caloriesIn"])

            calories_in_time_series_data5 = authd_client.time_series(resource="foods/log/caloriesIn", base_date=day5, period="1d")
            calories_in_day5 = sum(float(c["value"]) for c in calories_in_time_series_data5["foods-log-caloriesIn"])

            calories_in_time_series_data6 = authd_client.time_series(resource="foods/log/caloriesIn", base_date=day6, period="1d")
            calories_in_day6 = sum(float(c["value"]) for c in calories_in_time_series_data6["foods-log-caloriesIn"])

            calories_in_time_series_data7 = authd_client.time_series(resource="foods/log/caloriesIn", base_date=day7, period="1d")
            calories_in_day7 = sum(float(c["value"]) for c in calories_in_time_series_data7["foods-log-caloriesIn"])

            currentData = [calories_in_day1,
                           calories_in_day2,
                           calories_in_day3,
                           calories_in_day4,
                           calories_in_day5,
                           calories_in_day6,
                           calories_in_day7]

            # There is only one food goal for all days
            food_goal_data = authd_client.food_goal()
            currentGoals = [food_goal_data["goals"]["calories"],
                            food_goal_data["goals"]["calories"],
                            food_goal_data["goals"]["calories"],
                            food_goal_data["goals"]["calories"],
                            food_goal_data["goals"]["calories"],
                            food_goal_data["goals"]["calories"],
                            food_goal_data["goals"]["calories"]]

            # Changed to match other resources (used to be only calories remaining)
            print_data(
                resource="caloriesIn",
                data=currentData,
                goal=currentGoals,
                weekdays=weekdays
            )
        except KeyError as err:
            handle_key_error(err, "caloriesIn")

    ##################################################
    print_json("status", "API polling stage", "Water")
    ##################################################
    if len(resource_list) == 0 or "water" in resource_list:
        try:

            # get data for all days
            water_time_series_data1 = authd_client.time_series(resource="foods/log/water", base_date=day1, period="1d")
            water_summary_time_series1 = water_time_series_data1["foods-log-water"]
            water_summary_day1 = water_summary_time_series1[0]["value"]

            water_time_series_data2 = authd_client.time_series(resource="foods/log/water", base_date=day2, period="1d")
            water_summary_time_series2 = water_time_series_data2["foods-log-water"]
            water_summary_day2 = water_summary_time_series2[0]["value"]
            
            water_time_series_data3 = authd_client.time_series(resource="foods/log/water", base_date=day3, period="1d")
            water_summary_time_series3 = water_time_series_data3["foods-log-water"]
            water_summary_day3 = water_summary_time_series3[0]["value"]

            water_time_series_data4 = authd_client.time_series(resource="foods/log/water", base_date=day4, period="1d")
            water_summary_time_series4 = water_time_series_data4["foods-log-water"]
            water_summary_day4 = water_summary_time_series4[0]["value"]

            water_time_series_data5 = authd_client.time_series(resource="foods/log/water", base_date=day5, period="1d")
            water_summary_time_series5 = water_time_series_data5["foods-log-water"]
            water_summary_day5 = water_summary_time_series5[0]["value"]

            water_time_series_data6 = authd_client.time_series(resource="foods/log/water", base_date=day6, period="1d")
            water_summary_time_series6 = water_time_series_data6["foods-log-water"]
            water_summary_day6 = water_summary_time_series6[0]["value"]

            water_time_series_data7 = authd_client.time_series(resource="foods/log/water", base_date=day7, period="1d")
            water_summary_time_series7 = water_time_series_data7["foods-log-water"]
            water_summary_day7 = water_summary_time_series7[0]["value"]

            currentData = [max(int(round(float(water_summary_day1))),0),
                           max(int(round(float(water_summary_day2))),0),
                           max(int(round(float(water_summary_day3))),0),
                           max(int(round(float(water_summary_day4))),0),
                           max(int(round(float(water_summary_day5))),0),
                           max(int(round(float(water_summary_day6))),0),
                           max(int(round(float(water_summary_day7))),0)]
            
            # There is only one water goal for all days
            water_goal_data = authd_client.water_goal()
            currentGoals = [water_goal_data["goal"]["goal"],
                            water_goal_data["goal"]["goal"],
                            water_goal_data["goal"]["goal"],
                            water_goal_data["goal"]["goal"],
                            water_goal_data["goal"]["goal"],
                            water_goal_data["goal"]["goal"],
                            water_goal_data["goal"]["goal"]]

            # Changed to match other resources (used to be only water remaining)
            print_data(
                resource="water",
                data=currentData,
                goal=currentGoals,
                weekdays=weekdays
            )
        except KeyError as err:
            handle_key_error(err, "water")
