import json
import pytz
from datetime import datetime, timedelta

from telegram import InlineKeyboardButton


class Booking:
    booking_status = False
    date = ''
    time = ''
    people = 0
    timezone_madrid = pytz.timezone('Europe/Madrid')
    datetime_madrid = datetime.now(timezone_madrid)
    today = datetime_madrid.strftime("%d-%m-%Y")

    def next_dates_buttons(self):
        date_list = []
        d = self.datetime_madrid.strptime(self.today, "%d-%m-%Y")
        hour = self.datetime_madrid.strftime('%H')
        if self.datetime_madrid.weekday() != 0 and int(hour) < 20:
            date_list.append(
                [InlineKeyboardButton(
                    d.strftime("%d-%m-%Y"),
                    callback_data=json.dumps({"name": "date", "data": d.strftime("%d-%m-%Y")})
                )]
            )
        for x in range(0, 7):
            d = d + timedelta(days=1)
            if d.weekday() != 0:
                date_list.append(
                    [InlineKeyboardButton(
                        d.strftime("%d-%m-%Y"),
                        callback_data=json.dumps({"name": "date", "data": d.strftime("%d-%m-%Y")})
                    )]
                )
        return date_list

    def day_turns_buttons(self, date):
        hour = self.datetime_madrid.strftime('%H')
        turn_list = []
        if self.datetime_madrid.strftime('%d-%m-%Y') == date and int(hour) > 12:
            turn_list.append(
                [InlineKeyboardButton(
                    "Tarde",
                    callback_data=json.dumps({"name": "people", "data": "afternoon"})
                )]
            )
        else:
            turn_list.append(
                [InlineKeyboardButton(
                    "Mañana",
                    callback_data=json.dumps({"name": "people", "data": "morning"})
                )]
            )
            turn_list.append(
                [InlineKeyboardButton(
                    "Tarde",
                    callback_data=json.dumps({"name": "people", "data": "afternoon"})
                )]
            )

        self.date = date
        return turn_list
