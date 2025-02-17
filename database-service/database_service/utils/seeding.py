import pandas as pd
from sqlalchemy import text, Date, Time, Numeric
from database_service.utils import engine


def seed_data() -> None:
    with engine.connect() as conn:
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS sales (
                date DATE,
                week_day VARCHAR(9),
                hour TIME,
                ticket_number VARCHAR(20),
                waiter INT,
                product_name VARCHAR(255),
                quantity INT,
                unitary_price DECIMAL(10,2),
                total DECIMAL(10,2)
            )
        """)
        )
        conn.commit()

    df = pd.read_csv("../../data/data.csv", parse_dates=["date"])

    for col in ["unitary_price", "total"]:
        df[col] = df[col] / 100

    print(f"Seeding into database...\nTail(20): {df.tail(20)}")

    df.to_sql(
        "sales",
        engine,
        if_exists="replace",
        index=False,
        dtype={
            "date": Date(),
            "hour": Time(),
            "unitary_price": Numeric(10, 2),
            "total": Numeric(10, 2),
        },
    )
