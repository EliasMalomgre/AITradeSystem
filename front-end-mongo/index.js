const { MongoClient, ObjectID } = require('mongodb');
const uri = "";
const express = require('express')
const app = express()
const dayjs = require('dayjs')
const moment = require('moment')
const worker = require('worker_threads')

// express (REST)
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    next();
});


// - shareData
app.get('/getHistory', async function (req, res) {
    console.log('got request for ' + req.query.name + ' | ' + req.query.freq)
    const data = await getStockHistoryData(req.query.name, req.query.freq, null, null)
    res.send(data)
})

app.get('/getHistoryDated', async function (req, res) {
    console.log('got request for ' + req.query.name + ' | ' + req.query.freq + ' | ' + req.query.beginDate + ' | ' + req.query.endDate)
    const data = await getStockHistoryData(req.query.name, req.query.freq, req.query.beginDate, req.query.endDate)
    res.send(data)
})

// - wallet
app.get('/getWallet', async function (req, res) {
    console.log('Got request for wallet')
    const data = await getWalletData()
    res.send(data)
})

// - position
app.get('/getPositions', async function (req, res) {
    console.log('Got request for positions')
    //const data = await getPositions()
    const data = await getAllPositions()
    res.send(data)
})

app.get('/getPosition', async function (req, res) {
    console.log('Got request for position ' + req.query.positionId)
    const data = await getPosition(req.query.positionId)
    res.send(data)
})

app.get('/getBeginEnd', async function (req, res) {
    console.log('Got request for begin and end date for ' + req.query.positionId)
    const data = await getBAndEDate(req.query.positionId)
    res.send(data)
})

app.get('/getPositionStats', async function(req, res){
    console.log('Got stats request for position '+req.query.positionId)
    const data = await getPositionStats(req.query.positionId)
    res.send(data)
})

// - transaction
app.get('/getTransactions', async function (req, res) {
    console.log('Got transations request for position ' + req.query.positionId)
    const data = await getTransactionsData(req.query.positionId)
    res.send(data)
})

app.get('/getAnnotations', async function (req, res) {
    console.log('Got annotations request for position ' + req.query.positionId)
    const data = await getAnnotations(req.query.positionId)
    res.send(data)
})

// - stop-loss
app.get('/getStopLoss', async function (req, res) {
    console.log('Got stop loss request for position ' + req.query.positionId)
    const data = await getStopLoss(req.query.positionId)
    res.send(data)
})

app.listen(3000)


// repo functions
// - stock history
async function getStockHistory(client, stockName, frequency) {
    const cursor = await client.db("TradeDB").collection("share_entry").find({
        name: { $eq: stockName },
        freq: { $eq: frequency }
    }).sort({ date: -1 })
    const results = await cursor.toArray();
    return results
}

async function getStockHistoryDated(client, stockName, frequency, beginDate, endDate) {
    var PbeginDate = new Date(beginDate).toISOString()
    var PendDate = new Date(endDate).toISOString()
    if (frequency === "Frequency.ONE_DAY") {
        frequency = "1d"
    }

    const cursor = await client.db("TradeDB").collection("share_entry").find({
        name: { $eq: stockName },
        freq: { $eq: frequency },
        date: {
            $gte: new Date(PbeginDate),
            $lte: new Date(PendDate)
        }
    }).sort({ date: 1 })
    const results = await cursor.toArray();
    return results
}

function parseStockHistory(stockData) {
    var result = []
    stockData.forEach(entry => {
        var dataEntry = { x: entry.date, y: [entry.open.toFixed(2), entry.high.toFixed(2), entry.low.toFixed(2), entry.close.toFixed(2)] }
        result.push(dataEntry)
    })
    return result
}

async function getStockHistoryData(stockName, frequency, beginDate, endDate) {
    const client = new MongoClient(uri);
    try {
        await client.connect();
        var res = null

        if (beginDate === null && endDate === null) {
            res = await getStockHistory(client, stockName, frequency)
        } else {
            res = await getStockHistoryDated(client, stockName, frequency, beginDate, endDate)
        }

        const parsedRes = parseStockHistory(res)
        return parsedRes;
    } catch (e) {
        console.error(e);
    } finally {
        await client.close();
    }
}

// - wallet
async function getWallet(client) {
    const cursor = await client.db("TradeDB").collection("wallet").findOne();
    return cursor
}

async function getWalletData() {
    const client = new MongoClient(uri);
    try {
        await client.connect();
        var res = await getWallet(client);
        return res
    } catch (e) {
        console.error(e)
    } finally {
        await client.close()
    }
}

// - positions
async function getPositionsFromWallet(client, wallet) {
    var positions = []
    wallet.positions.forEach(async function (pos) {
        const id = pos._ref.oid
        const position = await client.db("TradeDB").collection("position").findOne({
            _id: { $eq: id }
        })
        positions.push(position)
    })
    return positions
}

