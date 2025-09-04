import json
import os
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict

try:
    import yaml
except ImportError:
    yaml = None

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from dotenv import load_dotenv


STATE_PATH = Path(__file__).parent / "state.json"
PROBLEMS_PATH = Path(__file__).parent / "problems.yaml"


load_dotenv()

BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

if not BOT_TOKEN or not CHANNEL_ID:
    raise RuntimeError("Faltan variables SLACK_BOT_TOKEN o SLACK_CHANNEL_ID en .env")




def load_problems() -> List[Dict]:
    if PROBLEMS_PATH.exists():
        if yaml is None:
            raise RuntimeError("Instala pyyaml o elimina problems.yaml")
        with PROBLEMS_PATH.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or []
            assert isinstance(data, list)
            return data
    return DEFAULT_PROBLEMS


def init_state(n: int) -> Dict:
    order = list(range(n))
    random.shuffle(order)
    return {"order": order, "pos": 0, "last_post": None}


def load_state(n: int) -> Dict:
    if STATE_PATH.exists():
        with STATE_PATH.open("r", encoding="utf-8") as f:
            state = json.load(f)
        if "order" not in state or len(state["order"]) != n:
            state = init_state(n)
    else:
        state = init_state(n)
    return state


def save_state(state: Dict):
    STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def today_iso() -> str:
    return datetime.now().date().isoformat()


def select_today(problems: List[Dict], state: Dict) -> Dict:
    if state.get("last_post") == today_iso():
        return problems[state["order"][state["pos"] - 1]]

    pos = state.get("pos", 0)
    idx = state["order"][pos]
    problem = problems[idx]

    state["pos"] = (pos + 1) % len(problems)
    state["last_post"] = today_iso()

    return problem


def build_message(problem: Dict) -> Dict:
    title, prompt = problem.get("title"), problem.get("prompt")
    hints = problem.get("hints", [])
    tags = problem.get("tags", [])

    hints_md = "\n".join([f"• {h}" for h in hints]) if hints else "—"
    tags_md = ", ".join(tags) if tags else "principiante"

    header = f":snake: *Reto Python del día:* *{title}*"
    body = f"{prompt}\n\n*Pistas:*\n{hints_md}\n\n*Etiquetas:* `{tags_md}`"

    return {
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": header}},
            {"type": "section", "text": {"type": "mrkdwn", "text": body}},
            {"type": "divider"}
        ]
    }


def post_to_slack(payload: Dict):
    client = WebClient(token=BOT_TOKEN)
    try:
        client.chat_postMessage(channel=CHANNEL_ID, **payload)
    except SlackApiError as e:
        raise RuntimeError(
            f"Error Slack: {e.response.data if hasattr(e, 'response') else e}"
        )

def cargar_preguntas():
   # raise Exception("Sorry, no hay implementacion")
    from POO import cargar_preguntas_poo
    cargar_preguntas_poo()  # Ejecutar la función de POO

def main():
    # Cargar variables desde .env
    load_dotenv()
    if not BOT_TOKEN or not CHANNEL_ID:
        raise RuntimeError("Faltan variables de entorno")
    cargar_preguntas()
    problems = load_problems()
    state = load_state(len(problems))
    prob = select_today(problems, state)
    payload = build_message(prob)

    post_to_slack(payload)
    save_state(state)

    print("Publicado:", prob["title"])


if __name__ == "__main__":
    main()