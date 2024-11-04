const express = require('express')
const session = require('express-session')

const app = express()
app.set('view engine', 'ejs');

app.use(session({secret: process.env['COOKIE_SECRET'], saveUninitialized: false, resave: false}))

const items = {
    'gelato': [1, 'Gelato'],
    'coppa_del_nonno': [5, 'Coppa del Nonno'],
    'granita': [5, 'Granita'],
    'acqua': [100, 'Acqua'],
    'happy_hippo': [1000, 'Happy Hippo'],
    'flag': [1000000000, process.env['FLAG']],
}

app.get('/', (req, res) => {
    if (!req.session.balance)
        req.session.balance = 0
    
    res.render('index', {prices: Object.entries(items).map(([item, [price]]) => [item, price]), balance: req.session.balance})
})

app.get('/withdraw', (req, res) => {
    if (!req.session.balance)
        req.session.balance = 0
    
    if (req.session.balance > 10000) {
        return res.redirect('/?error=You+have+too+much+money')
    }

    const amountStr = req.query.amount || ''    
    if (typeof amountStr !== 'string' || amountStr.length > 4) {
        return res.redirect('/?error=Invalid+withdraw+amount')
    }
    
    const amount = +amountStr
    if (!isFinite(amount) || amount <= 0) {
        return res.redirect('/?error=Invalid+withdraw+amount')
    }
    
    req.session.balance += amount
    return res.redirect('/')
})

app.get('/buy', (req, res) => {
    if (!req.session.balance)   
        req.session.balance = 0
    
    const item = req.query.item
    if (!(item in items)) {
        return res.redirect('/?error=Invalid+item')
    }
    
    const [cost, reward] = items[item]
    if (req.session.balance < cost) {
        return res.redirect('/?error=Not+enough+money')
    }
    
    req.session.balance -= cost
    return res.redirect('/?reward=' + reward)
})

app.listen(parseInt(process.env['PORT']), () => console.log('Listening...'))