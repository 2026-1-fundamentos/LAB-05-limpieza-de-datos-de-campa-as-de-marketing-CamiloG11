"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import os
import zipfile

import pandas as pd


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortgage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaign_contacts
    - previous_outcome: cambiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - cons_price_idx
    - euribor_three_months
    """

    input_dir = "files/input"
    output_dir = "files/output"
    os.makedirs(output_dir, exist_ok=True)

    # -- Leer todos los archivos zip directamente --
    all_data = []
    for fname in sorted(os.listdir(input_dir)):
        if not fname.endswith(".csv.zip"):
            continue
        with zipfile.ZipFile(os.path.join(input_dir, fname)) as zf:
            csv_file = zf.namelist()[0]
            with zf.open(csv_file) as fh:
                chunk = pd.read_csv(fh, index_col=0)
                all_data.append(chunk)

    data = pd.concat(all_data, ignore_index=True)

    # -- Mapeo de meses a número --
    month_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12",
    }

    # ============================================================
    #  client.csv
    # ============================================================
    client = pd.DataFrame()
    client["client_id"] = data["client_id"]
    client["age"] = data["age"]
    client["job"] = (
        data["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )
    client["marital"] = data["marital"]
    client["education"] = (
        data["education"]
        .str.replace(".", "_", regex=False)
        .replace("unknown", pd.NA)
    )
    client["credit_default"] = (data["credit_default"] == "yes").astype(int)
    client["mortgage"] = (data["mortgage"] == "yes").astype(int)

    client.to_csv(os.path.join(output_dir, "client.csv"), index=False)

    # ============================================================
    #  campaign.csv
    # ============================================================
    campaign = pd.DataFrame()
    campaign["client_id"] = data["client_id"]
    campaign["number_contacts"] = data["number_contacts"]
    campaign["contact_duration"] = data["contact_duration"]
    campaign["previous_campaign_contacts"] = data["previous_campaign_contacts"]
    campaign["previous_outcome"] = (
        data["previous_outcome"] == "success"
    ).astype(int)
    campaign["campaign_outcome"] = (
        data["campaign_outcome"] == "yes"
    ).astype(int)
    campaign["last_contact_date"] = (
        "2022-"
        + data["month"].map(month_map)
        + "-"
        + data["day"].astype(str).str.zfill(2)
    )

    campaign.to_csv(os.path.join(output_dir, "campaign.csv"), index=False)

    # ============================================================
    #  economics.csv
    # ============================================================
    economics = pd.DataFrame()
    economics["client_id"] = data["client_id"]
    economics["cons_price_idx"] = data["cons_price_idx"]
    economics["euribor_three_months"] = data["euribor_three_months"]

    economics.to_csv(os.path.join(output_dir, "economics.csv"), index=False)


if __name__ == "__main__":
    clean_campaign_data()