async function getPositionFromId(client, positionId) {
    positionId = ObjectID(positionId)
    const res = await client.db("TradeDB").collection("position").findOne({
        _id: { $eq: positionId }
    })
    return res
}

async function getPosition(positionId) {
    const client = new MongoClient(uri);
    try {
        await client.connect();
        var res = getPositionFromId(client, positionId)
        return res
    } catch (e) {
        console.error(e)
    } finally {
        await client.close()
    }
}

async function getPositionStats(positions){
    const client = new MongoClient(uri);
    try {
        await client.connect();
        for (var pos of positions){
            var transactions = await getTransactions(client, pos)
            var res = daysBetween(transactions[0].time_stamp, transactions[transactions.length-1].time_stamp)
            pos.posLength = res

            var sum = 0;
            var amount = 0;
            for (transaction of transactions){
                if (transaction.action === "TransactionAction.BUY" || transaction.action === "TransactionAction.SHORT"){
                    sum += (transaction.amount * transaction.price_per_share)
                    amount++;
                }
            }

            var riskAmount = (sum/amount) * pos.risk
            var RValue = (pos.realized_p_and_l + pos.p_and_l) / riskAmount
            pos.rMultiple = RValue.toFixed(2)
        }
        return positions
    } catch (e) {
        console.error(e)
    } finally {
        await client.close()
    }
}

async function getAllPositions() {
    const client = new MongoClient(uri);
    try {
        await client.connect();
        const positions = await client.db("TradeDB").collection("position").find().toArray()
        const result = getValidPositions(positions)
        return result
    } catch (e) {
        console.error(e)
    } finally {
        await client.close()
    }
}

async function getValidPositions(positions) {
    validPos = []
    for (p of positions) {
        if (p.current_transactions !== null) {
            if (p.current_transactions.length > 0) {
                validPos.push(p)
            }
        }
    }
    validPos = await getPositionStats(validPos)
    return validPos
}


async function getPositions() {
    const client = new MongoClient(uri);
    try {
        await client.connect();
        var wallet = await getWallet(client);
        var res = getPositionsFromWallet(client, wallet)
        return res
    } catch (e) {
        console.error(e)
    } finally {
        await client.close()
    }
}

// - transactions
async function getTransactions(client, position) {
    var transactions = []
    /*await position.current_transactions.forEach(async function (transaction) {
        const id = transaction._ref.oid
        const transac = await client.db("TradeDB").collection("transaction_log").findOne({
            _id: { $eq: id }
        })
        transactions.push(transac)
        if (transactions.length === position.current_transactions.length){
            console.log('nu mag ik!')
        }
    })*/

    for (const transaction of position.current_transactions) {
        const id = transaction._ref.oid
        const transac = await client.db("TradeDB").collection("transaction_log").findOne({
            _id: { $eq: id }
        })
        transactions.push(transac)
    }
    return transactions

}

async function getTransactionsData(positionId) {
    const client = new MongoClient(uri);
    try {
        await client.connect();
        var position = await getPositionFromId(client, positionId);
        var transactions = await getTransactions(client, position);
        return transactions
    } catch (e) {
        console.error(e)
    } finally {
        await client.close()
    }
}

function parseToAnnotations(transactions) {
    var annotations = []
    for (var trans of transactions) {
        const borderColor = getBorderColor(trans);
        const background = getBackgroundColor(trans);
        const dateTimeFormat = getFormattedTimeStamp(trans);
        var annotation = {
            x: dayjs(trans.time_stamp).format(dateTimeFormat),
            borderColor: borderColor,
            label: {
                borderColor: borderColor,
                style: {
                    fontSize: "12px",
                    color: "#fff",
                    background: background
                },
                orientation: "horizontal",
                text: trans.amount + "@" + "$" + trans.price_per_share.toFixed(2).toString()
            }
        }
        annotations.push(annotation);
    }
    return annotations;
}

async function getBAndEDate(positionId, context = true) {
    const client = new MongoClient(uri);
    try {
        await client.connect();
        var position = await getPositionFromId(client, positionId);
        var transactions = await getTransactions(client, position);

        // sorting from old to new
        function compareTransactions(a, b) {
            if (a.time_stamp > b.time_stamp) return 1;
            if (a.time_stamp < b.time_stamp) return -1;
            return 0;
        }

        transactions.sort(compareTransactions)

        var dates = { beginDate: '2020-01-01', endDate: '2020-02-01' }
        dates.beginDate = transactions[0].time_stamp
        dates.endDate = transactions[transactions.length - 1].time_stamp
        if (context) {
            dates = getAddForFrequency(position, dates)
        }
        return dates
    } catch (e) {
        console.error(e)
    } finally {
        await client.close()
    }
}

