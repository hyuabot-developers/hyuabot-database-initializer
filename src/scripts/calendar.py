import datetime

import urllib3
import ssl
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from sqlalchemy import delete, insert
from sqlalchemy.orm import Session

from models.calendar import CalendarVersion, CalendarCategory, Calendar


class HTTPSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("AES256-GCM-SHA384")
        self.poolmanager = urllib3.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLSv1_2,
            ssl_context=ctx,
        )


async def insert_calendar_data(db_session: Session):
    calendar_url = "https://www.hanyang.ac.kr/web/www/-93"
    params = {
        "p_p_id": "calendarView_WAR_eventportlet",
        "p_p_lifecycle": "0",
        "p_p_state": "normal",
        "p_p_mode": "view",
        "p_p_col_id": "column-1",
        "p_p_col_count": "1",
        "_calendarView_WAR_eventportlet_action": "view",
    }
    now_year = datetime.datetime.now().astimezone(tz=datetime.timezone(datetime.timedelta(hours=9))).year
    data: dict[int, list[str]] = {}
    for i in range(now_year - 8, now_year + 1):
        form_data = {
            "_calendarView_WAR_eventportlet_sYear": i,
            "_calendarView_WAR_eventportlet_sMonth": 0,
        }
        data[i] = []
        with requests.Session() as session:
            session.mount("https://", HTTPSAdapter())
            response = session.post(calendar_url, params=params, data=form_data)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            selector = "div > div > div > div > table > tbody > tr > td > div > p > span"
            for span in soup.select(selector):
                data[i].append(span.text.strip())

    insert_data = []
    event_id = 1
    for k, v in data.items():
        for index in range(0, len(v), 2):
            year = k
            if "~" in v[index]:
                start_date = v[index].split(" ")[0]
                end_date = v[index].split(" ")[3]
                start_month, start_day = str(start_date).split("/")
                if "/" in end_date:
                    end_month, end_day = str(end_date).split("/")
                else:
                    end_month, end_day = start_month, end_date
            else:
                start_month, start_day = str(v[index]).split(" ")[0].split("/")
                end_month, end_day = start_month, start_day

            if int(start_month) < 3:
                year += 1
            start_datetime = datetime.datetime(year, int(start_month), int(start_day))
            if (int(start_month) > int(end_month)
                    or (int(start_month) == int(end_month) and int(start_day) > int(end_day))):
                year += 1
            end_datetime = datetime.datetime(year, int(end_month), int(end_day))
            insert_data.append({
                "academic_calendar_id": event_id,
                "category_id": 1,
                "start_date": start_datetime,
                "end_date": end_datetime,
                "title": v[index + 1],
                "description": "",
            })
            event_id += 1
    # Delete all calendar data
    delete_calendar_statement = delete(Calendar)
    db_session.execute(delete_calendar_statement)
    delete_calendar_category_statement = delete(CalendarCategory)
    db_session.execute(delete_calendar_category_statement)
    delete_calendar_version_statement = delete(CalendarVersion)
    db_session.execute(delete_calendar_version_statement)
    db_session.commit()
    # Insert new calendar data
    now = datetime.datetime.now().astimezone(tz=datetime.timezone(datetime.timedelta(hours=9)))
    insert_version_statement = insert(CalendarVersion).values({
        "version_id": 1,
        "version_name": now.strftime("%Y-%m-%d %H:%M:%S"),
        "created_at": now,
    })
    db_session.execute(insert_version_statement)
    insert_category_statement = insert(CalendarCategory).values({
        "category_id": 1,
        "category_name": "전체",
    })
    db_session.execute(insert_category_statement)
    insert_calendar_statement = insert(Calendar).values(insert_data)
    db_session.execute(insert_calendar_statement)
    db_session.commit()
