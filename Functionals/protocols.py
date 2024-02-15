from Utilities.functions import *
from Functionals.background_ai import *

def play_alarm():
    play_notification_sound("./AudioFiles/alarm_clock.mp3")

def check_for_alarm():
    alarms = loadconfig("./Settings/reminders.json")

    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")

    for alarm in alarms["reminders"]:
        alarm_time = alarm.get("time")

        if alarm_time == formatted_time:
            return alarm
    
    return None


def perform_action(task):
    task = task.get("tag")

    if task == "alarm":
        play_alarm()
    
def background_run_protocols():
    Instance = TaskAI()

    while True:

        task = None

        if check_for_alarm() is not None:
            task = Instance.compare("Time is matching")
    
        if task is not None:
            perform_action(task)

def run_protocols():
    print("Background protocols loop is now active.")
    threading.Thread(target=background_run_protocols, args=()).start()