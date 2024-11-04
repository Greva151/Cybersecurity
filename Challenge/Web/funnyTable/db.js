const mysql = require('mysql');

const db = mysql.createConnection({
    host: process.env['DB_HOST'],
    user: process.env['DB_USER'],
    password: process.env['DB_PASSWD'],
    database: process.env['DB_NAME']
});

const connect = () => {
    return new Promise((accept, reject) => {
        db.connect((error) => {
            if (error) {
                reject(error)
                return
            }

            accept()
        });
    })
}

const query = (query, args) => {
    return new Promise((accept, reject) => {
        db.query(query, args, (error, results) => {
            if (error) {
                reject(error)
                return
            }

            accept(results)
        })
    })
}

module.exports = {connect, query}