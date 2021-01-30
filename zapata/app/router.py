from datetime import datetime

import pandas as pd
from flask import Blueprint, flash, redirect, render_template, request, url_for
from wtforms import Form, IntegerField, StringField

from database import db
from models import Building, Incident

router = Blueprint("router", __name__)


def color_negative_red(row) -> list[str]:
    return [
        "background-color: red"
        if row["Alert"] and index == datetime.now().strftime("%b")
        else "background-color: white"
        for index, val in row.items()
    ]


def render(df, name) -> str:
    df.index += 1

    props = [("border", "2px solid black")]

    styles = [
        {"selector": "table, th, td", "props": props},
    ]

    if name == "income":
        df = df[["Total", "Monthly", "Jan", "Feb", "Balance", "Alert"]]

        return (
            df.style.hide_columns(["Alert"])
            .set_properties(
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
    else:
        return (
            df.style.set_properties(
                **{
                    "background-color": "white",
                    "color": "black",
                }
            )
            .set_table_styles(styles)
            .render()
        )


@router.route("/", methods=["GET"])
def _index() -> str:
    with db.engine.begin() as conn:
        df = pd.read_sql_table("income", conn)
        df["Monthly"] = (df["Total"] / 12).astype(int)
        df["Balance"] = df["Total"] - sum([df["Jan"], df["Feb"]])

        currentMonth = datetime.now().month
        df["Alert"] = currentMonth * df["Monthly"] > sum(
            [df["Jan"], df["Feb"]]
        )

        df.to_sql("income", con=conn, if_exists="replace", index=False)

    with db.engine.begin() as conn:
        df1 = pd.read_sql_table("income", conn)
        df2 = pd.read_sql_table("incidents", conn)
        df3 = pd.read_sql_table("buildings", conn)

    return render_template(
        "index.html",
        income=render(df1, "income"),
        incidents=render(df2, "incidents"),
        buildings=render(df3, "buildings"),
    )


@router.route("/incident", methods=["GET", "POST"])
def _incident() -> str:
    class newIncident(Form):
        description = StringField("Description")

    form = newIncident(request.form)

    if request.method == "POST" and form.validate():
        try:
            db.session.add(Incident(description=form.description.data))
            db.session.commit()
            flash("Incident was created", "success")
        except Exception as e:
            print(f"{e}", flush=True)
            flash(f"{e}", category="warning")
        return redirect(url_for("router._index"))
    return render_template("incident.html", form=form)


@router.route("/building", methods=["GET", "POST"])
def _building() -> str:
    class newBuilding(Form):
        address = StringField("Address")
        flats = IntegerField("Number of Flats")

    form = newBuilding(request.form)

    if request.method == "POST" and form.validate():
        try:
            db.session.add(
                Building(address=form.address.data, flats=form.flats.data)
            )
            db.session.commit()
            flash("Building was created", "success")
        except Exception as e:
            print(f"{e}", flush=True)
            flash(f"{e}", category="warning")
        return redirect(url_for("router._index"))
    return render_template("building.html", form=form)
