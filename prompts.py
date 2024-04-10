

class Prompts:

    to_webpage_rater = (
        "请对已爬取的网页内容进行评分。"
        "请确保你的评分反映了每个网页与用户需求-即{}的匹配程度。为网页分配一个从1到10的分数，"
        "其中10表示完美匹配用户需求。同时，请为评分提供简短的理由，解释为何该网页获得了此分数。"
        "Respond in the following "
        "json format which can be loaded by python json.loads()\n"
        "{{\n"
        '    "score": "score", \n'
        '    "reason": "reason why it gets the score",\n'
        "}}"
    )

















