import pandas as pd
import yfinance as yf


def getFinanceData(indicators, startDate, endDate):
    data = []

    try:
        for indicator in indicators:
            # Download data for each indicator and append it to the list
            df = yf.download(indicator, start=startDate, end=endDate, interval="1mo")
            data.append(df)

        return data
    except Exception as e:
        print(e)


def cagr(revenue, montantInvest, dateRange):
    return (revenue / montantInvest) ** (1 / dateRange) - 1


def ratioSharp(rendementMoyen, rendementSansRisque, volatilite):
    return (rendementMoyen - rendementSansRisque) / volatilite


def volatilite(prix_action):
    return prix_action.std()


def revenue(name, montantInitial, montantRecurant, financeTable):
    # variationsList = [["Date", "Montant Investi", "Revenue"]]
    variationsList = []
    variationsList.append(
        [financeTable.index[0].strftime("%d/%m/%Y"), montantInitial, montantInitial]
    )

    montantInvest = montantInitial

    # calcule de rendement
    nbAction = 0

    # le prix d'action au moment d'investisement
    prixAction = financeTable["Adj Close"].iloc[0]

    # nombre d'action que on peut acheter
    nbAction = montantInvest // prixAction

    liquidite = montantInvest - (prixAction * nbAction)

    for ind in financeTable.index[1:]:
        # montant qu'on va ivestir ce mois
        montantRecMois = montantRecurant + liquidite

        # prix action lors de l'achat
        # prixAction = financeTable["Adj Close"].iloc[ind]
        prixAction = financeTable.loc[ind, "Adj Close"]

        # nombre d'action achetées ce mois
        nbActionAchete = montantRecMois // prixAction

        # nb action total
        nbAction += nbActionAchete

        # liquidité
        liquidite = montantRecMois - nbActionAchete * prixAction

        # mise a jour de montant investi
        montantInvest += montantRecurant

        variationsList.append(
            [ind.strftime("%d/%m/%Y"), montantInvest, nbAction * prixAction + liquidite]
        )

    lastAdjClose = financeTable["Adj Close"].iloc[-1]
    revenue = nbAction * lastAdjClose + liquidite
    rendementMoyen = (revenue / montantInvest) - 1

    return {
        "name": name,
        "montantInvest": montantInvest,
        "revenue": revenue,
        "rendementMoyen": rendementMoyen,
        "variations": variationsList,
    }


def ecartInterquartille(df):
    # calcule de l'ecart interquartille
    quartiles = df["Close"].quantile([0.25, 0.75])
    iqr = quartiles[0.75] - quartiles[0.25]
    return iqr


def ecartType(df):
    return df.std()


def moyenne(df):
    return df.mean()


def getData(indicators, startDate, endDate, montantInitial, montantRecurant):
    data = getFinanceData(indicators, startDate, endDate)

    revenueStats = []
    for i in range(len(data)):
        rev = revenue(indicators[i], montantInitial, montantRecurant, data[i])
        revenueStats.append(rev)

    df = pd.DataFrame(
        revenueStats[0]["variations"],
        columns=[
            "date",
            f"{revenueStats[0]['name']} investi",
            f"{revenueStats[0]['name']} revenue",
        ],
    )

    if len(revenueStats) == 2:
        df2 = pd.DataFrame(
            revenueStats[1]["variations"],
            columns=[
                "date",
                f"{revenueStats[1]['name']} investi",
                f"{revenueStats[1]['name']} revenue",
            ],
        )

        df = pd.merge(df, df2, on="date", how="outer")
        df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
        df = df.sort_values(by="date")
        df = df.fillna(0, inplace=False)

    result = {"indicators": [], "variations": []}

    for i in range(len(revenueStats)):
        result["indicators"].append(
            {
                "name": revenueStats[i]["name"],
                "montantInvest": revenueStats[i]["montantInvest"],
                "revenue": revenueStats[i]["revenue"],
                "rendementMoyen": revenueStats[i]["rendementMoyen"],
            }
        )

    variationsRes = df.values.tolist()
    variationsRes.insert(0, df.columns.tolist())
    result["variations"] = variationsRes

    return result

    # # calcule de cagr
    # dateRange = data.index[-1].year - data.index[0].year
    # cagr_result = cagr(
    #     revenueStats["revenue"], revenueStats["montantInvest"], dateRange
    # )

    # # calcule de volatilite
    # volatilite_result = volatilite(data["Adj Close"])

    # # calcule de ratio de sharp
    # rendementSansRisque = 0.03
    # ratioSharp_result = ratioSharp(
    #     revenueStats["rendementMoyen"], rendementSansRisque, volatilite_result
    # )

    # # calcule de la moyenne
    # moyenne_result = moyenne(data["Adj Close"])

    # # calcule de l'ecart type
    # ecartType_result = ecartType(data["Adj Close"])

    # # calcule de l'ecart interquartille
    # ecartInterquartille_result = ecartInterquartille(data)

    # revenueStats["indicator"] = indicator
    # revenueStats["cagr"] = cagr_result
    # revenueStats["volatilite"] = volatilite_result
    # revenueStats["ratioSharp"] = ratioSharp_result
    # revenueStats["moyenne"] = moyenne_result
    # revenueStats["ecartType"] = ecartType_result
    # revenueStats["ecartInterquartille"] = ecartInterquartille_result
    # revenueStats["montantInitial"] = montantInitial
    # revenueStats["montantRecurant"] = montantRecurant
