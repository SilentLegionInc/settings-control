import datetime
import subprocess


def ceil_datetime_up_to_minutes(value):
    temp = value.replace(second=0, microsecond=0)
    if temp == value:
        return value
    else:
        return temp + datetime.timedelta(minutes=1)


def floor_datetime_up_to_minutes(value):
    return value.replace(second=0, microsecond=0)


# send a command to the shell and return the result
def cmd(command):
    return subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ).stdout.read().decode()


def allowed_file_extension(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
