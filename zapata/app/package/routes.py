#!/usr/bin/env python3

import pandas as pd
from flask import flash, redirect, render_template, request, url_for
from mailchimp3 import MailChimp
from passlib.hash import sha256_crypt
from wtforms import Form, PasswordField, StringField, validators
from wtforms.validators import DataRequired, Email

from modules.secrets import get_secret


class newAccountForm(Form):
    name = StringField(
        "Name",
        [
            validators.Regexp(
                r"[A-Za-z\s]+",
                message="Name may only contain alphanumeric \
                          characters and spaces",
            ),
            validators.Length(min=1, max=50),
        ],
    )
    email = StringField(
        "Email", [validators.Email(), validators.Length(min=6, max=50)]
    )
    username = StringField(
        "Username",
        [
            validators.Regexp(
                r"[A-Za-z0-9_]+",
                message="Name may only contain alphanumeric \
                          characters",
            ),
            validators.Length(min=4, max=25),
        ],
    )
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords do not match"),
        ],
    )
    confirm = PasswordField("Confirm Password")


def configure_routes(app, db):
    class SubscribeForm(Form):
        email = StringField("Email", validators=[DataRequired(), Email()])

    @app.route("/", methods=["GET", "POST"])
    @app.route("/home", methods=["GET", "POST"])
    def home():
        form = SubscribeForm(request.form)

        if request.method == "POST" and form.validate():
            app.logger.info("New subscriber %s", form.email.data)

            add_subscriber(app, db, form.email.data)
            return redirect(url_for("home"))

        return render_template("index.html", form=form)

    @app.route("/new_account", methods=["GET", "POST"])
    def new_account():
        form = newAccountForm(request.form)

        if request.method == "POST" and form.validate():
            name = form.name.data
            email = form.email.data
            username = form.username.data
            password = sha256_crypt.encrypt(str(form.password.data))

            try:
                # Create cursor
                cur = db.connection.cursor()

                cur.execute(
                    "INSERT INTO users(name, email, username, password) \
                    VALUES(%s, %s, %s, %s)",
                    (name, email, username, password),
                )

                # Commit to DB
                db.connection.commit()

                # Close connection
                cur.close()

                flash("Account was created", "success")

            except Exception as e:
                flash("{}".format(e.args[1]), category="warning")

            return redirect(url_for("home"))

        return render_template("new_account.html", form=form)

    def add_subscriber(app, db, email):
        try:
            cur = db.connection.cursor()
            cur.execute(
                "INSERT INTO subscribers (email) VALUES ('{0}')".format(email)
            )
            db.connection.commit()
            cur.close()
            client = MailChimp(
                mc_api=get_secret("vault-server", "mailchimp/apikey"),
                mc_user=get_secret("vault-server", "mailchimp/username"),
            )
            client.lists.members.create(
                get_secret("vault-server", "mailchimp/listid"),
                {
                    "email_address": "{email}".format(email=email),
                    "status": "subscribed",
                },
            )
            flash("You are now subscribed", "success")

        except Exception as e:
            app.logger.info(e)

    def format(x) -> str:
        return f"₪ {x}"

    @app.route("/building", methods=["GET", "POST"])
    def building() -> str:
        d = {
            "Appartment": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
            ],
            "Total": [
                5400,
                5400,
                3780,
                3780,
                3780,
                3780,
                3780,
                4500,
                4500,
                4860,
                5400,
                5400,
                4860,
                5400,
                4860,
                5400,
                4860,
                7200,
                7200,
            ],
            "Monthly": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ],
            "January": [
                0,
                0,
                0,
                315,
                0,
                157,
                0,
                0,
                0,
                0,
                450,
                0,
                0,
                5400,
                0,
                1350,
                405,
                0,
                600,
            ],
            "Balance": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ],
        }
        df = pd.DataFrame(data=d)
        df["Monthly"] = (df["Total"] / 12).astype(int)
        df["Balance"] = df["Total"] - df["January"]

        df["Total"] = df["Total"].apply(format)
        df["Monthly"] = df["Monthly"].apply(format)
        df["January"] = df["January"].apply(format)
        df["Balance"] = df["Balance"].apply(format)

        return render_template("building.html", table=df.to_html(index=False))