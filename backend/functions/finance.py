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
    evolution = []
    evolution.append(
        [financeTable.index[0].strftime("%d/%m/%Y"), financeTable["Adj Close"].iloc[0]]
    )
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

        evolution.append([ind.strftime("%d/%m/%Y"), prixAction])

    lastAdjClose = financeTable["Adj Close"].iloc[-1]
    revenue = nbAction * lastAdjClose + liquidite
    rendementMoyen = (revenue / montantInvest) - 1

    # calculate the metrics
    dateRange = financeTable.index[-1].year - financeTable.index[0].year
    cagr_result = cagr(revenue, montantInitial, dateRange)
    volatilite_result = volatilite(financeTable["Adj Close"])
    ratioSharp_result = ratioSharp(rendementMoyen, 0.03, volatilite_result)
    moyenne_result = moyenne(financeTable["Adj Close"])
    ecartType_result = ecartType(financeTable["Adj Close"])
    ecartInterquartille_result = ecartInterquartille(financeTable)

    return {
        "name": name,
        "montantInvest": montantInvest,
        "revenue": revenue,
        "rendementMoyen": rendementMoyen,
        "variations": variationsList,
        "cagr": cagr_result,
        "volatilite": volatilite_result,
        "ratioSharp": ratioSharp_result,
        "moyenne": moyenne_result,
        "ecartType": ecartType_result,
        "ecartInterquartille": ecartInterquartille_result,
        "evolution": evolution,
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

    evolutionDf = pd.DataFrame(
        revenueStats[0]["evolution"],
        columns=["date", f"{revenueStats[0]['name']}"],
    )
    if len(revenueStats) == 2:
        evolutionDf2 = pd.DataFrame(
            revenueStats[1]["evolution"],
            columns=["date", f"{revenueStats[1]['name']}"],
        )
        evolutionDf = pd.merge(evolutionDf, evolutionDf2, on="date", how="outer")
        evolutionDf["date"] = pd.to_datetime(evolutionDf["date"], format="%d/%m/%Y")
        evolutionDf = evolutionDf.sort_values(by="date")
        evolutionDf = evolutionDf.fillna(0, inplace=False)

    result = {"indicators": [], "variations": [], "evolution": []}

    for i in range(len(revenueStats)):
        result["indicators"].append(
            {
                "name": revenueStats[i]["name"],
                "montantInvest": revenueStats[i]["montantInvest"],
                "revenue": revenueStats[i]["revenue"],
                "rendementMoyen": revenueStats[i]["rendementMoyen"],
                "cagr": revenueStats[i]["cagr"],
                "volatilite": revenueStats[i]["volatilite"],
                "ratioSharp": revenueStats[i]["ratioSharp"],
                "moyenne": revenueStats[i]["moyenne"],
                "ecartType": revenueStats[i]["ecartType"],
                "ecartInterquartille": revenueStats[i]["ecartInterquartille"],
            }
        )

    variationsRes = df.values.tolist()
    variationsRes.insert(0, df.columns.tolist())
    result["variations"] = variationsRes

    evolutionRes = evolutionDf.values.tolist()
    evolutionRes.insert(0, evolutionDf.columns.tolist())
    result["evolution"] = evolutionRes

    return result