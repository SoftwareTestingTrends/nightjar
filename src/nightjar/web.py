"""The NightJar web app: one server-rendered page plus a small JSON API.

Run with:  uv run uvicorn nightjar.web:create_app --factory --reload
"""

import os
from collections.abc import Callable
from datetime import UTC, datetime, time
from pathlib import Path

from fastapi import FastAPI, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from nightjar.coach import Coach, ask_coach, get_coach
from nightjar.coach.service import DEFAULT_TRACE_PATH
from nightjar.diary import Diary, local_input_to_aware, parse_csv
from nightjar.models import Night, User
from nightjar.nudge import next_nudge
from nightjar.sleep_window import usual_bedtime

HERE = Path(__file__).parent
Clock = Callable[[], datetime]


def system_clock() -> datetime:
    return datetime.now(UTC)


class CoachQuestion(BaseModel):
    question: str


def create_app(
    diary: Diary | None = None,
    coach: Coach | None = None,
    clock: Clock = system_clock,
    trace_path: Path = DEFAULT_TRACE_PATH,
) -> FastAPI:
    diary = diary or Diary(os.environ.get("NIGHTJAR_DB", "nightjar.db"))
    coach = coach or get_coach()
    templates = Jinja2Templates(directory=HERE / "templates")
    app = FastAPI(title="NightJar")
    app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")

    def render(request: Request, status_code: int = 200, **extra) -> HTMLResponse:
        user, nights = diary.user(), diary.nights()
        context = {
            "user": user,
            "nights": nights,
            "usual_bedtime": usual_bedtime(nights),
            "nudge": next_nudge(user, nights, clock()),
            "imported": request.query_params.get("imported"),
            **extra,
        }
        return templates.TemplateResponse(request, "index.html", context, status_code=status_code)

    @app.get("/", response_class=HTMLResponse)
    def home(request: Request):
        return render(request)

    @app.post("/nights")
    def add_night(
        request: Request,
        bedtime: str = Form(...),
        wake_time: str = Form(...),
        timezone: str = Form(...),
        notes: str = Form(""),
    ):
        try:
            diary.add_night(
                Night(
                    bedtime=local_input_to_aware(bedtime, timezone),
                    wake_time=local_input_to_aware(wake_time, timezone),
                    timezone=timezone,
                    notes=notes.strip(),
                )
            )
        except ValueError as error:
            return render(request, status_code=400, error=str(error))
        return RedirectResponse("/", status_code=303)

    @app.post("/import")
    async def import_csv(request: Request, file: UploadFile):
        try:
            nights = parse_csv((await file.read()).decode("utf-8-sig"))
        except (ValueError, UnicodeDecodeError) as error:
            return render(request, status_code=400, error=f"Import failed. {error}")
        count = diary.add_nights(nights)
        return RedirectResponse(f"/?imported={count}", status_code=303)

    @app.post("/settings")
    def save_settings(
        request: Request,
        timezone: str = Form(...),
        quiet_start: str = Form(""),
        quiet_end: str = Form(""),
        wind_down_lead: str = Form(""),
    ):
        saved = diary.user()
        try:
            lead = int(wind_down_lead) if wind_down_lead.strip() else saved.wind_down_lead_minutes
            diary.save_user(
                User(
                    name=saved.name,
                    timezone=timezone.strip(),
                    quiet_start=time.fromisoformat(quiet_start) if quiet_start else None,
                    quiet_end=time.fromisoformat(quiet_end) if quiet_end else None,
                    wind_down_lead_minutes=lead,
                )
            )
        except ValueError as error:
            return render(request, status_code=400, error=str(error))
        return RedirectResponse("/", status_code=303)

    @app.post("/coach", response_class=HTMLResponse)
    def coach_page(request: Request, question: str = Form(...)):
        answer = ask_coach(coach, diary.nights(), question, trace_path)
        return render(request, question=question, answer=answer)

    @app.get("/api/nudge")
    def api_nudge():
        user = diary.user()
        nudge = next_nudge(user, diary.nights(), clock())
        if nudge is None:
            return {"nudge": None, "reason": "Log at least 7 nights to get a nudge."}
        return {
            "nudge": {
                "at": nudge.at.isoformat(),
                "local_time": f"{nudge.at:%H:%M}",
                "lead_minutes": user.wind_down_lead_minutes,
                "silent": nudge.silent,
                "text": nudge.text,
            }
        }

    @app.post("/api/coach")
    def api_coach(body: CoachQuestion):
        answer = ask_coach(coach, diary.nights(), body.question, trace_path)
        return {"answer": answer.text, "used_fallback": answer.used_fallback}

    return app
