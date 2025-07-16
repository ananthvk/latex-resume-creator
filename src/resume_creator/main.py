import json
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader, FileSystemLoader
from typing import Any, Dict

env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    block_start_string="<start-block>",
    block_end_string="<end-block>",
    variable_start_string="<start-variable>",
    variable_end_string="<end-variable>",
    comment_start_string="<start-comment>",
    comment_end_string="<end-comment>",
    line_comment_prefix="<line-comment>",
)


# https://stackoverflow.com/questions/29959191/how-to-parse-json-file-with-c-style-comments
class JSONWithCommentsDecoder(json.JSONDecoder):
    def __init__(self, **kw):
        super().__init__(**kw)

    def decode(self, s: str) -> Any:
        s = "\n".join(
            l if not l.lstrip().startswith("//") else "" for l in s.split("\n")
        )
        return super().decode(s)


def load_resume_data() -> Dict[Any, Any]:
    resume_json_path = Path(__file__).parent / "data" / "resume.json"
    with open(resume_json_path, "r", encoding="utf-8") as f:
        return json.load(f, cls=JSONWithCommentsDecoder)


def get_resume() -> str:
    load_dotenv()
    variables = load_resume_data()
    if os.environ.get("SHOW_PERSONAL_INFO") is not None:
        variables["personal_info"]["phone"] = os.environ.get("PHONE", " ")
        variables["personal_info"]["email"] = os.environ.get("EMAIL", " ")
    template = env.get_template("resume.tex")

    # Only select enabled experiences
    experiences = []
    for experience_id in variables["enabled"]["experiences"]:
        experiences += [variables["experiences"][experience_id]]
    variables["experiences"] = experiences

    # Only select enabled projects
    projects = []
    for project_id in variables["enabled"]["projects"]:
        projects += [variables["projects"][project_id]]
    variables["projects"] = projects

    # Only select enabled achievements
    achievements = []
    for achievement_id in variables["enabled"]["achievements"]:
        achievements += [variables["achievements"][achievement_id]]
    variables["achievements"] = achievements

    output = template.render(**variables)
    return output


def run():
    parser = argparse.ArgumentParser(description="Generate resume from JSON data")
    parser.add_argument(
        "--stdout", action="store_true", help="Output to stdout instead of file"
    )
    args = parser.parse_args()
    resume = get_resume()

    if args.stdout:
        print(resume)


if __name__ == "__main__":
    run()
