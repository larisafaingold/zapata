#!/usr/bin/env python3

from datetime import datetime

import pandas as pd
from flask import render_template


def configure_routes(app, db):
    def render(df) -> str:
        df = df[["Total", "Monthly", "January", "Balance"]]

        props = [("border", "2px solid black")]

        styles = [
            {"selector": "table, th, td", "props": props},
        ]

        return (
            df.style.set_properties(
                **{
                    "background-color": "white",
                    "color": "black",
                }
            )
            .apply(color_negative_red, axis=1)
            .format("₪ {}")
            .set_table_styles(styles)
            .render()
        )

    def color_negative_red(row) -> list[str]:
        currentMonth = datetime.now().month
        return [
            "background-color: red"
            if currentMonth * row["Monthly"] > sum([row["January"]])
            and index == "January"
            else "background-color: white"
            for index, val in row.items()
        ]

    @app.route("/", methods=["GET"])
    def index() -> str:
        df = pd.read_json("data.json")
        df["Monthly"] = (df["Total"] / 12).astype(int)
        df["Balance"] = df["Total"] - sum([df["January"]])

        return render_template("index.html", table=render(df))
