from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()
df = pd.read_excel("דוח_ירי_צבאי.xlsx")

ALLOWED_QUERIES = {
    "כמה טילים נורו בסך הכל?": lambda df: df["טילים שנורו"].sum(),
    "מה האזור עם הכי הרבה פגיעות ישירות?": lambda df: df.loc[df["פגיעות ישירות"].idxmax()]["אזור"],
    "מה סוג הירי הנפוץ ביותר?": lambda df: df["סוג ירי"].value_counts().idxmax(),
    "מה אחוז ההצלחות של מערכת היירוט?": lambda df: round((df["יירוטים מוצלחים"].sum() / df["טילים שנורו"].sum()) * 100, 2),
    "כמה אירועים התרחשו בתאריך 2025-07-02?": lambda df: df[df["תאריך"] == "2025-07-02"].shape[0],
    "כמה פגיעות ישירות היו בסך הכל?": lambda df: df["פגיעות ישירות"].sum(),
    "מה הממוצע של טילים פר אירוע?": lambda df: round(df["טילים שנורו"].mean(), 2),
    "כמה אזורים שונים הופיעו בדוח?": lambda df: df["אזור"].nunique()
}

class QuestionInput(BaseModel):
    question: str

class AnswerOutput(BaseModel):
    answer: str

@app.post("/call", response_model=AnswerOutput)
def call_mcp(query: QuestionInput):
    question = query.question.strip()
    if question not in ALLOWED_QUERIES:
        return {"answer": "השאלה לא קיימת ברשימת השאלות הנתמכות."}
    try:
        result = ALLOWED_QUERIES[question](df)
        return {"answer": str(result)}
    except Exception as e:
        return {"answer": f"שגיאה בביצוע השאילתה: {e}"}