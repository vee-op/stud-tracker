from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.crud import create_student, get_student_progress, update_student_progress, count_students, get_all_students
# added -  get_all_students (in line 4 above)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

#added - health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    total = await count_students()
    return templates.TemplateResponse("index.html", {"request": request, "total": total})

@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register_submit(request: Request, name: str = Form(...)):
    student = await create_student(name)
    return templates.TemplateResponse("register.html", {"request": request, "message": f"Welcome, {student.name}!"})

@app.get("/progress", response_class=HTMLResponse)
async def progress_form(request: Request):
    return templates.TemplateResponse("progress.html", {"request": request})

@app.post("/progress", response_class=HTMLResponse)
async def progress_submit(request: Request, name: str = Form(...)):
    student = await get_student_progress(name)
    progress = []

    if student and  "progress" in student:
       for week, status in student["progress"].items():
          progress.append({"week": week, "status": status})
    return templates.TemplateResponse("progress.html", {"request": request, "progress": progress, "name": name})

@app.get("/update", response_class=HTMLResponse)
async def update_form(request: Request):
    return templates.TemplateResponse("update.html", {"request": request})

@app.post("/update", response_class=HTMLResponse)
async def update_submit(
    request: Request,
    name: str = Form(...),
    week: str = Form(...),
    status: str = Form(...)
):
    await update_student_progress(name, week, status)
    return templates.TemplateResponse("update.html", {"request": request, "message": "Progress updated successfully!"})

# added Admin routes operations - Get all students
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    students = await get_all_students()
    return templates.TemplateResponse("admin.html", {"request": request, "students": students})