async function getAnnotations(positionId) {
    const client = new MongoClient(uri);
    try {
        await client.connect();
        var position = await getPositionFromId(client, positionId);
        var transactions = await getTransactions(client, position);
        var res = parseToAnnotations(transactions)
        return res
    } catch (e) {
        console.error(e)
    } finally {
        await client.close()
    }
}

// - stop loss

async function getStopLoss(positionId) {
    const client = new MongoClient(uri);
    try {
        await client.connect();
        var position = await getPositionFromId(client, positionId);
        var res = parseStopLossData(position)

        return res
    } catch (e) {
        console.error(e)
    } finally {
        await client.close()
    }
}

function parseStopLossData(position) {
    var result = []
    var dateTimeFormat = getFormattedTimeStamp(position)

    for (sl of Object.keys(position.stop_loss)) {
        const slValue = { x: dayjs(sl).format(dateTimeFormat), y: position.stop_loss[sl] }
        result.push(slValue)
    }

    return result
}

// - ondersteuning

function getBorderColor(transaction) {
    if (transaction.action === "TransactionAction.BUY") {
        return "#4caf50";
    }
    if (transaction.action === "TransactionAction.SELL") {
        return "#f32f2f";
    }
    if (transaction.action === "TransactionAction.SHORT") {
        return "#1976d2";
    }
    if (transaction.action === "TransactionAction.COVER") {
        return "#f9a825";
    }
}

function getBackgroundColor(transaction) {
    if (transaction.action === "TransactionAction.BUY") {
        return "#80e27e";
    }
    if (transaction.action === "TransactionAction.SELL") {
        return "#ff7961";
    }
    if (transaction.action === "TransactionAction.SHORT") {
        return "#63a4ff";
    }
    if (transaction.action === "TransactionAction.COVER") {
        return "#ffd95a";
    }
}

function getFormattedTimeStamp(transaction) {
    if (transaction.frequency === "1d" || transaction.frequency === "Frequency.ONE_DAY") {
        return "DD MMM";
    }
    if (transaction.frequency === "1h" || transaction.frequency === "Frequency.ONE_HOUR") {
        return "DD MMM HH";
    }
    if (transaction.frequency === "1m" || transaction.frequency === "Frequency.ONE_MINUTE") {
        return "DD MMM HH:mm";
    }
    if (transaction.frequency === "1w" || transaction.frequency === "1m" || transaction.frequency === "Frequency.ONE_WEEK" || transaction.frequency === "Frequency.ONE_MONTH") {
        return "DD MMM YYYY";
    }
}

function getAddForFrequency(position, dates) {
    if (position.frequency === "1d" || position.frequency === "Frequency.ONE_DAY") {
        const copy = new Date(Number(dates.beginDate))
        copy.setDate(dates.beginDate.getDate() - 5)
        dates.beginDate = copy;

        const copy2 = new Date(Number(dates.endDate))
        copy2.setDate(dates.endDate.getDate() + 5)
        dates.endDate = copy2;

        return dates
    }
    if (position.frequency === "1h" || position.frequency === "Frequency.ONE_HOUR") {
        const copy = moment(dates.beginDate).subtract(300, 'minutes').toDate()
        dates.beginDate = copy;

        const copy2 = moment(dates.endDate).add(300, 'minutes').toDate()
        dates.endDate = copy2;

        return dates
    }
    if (position.frequency === "1m" || position.frequency === "Frequency.ONE_MINUTE") {
        const copy = moment(dates.beginDate).subtract(5, 'minutes').toDate()
        dates.beginDate = copy;

        const copy2 = moment(dates.endDate).add(5, 'minutes').toDate()
        dates.endDate = copy2;

        return dates
    }
    if (position.frequency === "1w" || position.frequency === "Frequency.ONE_WEEK") {
        const copy = new Date(Number(dates.beginDate))
        copy.setDate(dates.beginDate.getDate() - 21)
        dates.beginDate = copy;

        const copy2 = new Date(Number(dates.endDate))
        copy2.setDate(dates.endDate.getDate() + 21)
        dates.endDate = copy2;

        return dates
    }
    if (position.frequency === "1M" || position.frequency === "Frequency.ONE_MONTH") {
        const copy = new Date(Number(dates.beginDate))
        copy.setDate(dates.beginDate.getDate() - 90)
        dates.beginDate = copy;

        const copy2 = new Date(Number(dates.endDate))
        copy2.setDate(dates.endDate.getDate() + 90)
        dates.endDate = copy2;

        return dates
    }

}

function daysBetween(firstDate, secondDate){
    const oneDay = 24 * 60 * 60 * 1000;
    return Math.round(Math.abs((firstDate - secondDate) / oneDay));
}