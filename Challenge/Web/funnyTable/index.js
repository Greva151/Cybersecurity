const express = require('express')
const {connect, query} = require('./db');

(async () => {
    await connect()

    const app = express()

    app.get('/', async (req, res) => {
        const posts = await query('select id, title from posts')
        res.send(`<html lang="en"><body><ul>${posts.map(x => '<li><a href="/post?id=' + x.id + '">' + x.title + '</a></li>').join('')}<ul></body></html>`)
    })
    
    app.get('/post', async (req, res) => {
        const postId = req.query.id;
        
        try {
            const posts = await query('select title, content from posts where id = ' + postId + ' limit 1')
            if (posts.length === 0) {
                res.send('<html lang="en"><body>No such post</body></html>')
                return
            }

            const post = posts[0]
            res.send(`<html lang="en"><body><h1>${post.title}</h1><p>${post.content}</p></body></html>`)
        } catch (err) {
            console.error(err)
            res.send(`<html lang="en"><body><h2>An error occurred</h2></body></html>`)
        }
    })

    app.listen(parseInt(process.env['PORT']), () => console.log('Listening...'))
})()
