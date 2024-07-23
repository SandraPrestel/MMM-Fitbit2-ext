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
        weekdays=["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
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
            data=[0,0,0,0,0,0,0],
            goals=[1,1,1,1,1,1,1],
            weekdays=["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
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
    
    days = []
    for i in range(7):
        days.append(today - timedelta(days=7-i))

    print_json("debug", "days:" + str(days))
    
    # Get the weekday for these days
    week = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    weekdays = []
    for day in days:
        weekdays.append(week[day.weekday()])
    
    print_json("debug", "weekdays" + str(weekdays))

    
    #####################################################
    print_json("status", "API polling stage", "Activity")
    #####################################################
    activity_resources_all = [
        "steps", "caloriesOut", "distance", "activeMinutes"]
    activity_resources_easy_parse = ["steps", "caloriesOut"]

    if len(resource_list) == 0 or \
            any(item in activity_resources_all for item in resource_list):

        # Data is requested for the 7 days defined above
        activity_summaries = []
        activity_goals = []

        for day in days:
            activity_list = authd_client.activities(day)
            activity_summaries.append(activity_list["summary"])
            activity_goals.append(activity_list["goals"])

            print_json("debug", "Activity summary :" + str(day) + " - " + str(activity_list))

        # The easily parsable resources are printed first within a loop
        if len(resource_list) == 0:
            activity_resources_selected = activity_resources_easy_parse
        else:
            activity_resources_selected = set(resource_list) & \
                set(activity_resources_easy_parse)

        for resource in activity_resources_selected:
            try:
                currentData = []
                currentGoals = []

                for i in range(7):
                    currentData.append(activity_summaries[i][resource])
                    currentGoals.append(activity_goals[i][resource])

                print_json("debug", "CurrentData:" + str(currentData))

                print_data(
                    resource=resource,
                    data=currentData,
                    goals=currentGoals,
                    weekdays=weekdays
                )
            except KeyError as err:
                handle_key_error(err, resource)

        # These require more complicated parsing
        if len(resource_list) == 0 or "activeMinutes" in resource_list:
            try:
                currentData = []
                currentGoals = []

                for i in range(7):
                    currentData.append(activity_summaries[i]["fairlyActiveMinutes"]+activity_summaries[i]["veryActiveMinutes"])
                    currentGoals.append(activity_goals[i]["activeMinutes"])

                print_data(
                    resource="activeMinutes",
                    data=currentData,
                    goals=currentGoals,
                    weekdays=weekdays
                )
            except KeyError as err:
                handle_key_error(err, "activeMinutes")

        if len(resource_list) == 0 or "distance" in resource_list:
            try:
                currentData = []
                currentGoals = []

                for i in range(7):
                    allDistances = activity_summaries[i]["distances"]
                    dailyDistance = None

                    for x in allDistances:
                        if x["activity"] == "total":
                            dailyDistance1 = x["distance"]
                            break
                    if dailyDistance is None:
                        dailyDistance = 0

                    currentData.append(dailyDistance)
                    currentGoals.append(activity_goals[i]["distance"])
                
                print_data(
                    resource="distance",
                    data=currentData,
                    goals=currentGoals,
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
            currentData = []
            currentGoals = []

            # python-fitbit does not have a function to get sleep goals
            # so we make it ourselves
            def get_sleep_goal(fitbit_client):
                """
                https://dev.fitbit.com/build/reference/web-api/sleep/#sleep-goals
                """
                url = "{0}/{1}/user/-/sleep/goal.json".format(
                    *fitbit_client._get_common_args()
                )
                return fitbit_client.make_request(url)
            
            sleep_goal_data = get_sleep_goal(authd_client)

            for day in days:
                sleep_data = authd_client.sleep(day)
                sleep_summary = sleep_data["summary"]
                total_minutes_asleep = sleep_summary["totalMinutesAsleep"]

                currentData.append(total_minutes_asleep)

                # There is only one sleep goal for all days
                currentGoals.append(sleep_goal_data["goal"]["minDuration"])

            # --------------
            print_data(
                resource="sleep",
                data=currentData,
                goals=currentGoals,
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
            currentData = []
            currentGoals = []

            for day in days:
                heart_time_series_data = authd_client.time_series(resource="activities/heart", base_date=day, period="1d")
                heart_summary_time_series = heart_time_series_data["activities-heart"]
                heart_summary_day = heart_summary_time_series[0]["value"]

                currentData.append(heart_summary_day["restingHeartRate"])

                # There is no goal for heart rate
                currentGoals.append(0)

            # --------------
            print_data(
                resource="restingHeart",
                data=currentData,
                goals=currentGoals,
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
            currentData = []
            currentGoals = []

            food_goal_data = authd_client.food_goal()

            for day in days:
                calories_in_time_series_data = authd_client.time_series(resource="foods/log/caloriesIn", base_date=day, period="1d")
                calories_in_day = sum(float(c["value"]) for c in calories_in_time_series_data["foods-log-caloriesIn"])

                currentData.append(calories_in_day)

                 # There is only one food goal for all days
                currentGoals.append(food_goal_data["goals"]["calories"]) 

            # Changed to match other resources (was only calories remaining in fitbit2)
            print_data(
                resource="caloriesIn",
                data=currentData,
                goals=currentGoals,
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
            currentData = []
            currentGoals = []

            water_goal_data = authd_client.water_goal()

            for day in days:
                water_time_series_data = authd_client.time_series(resource="foods/log/water", base_date=day, period="1d")
                water_summary_time_series = water_time_series_data["foods-log-water"]
                water_summary_day = water_summary_time_series[0]["value"]
                
                currentData.append(max(int(round(float(water_summary_day))),0))

                # There is only one water goal for all days
                currentGoals.append(water_goal_data["goal"]["goal"])    

            # Changed to match other resources (was only water remaining in fitbit2)
            print_data(
                resource="water",
                data=currentData,
                goals=currentGoals,
                weekdays=weekdays
            )
        except KeyError as err:
            handle_key_error(err, "water")
